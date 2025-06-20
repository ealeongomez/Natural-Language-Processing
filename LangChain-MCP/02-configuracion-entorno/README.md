# 2. Configuración del Entorno

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **git** (para clonar repositorios)

## Instalación de Dependencias

### 1. Crear Entorno Virtual

Es altamente recomendado usar un entorno virtual para evitar conflictos entre dependencias:

```bash
# Navegar a la carpeta principal del proyecto
cd ..

# Crear entorno virtual
python -m venv langchain-mcp-env

# Activar entorno virtual
# En Windows:
langchain-mcp-env\Scripts\activate

# En macOS/Linux:
source langchain-mcp-env/bin/activate
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias desde la carpeta principal
pip install -r requirements.txt
```

### 3. Verificar Instalación

```bash
# Verificar que LangChain está instalado
python -c "import langchain; print('LangChain instalado correctamente')"

# Verificar que MCP está disponible
python -c "import mcp; print('MCP disponible')"
```

## Configuración de Variables de Entorno

### 1. Crear Archivo .env

Crea un archivo `.env` en la carpeta principal del proyecto:

```bash
# Navegar a la carpeta principal
cd ..

# Copiar archivo de ejemplo
cp LangChain-MCP/env.example .env

# Editar el archivo .env
nano .env  # o usar tu editor preferido
```

Contenido del archivo `.env`:

```bash
# API Keys
OPENAI_API_KEY=tu_api_key_aqui
ANTHROPIC_API_KEY=tu_api_key_aqui

# Configuración MCP
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000

# Configuración de desarrollo
DEBUG=True
LOG_LEVEL=INFO
```

### 2. Cargar Variables de Entorno

En tu código Python:

```python
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar variables de entorno desde la carpeta principal
directorio_actual = Path(__file__).parent
directorio_principal = directorio_actual.parent.parent
archivo_env = directorio_principal / ".env"

load_dotenv(archivo_env)

# Usar variables
api_key = os.getenv("OPENAI_API_KEY")
```

## Configuración de LangChain

### 1. Configuración Básica

```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os

# Configurar modelo de OpenAI
llm = OpenAI(
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# O usar ChatOpenAI para modelos de chat
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7
)
```

### 2. Configuración de Logging

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Configuración de MCP Server

### 1. Servidor MCP Básico

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Crear servidor MCP
server = Server("mi-servidor-mcp")

# Configurar herramientas
@server.tool()
async def mi_herramienta(parametro: str) -> str:
    return f"Resultado: {parametro}"

# Ejecutar servidor
if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP...")
    stdio_server.run(server)
```

### 2. Configuración de Herramientas

```python
from mcp.types import Tool

# Definir herramienta
mi_tool = Tool(
    name="calculadora",
    description="Calcula operaciones matemáticas básicas",
    inputSchema={
        "type": "object",
        "properties": {
            "operacion": {"type": "string"},
            "numeros": {"type": "array", "items": {"type": "number"}}
        }
    }
)
```

## Verificación de la Configuración

### Script de Verificación

El script `verificar_configuracion.py` está diseñado para verificar automáticamente:

- ✅ Versión de Python (3.8+)
- ✅ Dependencias instaladas
- ✅ Archivo `.env` en la carpeta principal
- ✅ API key de OpenAI configurada
- ✅ Formato válido de la API key

```bash
# Navegar al tutorial
cd LangChain-MCP

# Ejecutar script de verificación
python 02-configuracion-entorno/verificar_configuracion.py
```

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de que el entorno virtual esté activado
source langchain-mcp-env/bin/activate

# Reinstala las dependencias desde la carpeta principal
pip install -r ../requirements.txt --force-reinstall
```

### Error: "API Key not found"
```bash
# Verifica que el archivo .env existe en la carpeta principal
ls -la ../.env

# Verifica el contenido del archivo
cat ../.env

# Asegúrate de que la variable esté configurada correctamente
OPENAI_API_KEY=sk-tu_api_key_aqui
```

### Error: "requirements.txt not found"
```bash
# Verifica que estás en la carpeta correcta
pwd

# El requirements.txt debe estar en la carpeta principal
ls -la ../requirements.txt
```

### Error: "Permission denied"
```bash
# En macOS/Linux, puede necesitar permisos
chmod +x 02-configuracion-entorno/verificar_configuracion.py
```

## Estructura de Archivos Final

```
Natural-Language-Processing/
├── requirements.txt          # Dependencias del proyecto
├── .env                      # Variables de entorno (crear desde env.example)
├── langchain-mcp-env/        # Entorno virtual (crear)
└── LangChain-MCP/
    ├── README.md
    ├── env.example           # Plantilla para .env
    ├── 02-configuracion-entorno/
    │   ├── README.md
    │   └── verificar_configuracion.py
    └── ... (otros módulos)
```

## Próximos Pasos

Una vez que hayas completado la configuración, puedes ejecutar el script de verificación:

```bash
cd LangChain-MCP
python 02-configuracion-entorno/verificar_configuracion.py
```

Si todo está correcto, puedes continuar con el siguiente módulo sobre integración básica.

---

**Siguiente**: [Integración Básica](../03-integracion-basica/) 