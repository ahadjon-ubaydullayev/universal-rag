# RAG Chatbot Frontend

This is the frontend for the RAG (Retrieval-Augmented Generation) chatbot. It provides a clean and intuitive interface for interacting with the chatbot.

## Features

- Modern and responsive UI using Chakra UI
- Real-time chat interface
- Sample questions sidebar
- Message history
- Loading states and error handling

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend server running on http://localhost:8000

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## Usage

1. Type your question in the input field at the bottom of the chat area
2. Click the "Send" button or press Enter to send your message
3. Click on any sample question in the sidebar to quickly ask common questions
4. Wait for the chatbot's response

## Development

The project is built with:
- React
- TypeScript
- Vite
- Chakra UI
- Axios

## Project Structure

```
src/
  ├── components/
  │   ├── Navbar.tsx
  │   ├── Sidebar.tsx
  │   └── ChatArea.tsx
  ├── App.tsx
  └── main.tsx
``` 