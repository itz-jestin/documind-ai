from dotenv import load_dotenv
import os

load_dotenv()

print("OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))