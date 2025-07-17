import sys
import os
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.core.utils import search_news
from app.core.logger import logger
import logging

# Configure logger to show debug messages
logger.setLevel(logging.DEBUG)

def run_test(topic):
    print(f"\n--- Testing search_news with topic: '{topic}' ---")
    try:
        result_json = search_news(topic)
        print(f"search_news returned: {result_json}")
        # If result_json is a valid JSON string, try to parse it
        try:
            parsed_result = json.loads(result_json)
            print(f"Number of articles found: {len(parsed_result)}")
        except json.JSONDecodeError:
            print("Returned string is not valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Test cases
    run_test("AI")
    run_test("Middle East tensions")
    run_test("tech layoffs")
    run_test("nonexistent topic that should return 0")
