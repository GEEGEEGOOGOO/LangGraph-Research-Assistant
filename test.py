import os
from langchain_google_genai import ChatGoogleGenerativeAI

# PLACEHOLDER: Replace with your actual API key
GEMINI_API_KEY = "AIzaSyD2YZ2GgvuIhF1IXIQ5gn8F9TJVV-MPnhA"

def test_key():
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("Please replace 'YOUR_GEMINI_API_KEY_HERE' with your actual API key in the script.")
        return

    print(f"Testing with key: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")
    
    try:
        print("Initializing ChatGoogleGenerativeAI...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
        print("Invoking model...")
        response = llm.invoke("Hello, are you working?")
        print("Success! Response:")
        print(response.content)
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    test_key()
