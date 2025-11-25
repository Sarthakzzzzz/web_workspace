"""
resolver.py — Logic module for EnvZero dependency resolution

Define a function detect_stack(prompt: str) -> dict which parses a natural
language description and returns a manifest with keys: "stack", "system_packages",
"app_dependencies".

This is intentionally simple and keyword-based, serving as a library module.
"""

from typing import Dict, List
import re


def _add_unique(collection: List[str], items: List[str]):
    for item in items:
        if item not in collection:
            collection.append(item)


def detect_stack(prompt: str) -> Dict[str, List[str]]:
    """Detect a technology stack based on a natural language prompt.

    Args:
        prompt: Natural language prompt (e.g. "FastAPI with React")

    Returns:
        A dict with keys:
            - stack: concatenated detected stacks (e.g. "Python/FastAPI + JavaScript/React")
            - system_packages: list of system-level package names
            - app_dependencies: list of application/library dependencies

    Raises:
        TypeError: if prompt is not a string
        ValueError: if prompt is empty or whitespace-only
    """
    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")

    text = prompt.strip()
    if not text:
        raise ValueError("prompt must not be empty")

    text_low = text.lower()

    stacks: List[str] = []
    system_packages: List[str] = []
    app_dependencies: List[str] = []

    # Python backends
    if re.search(r"\bdjango\b", text_low):
        stacks.append("Python/Django")
        _add_unique(system_packages, [
                    "python3-dev", "libpq-dev", "build-essential"])
        _add_unique(app_dependencies, ["Django>=3.2", "psycopg2-binary"])

    if re.search(r"\bflask\b", text_low):
        stacks.append("Python/Flask")
        _add_unique(system_packages, ["python3-dev", "build-essential"])
        _add_unique(app_dependencies, ["Flask>=2.0"])

    if re.search(r"\bfastapi\b", text_low):
        stacks.append("Python/FastAPI")
        _add_unique(system_packages, ["python3-dev", "build-essential"])
        _add_unique(app_dependencies, ["fastapi", "uvicorn[standard]"])

    # JavaScript frontends
    if re.search(r"\breact\b", text_low):
        stacks.append("JavaScript/React")
        _add_unique(system_packages, ["nodejs", "npm", "build-essential"])
        _add_unique(app_dependencies, ["react", "react-dom"])

    if re.search(r"\bvue\b", text_low):
        stacks.append("JavaScript/Vue")
        _add_unique(system_packages, ["nodejs", "npm", "build-essential"])
        _add_unique(app_dependencies, ["vue"])

    # Node/Express
    if re.search(r"\bnode\b|\bexpress\b", text_low):
        if "JavaScript/React" not in stacks and "JavaScript/Vue" not in stacks:
            stacks.append("JavaScript/Node")
        _add_unique(system_packages, ["nodejs", "npm"])
        _add_unique(app_dependencies, ["express"])

    # CSS/build tools
    if re.search(r"\btailwind\b", text_low):
        _add_unique(system_packages, ["nodejs", "npm"])
        _add_unique(app_dependencies, ["tailwindcss"])

    # Databases
    if re.search(r"\bpostgres\b|\bpostgresql\b|\bpg\b", text_low):
        _add_unique(system_packages, ["postgresql-client", "libpq-dev"])
        _add_unique(app_dependencies, ["psycopg2-binary"])

    if re.search(r"\bmongodb\b|\bmongo\b", text_low):
        _add_unique(system_packages, ["mongodb-clients"])
        _add_unique(app_dependencies, ["pymongo"])

    # Unknown fallback
    if not stacks:
        stacks.append("Unknown")
        _add_unique(system_packages, ["build-essential"])  # safe default

    manifest: Dict[str, List[str]] = {
        "stack": " + ".join(stacks),
        "system_packages": sorted(system_packages),
        "app_dependencies": sorted(app_dependencies),
    }

    return manifest
