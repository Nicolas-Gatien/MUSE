import json
import openai

with open("config\\api_keys.json") as f:
    keys = json.load(f)

openai.api_key = keys["openai"]

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class TextEmbedding:
    def __init__(self, model_id="text-embedding-ada-002"):
        self.texts = []
        self.embeddings = []
        self.model_id = model_id

    def add_text(self, text):
        # Get the embeddings from the OpenAI API
        response = openai.Embedding.create(
            input=[text],
            model=self.model_id
        )

        embedding = response['data'][0]['embedding']
        self.texts.append(text)
        self.embeddings.append(embedding)

    def get_most_relevant_text(self, input_text):
        # Get the embedding of the input text
        response = openai.Embedding.create(
            input=[input_text],
            model=self.model_id
        )
        
        input_embedding = response['data'][0]['embedding']
        similarities = cosine_similarity([input_embedding], self.embeddings)
        most_relevant_index = np.argmax(similarities)
        return self.texts[most_relevant_index]

# Create an instance of the class
text_embedding = TextEmbedding(api_key="your-api-key-here")

# Add texts
text_embedding.add_text("The quick brown fox jumps over the lazy dog.")
text_embedding.add_text("The five boxing wizards jump quickly.")

# Get the most relevant text
print(text_embedding.get_most_relevant_text("How quick is the fox?"))
