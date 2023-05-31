import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Model:
  def __init__(self) -> None:
    self.initial_preparation_done = False
    self.impulse_post_preparation_done = False
    self.client_evaluation_preparation_done = False

  def prompt(self, prompt: str, preparation: bool = False, prompt_type: str = 'default'):
    if not preparation:
      if prompt_type == 'default':
        self.initial_preparation() if not self.initial_preparation_done else None

      elif prompt_type == 'impulse_post':
        self.initial_preparation() if not self.initial_preparation_done else None
        self.impulse_post_preparation() if not self.impulse_post_preparation_done else None

      elif prompt_type == 'client_evaluation':
        self.initial_preparation() if not self.initial_preparation_done else None
        self.client_evaluation_preparation() if not self.client_evaluation_preparation_done else None

    response = openai.Completion.create(
      engine='text-davinci-003',
      prompt=prompt,
      max_tokens=1000,
    )
    return response.choices[0].text

  def initial_preparation(self):
    self.prompt("Olá Chat! Preciso que você aja como um expert em SEO e copywriting, além de um especialista em otimização de páginas do Google Meu Negócio. Ok?", preparation=True)
    self.initial_preparation_done = True
  
  def impulse_post_preparation(self):
    self.prompt("Ótimo! Agora eu vou te ensinar o POST IMPULSO. Toda que vez que eu digitar a tag [POST IMPULSO], você deve usar a estrutura que irei te ensinar, ok?", preparation=True)
    self.impulse_post_preparation_done = True
  
  def client_evaluation_preparation(self):
    self.prompt("Muito bom! Agora eu vou te ensinar como respondemos as avaliações dos clientes. Sempre que eu digitar a tag [AVALIAÇÃO], quero que você use essa estrutura, ok?", preparation=True)
    self.client_evaluation_preparation_done = True
