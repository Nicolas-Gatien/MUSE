import json
import openai

from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

class MemoryModule:
    def __init__(self, model_id="text-embedding-ada-002"):
        self.texts = []
        self.embeddings = []
        self.model_id = model_id
        with open("config\\api_keys.json") as f:
            self.keys = json.load(f)

        openai.api_key = self.keys["openai"]

    def add_memory(self, text):
        now = datetime.now()
        formatted_now = now.strftime("%d/%m/%Y %H:%M:%S")
        text = formatted_now + " " + text
        # Get the embeddings from the OpenAI API
        response = openai.Embedding.create(
            input=[text],
            model=self.model_id
        )

        embedding = response['data'][0]['embedding']
        self.texts.append(text)
        self.embeddings.append(embedding)

    def get_most_relevent_memories(self, input_text, top_n=3):
        # Get the embedding of the input text
        response = openai.Embedding.create(
            input=[input_text],
            model=self.model_id
        )
        
        input_embedding = response['data'][0]['embedding']
        similarities = cosine_similarity([input_embedding], self.embeddings)[0]

        # Get the indices of the top_n most similar texts
        most_relevant_indices = similarities.argsort()[-top_n:][::-1]
        return [self.texts[i] for i in most_relevant_indices]