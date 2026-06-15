# AI Farm Manager

FastAPI backend project structure for an AI Farm Manager application.

## Architecture

This project is built using a modular multi-agent architecture:

- **Agents**: Custom intelligent entities (Weather, Crop, Planner, Finance) that handle tasks using tools and memory.
- **Memory**: Support for short-term conversation context and long-term knowledge retention.
- **Skills**: Actionable modules (tools) that agents use to query data and perform calculations.
- **API (v1)**: Fast API endpoints exposed for consumption by a frontend.
- **Services**: Shared modules for interfacing with third-party platforms (databases, external weather APIs).

## Directory Structure

```
├── app/
│   ├── main.py                 # App entrypoint
│   ├── core/                   # App configurations and settings
│   ├── api/                    # Routers and endpoints
│   ├── agents/                 # Agent definitions and abstract base class
│   ├── memory/                 # Short/long-term memory mechanisms
│   ├── skills/                 # Skills/tools for agents
│   ├── schemas/                # Pydantic schemas for request validation
│   └── services/               # Shared external integrations
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment configurations
└── README.md                   # Project description
```

## Getting Started

1. Clone or navigate to the repository directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the `.env.example` file to `.env` and fill in the necessary keys.
5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
