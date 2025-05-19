from praisonaiagents import Agent

# Travel Research Agent
research_agent = Agent(
    instructions="Research about travel destinations, attractions, local customs, and travel requirements",
    llm="gpt-3.5-turbo"
)

# Flight Booking Agent
flight_agent = Agent(
    instructions="Search for available flights, compare prices, and recommend optimal flight choices",
    llm="gpt-3.5-turbo"
)

# Accommodation Agent
hotel_agent = Agent(
    instructions="Research hotels and accommodation based on budget and preferences",
    llm="gpt-3.5-turbo"
)

# Itinerary Planning Agent
itinerary_agent = Agent(
    instructions="Design detailed day-by-day travel plans incorporating activities, transport, and rest time",
    llm="gpt-3.5-turbo"
)
