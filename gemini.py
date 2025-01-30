import requests
import json
import base64
import certifi
import os
from config import GEMINI_API_KEY, SERPAPI_KEY # Ensure API Key is in config.py

# Load API key from environment variables if not in config.py
API_KEY = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)


def get_gemini_response(user_input):
    """Generate a text response using Gemini API"""
    API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": user_input}]}]  # ✅ Correct JSON structure
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No response generated.")
        else:
            return "No response generated."
    else:
        return f"❌ Error generating response: {response.status_code} - {response.text}"


def analyze_image_or_file(image_path):
    """Analyze an image using Gemini API (New Model)"""
    API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}

    # Read image & convert to base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": "image/png", "data": image_data}},  # Change mime_type if needed
                {"text": "Describe this image."}
            ]
        }]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No description found.")
        else:
            return "No description found."
    else:
        return f"❌ Could not analyze the file. Error {response.status_code}: {response.text}"
    

def perform_web_search(query):
    """Perform a web search using SerpAPI and return results with clickable links."""
    SERPAPI_URL = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5,  # Fetch top 5 results
    }

    try:
        response = requests.get(SERPAPI_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("organic_results", [])

            if not results:
                return "❌ No relevant search results found."

            # Format results with clickable links
            search_summary = "**🔎 Web Search Results:**\n\n"
            for idx, result in enumerate(results, start=1):
                title = result.get("title", "No title")
                link = result.get("link", "#")
                snippet = result.get("snippet", "No description available.")
                search_summary += f"**{idx}. [{title}]({link})**\n_{snippet}_\n\n"

            return search_summary
        else:
            return f"❌ Web search error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Web search failed: {str(e)}"
