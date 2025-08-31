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
