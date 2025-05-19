from agents import research_agent, flight_agent, hotel_agent, itinerary_agent
from praisonaiagents import Agents
from pdf_generator import generate_pdf
import time
from functools import wraps

def timeout_handler(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            if time.time() - start_time > seconds:
                raise TimeoutError(f"Function took longer than {seconds} seconds")
            return result
        return wrapper
    return decorator

@timeout_handler(30)  # 30 seconds timeout
def generate_travel_plan(destination, dates, budget, preferences):
    """Generate a travel plan using the AI agents"""
    
    travel_query = f"""Create a comprehensive travel plan for {destination} during {dates}.
    Budget: {budget}
    Preferences: {preferences}
    
    Include:
    1. Information about the destination
    2. Flight recommendations
    3. Hotel options
    4. A day-by-day itinerary
    """
    
    agents = Agents(agents=[
        research_agent,
        flight_agent,
        hotel_agent,
        itinerary_agent
    ])
    
    try:
        result = agents.start(travel_query)
        
        if not result:
            return "Error: No response received from the AI agents. Please try again."
        
        formatted_result = f"""
=== TRAVEL PLAN: {destination} ===

Dates: {dates}
Budget: {budget}
Preferences: {preferences}

{result}
"""
        return formatted_result
    except TimeoutError:
        return "Error: Request timed out. Please try again."
    except Exception as e:
        return f"Error generating travel plan: {str(e)}"
