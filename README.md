# Kavak-Debate-Bot
This is an API for a chatbot that can hold a debate and attempt to convince the other side of its views

## Table of Contents
- [DebateBot](#debatebot)  
  - [Features](#features)  
  - [Requirements](#requirements)  
  - [Environment Variables](#environment-variables)  
  - [Installation](#installation)  
    - [Clone and Install](#clone-and-install)  
    - [Run with Docker](#run-with-docker)  
    - [Tear Down](#tear-down)  
  - [Testing](#testing)  
  - [Usage](#usage)  
  - [Project Structure](#project-structure)  
  - [Contributing](#contributing)  
  - [License](#license)

---

## Features
- Structured debates: Maintains a consistent stance across multiple exchanges.  
- Topic lock: Politely refuses to switch sides or drift into unrelated topics.  
- Contextual memory: Stores conversation history in Redis (or falls back to in-memory).  
- FastAPI backend with async endpoints.  
- Lightweight frontend with live chat UI.  
- Dockerized: Easy to run anywhere with `docker compose`.

##DebateBot Architecture Overview
<img width="1844" height="290" alt="image" src="https://github.com/user-attachments/assets/e004cbc8-3969-49ee-89d8-cdab0cf51a35" />

## Installation and Usage in local

## Installation

### Clone the repository
```bash
git clone https://github.com/<your-username>/Kavak-Debate-Bot.git
cd Kavak-Debate-Bot
```

### Environment variables

Create a `.env` file in the project root with the following variables:

```ini
# Required
OPENAI_API_KEY=sk-xxxxxx

# Optional
MODEL_NAME=gpt-4o-mini
ENV=development
REQUEST_TIMEOUT_SECONDS=25
MAX_HISTORY_PAIRS=5

# Optional Redis
# Example for local Redis:
# REDIS_URL=redis://localhost:6379/0
# Example for Render Redis:
# REDIS_URL=rediss://red-xxxxx:password@hostname:6379/0
```

⚠️ Never commit your `.env` file. Ensure `.env` is in `.gitignore`.

---

## Usage

### Run with Docker (recommended)

Ensure Docker Desktop is running.

Start services:
```bash
make run
```

This starts FastAPI (port 8080) and Redis.

Open [http://localhost:8080](http://localhost:8080) to use the app.

Health check:
```bash
curl -s http://localhost:8080/health
```

Stop services:
```bash
make down
```

Clean (remove containers, networks, volumes):
```bash
make clean
```

---

### Run locally with venv

Create a Python virtual environment and install dependencies:
```bash
make install
source .venv/bin/activate
```

Run the API:
```bash
uvicorn app.main:app --reload --port 8080
```

Open [http://localhost:8080](http://localhost:8080).

To run Redis locally:
```bash
docker run -p 6379:6379 redis:7
export REDIS_URL=redis://localhost:6379/0
```
