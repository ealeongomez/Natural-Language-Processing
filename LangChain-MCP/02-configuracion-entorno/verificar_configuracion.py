#!/usr/bin/env python3
"""
Script para verificar que todo está configurado correctamente
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def cargar_variables_entorno():
    """Cargar variables de entorno desde la carpeta principal"""
    # Buscar el archivo .env en la carpeta principal
    directorio_actual = Path(__file__).parent
    directorio_principal = directorio_actual.parent.parent  # Subir dos niveles
    
    archivo_env = directorio_principal / ".env"
    
    if archivo_env.exists():
        load_dotenv(archivo_env)
        print(f"✅ Archivo .env encontrado en: {archivo_env}")
        return True
    else:
        print(f"❌ Archivo .env no encontrado en: {archivo_env}")
        print("💡 Crea el archivo .env copiando desde env.example:")
        print(f"   cp {directorio_principal}/env.example {directorio_principal}/.env")
        return False

def verificar_python():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requerido")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def verificar_dependencias():
    """Verificar dependencias instaladas"""
    dependencias = [
        "langchain",
        "mcp",
        "requests",
        "pandas",
        "pydantic",
        "python-dotenv"
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} no encontrado")
            return False
    return True

def verificar_variables_entorno():
    """Verificar variables de entorno"""
    variables_requeridas = ["OPENAI_API_KEY"]
    variables_opcionales = ["ANTHROPIC_API_KEY", "OPENWEATHER_API_KEY", "NEWS_API_KEY"]
    
    print("\n🔑 Verificando variables de entorno:")
    
    # Verificar variables requeridas
    for var in variables_requeridas:
        valor = os.getenv(var)
        if valor:
            # Ocultar parte de la API key por seguridad
            if "API_KEY" in var and len(valor) > 10:
                valor_oculto = valor[:7] + "..." + valor[-4:]
                print(f"✅ {var}: {valor_oculto}")
            else:
                print(f"✅ {var}: configurada")
        else:
            print(f"❌ {var} no configurada")
            return False
    
    # Verificar variables opcionales
    print("\n📋 Variables opcionales:")
    for var in variables_opcionales:
        valor = os.getenv(var)
        if valor:
            print(f"✅ {var}: configurada")
        else:
            print(f"⚠️  {var}: no configurada (opcional)")
    
    return True

def verificar_requirements_txt():
    """Verificar que requirements.txt existe en la carpeta principal"""
    directorio_actual = Path(__file__).parent
    directorio_principal = directorio_actual.parent.parent
    archivo_requirements = directorio_principal / "requirements.txt"
    
    if archivo_requirements.exists():
        print(f"✅ requirements.txt encontrado en: {archivo_requirements}")
        return True
    else:
        print(f"❌ requirements.txt no encontrado en: {archivo_requirements}")
        return False

def verificar_api_key_openai():
    """Verificar que la API key de OpenAI sea válida"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No se puede verificar API key: OPENAI_API_KEY no configurada")
        return False
    
    # Verificar formato básico
    if not api_key.startswith("sk-"):
        print("❌ API key de OpenAI debe comenzar con 'sk-'")
        return False
    
    if len(api_key) < 20:
        print("❌ API key de OpenAI parece ser muy corta")
        return False
    
    print("✅ Formato de API key de OpenAI válido")
    
    # Opcional: Verificar conectividad con OpenAI
    try:
        import openai
        openai.api_key = api_key
        # Intentar una llamada simple (esto puede consumir créditos)
        # response = openai.Model.list()
        # print("✅ Conexión con OpenAI exitosa")
        print("💡 Para verificar conectividad completa, ejecuta un ejemplo")
    except ImportError:
        print("⚠️  openai no instalado, no se puede verificar conectividad")
    except Exception as e:
        print(f"⚠️  Error al verificar conectividad: {e}")
    
    return True

def main():
    print("🔍 Verificando configuración de LangChain-MCP...\n")
    
    # Cargar variables de entorno primero
    if not cargar_variables_entorno():
        print("\n❌ No se pueden verificar las variables de entorno")
        return
    
    checks = [
        verificar_python(),
        verificar_requirements_txt(),
        verificar_dependencias(),
        verificar_variables_entorno(),
        verificar_api_key_openai()
    ]
    
    print("\n" + "="*60)
    
    if all(checks):
        print("\n🎉 ¡Todo configurado correctamente!")
        print("Puedes continuar con el siguiente módulo.")
        print("\n📝 Próximos pasos:")
        print("1. Ejecutar ejemplo básico: python 03-integracion-basica/cliente_langchain.py")
        print("2. Continuar con el tutorial: leer 03-integracion-basica/README.md")
    else:
        print("\n❌ Hay problemas en la configuración.")
        print("Revisa los errores anteriores y corrige los problemas.")
        print("\n💡 Consejos:")
        print("- Asegúrate de tener Python 3.8+ instalado")
        print("- Instala las dependencias: pip install -r ../requirements.txt")
        print("- Configura tu API key de OpenAI en el archivo .env")
        print("- Obtén una API key gratis en: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main() 