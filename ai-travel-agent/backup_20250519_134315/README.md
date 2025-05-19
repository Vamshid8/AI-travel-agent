# AI Travel Planner

An intelligent travel planning application that uses AI to generate personalized travel itineraries, cost estimates, and PDF reports.

## Features

- User authentication and authorization
- AI-powered travel plan generation
- Cost estimation with currency conversion
- PDF report generation
- Database storage for travel plans
- Rate limiting and security features
- Comprehensive logging
- Unit testing
- RESTful API endpoints

## Tech Stack

- Python 3.12
- Flask (Web Framework)
- SQLAlchemy (ORM)
- JWT (Authentication)
- ReportLab (PDF Generation)
- Gradio (UI)
- Pytest (Testing)
- SQLite (Database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-travel-agent.git
cd ai-travel-agent
```

2. Create and activate a virtual environment:
```bash
conda create -n travel-agent python=3.12
conda activate travel-agent
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

## Running the Application

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Run the application:
```bash
python app.py
```

3. Run tests:
```bash
pytest
```

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new user
- POST `/auth/login` - Login and get JWT token

### Travel Plans
- POST `/api/travel-plans` - Create a new travel plan
- GET `/api/travel-plans` - Get all travel plans for the authenticated user

## Project Structure

```
ai-travel-agent/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── logger.py           # Logging configuration
├── planner.py          # AI travel planning logic
├── pdf_generator.py    # PDF generation
├── requirements.txt    # Project dependencies
├── tests/             # Test files
│   └── test_app.py
├── logs/              # Log files
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the AI models
- Flask community for the web framework
- All contributors who have helped improve this project 