import ollama


class OllamaEmbeddingAdapter:
    def __init__(
        self,
        model="nomic-embed-text:latest",
        host="http://host.docker.internal:11434"
    ):
        self.model = model
        self.client = ollama.Client(
            host=host
        )


    def embed(self, text: str):

        response = self.client.embeddings(
            model=self.model,
            prompt=text
        )

        return response["embedding"]
