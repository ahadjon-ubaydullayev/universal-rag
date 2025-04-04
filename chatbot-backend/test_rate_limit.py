import requests
import time
from logger import logger

def test_rate_limit():
    base_url = "http://localhost:8000/chat/"
    
    logger.info("Starting rate limit test")
    
    for i in range(15):  
        try:
            response = requests.get(f"{base_url}/")
            logger.info(f"Request {i+1}: Status {response.status_code}")
            if response.status_code == 429:
                logger.warning(f"Rate limit hit! Response: {response.json()}")
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.info(f"Waiting {retry_after} seconds before next request")
                time.sleep(retry_after)
            else:
                time.sleep(0.1)  
        except Exception as e:
            logger.error(f"Error during request {i+1}: {str(e)}")

if __name__ == "__main__":
    test_rate_limit() 