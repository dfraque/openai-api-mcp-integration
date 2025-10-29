from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

resp = client.responses.create(
    model="gpt-4o-mini",
    tools=[
        {
            "type": "mcp",
            "server_label": "test_server",
            "server_url": "https://combative-red-kite.fastmcp.app/mcp",
            "require_approval": "never",
        },
    ],
    input="How many r's are in the word 'Terrarium'?",
)

print(resp.output_text)