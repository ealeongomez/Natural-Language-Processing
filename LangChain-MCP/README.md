# LangChain con MCP (Model Context Protocol) - Tutorial Completo

Este tutorial te guiará a través de la integración de LangChain con MCP (Model Context Protocol), una tecnología que permite a los modelos de lenguaje acceder a herramientas y datos externos de manera segura y eficiente.

## 📚 Contenido del Tutorial

### 1. [Fundamentos de MCP](./01-fundamentos-mcp/)
- ¿Qué es MCP?
- Arquitectura y componentes
- Casos de uso principales

### 2. [Configuración del Entorno](./02-configuracion-entorno/)
- Instalación de dependencias
- Configuración de LangChain
- Configuración de MCP Server

### 3. [Integración Básica](./03-integracion-basica/)
- Primer ejemplo: Conectar LangChain con MCP
- Configuración de herramientas básicas
- Manejo de respuestas

### 4. [Herramientas Avanzadas](./04-herramientas-avanzadas/)
- Creación de herramientas personalizadas
- Integración con APIs externas
- Manejo de archivos y datos

### 5. [Aplicaciones Prácticas](./05-aplicaciones-practicas/)
- Chatbot con acceso a datos en tiempo real
- Asistente de análisis de datos
- Integración con bases de datos

### 6. [Mejores Prácticas](./06-mejores-practicas/)
- Seguridad y autenticación
- Optimización de rendimiento
- Debugging y troubleshooting

## �� Inicio Rápido

### Opción 1: Configuración Automática (Recomendada)

```bash
# Ejecutar script de configuración automática
python setup.py
```

Este script automáticamente:
- ✅ Verifica la versión de Python
- ✅ Crea un entorno virtual
- ✅ Configura el archivo .env
- ✅ Instala todas las dependencias

### Opción 2: Configuración Manual

#### 1. Configurar Variables de Entorno

**IMPORTANTE**: Antes de comenzar, necesitas configurar tu API key de OpenAI.

```bash
# Navegar a la carpeta principal del proyecto
cd ..

# Copiar archivo de ejemplo
cp LangChain-MCP/env.example .env

# Editar el archivo .env con tu API key
nano .env  # o usar tu editor preferido
```

En el archivo `.env`, reemplaza `tu_openai_api_key_aqui` con tu API key real:

```bash
OPENAI_API_KEY=sk-tu_api_key_real_aqui
```

**¿No tienes una API key?** Obtén una gratis en: https://platform.openai.com/api-keys

#### 2. Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv langchain-mcp-env

# Activar entorno virtual
# En Windows:
langchain-mcp-env\Scripts\activate

# En macOS/Linux:
source langchain-mcp-env/bin/activate

# Instalar dependencias (desde la carpeta principal)
pip install -r requirements.txt
```

#### 3. Verificar Configuración

```bash
# Navegar al tutorial
cd LangChain-MCP

# Verificar que todo está configurado correctamente
python 02-configuracion-entorno/verificar_configuracion.py
```

#### 4. Ejecutar el Primer Ejemplo

```bash
# Ejecutar el primer ejemplo
python 03-integracion-basica/cliente_langchain.py
```

## 📋 Prerrequisitos

- **Python 3.8 o superior**
- **API Key de OpenAI** (gratuita en https://platform.openai.com/api-keys)
- **Conocimientos básicos de LangChain**
- **Familiaridad con APIs REST**
- **Entorno virtual** (recomendado)

## 🛠️ Tecnologías Utilizadas

- **LangChain**: Framework para aplicaciones de IA
- **MCP**: Model Context Protocol
- **Python**: Lenguaje principal
- **FastAPI**: Para servidores MCP (opcional)
- **Pydantic**: Para validación de datos

## 📖 Estructura del Proyecto

```
Natural-Language-Processing/
├── requirements.txt
├── .env (crear desde LangChain-MCP/env.example)
├── langchain-mcp-env/ (crear con setup.py)
├── LangChain-MCP/
│   ├── README.md
│   ├── setup.py (configuración automática)
│   ├── env.example
│   ├── 01-fundamentos-mcp/
│   ├── 02-configuracion-entorno/
│   ├── 03-integracion-basica/
│   ├── 04-herramientas-avanzadas/
│   ├── 05-aplicaciones-practicas/
│   ├── 06-mejores-practicas/
│   └── ejercicios/
└── otros_proyectos/
```

## 🔧 Configuración Detallada

### Variables de Entorno Requeridas

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `OPENAI_API_KEY` | API key de OpenAI | ✅ Sí | `sk-...` |
| `ANTHROPIC_API_KEY` | API key de Anthropic | ❌ No | `sk-ant-...` |
| `OPENWEATHER_API_KEY` | API key de OpenWeather | ❌ No | `1234567890abcdef` |
| `NEWS_API_KEY` | API key de News API | ❌ No | `1234567890abcdef` |

### Configuración Opcional

```bash
# Para ejercicios avanzados
OPENWEATHER_API_KEY=tu_api_key_aqui
NEWS_API_KEY=tu_api_key_aqui

# Para seguridad
MCP_SECRET_KEY=clave_secreta_muy_segura
JWT_SECRET_KEY=otra_clave_secreta

# Para desarrollo
DEBUG=True
LOG_LEVEL=INFO
```

## 🚨 Solución de Problemas

### Error: "OPENAI_API_KEY not found"
```bash
# Verificar que el archivo .env existe en la carpeta principal
ls -la ../.env

# Verificar el contenido
cat ../.env

# Asegúrate de que la variable esté correctamente configurada
OPENAI_API_KEY=sk-tu_api_key_aqui
```

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de que el entorno virtual esté activado
source langchain-mcp-env/bin/activate

# Reinstalar dependencias desde la carpeta principal
pip install -r ../requirements.txt --force-reinstall
```

### Error: "requirements.txt not found"
```bash
# Verificar que estás en la carpeta correcta
pwd

# El requirements.txt debe estar en la carpeta principal
ls -la ../requirements.txt
```

### Error: "API key invalid"
```bash
# Verificar que tu API key sea válida
# Obtén una nueva en: https://platform.openai.com/api-keys
```

### Error: "setup.py not found"
```bash
# Verificar que estás en la carpeta correcta
cd LangChain-MCP

# Ejecutar setup
python setup.py
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor, lee las guías de contribución antes de enviar un pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [Documentación oficial de LangChain](https://python.langchain.com/)
- [Especificación MCP](https://modelcontextprotocol.io/)
- [GitHub de MCP](https://github.com/modelcontextprotocol)
- [OpenAI API Keys](https://platform.openai.com/api-keys)

---

**¡Comienza con el [primer módulo](./01-fundamentos-mcp/) para entender los fundamentos de MCP!** 