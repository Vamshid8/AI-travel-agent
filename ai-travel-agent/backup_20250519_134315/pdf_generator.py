from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def generate_pdf(destination, dates, budget, preferences, plan):
    # Create PDF
    pdf_path = f"travel_plan_{destination.replace(' ', '_')}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Set font
    c.setFont("Helvetica", 12)
    
    # Add content
    y = 750  # Starting y position
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Travel Plan for {destination}")
    y -= 30
    
    # Details
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Dates: {dates}")
    y -= 20
    c.drawString(50, y, f"Budget: {budget}")
    y -= 20
    c.drawString(50, y, f"Preferences: {preferences}")
    y -= 40
    
    # Plan
    c.drawString(50, y, "Itinerary:")
    y -= 20
    
    # Split plan into lines and add to PDF
    for line in plan.split('\n'):
        if y < 50:  # Check if we need a new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
        c.drawString(50, y, line)
        y -= 15
    
    c.save()
    return pdf_path
