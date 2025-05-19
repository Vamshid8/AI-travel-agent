# AI Travel Planner

An intelligent travel planning application that uses AI agents to generate personalized travel itineraries.

## Features

- AI-powered travel research
- Flight recommendations
- Hotel and accommodation suggestions
- Detailed day-by-day itineraries
- User-friendly web interface
- Real-time travel planning

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

5. Run the application:
```bash
python app.py
```

## How to Use

1. Enter your destination
2. Specify your travel dates
3. Indicate your budget range
4. Share your travel preferences
5. Click 'Generate Travel Plan'

The AI agents will research and create a comprehensive travel plan for you.

## Tech Stack

- Python
- Gradio (UI Framework)
- PraisonAI Agents
- Groq LLM
- Serper API 