import os
import google.generativeai as genai
import argparse
import json

def load_api_key_from_file(filepath):
    """
    Loads the API key from a JSON file.

    Args:
        filepath: The path to the JSON file.

    Returns:
        The API key, or None if an error occurred.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get('key')
    except FileNotFoundError:
        print(f"Error: API key file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None
    except Exception as e:
        print(f"Error: An error occurred while loading the API key: {e}")
        return None

def query_gemini_flash(question, api_key=None):
    """
    Queries the Google Gemini Flash API with a given question and returns the response.

    Args:
        question: The question to ask the API.
        api_key: Your Google Gemini API key.  If None, tries to read from environment variable 'GOOGLE_API_KEY'.

    Returns:
        The response from the Gemini Flash API, or None if an error occurred.
    """
    if not api_key:
        api_key = load_api_key_from_file("keys/GOOGLE_API_KEY.json")

        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                print("Error: Google API key not provided, not found in keys/GOOGLE_API_KEY.json, and GOOGLE_API_KEY environment variable not set.")
                return None

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash') # Use the correct model name (flash version)

    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        print(f"Error: An error occurred while querying the API: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Google Gemini Flash API from the command line.")
    parser.add_argument("question", nargs="+", help="The question to ask the API.  Enclose in quotes if multiple words.")
    parser.add_argument("--api-key", help="Your Google Gemini API key.  Overrides environment variable and file.", default=None)

    args = parser.parse_args()

    question = " ".join(args.question)

    response = query_gemini_flash(question, args.api_key)

    if response:
        print(response)
