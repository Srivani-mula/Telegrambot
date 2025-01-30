import httpx

response = httpx.get("https://google.generativeai.googleapis.com")
print(response.text)
