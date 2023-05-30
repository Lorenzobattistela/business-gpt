import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def prompt(prompt: str):
    response = openai.Completion.create(
      engine='text-davinci-003',
      prompt=prompt,
      max_tokens=1000,
    )
    return response.choices[0].text

def initial_preparation():
    prompt("Olá Chat! Preciso que você aja como um expert em SEO e copywriting, além de um especialista em otimização de páginas do Google Meu Negócio. Ok?")
