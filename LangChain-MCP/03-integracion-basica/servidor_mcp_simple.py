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