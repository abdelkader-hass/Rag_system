from pydantic import BaseModel
from litellm import completion
import json
# Define the expected output schema using Pydantic
class CategoryResult(BaseModel):
    category_id: int
    category_name: str
    reason: str

# Function to classify text into categories using AWS Bedrock via LiteLLM
def classify_text_with_bedrock(text: str, categories) -> CategoryResult:

    role = f"""
    You are a helpful classifier.
    Given the following text and dict of categories, determine which category best fits the text.
    the dict key is category name and value is UID of this category
    
    Return your answer strictly as a JSON object with fields:
    category_id, category_name, reason

    categories : {str(categories)}
    """


    response = completion(
        model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",  # example; choose your Bedrock model
        messages=[{"role": "system", "content": "what is my role"},{"role": "user", "content": role},
                  {"role": "system", "content": "okay give me your text to classify"},{"role": "user", "content": f"**Text**: {text}"}],
        response_format=CategoryResult,  # LiteLLM will validate + parse into Pydantic model
    )
    result_json=json.loads(response.choices[0].message.content)

    return result_json  # returns a CategoryResult object


