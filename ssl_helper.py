import ssl
import requests

# Create an SSL context to specify the trusted certificate authorities
context = ssl.create_default_context(cafile="path_to_ca_bundle.crt")

response = requests.get("https://google.generativeai.googleapis.com", verify=context)
print(response.text)
