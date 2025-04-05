import { config } from '../config'

interface ApiResponse {
    response: string;
}

interface ApiError {
    error: string;
    detail: string;}

class ApiService {
    private async fetchWithRetry(
        url: string,
        options: RequestInit,
        retries: number = config.MAX_RETRIES
    ): Promise<Response> {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    [config.API_KEY_HEADER]: config.API_KEY,
                    ...options.headers,
                },
            });

            if (!response.ok) {
                const error: ApiError = await response.json().catch(() => ({
                    error: 'Unknown error',
                    detail: response.statusText
                }));

                switch (response.status) {
                    case 401:
                        throw new Error(config.UNAUTHORIZED_ERROR);
                    case 413:
                        throw new Error(config.REQUEST_TOO_LARGE);
                    case 429:
                        throw new Error(config.RATE_LIMIT_ERROR);
                    case 422:
                        throw new Error(config.VALIDATION_ERROR);
                    default:
                        throw new Error(error.detail || config.API_ERROR);
                }
            }

            return response;
        } catch (error) {
            if (retries > 0) {
                await new Promise(resolve => setTimeout(resolve, config.RETRY_DELAY));
                return this.fetchWithRetry(url, options, retries - 1);
            }
            throw error;
        }
    }

    async generateResponse(question: string): Promise<string> {
        try {
            const response = await this.fetchWithRetry(
                `${config.API_BASE_URL}/generate/`,
                {
                    method: 'POST',
                    body: JSON.stringify({ question }),
                }
            );

            const data: ApiResponse = await response.json();
            return data.response;
        } catch (error) {
            if (error instanceof Error) {
                throw error;
            }
            throw new Error(config.DEFAULT_ERROR_MESSAGE);
        }
    }

    async chatResponse(question: string): Promise<string> {
        try {
            const response = await this.fetchWithRetry(
                `${config.API_BASE_URL}/chat/`,
                {
                    method: 'POST',
                    body: JSON.stringify({ question }),
                }
            );

            const data: ApiResponse = await response.json();
            return data.response;
        } catch (error) {
            if (error instanceof Error) {
                throw error;
            }
            throw new Error(config.DEFAULT_ERROR_MESSAGE);
        }
    }

    async checkHealth(): Promise<boolean> {
        try {
            const response = await this.fetchWithRetry(
                `${config.API_BASE_URL}/`,
                {
                    method: 'GET',
                }
            );
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

export const apiService = new ApiService(); 