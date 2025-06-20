# Ejercicios Prácticos

## Desafíos para Practicar LangChain con MCP

Esta sección contiene ejercicios prácticos de diferentes niveles de dificultad para que puedas aplicar lo aprendido en el tutorial.

## Estructura de Ejercicios

```
ejercicios/
├── README.md
├── nivel_basico/
│   ├── ejercicio_1_calculadora.md
│   ├── ejercicio_2_conversor.md
│   └── ejercicio_3_validacion.md
├── nivel_intermedio/
│   ├── ejercicio_1_api_weather.md
│   ├── ejercicio_2_file_processor.md
│   └── ejercicio_3_database_tools.md
├── nivel_avanzado/
│   ├── ejercicio_1_chatbot_completo.md
│   ├── ejercicio_2_analytics_platform.md
│   └── ejercicio_3_microservices.md
└── soluciones/
    ├── nivel_basico/
    ├── nivel_intermedio/
    └── nivel_avanzado/
```

## Nivel Básico

### Ejercicio 1: Calculadora Avanzada

**Objetivo**: Crear una calculadora MCP con operaciones matemáticas complejas.

**Requisitos**:
- Implementar operaciones básicas (suma, resta, multiplicación, división)
- Agregar operaciones avanzadas (potencia, raíz cuadrada, factorial)
- Incluir conversiones de unidades básicas
- Manejar errores (división por cero, números negativos en raíz cuadrada)

**Herramientas a implementar**:
```python
@server.tool()
async def calcular_factorial(n: int) -> int:
    """Calcular factorial de un número"""

@server.tool()
async def calcular_raiz_cuadrada(n: float) -> float:
    """Calcular raíz cuadrada de un número"""

@server.tool()
async def convertir_temperatura(valor: float, de_unidad: str, a_unidad: str) -> float:
    """Convertir entre Celsius, Fahrenheit y Kelvin"""
```

**Criterios de evaluación**:
- ✅ Todas las operaciones funcionan correctamente
- ✅ Manejo adecuado de errores
- ✅ Documentación clara de las funciones
- ✅ Tests unitarios implementados

---

### Ejercicio 2: Conversor de Formatos

**Objetivo**: Crear herramientas para convertir entre diferentes formatos de datos.

**Requisitos**:
- Convertir JSON a CSV y viceversa
- Convertir texto a diferentes formatos (Markdown, HTML, texto plano)
- Comprimir y descomprimir datos
- Validar formatos de entrada

**Herramientas a implementar**:
```python
@server.tool()
async def json_a_csv(datos_json: str, nombre_archivo: str) -> str:
    """Convertir JSON a CSV"""

@server.tool()
async def csv_a_json(archivo_csv: str) -> str:
    """Convertir CSV a JSON"""

@server.tool()
async def texto_a_markdown(texto: str) -> str:
    """Convertir texto plano a Markdown"""

@server.tool()
async def comprimir_datos(datos: str) -> bytes:
    """Comprimir datos usando gzip"""
```

**Criterios de evaluación**:
- ✅ Conversiones funcionan correctamente
- ✅ Manejo de archivos grandes
- ✅ Preservación de estructura de datos
- ✅ Validación de formatos de entrada

---

### Ejercicio 3: Sistema de Validación

**Objetivo**: Implementar un sistema completo de validación de datos.

**Requisitos**:
- Validar emails, teléfonos, URLs
- Validar formatos de fecha y hora
- Validar números de tarjeta de crédito (Luhn algorithm)
- Generar reportes de validación

**Herramientas a implementar**:
```python
@server.tool()
async def validar_email(email: str) -> Dict[str, Any]:
    """Validar formato y dominio de email"""

@server.tool()
async def validar_tarjeta_credito(numero: str) -> Dict[str, Any]:
    """Validar número de tarjeta de crédito"""

@server.tool()
async def validar_fecha_hora(fecha: str, formato: str) -> Dict[str, Any]:
    """Validar formato de fecha y hora"""

@server.tool()
async def generar_reporte_validacion(datos: List[Dict]) -> Dict[str, Any]:
    """Generar reporte de validación de múltiples datos"""
```

**Criterios de evaluación**:
- ✅ Validaciones precisas y completas
- ✅ Manejo de casos edge
- ✅ Reportes informativos
- ✅ Performance optimizada

## Nivel Intermedio

### Ejercicio 1: API de Clima Avanzada

**Objetivo**: Crear una API de clima completa con múltiples proveedores.

**Requisitos**:
- Integrar múltiples APIs de clima (OpenWeatherMap, WeatherAPI, etc.)
- Implementar cache inteligente
- Agregar pronósticos extendidos
- Incluir alertas meteorológicas

**Herramientas a implementar**:
```python
@server.tool()
async def obtener_clima_multi_proveedor(ciudad: str) -> Dict[str, Any]:
    """Obtener clima de múltiples proveedores y comparar"""

@server.tool()
async def pronostico_extendido(ciudad: str, dias: int) -> Dict[str, Any]:
    """Obtener pronóstico extendido con análisis de tendencias"""

@server.tool()
async def alertas_meteorologicas(ciudad: str) -> List[Dict[str, Any]]:
    """Obtener alertas meteorológicas activas"""

@server.tool()
async def historial_clima(ciudad: str, fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
    """Obtener historial de clima para análisis"""
```

**Criterios de evaluación**:
- ✅ Integración con múltiples APIs
- ✅ Sistema de cache eficiente
- ✅ Manejo de errores de APIs
- ✅ Análisis de datos meteorológicos

---

### Ejercicio 2: Procesador de Archivos Avanzado

**Objetivo**: Crear un sistema completo de procesamiento de archivos.

**Requisitos**:
- Procesar múltiples formatos (PDF, DOCX, TXT, CSV, JSON)
- Extraer texto y metadatos
- Implementar búsqueda de texto
- Generar resúmenes automáticos

**Herramientas a implementar**:
```python
@server.tool()
async def extraer_texto_pdf(archivo: str) -> Dict[str, Any]:
    """Extraer texto y metadatos de PDF"""

@server.tool()
async def buscar_en_archivos(termino: str, directorio: str) -> List[Dict[str, Any]]:
    """Buscar término en múltiples archivos"""

@server.tool()
async def generar_resumen_texto(texto: str, longitud: int) -> str:
    """Generar resumen automático de texto"""

@server.tool()
async def analizar_sentimiento_archivo(archivo: str) -> Dict[str, Any]:
    """Analizar sentimiento del contenido de un archivo"""
```

**Criterios de evaluación**:
- ✅ Soporte para múltiples formatos
- ✅ Extracción precisa de contenido
- ✅ Búsqueda eficiente
- ✅ Análisis de contenido inteligente

---

### Ejercicio 3: Herramientas de Base de Datos

**Objetivo**: Crear herramientas para interactuar con bases de datos.

**Requisitos**:
- Conectar con diferentes tipos de BD (SQLite, PostgreSQL, MySQL)
- Ejecutar consultas dinámicas
- Generar reportes automáticos
- Implementar backup y restore

**Herramientas a implementar**:
```python
@server.tool()
async def ejecutar_consulta_sql(consulta: str, base_datos: str) -> Dict[str, Any]:
    """Ejecutar consulta SQL dinámica"""

@server.tool()
async def generar_reporte_automatico(tabla: str, metricas: List[str]) -> Dict[str, Any]:
    """Generar reporte automático de métricas"""

@server.tool()
async def backup_base_datos(base_datos: str, destino: str) -> Dict[str, Any]:
    """Crear backup de base de datos"""

@server.tool()
async def analizar_rendimiento_consultas(base_datos: str) -> Dict[str, Any]:
    """Analizar rendimiento de consultas"""
```

**Criterios de evaluación**:
- ✅ Conexión segura a bases de datos
- ✅ Consultas optimizadas
- ✅ Reportes informativos
- ✅ Manejo de errores de BD

## Nivel Avanzado

### Ejercicio 1: Chatbot Empresarial Completo

**Objetivo**: Crear un chatbot empresarial con múltiples funcionalidades.

**Requisitos**:
- Integración con CRM y ERP
- Procesamiento de pedidos automático
- Análisis de sentimiento de clientes
- Generación de reportes ejecutivos

**Funcionalidades a implementar**:
- Gestión de clientes y productos
- Procesamiento de pedidos
- Análisis de ventas y tendencias
- Integración con sistemas externos
- Dashboard ejecutivo

**Criterios de evaluación**:
- ✅ Integración completa con sistemas empresariales
- ✅ Procesamiento automático de pedidos
- ✅ Análisis avanzado de datos
- ✅ Interfaz de usuario intuitiva
- ✅ Escalabilidad y rendimiento

---

### Ejercicio 2: Plataforma de Analytics

**Objetivo**: Crear una plataforma completa de análisis de datos.

**Requisitos**:
- Carga y procesamiento de datos masivos
- Generación de visualizaciones automáticas
- Machine Learning básico
- API REST completa

**Funcionalidades a implementar**:
- ETL de datos
- Análisis estadístico avanzado
- Generación de gráficos y dashboards
- Predicciones usando ML
- API para integración externa

**Criterios de evaluación**:
- ✅ Procesamiento eficiente de datos grandes
- ✅ Visualizaciones informativas
- ✅ Modelos ML funcionales
- ✅ API bien documentada
- ✅ Performance optimizada

---

### Ejercicio 3: Arquitectura de Microservicios

**Objetivo**: Crear una arquitectura de microservicios con MCP.

**Requisitos**:
- Múltiples servicios MCP especializados
- Comunicación entre servicios
- Load balancing y alta disponibilidad
- Monitoreo y logging centralizado

**Servicios a implementar**:
- Servicio de autenticación
- Servicio de procesamiento de datos
- Servicio de notificaciones
- Servicio de analytics
- Gateway API

**Criterios de evaluación**:
- ✅ Arquitectura escalable
- ✅ Comunicación eficiente entre servicios
- ✅ Alta disponibilidad
- ✅ Monitoreo completo
- ✅ Documentación técnica

## Cómo Enviar Soluciones

### Formato de Entrega

1. **Estructura del proyecto**:
```
ejercicio_X_tu_nombre/
├── README.md
├── requirements.txt
├── servidor_mcp.py
├── cliente_langchain.py
├── tests/
│   └── test_ejercicio.py
└── docs/
    └── documentacion.md
```

2. **README.md debe incluir**:
- Descripción del ejercicio
- Instrucciones de instalación
- Ejemplos de uso
- Criterios cumplidos
- Problemas encontrados y soluciones

3. **Tests obligatorios**:
- Tests unitarios para cada herramienta
- Tests de integración
- Tests de rendimiento (para ejercicios avanzados)

### Criterios de Evaluación

**Puntuación por ejercicio**:
- **Funcionalidad (40%)**: ¿Funciona correctamente?
- **Código (25%)**: ¿Está bien estructurado y documentado?
- **Tests (20%)**: ¿Tiene cobertura de tests adecuada?
- **Innovación (15%)**: ¿Añade funcionalidades extra interesantes?

**Niveles de logro**:
- 🥉 **Bronce**: Funcionalidad básica implementada
- 🥈 **Plata**: Funcionalidad completa + tests
- 🥇 **Oro**: Funcionalidad completa + tests + innovación

## Recursos Adicionales

### Documentación Útil
- [LangChain Documentation](https://python.langchain.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Python Testing Guide](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

### Herramientas Recomendadas
- **Testing**: pytest, pytest-asyncio
- **Linting**: flake8, black
- **Documentation**: Sphinx, MkDocs
- **CI/CD**: GitHub Actions, GitLab CI

### Comunidad
- [LangChain Discord](https://discord.gg/langchain)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/langchain)

---

**¡Manos a la obra! ¡Es hora de practicar y crear algo increíble! 🚀** 