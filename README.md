# AI-travel-agent
An intelligent travel planning application that uses AI agents to generate personalized travel itineraries.

Features
AI-powered travel research
Flight recommendations
Hotel and accommodation suggestions
Detailed day-by-day itineraries
User-friendly web interface
Real-time travel planning
Setup
Create a virtual environment:
python -m venv .venv
Activate the virtual environment:
# On Windows
.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Set up environment variables: Create a .env file with the following variables:
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
Run the application:
python app.py
How to Use
Enter your destination
Specify your travel dates
Indicate your budget range
Share your travel preferences
Click 'Generate Travel Plan'
The AI agents will research and create a comprehensive travel plan for you.

Tech Stack
Python
Gradio (UI Framework)
PraisonAI Agents
Groq LLM
Serper API
