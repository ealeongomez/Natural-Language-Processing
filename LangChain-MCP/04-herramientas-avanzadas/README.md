# 4. Herramientas Avanzadas

## Creación de Herramientas Personalizadas

En este módulo aprenderás a crear herramientas MCP más complejas y avanzadas, incluyendo integración con APIs externas, manejo de archivos y procesamiento de datos.

## Estructura del Proyecto

```
04-herramientas-avanzadas/
├── README.md
├── herramientas_api/
│   ├── __init__.py
│   ├── weather_api.py
│   ├── news_api.py
│   └── currency_api.py
├── herramientas_archivos/
│   ├── __init__.py
│   ├── file_processor.py
│   └── data_analyzer.py
├── herramientas_bd/
│   ├── __init__.py
│   ├── database_tools.py
│   └── sql_queries.py
└── servidor_avanzado.py
```

## Ejemplo 1: Integración con APIs Externas

### Herramienta de Clima

Crea el archivo `herramientas_api/weather_api.py`:

```python
#!/usr/bin/env python3
"""
Herramientas para integración con APIs de clima
"""

import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class WeatherAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Inicializar API de clima"""
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    async def obtener_clima_actual(self, ciudad: str, pais: str = "") -> Dict[str, Any]:
        """Obtener clima actual de una ciudad"""
        try:
            # Si no hay API key, usar datos simulados
            if not self.api_key:
                return self._simular_clima(ciudad)
            
            params = {
                'q': f"{ciudad},{pais}" if pais else ciudad,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            response = requests.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._procesar_datos_clima(data)
            
        except requests.RequestException as e:
            return {
                "error": f"Error al obtener datos del clima: {str(e)}",
                "ciudad": ciudad
            }
    
    async def obtener_pronostico(self, ciudad: str, dias: int = 5) -> Dict[str, Any]:
        """Obtener pronóstico del tiempo"""
        try:
            if not self.api_key:
                return self._simular_pronostico(ciudad, dias)
            
            params = {
                'q': ciudad,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'es',
                'cnt': dias
            }
            
            response = requests.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._procesar_pronostico(data)
            
        except requests.RequestException as e:
            return {
                "error": f"Error al obtener pronóstico: {str(e)}",
                "ciudad": ciudad
            }
    
    def _procesar_datos_clima(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar datos de la API de clima"""
        return {
            "ciudad": data.get("name", "Desconocida"),
            "pais": data.get("sys", {}).get("country", ""),
            "temperatura": {
                "actual": round(data.get("main", {}).get("temp", 0), 1),
                "minima": round(data.get("main", {}).get("temp_min", 0), 1),
                "maxima": round(data.get("main", {}).get("temp_max", 0), 1)
            },
            "humedad": data.get("main", {}).get("humidity", 0),
            "presion": data.get("main", {}).get("pressure", 0),
            "descripcion": data.get("weather", [{}])[0].get("description", ""),
            "icono": data.get("weather", [{}])[0].get("icon", ""),
            "viento": {
                "velocidad": data.get("wind", {}).get("speed", 0),
                "direccion": data.get("wind", {}).get("deg", 0)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def _simular_clima(self, ciudad: str) -> Dict[str, Any]:
        """Simular datos de clima para desarrollo"""
        import random
        
        temperaturas = {
            "madrid": {"actual": 22, "min": 15, "max": 28},
            "barcelona": {"actual": 25, "min": 18, "max": 30},
            "valencia": {"actual": 28, "min": 20, "max": 32},
            "sevilla": {"actual": 30, "min": 22, "max": 35}
        }
        
        ciudad_lower = ciudad.lower()
        if ciudad_lower in temperaturas:
            temp = temperaturas[ciudad_lower]
        else:
            temp = {"actual": random.randint(15, 30), "min": random.randint(10, 25), "max": random.randint(25, 35)}
        
        return {
            "ciudad": ciudad,
            "pais": "ES",
            "temperatura": {
                "actual": temp["actual"],
                "minima": temp["min"],
                "maxima": temp["max"]
            },
            "humedad": random.randint(40, 80),
            "presion": random.randint(1000, 1020),
            "descripcion": "Soleado",
            "icono": "01d",
            "viento": {
                "velocidad": random.uniform(0, 20),
                "direccion": random.randint(0, 360)
            },
            "timestamp": datetime.now().isoformat(),
            "simulado": True
        }
    
    def _simular_pronostico(self, ciudad: str, dias: int) -> Dict[str, Any]:
        """Simular pronóstico del tiempo"""
        import random
        
        pronostico = []
        for i in range(dias):
            fecha = datetime.now() + timedelta(days=i)
            pronostico.append({
                "fecha": fecha.strftime("%Y-%m-%d"),
                "temperatura": {
                    "minima": random.randint(10, 20),
                    "maxima": random.randint(20, 30)
                },
                "descripcion": random.choice(["Soleado", "Nublado", "Lluvia", "Parcialmente nublado"]),
                "humedad": random.randint(40, 80)
            })
        
        return {
            "ciudad": ciudad,
            "pronostico": pronostico,
            "simulado": True
        }
```

### Herramienta de Noticias

Crea el archivo `herramientas_api/news_api.py`:

```python
#!/usr/bin/env python3
"""
Herramientas para integración con APIs de noticias
"""

import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class NewsAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Inicializar API de noticias"""
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    async def buscar_noticias(self, 
                            termino: str, 
                            idioma: str = "es",
                            max_resultados: int = 10,
                            desde: Optional[str] = None) -> Dict[str, Any]:
        """Buscar noticias por término"""
        try:
            if not self.api_key:
                return self._simular_noticias(termino, max_resultados)
            
            params = {
                'q': termino,
                'language': idioma,
                'pageSize': max_resultados,
                'sortBy': 'publishedAt'
            }
            
            if desde:
                params['from'] = desde
            
            response = requests.get(f"{self.base_url}/everything", 
                                  params=params,
                                  headers={'X-API-Key': self.api_key})
            response.raise_for_status()
            
            data = response.json()
            return self._procesar_noticias(data)
            
        except requests.RequestException as e:
            return {
                "error": f"Error al buscar noticias: {str(e)}",
                "termino": termino
            }
    
    async def noticias_tendencia(self, 
                                categoria: str = "general",
                                pais: str = "es",
                                max_resultados: int = 10) -> Dict[str, Any]:
        """Obtener noticias de tendencia"""
        try:
            if not self.api_key:
                return self._simular_tendencias(categoria, max_resultados)
            
            params = {
                'category': categoria,
                'country': pais,
                'pageSize': max_resultados
            }
            
            response = requests.get(f"{self.base_url}/top-headlines", 
                                  params=params,
                                  headers={'X-API-Key': self.api_key})
            response.raise_for_status()
            
            data = response.json()
            return self._procesar_noticias(data)
            
        except requests.RequestException as e:
            return {
                "error": f"Error al obtener tendencias: {str(e)}",
                "categoria": categoria
            }
    
    def _procesar_noticias(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar datos de noticias"""
        articulos = []
        
        for articulo in data.get("articles", []):
            articulos.append({
                "titulo": articulo.get("title", ""),
                "descripcion": articulo.get("description", ""),
                "url": articulo.get("url", ""),
                "imagen": articulo.get("urlToImage", ""),
                "fuente": articulo.get("source", {}).get("name", ""),
                "fecha": articulo.get("publishedAt", ""),
                "autor": articulo.get("author", "")
            })
        
        return {
            "total_resultados": data.get("totalResults", len(articulos)),
            "articulos": articulos,
            "timestamp": datetime.now().isoformat()
        }
    
    def _simular_noticias(self, termino: str, max_resultados: int) -> Dict[str, Any]:
        """Simular noticias para desarrollo"""
        import random
        
        fuentes = ["TechNews", "ScienceDaily", "InnovationHub", "FutureTech", "DigitalTrends"]
        autores = ["Ana García", "Carlos López", "María Rodríguez", "Juan Pérez", "Laura Martín"]
        
        articulos = []
        for i in range(min(max_resultados, 5)):
            articulos.append({
                "titulo": f"Avances en {termino} revolucionan la industria tecnológica",
                "descripcion": f"Los últimos desarrollos en {termino} están cambiando el panorama tecnológico mundial.",
                "url": f"https://ejemplo.com/noticia-{i+1}",
                "imagen": f"https://ejemplo.com/imagen-{i+1}.jpg",
                "fuente": random.choice(fuentes),
                "fecha": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                "autor": random.choice(autores)
            })
        
        return {
            "total_resultados": len(articulos),
            "articulos": articulos,
            "termino_busqueda": termino,
            "simulado": True
        }
    
    def _simular_tendencias(self, categoria: str, max_resultados: int) -> Dict[str, Any]:
        """Simular noticias de tendencia"""
        categorias = {
            "general": ["Política", "Economía", "Sociedad"],
            "technology": ["Inteligencia Artificial", "Blockchain", "IoT"],
            "science": ["Investigación", "Descubrimientos", "Innovación"],
            "business": ["Mercados", "Empresas", "Finanzas"]
        }
        
        temas = categorias.get(categoria, ["Noticias generales"])
        
        articulos = []
        for i, tema in enumerate(temas[:max_resultados]):
            articulos.append({
                "titulo": f"Últimas noticias sobre {tema}",
                "descripcion": f"Descubre las novedades más importantes en {tema}.",
                "url": f"https://ejemplo.com/tendencia-{i+1}",
                "imagen": f"https://ejemplo.com/tendencia-{i+1}.jpg",
                "fuente": "TrendingNews",
                "fecha": datetime.now().isoformat(),
                "autor": "Redacción"
            })
        
        return {
            "total_resultados": len(articulos),
            "articulos": articulos,
            "categoria": categoria,
            "simulado": True
        }
```

## Ejemplo 2: Manejo de Archivos y Datos

### Procesador de Archivos

Crea el archivo `herramientas_archivos/file_processor.py`:

```python
#!/usr/bin/env python3
"""
Herramientas para procesamiento de archivos
"""

import os
import json
import csv
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path

class FileProcessor:
    def __init__(self, base_path: str = "./datos"):
        """Inicializar procesador de archivos"""
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    async def leer_archivo_json(self, nombre_archivo: str) -> Dict[str, Any]:
        """Leer archivo JSON"""
        try:
            ruta_archivo = self.base_path / nombre_archivo
            if not ruta_archivo.exists():
                return {"error": f"Archivo {nombre_archivo} no encontrado"}
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            return {
                "archivo": nombre_archivo,
                "datos": datos,
                "tamaño": len(datos) if isinstance(datos, list) else 1
            }
            
        except Exception as e:
            return {"error": f"Error al leer archivo: {str(e)}"}
    
    async def escribir_archivo_json(self, 
                                  nombre_archivo: str, 
                                  datos: Dict[str, Any]) -> Dict[str, Any]:
        """Escribir archivo JSON"""
        try:
            ruta_archivo = self.base_path / nombre_archivo
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            return {
                "mensaje": f"Archivo {nombre_archivo} guardado exitosamente",
                "ruta": str(ruta_archivo),
                "tamaño": len(str(datos))
            }
            
        except Exception as e:
            return {"error": f"Error al escribir archivo: {str(e)}"}
    
    async def leer_archivo_csv(self, nombre_archivo: str) -> Dict[str, Any]:
        """Leer archivo CSV"""
        try:
            ruta_archivo = self.base_path / nombre_archivo
            if not ruta_archivo.exists():
                return {"error": f"Archivo {nombre_archivo} no encontrado"}
            
            df = pd.read_csv(ruta_archivo)
            
            return {
                "archivo": nombre_archivo,
                "filas": len(df),
                "columnas": list(df.columns),
                "datos": df.head(10).to_dict('records'),
                "resumen": {
                    "tipos": df.dtypes.to_dict(),
                    "valores_nulos": df.isnull().sum().to_dict()
                }
            }
            
        except Exception as e:
            return {"error": f"Error al leer CSV: {str(e)}"}
    
    async def analizar_archivo(self, nombre_archivo: str) -> Dict[str, Any]:
        """Analizar archivo y obtener estadísticas"""
        try:
            ruta_archivo = self.base_path / nombre_archivo
            if not ruta_archivo.exists():
                return {"error": f"Archivo {nombre_archivo} no encontrado"}
            
            # Obtener información básica del archivo
            stat = ruta_archivo.stat()
            
            # Determinar tipo de archivo
            extension = ruta_archivo.suffix.lower()
            
            if extension == '.json':
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                tipo = "JSON"
                elementos = len(datos) if isinstance(datos, list) else 1
                
            elif extension == '.csv':
                df = pd.read_csv(ruta_archivo)
                tipo = "CSV"
                elementos = len(df)
                
            else:
                tipo = "Desconocido"
                elementos = 0
            
            return {
                "archivo": nombre_archivo,
                "tipo": tipo,
                "tamaño_bytes": stat.st_size,
                "tamaño_mb": round(stat.st_size / (1024 * 1024), 2),
                "elementos": elementos,
                "ultima_modificacion": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "ruta_completa": str(ruta_archivo.absolute())
            }
            
        except Exception as e:
            return {"error": f"Error al analizar archivo: {str(e)}"}
    
    async def listar_archivos(self, extension: Optional[str] = None) -> Dict[str, Any]:
        """Listar archivos en el directorio"""
        try:
            archivos = []
            
            for archivo in self.base_path.iterdir():
                if archivo.is_file():
                    if extension is None or archivo.suffix.lower() == extension.lower():
                        stat = archivo.stat()
                        archivos.append({
                            "nombre": archivo.name,
                            "extension": archivo.suffix,
                            "tamaño_bytes": stat.st_size,
                            "ultima_modificacion": datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
            
            return {
                "directorio": str(self.base_path),
                "total_archivos": len(archivos),
                "archivos": archivos
            }
            
        except Exception as e:
            return {"error": f"Error al listar archivos: {str(e)}"}
```

## Servidor MCP Avanzado

Crea el archivo `servidor_avanzado.py`:

```python
#!/usr/bin/env python3
"""
Servidor MCP avanzado con herramientas complejas
"""

import asyncio
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Importar herramientas
from herramientas_api.weather_api import WeatherAPI
from herramientas_api.news_api import NewsAPI
from herramientas_archivos.file_processor import FileProcessor

# Crear servidor MCP
server = Server("herramientas-avanzadas-mcp")

# Inicializar APIs
weather_api = WeatherAPI()
news_api = NewsAPI()
file_processor = FileProcessor()

# Herramientas de clima
@server.tool()
async def obtener_clima_actual(ciudad: str, pais: str = "") -> Dict[str, Any]:
    """Obtener clima actual de una ciudad"""
    return await weather_api.obtener_clima_actual(ciudad, pais)

@server.tool()
async def obtener_pronostico(ciudad: str, dias: int = 5) -> Dict[str, Any]:
    """Obtener pronóstico del tiempo para una ciudad"""
    return await weather_api.obtener_pronostico(ciudad, dias)

# Herramientas de noticias
@server.tool()
async def buscar_noticias(termino: str, max_resultados: int = 10) -> Dict[str, Any]:
    """Buscar noticias por término"""
    return await news_api.buscar_noticias(termino, max_resultados=max_resultados)

@server.tool()
async def noticias_tendencia(categoria: str = "general", max_resultados: int = 10) -> Dict[str, Any]:
    """Obtener noticias de tendencia por categoría"""
    return await news_api.noticias_tendencia(categoria, max_resultados=max_resultados)

# Herramientas de archivos
@server.tool()
async def leer_archivo_json(nombre_archivo: str) -> Dict[str, Any]:
    """Leer archivo JSON"""
    return await file_processor.leer_archivo_json(nombre_archivo)

@server.tool()
async def escribir_archivo_json(nombre_archivo: str, datos: Dict[str, Any]) -> Dict[str, Any]:
    """Escribir archivo JSON"""
    return await file_processor.escribir_archivo_json(nombre_archivo, datos)

@server.tool()
async def leer_archivo_csv(nombre_archivo: str) -> Dict[str, Any]:
    """Leer archivo CSV"""
    return await file_processor.leer_archivo_csv(nombre_archivo)

@server.tool()
async def analizar_archivo(nombre_archivo: str) -> Dict[str, Any]:
    """Analizar archivo y obtener estadísticas"""
    return await file_processor.analizar_archivo(nombre_archivo)

@server.tool()
async def listar_archivos(extension: str = None) -> Dict[str, Any]:
    """Listar archivos en el directorio de datos"""
    return await file_processor.listar_archivos(extension)

if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP avanzado...")
    stdio_server.run(server)
```

## Cómo Usar las Herramientas Avanzadas

### 1. Configurar APIs (Opcional)

Para usar APIs reales, agrega las claves a tu archivo `.env`:

```bash
# APIs opcionales
OPENWEATHER_API_KEY=tu_api_key_aqui
NEWS_API_KEY=tu_api_key_aqui
```

### 2. Ejecutar el Servidor

```bash
python servidor_avanzado.py
```

### 3. Ejemplos de Uso

```python
# Clima
"¿Cuál es el clima actual en Madrid?"
"Obtén el pronóstico del tiempo para Barcelona para los próximos 3 días"

# Noticias
"Busca noticias sobre inteligencia artificial"
"¿Cuáles son las noticias de tendencia en tecnología?"

# Archivos
"Lee el archivo datos.json"
"Analiza el archivo productos.csv"
"Lista todos los archivos JSON en el directorio"
```

## Próximos Pasos

En el siguiente módulo aprenderás a crear aplicaciones prácticas completas usando estas herramientas.

---

**Siguiente**: [Aplicaciones Prácticas](../05-aplicaciones-practicas/) 