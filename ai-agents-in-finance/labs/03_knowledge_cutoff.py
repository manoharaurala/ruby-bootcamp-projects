from openai import OpenAI
from ai_agents_finance.config import load_config

client = OpenAI(
    api_key = load_config()["openai_api_key"]
)

response = client.responses.create(
    model="gpt-4.1",
    input="Give me the latest news about NVIDIA.",
)
print(response.output_text)