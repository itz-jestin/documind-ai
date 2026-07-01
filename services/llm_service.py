from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def ask_llm(context, question):

    start = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    
                    Context:
                    {context}
                    
                    Question:
                    {question}
                    
                    Instructions:
                    - Answer only from the provided context.
                    - Keep the answer under 50 words.
                    - Do not explain your reasoning.
                    - If the answer is not clearly present, say:
                      "The information is not available in the PDF."
                    - Do not guess.
                    """
                                    }
                                ]
                            )

        print("LLM Response Time:", time.perf_counter() - start)

        return response.choices[0].message.content

    except RateLimitError:
        print("OpenRouter Rate Limit exceeded.")
        return "⚠️ The AI service is currently busy. Please try again in a few seconds."

    except Exception as e:
        print("=" * 50)
        print("LLM ERROR")
        print(type(e))
        print(e)
        print("=" * 50)
    
        return "⚠️ Unable to generate an answer at the moment."