"""
main.py — FastAPI orchestrator for EnvZero

Endpoints:
  - GET / -> health check
  - POST /api/resolve -> resolves a natural language prompt into a manifest

This server imports `detect_stack` from `services.inference.resolver` and calls it directly
-- no subprocesses.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict
import logging

from starlette.concurrency import run_in_threadpool

# Import resolver function
from services.inference.resolver import detect_stack

# Setup logger
logger = logging.getLogger("envzero")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI(title="EnvZero Orchestrator", version="0.1.0")


class ResolveRequest(BaseModel):
    prompt: str = Field(...,
                        description="Natural language prompt describing the dev environment")


class ResolveResponse(BaseModel):
    ok: bool
    manifest: Dict[str, Any]


@app.get("/", tags=["health"])
async def root():
    return {"status": "EnvZero Orchestrator Running"}


@app.post("/api/resolve", response_model=ResolveResponse, tags=["resolve"])
async def api_resolve(req: ResolveRequest):
    try:
        prompt = req.prompt.strip()
        if not prompt:
            raise HTTPException(
                status_code=400, detail="prompt must not be empty")
        if len(prompt) > 4096:
            raise HTTPException(status_code=413, detail="prompt is too large")

        # Offload detection to threadpool to keep the event loop free
        manifest = await run_in_threadpool(detect_stack, prompt)

        # Validate returned manifest
        if not isinstance(manifest, dict):
            logger.error(
                "Invalid manifest type returned from detect_stack: %s", type(manifest))
            raise HTTPException(
                status_code=502, detail="Invalid manifest returned by resolver")
        expected_keys = {"stack", "system_packages", "app_dependencies"}
        if not expected_keys.issubset(set(manifest.keys())):
            logger.error("Manifest missing required keys: %s", manifest.keys())
            raise HTTPException(
                status_code=502, detail="Resolver returned incomplete manifest")

        return {"ok": True, "manifest": manifest}

    except HTTPException:
        # Re-raise HTTP exceptions for FastAPI to handle
        raise
    except (ValueError, TypeError) as e:
        # Treat resolver input issues as client errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as err:
        logger.exception("Unexpected error in /api/resolve")
        # Hide internal details in production; provide minimal info in response
        raise HTTPException(status_code=500, detail="Internal server error")


# Exception handler for HTTPExceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "error": exc.detail})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.orchestrator.main:app",
                host="0.0.0.0", port=3001, log_level="info")
