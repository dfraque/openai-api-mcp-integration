"""
Cliente MCP - Gestión de ideas de proyectos
-------------------------------------------
Este cliente:
1️. Se conecta a un MCP Server.
2. Usa tools para agregar y listar ideas.
3. Usa resources (guías, ejemplos).
4. Usa prompts para generar análisis con GPT-4o-mini.
"""

import os
import asyncio
from openai import OpenAI
from fastmcp import Client

os.environ["OPENAI_API_KEY"] = ""

OPENAI_MODEL = "gpt-4o-mini"
MCP_SERVER_URL = ""


async def main():
    # Conexión al servidor MCP
    client_mcp = Client(MCP_SERVER_URL)

    async with client_mcp:
        print("✅ Conectado al servidor MCP de Gestión de Ideas de Proyectos")

        # Crear una idea con la tool `add_idea`
        response_add = await client_mcp.call_tool(
            "add_idea",
            {"title": "App Verde", "description": "Una app que incentiva el reciclaje con recompensas.", "author": "Danilo"}
        )
        print(f"🆕 {response_add}\n")

        # Listar ideas registradas
        ideas = await client_mcp.call_tool("list_ideas")
        print("📋 Ideas registradas:")
        print(ideas.content)

        # Obtener un recurso (guía)
        guide = await client_mcp.read_resource("ideas://guide")
        print("📘 Guía para evaluar ideas:\n", guide, "\n")

        # Obtener un recurso (ejemplos)
        examples = await client_mcp.read_resource("ideas://examples")
        print("💡 Ejemplos inspiradores:\n", examples, "\n")

        # Obtener un prompt (por ejemplo, "analyze_idea")
        prompt_template = await client_mcp.get_prompt("analyze_idea")
        prompt_text = prompt_template.messages[0].content.text

        # Reemplazar variable de plantilla con una idea concreta
        idea_description = "Una aplicación móvil que conecta turistas con guías locales según sus intereses culturales y gastronómicos."
        final_prompt = prompt_text.replace("{{idea_description}}", idea_description)

        print("\n🧩 Prompt final que se enviará al modelo:\n")
        print(final_prompt)

        # Crear cliente OpenAI
        client_openai = OpenAI()

        # Enviar el prompt al modelo GPT-4o-mini
        print("\n🧠 Generando análisis con GPT-4o-mini...")
        response = client_openai.responses.create(
            model=OPENAI_MODEL,
            input=final_prompt,
        )

        print("\n💬 Respuesta del modelo:\n")
        print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
