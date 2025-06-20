# 3. Integración Básica

## Primer Ejemplo: Conectar LangChain con MCP

En este módulo aprenderás a crear tu primera integración entre LangChain y MCP. Comenzaremos con un ejemplo simple que demuestra los conceptos fundamentales.

## Estructura del Proyecto

```
03-integracion-basica/
├── README.md
├── ejemplo_basico.py
├── servidor_mcp_simple.py
├── cliente_langchain.py
└── datos_ejemplo/
    └── productos.json
```

## Ejemplo 1: Calculadora Simple

### Servidor MCP Básico

Crea el archivo `servidor_mcp_simple.py`:

```python
#!/usr/bin/env python3
"""
Servidor MCP simple con herramientas básicas
"""

import json
import math
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

# Crear servidor MCP
server = Server("calculadora-mcp")

@server.tool()
async def sumar(a: float, b: float) -> float:
    """Suma dos números"""
    return a + b

@server.tool()
async def restar(a: float, b: float) -> float:
    """Resta dos números"""
    return a - b

@server.tool()
async def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números"""
    return a * b

@server.tool()
async def dividir(a: float, b: float) -> float:
    """Divide dos números"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

@server.tool()
async def calcular_potencia(base: float, exponente: float) -> float:
    """Calcula la potencia de un número"""
    return math.pow(base, exponente)

@server.tool()
async def obtener_info_producto(id_producto: int) -> Dict[str, Any]:
    """Obtiene información de un producto por ID"""
    # Simulación de base de datos
    productos = {
        1: {"id": 1, "nombre": "Laptop", "precio": 999.99, "stock": 10},
        2: {"id": 2, "nombre": "Mouse", "precio": 29.99, "stock": 50},
        3: {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 25}
    }
    
    if id_producto in productos:
        return productos[id_producto]
    else:
        return {"error": "Producto no encontrado"}

if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP...")
    stdio_server.run(server)
```

### Cliente LangChain

Crea el archivo `cliente_langchain.py`:

```python
#!/usr/bin/env python3
"""
Cliente LangChain que se conecta al servidor MCP
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import MCPToolkit
from langchain.agents import initialize_agent, AgentType

# Cargar variables de entorno
load_dotenv()

class ClienteLangChainMCP:
    def __init__(self):
        """Inicializar cliente LangChain con MCP"""
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
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
    
    # Crear cliente
    cliente = ClienteLangChainMCP()
    
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
```

## Ejemplo 2: Chatbot con Herramientas Personalizadas

### Servidor MCP Avanzado

Crea el archivo `servidor_mcp_avanzado.py`:

```python
#!/usr/bin/env python3
"""
Servidor MCP avanzado con herramientas más complejas
"""

import json
import requests
from datetime import datetime
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("herramientas-avanzadas-mcp")

@server.tool()
async def obtener_clima(ciudad: str) -> Dict[str, Any]:
    """Obtiene el clima actual de una ciudad"""
    # Nota: En un ejemplo real, usarías una API real
    # Por ahora simulamos la respuesta
    climas = {
        "madrid": {"temperatura": 22, "condicion": "Soleado", "humedad": 45},
        "barcelona": {"temperatura": 25, "condicion": "Parcialmente nublado", "humedad": 60},
        "valencia": {"temperatura": 28, "condicion": "Soleado", "humedad": 50}
    }
    
    ciudad_lower = ciudad.lower()
    if ciudad_lower in climas:
        return {
            "ciudad": ciudad,
            "clima": climas[ciudad_lower],
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {"error": f"No hay datos disponibles para {ciudad}"}

@server.tool()
async def convertir_moneda(cantidad: float, de_moneda: str, a_moneda: str) -> Dict[str, Any]:
    """Convierte entre diferentes monedas"""
    # Tasas de cambio simuladas
    tasas = {
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 130.5},
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.8},
        "GBP": {"EUR": 1.16, "USD": 1.37, "JPY": 151.2}
    }
    
    if de_moneda in tasas and a_moneda in tasas[de_moneda]:
        tasa = tasas[de_moneda][a_moneda]
        resultado = cantidad * tasa
        return {
            "cantidad_original": cantidad,
            "moneda_origen": de_moneda,
            "moneda_destino": a_moneda,
            "tasa_cambio": tasa,
            "resultado": round(resultado, 2)
        }
    else:
        return {"error": "Monedas no soportadas"}

@server.tool()
async def buscar_noticias(termino: str, max_resultados: int = 5) -> List[Dict[str, Any]]:
    """Busca noticias relacionadas con un término"""
    # Simulación de búsqueda de noticias
    noticias_ejemplo = [
        {
            "titulo": f"Avances en {termino} revolucionan la industria",
            "resumen": f"Los últimos desarrollos en {termino} están cambiando el panorama tecnológico.",
            "fecha": "2024-01-15",
            "fuente": "TechNews"
        },
        {
            "titulo": f"Expertos discuten el futuro de {termino}",
            "resumen": f"Una conferencia internacional abordó las tendencias en {termino}.",
            "fecha": "2024-01-14",
            "fuente": "ScienceDaily"
        }
    ]
    
    return noticias_ejemplo[:max_resultados]

@server.tool()
async def analizar_sentimiento(texto: str) -> Dict[str, Any]:
    """Analiza el sentimiento de un texto"""
    # Análisis simple de sentimiento
    palabras_positivas = ["bueno", "excelente", "fantástico", "maravilloso", "genial"]
    palabras_negativas = ["malo", "terrible", "horrible", "pésimo", "decepcionante"]
    
    texto_lower = texto.lower()
    positivas = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
    negativas = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
    
    if positivas > negativas:
        sentimiento = "positivo"
        puntuacion = 0.8
    elif negativas > positivas:
        sentimiento = "negativo"
        puntuacion = 0.2
    else:
        sentimiento = "neutral"
        puntuacion = 0.5
    
    return {
        "texto": texto,
        "sentimiento": sentimiento,
        "puntuacion": puntuacion,
        "palabras_positivas": positivas,
        "palabras_negativas": negativas
    }

if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP avanzado...")
    stdio_server.run(server)
```

## Ejemplo Completo: Chatbot Interactivo

Crea el archivo `chatbot_interactivo.py`:

```python
#!/usr/bin/env python3
"""
Chatbot interactivo usando LangChain y MCP
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import MCPToolkit
from langchain.agents import initialize_agent, AgentType

load_dotenv()

class ChatbotInteractivo:
    def __init__(self):
        """Inicializar chatbot"""
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configurar toolkit MCP
        self.mcp_toolkit = MCPToolkit(
            server_command=["python", "servidor_mcp_avanzado.py"]
        )
        
        # Inicializar agente
        self.agent = initialize_agent(
            tools=self.mcp_toolkit.get_tools(),
            llm=self.chat_model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        self.historial = []
    
    def agregar_al_historial(self, usuario: str, bot: str):
        """Agregar mensaje al historial"""
        self.historial.append({"usuario": usuario, "bot": bot})
    
    def mostrar_historial(self):
        """Mostrar historial de conversación"""
        if not self.historial:
            print("No hay historial de conversación.")
            return
        
        print("\n📜 Historial de conversación:")
        print("=" * 50)
        for i, mensaje in enumerate(self.historial, 1):
            print(f"{i}. Usuario: {mensaje['usuario']}")
            print(f"   Bot: {mensaje['bot']}")
            print("-" * 30)
    
    async def procesar_mensaje(self, mensaje: str) -> str:
        """Procesar mensaje del usuario"""
        try:
            respuesta = await self.agent.arun(mensaje)
            self.agregar_al_historial(mensaje, respuesta)
            return respuesta
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.agregar_al_historial(mensaje, error_msg)
            return error_msg
    
    def procesar_mensaje_sincrono(self, mensaje: str) -> str:
        """Procesar mensaje de forma síncrona"""
        return asyncio.run(self.procesar_mensaje(mensaje))

def main():
    """Función principal del chatbot interactivo"""
    print("🤖 Bienvenido al Chatbot con MCP!")
    print("Escribe 'salir' para terminar, 'historial' para ver el historial")
    print("=" * 60)
    
    chatbot = ChatbotInteractivo()
    
    while True:
        try:
            # Obtener entrada del usuario
            mensaje = input("\n👤 Tú: ").strip()
            
            # Verificar comandos especiales
            if mensaje.lower() == 'salir':
                print("👋 ¡Hasta luego!")
                break
            elif mensaje.lower() == 'historial':
                chatbot.mostrar_historial()
                continue
            elif not mensaje:
                continue
            
            # Procesar mensaje
            print("🤖 Bot: Procesando...")
            respuesta = chatbot.procesar_mensaje_sincrono(mensaje)
            print(f"🤖 Bot: {respuesta}")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Cómo Ejecutar los Ejemplos

### 1. Ejemplo Básico

```bash
# Terminal 1: Ejecutar servidor MCP
python servidor_mcp_simple.py

# Terminal 2: Ejecutar cliente LangChain
python cliente_langchain.py
```

### 2. Chatbot Interactivo

```bash
# Ejecutar chatbot interactivo
python chatbot_interactivo.py
```

## Pruebas y Verificación

### Script de Pruebas

Crea el archivo `pruebas_integracion.py`:

```python
#!/usr/bin/env python3
"""
Script para probar la integración básica
"""

import asyncio
from cliente_langchain import ClienteLangChainMCP

async def ejecutar_pruebas():
    """Ejecutar pruebas de integración"""
    print("🧪 Ejecutando pruebas de integración...")
    
    cliente = ClienteLangChainMCP()
    
    pruebas = [
        "Calcula 10 + 5",
        "¿Cuál es 20 multiplicado por 3?",
        "Obtén información del producto 1"
    ]
    
    for i, prueba in enumerate(pruebas, 1):
        print(f"\nPrueba {i}: {prueba}")
        print("-" * 40)
        
        try:
            resultado = await cliente.ejecutar_consulta(prueba)
            print(f"✅ Resultado: {resultado}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Pruebas completadas!")

if __name__ == "__main__":
    asyncio.run(ejecutar_pruebas())
```

## Próximos Pasos

En el siguiente módulo aprenderás a crear herramientas más avanzadas y personalizadas.

---

**Siguiente**: [Herramientas Avanzadas](../04-herramientas-avanzadas/) 