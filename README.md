# AI Chat Assistant

A Flask-based web application that provides an AI chat interface using OpenAI's GPT models.

## Features

- Modern, responsive UI with a blue theme
- Real-time chat interface with AI
- Loading states and error handling
- Easy navigation with home and profile buttons
- Mobile-friendly design

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd chatbotflask
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
PORT=5002
FLASK_ENV=development
DEBUG=true
```

5. Run the application:
```bash
python python.py
```

The application will be available at `http://localhost:5002`

## API Endpoints

### POST /api/chat
Send a chat message to the AI assistant.

Request body:
```json
{
    "query": "Your message here"
}
```

Response:
```json
{
    "query": "Your message",
    "response": "AI response",
    "success": true
}
```

## Deployment

This application can be deployed on platforms like Render. Make sure to:
1. Set up the environment variables (OPENAI_API_KEY)
2. Use gunicorn as the production server
3. Configure CORS settings if needed

## License

MIT License
