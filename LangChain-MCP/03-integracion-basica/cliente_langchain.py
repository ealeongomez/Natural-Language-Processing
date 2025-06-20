#!/usr/bin/env python3
"""
Cliente LangChain que se conecta al servidor MCP
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde la carpeta principal
directorio_actual = Path(__file__).parent
directorio_principal = directorio_actual.parent.parent
archivo_env = directorio_principal / ".env"

if archivo_env.exists():
    load_dotenv(archivo_env)
    print(f"✅ Variables de entorno cargadas desde: {archivo_env}")
else:
    print(f"❌ Archivo .env no encontrado en: {archivo_env}")
    print("💡 Crea el archivo .env copiando desde env.example:")
    print(f"   cp {directorio_principal}/env.example {directorio_principal}/.env")
    exit(1)

# Verificar que la API key esté configurada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY no configurada en el archivo .env")
    print("💡 Agrega tu API key de OpenAI al archivo .env")
    exit(1)

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
    from langchain.tools import MCPToolkit
    from langchain.agents import initialize_agent, AgentType
except ImportError as e:
    print(f"❌ Error al importar dependencias: {e}")
    print("💡 Instala las dependencias: pip install -r ../requirements.txt")
    exit(1)

class ClienteLangChainMCP:
    def __init__(self):
        """Inicializar cliente LangChain con MCP"""
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        # Configurar toolkit MCP
        self.mcp_toolkit = MCPToolkit(
            server_command=["python", "servidor_mcp_simple.py"]
        )
        
        # Inicializar agente
        self.agent = initialize_agent(
            tools=self.mcp_toolkit.get_tools(),
            llm=self.chat_model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    async def ejecutar_consulta(self, consulta: str) -> str:
        """Ejecutar una consulta usando el agente"""
        try:
            resultado = await self.agent.arun(consulta)
            return resultado
        except Exception as e:
            return f"Error: {str(e)}"
    
    def ejecutar_consulta_sincrona(self, consulta: str) -> str:
        """Ejecutar una consulta de forma síncrona"""
        return asyncio.run(self.ejecutar_consulta(consulta))

def main():
    """Función principal para probar la integración"""
    print("🤖 Iniciando cliente LangChain con MCP...")
    print(f"🔑 API Key configurada: {api_key[:7]}...{api_key[-4:]}")
    
    # Crear cliente
    try:
        cliente = ClienteLangChainMCP()
        print("✅ Cliente inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar cliente: {e}")
        return
    
    # Ejemplos de consultas
    consultas = [
        "Calcula 15 + 27",
        "¿Cuál es el resultado de 100 dividido por 4?",
        "Calcula 5 elevado a la 3",
        "Obtén información del producto con ID 2",
        "¿Cuánto es 50 multiplicado por 3.5?"
    ]
    
    print("\n📝 Ejecutando consultas de ejemplo:\n")
    
    for i, consulta in enumerate(consultas, 1):
        print(f"Consulta {i}: {consulta}")
        print("-" * 50)
        
        try:
            resultado = cliente.ejecutar_consulta_sincrona(consulta)
            print(f"Respuesta: {resultado}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main() 