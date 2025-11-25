# EnvZero

### A browser-based development workspace that handles environment setup automatically.

This project creates cloud-based coding environments that configure themselves based on what you want to build. It removes the need for local installations, allowing developers to jump straight into coding regardless of the technology stack.

---

## The Problem

For many developers, the gap between having an idea and starting to code is filled with hours of configuration. We face three main issues:

- **Setup Fatigue:** Setting up a project that uses multiple technologies (like a Python backend with a Node.js frontend) requires installing and configuring different tools that often don't play well together.
- **"It Works on My Machine":** Code that runs perfectly on one developer's computer often fails on another due to slight differences in operating systems or version numbers.
- **Dependency Hell:** Installing a new library for one project can accidentally break another project by changing global versions or system settings.

## The Solution

This platform solves these issues by moving the development environment to the cloud:

- **On-Demand Environments:** When a user starts a project, the system instantly creates a fresh, isolated workspace (container) specifically for that project.
- **Automated Configuration:** instead of manually typing installation commands, the user defines their requirements (e.g., "Django + Tailwind"). The system automatically installs the correct languages, libraries, and system tools needed to make them work together.
- **Zero Local Conflict:** Since every project runs in its own isolated cloud environment, nothing you do in one project can break another.
- **Export Ready:** Users can download their entire project as a ZIP file, complete with a standard configuration file, so it can run anywhere.

---

## Core Feature: Smart Dependency Resolver

_Note: This feature is currently in active development._

The key innovation of this project is a custom **Dependency Resolution System**.

Most package managers (like `pip` or `npm`) only look at code libraries. They don't check if your operating system has the right tools to run them. My system is being designed to:

1.  Analyze the libraries the user wants to use.
2.  Check the underlying system (OS) to ensure it has the necessary build tools or drivers.
3.  Automatically install those missing system tools before installing the code libraries, preventing common crash errors.

---

## Tech Stack

_[To be decided based on testing]_

- **Frontend:** [TBD]
- **Backend:** [TBD]
- **Infrastructure:** [TBD]

---

## Project Status

**Current Phase:** Prototyping and Logic Design.
_Currently working on the logic for the Dependency Resolution System to ensure smooth cross-platform installations._
