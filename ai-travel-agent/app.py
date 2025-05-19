from praisonaiagents import Agent, Agents, MCP
import os
from rich import print
import gradio as gr
from dotenv import load_dotenv
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check for required API keys
serper_api_key = os.getenv("SERPER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not serper_api_key:
    logger.error("SERPER_API_KEY not found in environment variables")
    print("[red]Error: SERPER_API_KEY not found in environment variables[/red]")
    print("Please create a .env file with your SERPER_API_KEY")
    sys.exit(1)

if not groq_api_key:
    logger.error("GROQ_API_KEY not found in environment variables")
    print("[red]Error: GROQ_API_KEY not found in environment variables[/red]")
    print("Please create a .env file with your GROQ_API_KEY")
    sys.exit(1)

logger.info("Initializing agents...")

# Travel Research Agent
research_agent = Agent(
    instructions="Research about travel destinations, attractions, local customs, and travel requirements",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-serper", env={"SERPER_API_KEY": serper_api_key})
)

# Flight Booking Agent
flight_agent = Agent(
    instructions="Search for available flights, compare prices, and recommend optimal flight choices",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-serper", env={"SERPER_API_KEY": serper_api_key})
)

# Accommodation Agent
hotel_agent = Agent(
    instructions="Research hotels and accommodation based on budget and preferences",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-serper", env={"SERPER_API_KEY": serper_api_key})
)

# Itinerary Planning Agent
itinerary_agent = Agent(
    instructions="Design detailed day-by-day travel plans incorporating activities, transport, and rest time",
    llm="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    tools=MCP("npx -y @modelcontextprotocol/server-serper", env={"SERPER_API_KEY": serper_api_key})
)

logger.info("All agents initialized successfully")

def generate_travel_plan(destination, dates, budget, preferences):
    """Generate a travel plan using the AI agents"""
    logger.info(f"Generating travel plan for {destination}")
    
    # Create the travel query
    travel_query = f"""Create a comprehensive travel plan for {destination} during {dates}.
    Budget: {budget}
    Preferences: {preferences}
    
    Include:
    1. Information about the destination
    2. Flight recommendations
    3. Hotel options
    4. A day-by-day itinerary
    """
    
    logger.info("Initializing agents team...")
    # Initialize the agents team
    agents = Agents(agents=[research_agent, flight_agent, hotel_agent, itinerary_agent])
    
    try:
        logger.info("Starting travel plan generation...")
        # Generate the travel plan
        result = agents.start(travel_query)
        logger.info("Travel plan generated successfully")
        
        # Format the output
        formatted_result = f"""
=== TRAVEL PLAN: {destination} ===

Dates: {dates}
Budget: {budget}
Preferences: {preferences}

{result}
"""
        
        return formatted_result
    except Exception as e:
        logger.error(f"Error generating travel plan: {str(e)}", exc_info=True)
        return f"Error generating travel plan: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="AI Travel Agency", theme="soft") as demo:
    gr.Markdown("# 🌍 AI Travel Agency")
    gr.Markdown("Plan your perfect trip with our AI agents")
    
    with gr.Row():
        with gr.Column(scale=1):
            destination = gr.Textbox(label="Destination", placeholder="London, UK", value="London, UK")
            dates = gr.Textbox(label="Travel Dates", placeholder="August 15-22, 2024", value="August 15-22, 2024")
            budget = gr.Textbox(label="Budget", placeholder="Mid-range (£1000-£1500)", value="Mid-range (£1000-£1500)")
            preferences = gr.Textbox(
                label="Travel Preferences", 
                placeholder="Historical sites, local cuisine, avoiding crowded tourist traps",
                value="Historical sites, local cuisine, avoiding crowded tourist traps"
            )
            submit_btn = gr.Button("Generate Travel Plan 🚀", variant="primary")
        
        with gr.Column(scale=2):
            output = gr.Markdown(label="Your Travel Plan")
    
    submit_btn.click(
        generate_travel_plan,
        inputs=[destination, dates, budget, preferences],
        outputs=output
    )
    
    gr.Markdown("### How to use")
    gr.Markdown("""
    1. Enter your destination
    2. Specify your travel dates
    3. Indicate your budget range
    4. Share your travel preferences
    5. Click 'Generate Travel Plan'
    
    *Note: Generation may take a minute or two as our AI agents research your perfect trip.*
    """)

if __name__ == "__main__":
    logger.info("Starting the application...")
    demo.launch() 