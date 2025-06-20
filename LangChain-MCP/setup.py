#!/usr/bin/env python3
"""
Script de configuración rápida para LangChain-MCP
"""

import os
import sys
import subprocess
from pathlib import Path
from shutil import copy2

def print_header():
    """Imprimir encabezado del script"""
    print("🚀 Configuración Rápida de LangChain-MCP")
    print("=" * 50)

def verificar_python():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def crear_entorno_virtual():
    """Crear entorno virtual"""
    directorio_principal = Path(__file__).parent.parent
    env_path = directorio_principal / "langchain-mcp-env"
    
    if env_path.exists():
        print(f"✅ Entorno virtual ya existe en: {env_path}")
        return True
    
    print("🔧 Creando entorno virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(env_path)], check=True)
        print(f"✅ Entorno virtual creado en: {env_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear entorno virtual: {e}")
        return False

def configurar_env():
    """Configurar archivo .env"""
    directorio_actual = Path(__file__).parent
    directorio_principal = directorio_actual.parent
    env_example = directorio_actual / "env.example"
    env_file = directorio_principal / ".env"
    
    if env_file.exists():
        print(f"✅ Archivo .env ya existe en: {env_file}")
        return True
    
    if not env_example.exists():
        print(f"❌ Archivo env.example no encontrado en: {env_example}")
        return False
    
    try:
        copy2(env_example, env_file)
        print(f"✅ Archivo .env creado en: {env_file}")
        print("💡 IMPORTANTE: Edita el archivo .env y agrega tu API key de OpenAI")
        print(f"   nano {env_file}")
        return True
    except Exception as e:
        print(f"❌ Error al crear archivo .env: {e}")
        return False

def instalar_dependencias():
    """Instalar dependencias"""
    directorio_principal = Path(__file__).parent.parent
    requirements_file = directorio_principal / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ requirements.txt no encontrado en: {requirements_file}")
        return False
    
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def mostrar_instrucciones():
    """Mostrar instrucciones finales"""
    print("\n" + "=" * 50)
    print("🎉 Configuración completada!")
    print("\n📝 Próximos pasos:")
    print("1. Edita el archivo .env y agrega tu API key de OpenAI:")
    print("   OPENAI_API_KEY=sk-tu_api_key_aqui")
    print("\n2. Activa el entorno virtual:")
    print("   source ../langchain-mcp-env/bin/activate")
    print("\n3. Verifica la configuración:")
    print("   python 02-configuracion-entorno/verificar_configuracion.py")
    print("\n4. Ejecuta el primer ejemplo:")
    print("   python 03-integracion-basica/cliente_langchain.py")
    print("\n💡 ¿No tienes una API key? Obtén una gratis en:")
    print("   https://platform.openai.com/api-keys")

def main():
    """Función principal"""
    print_header()
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Crear entorno virtual
    if not crear_entorno_virtual():
        sys.exit(1)
    
    # Configurar .env
    if not configurar_env():
        sys.exit(1)
    
    # Instalar dependencias
    if not instalar_dependencias():
        sys.exit(1)
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 