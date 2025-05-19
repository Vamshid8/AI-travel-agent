from planner import generate_travel_plan
import gradio as gr
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import time
from functools import lru_cache
import concurrent.futures
import threading
from pdf_generator import generate_pdf

# Load environment variables
load_dotenv()

# Global cache for exchange rates
exchange_rate_cache = {}
cache_lock = threading.Lock()

def get_exchange_rate(from_currency, to_currency):
    cache_key = f"{from_currency}_{to_currency}"
    
    # Check cache first
    with cache_lock:
        if cache_key in exchange_rate_cache:
            return exchange_rate_cache[cache_key]
    
    try:
        response = requests.get(
            f"https://api.exchangerate-api.com/v4/latest/{from_currency}",
            timeout=3  # Reduced timeout
        )
        data = response.json()
        rate = data['rates'][to_currency]
        
        # Update cache
        with cache_lock:
            exchange_rate_cache[cache_key] = rate
        
        return rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 1.0

def estimate_costs(destination, dates, budget, currency):
    # This is a placeholder function - you'll need to implement actual cost estimation logic
    base_costs = {
        'USD': {
            'flights': 500,
            'hotel': 100,
            'activities': 50,
            'food': 30,
            'transportation': 20
        }
    }
    
    # Convert costs to selected currency
    exchange_rate = get_exchange_rate('USD', currency)
    costs = {k: v * exchange_rate for k, v in base_costs['USD'].items()}
    
    return {
        'flights': f"{costs['flights']:.2f} {currency}",
        'hotel': f"{costs['hotel']:.2f} {currency}",
        'activities': f"{costs['activities']:.2f} {currency}",
        'food': f"{costs['food']:.2f} {currency}",
        'transportation': f"{costs['transportation']:.2f} {currency}",
        'total': f"{sum(costs.values()):.2f} {currency}"
    }

def create_interface():
    with gr.Blocks(title="AI Travel Planner") as demo:
        with gr.Column():
            gr.Markdown("# AI Travel Planner")
            gr.Markdown("Let our AI plan your dream trip!")

            with gr.Row():
                with gr.Column(scale=1):
                    destination = gr.Textbox(label="Destination", placeholder="e.g., Tokyo, Japan")
                    dates = gr.Textbox(label="Travel Dates", placeholder="e.g., July 10-20, 2025")
                    budget = gr.Textbox(label="Budget", placeholder="e.g., Mid-range ($1000 - $1500)")
                    currency = gr.Dropdown(
                        choices=["USD", "EUR", "INR", "GBP", "JPY"],
                        value="USD",
                        label="Currency"
                    )
                    preferences = gr.Textbox(
                        label="Travel Preferences",
                        placeholder="e.g., Nature, food, historical places",
                        lines=3
                    )
                    submit_btn = gr.Button("Generate Plan")

                with gr.Column(scale=1):
                    output = gr.Markdown("Your travel plan will appear here.")
                    cost_breakdown = gr.JSON(label="Cost Breakdown")
                    pdf_output = gr.File(label="Download PDF")

            def generate_plan(dest, dates, budget, curr, prefs):
                try:
                    start_time = time.time()
                    
                    # Add timeout settings for API calls
                    timeout = 30  # 30 seconds timeout
                    
                    # Use ThreadPoolExecutor for parallel processing with timeout
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        # Submit tasks with timeout
                        plan_future = executor.submit(generate_travel_plan, dest, dates, budget, prefs)
                        costs_future = executor.submit(estimate_costs, dest, dates, budget, curr)
                        
                        try:
                            # Get results with timeout
                            result = plan_future.result(timeout=timeout)
                            costs = costs_future.result(timeout=timeout)
                        except concurrent.futures.TimeoutError:
                            return "Error: Request timed out. Please try again.", None, None
                        except Exception as e:
                            return f"Error: {str(e)}", None, None
                    
                    execution_time = time.time() - start_time
                    print(f"Total execution time: {execution_time:.2f} seconds")
                    
                    # Generate PDF if we have a valid result
                    pdf_path = None
                    if result and not result.startswith("Error"):
                        try:
                            pdf_path = generate_pdf(dest, dates, budget, prefs, result)
                        except Exception as e:
                            print(f"Error generating PDF: {str(e)}")
                    
                    return result, costs, pdf_path
                except Exception as e:
                    print(f"Error in generate_plan: {str(e)}")
                    return f"Error: {str(e)}", None, None

            submit_btn.click(
                generate_plan,
                inputs=[destination, dates, budget, currency, preferences],
                outputs=[output, cost_breakdown, pdf_output]
            )

            gr.Markdown("""
            ## How to Use
            - Enter your destination and travel details
            - Select your preferred currency
            - Click "Generate Plan" to get a full itinerary with cost breakdown
            - Download the PDF version of your travel plan
            """)

    return demo

def main():
    try:
        demo = create_interface()
        demo.launch()
    except Exception as e:
        print(f"Error launching app: {str(e)}")

if __name__ == "__main__":
    main()
