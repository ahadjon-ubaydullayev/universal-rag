# Universal RAG Chatbot

A modern, secure, and responsive RAG (Retrieval-Augmented Generation) chatbot application with a React frontend and FastAPI backend.

## Features

- **Modern UI**: Built with React, TypeScript, and Chakra UI
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Built-in dark/light theme support
- **Security**: API key authentication, rate limiting, and input sanitization
- **Real-time Chat**: Interactive chat interface with markdown support
- **Sample Questions**: Quick access to common queries
- **Error Handling**: Comprehensive error handling and user feedback
- **Logging**: Secure logging with sensitive data masking

## Tech Stack

### Frontend
- React + TypeScript
- Chakra UI for components and styling
- Vite for build tooling
- React Markdown for message rendering

### Backend
- FastAPI
- Python 3.8+
- Pydantic for data validation
- OpenAI API integration
- Rate limiting with slowapi
- Secure logging

## Security Features

- API Key Authentication
- Request Size Limits
- Input Sanitization
- Rate Limiting
- CORS Configuration
- Sensitive Data Masking in Logs
- Environment-based Configuration

## Getting Started

### Prerequisites

- Node.js 16+
- Python 3.8+
- OpenAI API Key

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd chatbot-backend
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
API_KEY=your_openai_api_key
API_KEY_HEADER=X-API-Key
CORS_ORIGINS=http://localhost:5173,https://your-production-domain.com
MAX_REQUEST_SIZE=1048576
MAX_QUESTION_LENGTH=1000
RATE_LIMIT_GENERATE=10/minute
RATE_LIMIT_CHAT=30/minute
RATE_LIMIT_HEALTH=60/minute
DEVELOPMENT_MODE=true
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd chatbot-frontend
npm install
```

2. Create a `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_KEY=your_api_key
```

3. Start the development server:
```bash
npm run dev
```

## Project Structure

```
.
├── chatbot-backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration and settings
│   ├── logger.py            # Logging configuration
│   ├── security.py          # Security middleware
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── chatbot-frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── config.ts        # Frontend configuration
│   │   └── theme.ts         # Chakra UI theme
│   ├── package.json         # Node dependencies
│   └── .env                 # Frontend environment variables
└── README.md
```

## Security Best Practices

1. **API Keys**:
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly
   - Mask sensitive data in logs

2. **Rate Limiting**:
   - Configure appropriate limits per endpoint
   - Monitor and adjust based on usage

3. **Input Validation**:
   - Sanitize all user inputs
   - Validate request sizes
   - Use Pydantic models for data validation

4. **CORS**:
   - Configure allowed origins
   - Use environment variables for flexibility

## Development vs Production

### Development Mode
- API key checks are optional
- More verbose logging
- CORS allows localhost

### Production Mode
- Strict API key validation
- Minimal logging
- Restricted CORS origins
- Rate limiting enabled

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the API
- FastAPI team for the excellent framework
- Chakra UI for the component library

---
📌 **Stay tuned for more updates!** 🚀

