from starlette.requests import Request
from typing import Dict

import ray
from ray import serve
from ray.serve.handle import DeploymentHandle

from transformers import pipeline


@serve.deployment
class MaskFiller:
    def __init__(self):
        # Initialize the BERT fill-mask pipeline with the model "bert-base-uncased"
        self.model = pipeline("fill-mask", model="bert-base-uncased")

    def fill_mask(self, text: str) -> str:
        # Fill the mask in the provided text
        model_output = self.model(text)

        # Return the top prediction
        filled_text = model_output[0]["sequence"]

        return filled_text

    async def __call__(self, http_request: Request) -> Dict:
        try:
            # Attempt to get the request body as JSON
            request_dataL: str = await http_request.json()
            result = self.fill_mask(request_data)
            return {"filled_text": result}

        except Exception as e:
            # If there's any error, return a message
            return {"error": f"An error occurred: {str(e)}"}

    def reconfigure(self, config: Dict):
        # Placeholder for reconfiguration logic if needed
        pass


# Bind the deployment
app = MaskFiller.bind()
