export const config = {
    API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    API_KEY: import.meta.env.VITE_API_KEY || '',
    API_KEY_HEADER: 'X-API-Key',
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000, // 1 second
    MAX_MESSAGE_LENGTH: 500,
    DEFAULT_ERROR_MESSAGE: 'An error occurred. Please try again.',
    RATE_LIMIT_ERROR: 'Too many requests. Please wait a moment before trying again.',
    NETWORK_ERROR: 'Network error. Please check your connection and try again.',
    API_ERROR: 'API error. Please try again later.',
    VALIDATION_ERROR: 'Invalid input. Please check your message and try again.',
    UNAUTHORIZED_ERROR: 'Unauthorized. Please check your API key.',
    REQUEST_TOO_LARGE: 'Request too large. Please reduce the size of your message.',
    DEFAULT_QUESTIONS: [
        'What are the visiting hours at the hospital?',
        'Who are the cardiology specialists at Harmony Health Center?',
        'What payment options are available at the hospital?',
        'What specialties does the hospital offer?',
        'Where is Harmony Health Center located?'
    ]
} 