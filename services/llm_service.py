from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from pprint import pprint
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def ask_llm(context,question):

    
    start=time.perf_counter()
    response=client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {
                "role":"user",
                "content": f"""
                Context:
                {context}
                
                Question:
                {question}
                
                Instructions:
                - Answer only from the provided context.
                - Generate the answer in less that 10 seconds.
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
    print("Response object:")
    pprint(response.model_dump())
    print("Choices:", response.choices)
    
    try:
        return response.choices[0].message.content
    except Exception as e:
        print("LLM Error:", e)
        print(response)
        return f"LLM Error: {e}"
       