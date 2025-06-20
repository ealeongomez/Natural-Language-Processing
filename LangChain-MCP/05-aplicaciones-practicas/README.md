# 5. Aplicaciones Prácticas

## Casos de Uso Reales con LangChain y MCP

En este módulo aprenderás a crear aplicaciones completas y funcionales usando LangChain y MCP. Cada aplicación demuestra diferentes aspectos de la integración y te proporcionará ejemplos reales que puedes adaptar a tus necesidades.

## Estructura del Proyecto

```
05-aplicaciones-practicas/
├── README.md
├── chatbot_empresarial/
│   ├── __init__.py
│   ├── servidor_mcp.py
│   ├── chatbot.py
│   └── datos_ejemplo/
│       ├── productos.json
│       ├── clientes.csv
│       └── ventas.json
├── asistente_analisis/
│   ├── __init__.py
│   ├── servidor_mcp.py
│   ├── asistente.py
│   └── datos_ejemplo/
│       ├── dataset.csv
│       └── config.json
└── integrador_bd/
    ├── __init__.py
    ├── servidor_mcp.py
    ├── cliente.py
    └── schema.sql
```

## Aplicación 1: Chatbot Empresarial

### Descripción

Un chatbot inteligente que puede:
- Consultar información de productos
- Procesar pedidos
- Responder preguntas sobre la empresa
- Generar reportes básicos

### Servidor MCP Empresarial

Crea el archivo `chatbot_empresarial/servidor_mcp.py`:

```python
#!/usr/bin/env python3
"""
Servidor MCP para chatbot empresarial
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("chatbot-empresarial-mcp")

# Datos simulados de la empresa
PRODUCTOS = {
    1: {"id": 1, "nombre": "Laptop Pro", "precio": 1299.99, "stock": 15, "categoria": "Tecnología"},
    2: {"id": 2, "nombre": "Mouse Inalámbrico", "precio": 29.99, "stock": 50, "categoria": "Accesorios"},
    3: {"id": 3, "nombre": "Teclado Mecánico", "precio": 89.99, "stock": 25, "categoria": "Accesorios"},
    4: {"id": 4, "nombre": "Monitor 4K", "precio": 399.99, "stock": 10, "categoria": "Tecnología"},
    5: {"id": 5, "nombre": "Auriculares Bluetooth", "precio": 79.99, "stock": 30, "categoria": "Audio"}
}

CLIENTES = {
    1: {"id": 1, "nombre": "Juan Pérez", "email": "juan@email.com", "telefono": "+34 600 123 456"},
    2: {"id": 2, "nombre": "María García", "email": "maria@email.com", "telefono": "+34 600 789 012"},
    3: {"id": 3, "nombre": "Carlos López", "email": "carlos@email.com", "telefono": "+34 600 345 678"}
}

VENTAS = [
    {"id": 1, "cliente_id": 1, "producto_id": 1, "cantidad": 1, "fecha": "2024-01-15", "total": 1299.99},
    {"id": 2, "cliente_id": 2, "producto_id": 2, "cantidad": 2, "fecha": "2024-01-16", "total": 59.98},
    {"id": 3, "cliente_id": 1, "producto_id": 3, "cantidad": 1, "fecha": "2024-01-17", "total": 89.99},
    {"id": 4, "cliente_id": 3, "producto_id": 4, "cantidad": 1, "fecha": "2024-01-18", "total": 399.99}
]

@server.tool()
async def buscar_producto(termino: str) -> Dict[str, Any]:
    """Buscar productos por nombre o categoría"""
    resultados = []
    termino_lower = termino.lower()
    
    for producto in PRODUCTOS.values():
        if (termino_lower in producto["nombre"].lower() or 
            termino_lower in producto["categoria"].lower()):
            resultados.append(producto)
    
    return {
        "termino_busqueda": termino,
        "resultados": resultados,
        "total_encontrados": len(resultados)
    }

@server.tool()
async def obtener_producto_por_id(id_producto: int) -> Dict[str, Any]:
    """Obtener información detallada de un producto por ID"""
    if id_producto in PRODUCTOS:
        return {
            "producto": PRODUCTOS[id_producto],
            "encontrado": True
        }
    else:
        return {
            "error": f"Producto con ID {id_producto} no encontrado",
            "encontrado": False
        }

@server.tool()
async def verificar_stock(id_producto: int, cantidad: int = 1) -> Dict[str, Any]:
    """Verificar disponibilidad de stock para un producto"""
    if id_producto not in PRODUCTOS:
        return {"error": "Producto no encontrado"}
    
    producto = PRODUCTOS[id_producto]
    disponible = producto["stock"] >= cantidad
    
    return {
        "producto": producto["nombre"],
        "stock_disponible": producto["stock"],
        "cantidad_solicitada": cantidad,
        "disponible": disponible,
        "stock_insuficiente": producto["stock"] - cantidad if disponible else cantidad - producto["stock"]
    }

@server.tool()
async def procesar_pedido(cliente_id: int, producto_id: int, cantidad: int) -> Dict[str, Any]:
    """Procesar un pedido de un cliente"""
    # Verificar que el cliente existe
    if cliente_id not in CLIENTES:
        return {"error": "Cliente no encontrado"}
    
    # Verificar que el producto existe
    if producto_id not in PRODUCTOS:
        return {"error": "Producto no encontrado"}
    
    # Verificar stock
    stock_check = await verificar_stock(producto_id, cantidad)
    if not stock_check["disponible"]:
        return {"error": "Stock insuficiente", "detalles": stock_check}
    
    # Calcular total
    producto = PRODUCTOS[producto_id]
    total = producto["precio"] * cantidad
    
    # Simular procesamiento del pedido
    pedido = {
        "id": len(VENTAS) + 1,
        "cliente_id": cliente_id,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "estado": "procesado"
    }
    
    # Actualizar stock (en un caso real, esto se haría en una base de datos)
    PRODUCTOS[producto_id]["stock"] -= cantidad
    
    return {
        "mensaje": "Pedido procesado exitosamente",
        "pedido": pedido,
        "cliente": CLIENTES[cliente_id]["nombre"],
        "producto": producto["nombre"]
    }

@server.tool()
async def obtener_historial_cliente(cliente_id: int) -> Dict[str, Any]:
    """Obtener historial de compras de un cliente"""
    if cliente_id not in CLIENTES:
        return {"error": "Cliente no encontrado"}
    
    compras = [venta for venta in VENTAS if venta["cliente_id"] == cliente_id]
    
    total_gastado = sum(compra["total"] for compra in compras)
    
    return {
        "cliente": CLIENTES[cliente_id],
        "compras": compras,
        "total_compras": len(compras),
        "total_gastado": total_gastado
    }

@server.tool()
async def generar_reporte_ventas(fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
    """Generar reporte de ventas por período"""
    if not fecha_inicio:
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not fecha_fin:
        fecha_fin = datetime.now().strftime("%Y-%m-%d")
    
    ventas_periodo = [
        venta for venta in VENTAS 
        if fecha_inicio <= venta["fecha"] <= fecha_fin
    ]
    
    total_ventas = sum(venta["total"] for venta in ventas_periodo)
    productos_vendidos = {}
    
    for venta in ventas_periodo:
        producto_id = venta["producto_id"]
        if producto_id in PRODUCTOS:
            nombre_producto = PRODUCTOS[producto_id]["nombre"]
            if nombre_producto not in productos_vendidos:
                productos_vendidos[nombre_producto] = 0
            productos_vendidos[nombre_producto] += venta["cantidad"]
    
    return {
        "periodo": {"inicio": fecha_inicio, "fin": fecha_fin},
        "total_ventas": len(ventas_periodo),
        "ingresos_totales": total_ventas,
        "productos_vendidos": productos_vendidos,
        "ventas_detalle": ventas_periodo
    }

@server.tool()
async def obtener_informacion_empresa() -> Dict[str, Any]:
    """Obtener información general de la empresa"""
    return {
        "nombre": "TechStore S.L.",
        "descripcion": "Tienda especializada en tecnología y accesorios informáticos",
        "fundacion": "2020",
        "empleados": 25,
        "ubicacion": "Madrid, España",
        "contacto": {
            "telefono": "+34 900 123 456",
            "email": "info@techstore.es",
            "web": "www.techstore.es"
        },
        "horario": "Lunes a Viernes: 9:00-18:00, Sábados: 10:00-14:00",
        "servicios": [
            "Venta de productos tecnológicos",
            "Soporte técnico",
            "Reparación de equipos",
            "Consultoría IT"
        ]
    }

if __name__ == "__main__":
    print("🏢 Iniciando servidor MCP empresarial...")
    stdio_server.run(server)
```

### Chatbot Empresarial

Crea el archivo `chatbot_empresarial/chatbot.py`:

```python
#!/usr/bin/env python3
"""
Chatbot empresarial usando LangChain y MCP
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import MCPToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

load_dotenv()

class ChatbotEmpresarial:
    def __init__(self):
        """Inicializar chatbot empresarial"""
        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configurar toolkit MCP
        self.mcp_toolkit = MCPToolkit(
            server_command=["python", "servidor_mcp.py"]
        )
        
        # Configurar memoria para mantener contexto
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Inicializar agente
        self.agent = initialize_agent(
            tools=self.mcp_toolkit.get_tools(),
            llm=self.chat_model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        
        self.historial = []
    
    def agregar_al_historial(self, usuario: str, bot: str):
        """Agregar mensaje al historial"""
        self.historial.append({"usuario": usuario, "bot": bot})
    
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
    
    def mostrar_ayuda(self):
        """Mostrar comandos disponibles"""
        ayuda = """
🤖 **Chatbot Empresarial - Comandos Disponibles**

**Consultas de Productos:**
- "Busca laptops"
- "¿Qué productos tienes en stock?"
- "Muéstrame información del producto 1"
- "¿Hay stock del mouse inalámbrico?"

**Pedidos:**
- "Quiero hacer un pedido"
- "Procesa un pedido para el cliente 1, producto 2, cantidad 1"

**Clientes:**
- "Muéstrame el historial del cliente 1"
- "¿Qué ha comprado María García?"

**Reportes:**
- "Genera un reporte de ventas"
- "¿Cuáles fueron las ventas del último mes?"

**Información de la Empresa:**
- "Cuéntame sobre la empresa"
- "¿Cuál es el horario de atención?"

**Comandos Especiales:**
- 'ayuda' - Mostrar esta ayuda
- 'historial' - Ver historial de conversación
- 'salir' - Terminar sesión
        """
        print(ayuda)

def main():
    """Función principal del chatbot empresarial"""
    print("🏢 Bienvenido al Chatbot Empresarial de TechStore!")
    print("Escribe 'ayuda' para ver los comandos disponibles")
    print("=" * 60)
    
    chatbot = ChatbotEmpresarial()
    
    while True:
        try:
            # Obtener entrada del usuario
            mensaje = input("\n👤 Cliente: ").strip()
            
            # Verificar comandos especiales
            if mensaje.lower() == 'salir':
                print("👋 ¡Gracias por usar nuestro chatbot!")
                break
            elif mensaje.lower() == 'ayuda':
                chatbot.mostrar_ayuda()
                continue
            elif mensaje.lower() == 'historial':
                if chatbot.historial:
                    print("\n📜 Historial de conversación:")
                    for i, msg in enumerate(chatbot.historial, 1):
                        print(f"{i}. Cliente: {msg['usuario']}")
                        print(f"   Bot: {msg['bot'][:100]}...")
                else:
                    print("No hay historial de conversación.")
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

## Aplicación 2: Asistente de Análisis de Datos

### Descripción

Un asistente que puede:
- Cargar y analizar datasets
- Generar estadísticas descriptivas
- Crear visualizaciones
- Responder preguntas sobre los datos

### Servidor MCP para Análisis

Crea el archivo `asistente_analisis/servidor_mcp.py`:

```python
#!/usr/bin/env python3
"""
Servidor MCP para asistente de análisis de datos
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("asistente-analisis-mcp")

# Datasets de ejemplo
DATASETS = {}

@server.tool()
async def cargar_dataset(nombre_archivo: str) -> Dict[str, Any]:
    """Cargar un dataset desde un archivo CSV o JSON"""
    try:
        if nombre_archivo.endswith('.csv'):
            df = pd.read_csv(f"datos_ejemplo/{nombre_archivo}")
        elif nombre_archivo.endswith('.json'):
            df = pd.read_json(f"datos_ejemplo/{nombre_archivo}")
        else:
            return {"error": "Formato de archivo no soportado"}
        
        # Guardar dataset en memoria
        DATASETS[nombre_archivo] = df
        
        return {
            "mensaje": f"Dataset {nombre_archivo} cargado exitosamente",
            "filas": len(df),
            "columnas": list(df.columns),
            "tipos_datos": df.dtypes.to_dict(),
            "primeras_filas": df.head(5).to_dict('records')
        }
        
    except Exception as e:
        return {"error": f"Error al cargar dataset: {str(e)}"}

@server.tool()
async def estadisticas_descriptivas(nombre_dataset: str) -> Dict[str, Any]:
    """Generar estadísticas descriptivas del dataset"""
    if nombre_dataset not in DATASETS:
        return {"error": "Dataset no encontrado. Carga el dataset primero."}
    
    df = DATASETS[nombre_dataset]
    
    # Estadísticas numéricas
    stats_numericas = df.describe().to_dict()
    
    # Información general
    info = {
        "filas": len(df),
        "columnas": len(df.columns),
        "valores_nulos": df.isnull().sum().to_dict(),
        "tipos_datos": df.dtypes.to_dict()
    }
    
    return {
        "dataset": nombre_dataset,
        "informacion_general": info,
        "estadisticas_numericas": stats_numericas
    }

@server.tool()
async def buscar_valores(nombre_dataset: str, columna: str, valor: str) -> Dict[str, Any]:
    """Buscar valores específicos en una columna"""
    if nombre_dataset not in DATASETS:
        return {"error": "Dataset no encontrado"}
    
    df = DATASETS[nombre_dataset]
    
    if columna not in df.columns:
        return {"error": f"Columna {columna} no encontrada"}
    
    # Buscar valores que contengan el término
    resultados = df[df[columna].astype(str).str.contains(valor, case=False, na=False)]
    
    return {
        "dataset": nombre_dataset,
        "columna": columna,
        "termino_busqueda": valor,
        "resultados_encontrados": len(resultados),
        "datos": resultados.head(10).to_dict('records')
    }

@server.tool()
async def filtrar_datos(nombre_dataset: str, columna: str, operador: str, valor: Any) -> Dict[str, Any]:
    """Filtrar datos según criterios específicos"""
    if nombre_dataset not in DATASETS:
        return {"error": "Dataset no encontrado"}
    
    df = DATASETS[nombre_dataset]
    
    if columna not in df.columns:
        return {"error": f"Columna {columna} no encontrada"}
    
    try:
        if operador == "==":
            datos_filtrados = df[df[columna] == valor]
        elif operador == ">":
            datos_filtrados = df[df[columna] > valor]
        elif operador == "<":
            datos_filtrados = df[df[columna] < valor]
        elif operador == ">=":
            datos_filtrados = df[df[columna] >= valor]
        elif operador == "<=":
            datos_filtrados = df[df[columna] <= valor]
        else:
            return {"error": "Operador no soportado"}
        
        return {
            "dataset": nombre_dataset,
            "filtro": f"{columna} {operador} {valor}",
            "registros_originales": len(df),
            "registros_filtrados": len(datos_filtrados),
            "datos": datos_filtrados.head(10).to_dict('records')
        }
        
    except Exception as e:
        return {"error": f"Error al filtrar datos: {str(e)}"}

@server.tool()
async def agrupar_datos(nombre_dataset: str, columna_agrupar: str, columna_agregar: str, funcion: str = "mean") -> Dict[str, Any]:
    """Agrupar datos y aplicar función de agregación"""
    if nombre_dataset not in DATASETS:
        return {"error": "Dataset no encontrado"}
    
    df = DATASETS[nombre_dataset]
    
    if columna_agrupar not in df.columns or columna_agregar not in df.columns:
        return {"error": "Columna no encontrada"}
    
    try:
        if funcion == "mean":
            resultado = df.groupby(columna_agrupar)[columna_agregar].mean()
        elif funcion == "sum":
            resultado = df.groupby(columna_agrupar)[columna_agregar].sum()
        elif funcion == "count":
            resultado = df.groupby(columna_agrupar)[columna_agregar].count()
        elif funcion == "max":
            resultado = df.groupby(columna_agrupar)[columna_agregar].max()
        elif funcion == "min":
            resultado = df.groupby(columna_agrupar)[columna_agregar].min()
        else:
            return {"error": "Función de agregación no soportada"}
        
        return {
            "dataset": nombre_dataset,
            "agrupacion": columna_agrupar,
            "columna_agregada": columna_agregar,
            "funcion": funcion,
            "resultado": resultado.to_dict()
        }
        
    except Exception as e:
        return {"error": f"Error al agrupar datos: {str(e)}"}

@server.tool()
async def listar_datasets() -> Dict[str, Any]:
    """Listar datasets cargados en memoria"""
    return {
        "datasets_cargados": list(DATASETS.keys()),
        "total_datasets": len(DATASETS),
        "detalles": {
            nombre: {
                "filas": len(df),
                "columnas": list(df.columns)
            } for nombre, df in DATASETS.items()
        }
    }

if __name__ == "__main__":
    print("📊 Iniciando servidor MCP para análisis de datos...")
    stdio_server.run(server)
```

## Cómo Ejecutar las Aplicaciones

### 1. Chatbot Empresarial

```bash
cd chatbot_empresarial
python chatbot.py
```

### 2. Asistente de Análisis

```bash
cd asistente_analisis
python asistente.py
```

## Ejemplos de Uso

### Chatbot Empresarial

```
👤 Cliente: Busca laptops
🤖 Bot: Encontré 1 producto relacionado con "laptops":
- Laptop Pro (ID: 1) - Precio: €1,299.99 - Stock: 15 unidades

👤 Cliente: ¿Cuál es el historial del cliente 1?
🤖 Bot: El cliente Juan Pérez (ID: 1) tiene el siguiente historial:
- 2 compras realizadas
- Total gastado: €1,389.98
- Última compra: Teclado Mecánico por €89.99
```

### Asistente de Análisis

```
👤 Usuario: Carga el dataset ventas.csv
🤖 Bot: Dataset ventas.csv cargado exitosamente
- 100 filas, 5 columnas
- Columnas: fecha, producto, cantidad, precio, total

👤 Usuario: Genera estadísticas descriptivas
🤖 Bot: Estadísticas del dataset ventas.csv:
- Total de ventas: 100
- Ingresos totales: €45,230.50
- Producto más vendido: Laptop Pro (25 unidades)
```

## Próximos Pasos

En el siguiente módulo aprenderás las mejores prácticas para desarrollar aplicaciones con LangChain y MCP.

---

**Siguiente**: [Mejores Prácticas](../06-mejores-practicas/) 