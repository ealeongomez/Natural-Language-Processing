# 6. Mejores Prácticas

## Guías para Desarrollo Profesional con LangChain y MCP

En este módulo aprenderás las mejores prácticas para desarrollar aplicaciones robustas, seguras y escalables usando LangChain y MCP. Estas guías te ayudarán a crear código de calidad profesional.

## Estructura del Proyecto

```
06-mejores-practicas/
├── README.md
├── seguridad/
│   ├── autenticacion.py
│   ├── validacion_datos.py
│   └── logging_seguro.py
├── optimizacion/
│   ├── cache_manager.py
│   ├── rate_limiting.py
│   └── performance_monitor.py
├── testing/
│   ├── test_herramientas.py
│   ├── test_integracion.py
│   └── mocks.py
└── deployment/
    ├── dockerfile
    ├── docker-compose.yml
    └── config_produccion.py
```

## 1. Seguridad y Autenticación

### Autenticación de APIs

Crea el archivo `seguridad/autenticacion.py`:

```python
#!/usr/bin/env python3
"""
Sistema de autenticación para herramientas MCP
"""

import os
import hashlib
import hmac
import time
from typing import Dict, Any, Optional
from functools import wraps
from datetime import datetime, timedelta
import jwt

class AutenticadorMCP:
    def __init__(self, secret_key: Optional[str] = None):
        """Inicializar autenticador"""
        self.secret_key = secret_key or os.getenv("MCP_SECRET_KEY", "default-secret-key")
        self.api_keys = self._cargar_api_keys()
        self.sesiones = {}
    
    def _cargar_api_keys(self) -> Dict[str, Dict[str, Any]]:
        """Cargar API keys desde variables de entorno"""
        keys = {}
        
        # Cargar desde variables de entorno
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            keys["openai"] = {
                "key": openai_key,
                "permisos": ["llm", "chat"],
                "rate_limit": 1000  # requests per hour
            }
        
        weather_key = os.getenv("OPENWEATHER_API_KEY")
        if weather_key:
            keys["weather"] = {
                "key": weather_key,
                "permisos": ["weather"],
                "rate_limit": 100
            }
        
        return keys
    
    def generar_token(self, user_id: str, permisos: list, expiracion_horas: int = 24) -> str:
        """Generar token JWT para autenticación"""
        payload = {
            "user_id": user_id,
            "permisos": permisos,
            "exp": datetime.utcnow() + timedelta(hours=expiracion_horas),
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verificar_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def verificar_permiso(self, token: str, permiso_requerido: str) -> bool:
        """Verificar si el token tiene un permiso específico"""
        payload = self.verificar_token(token)
        if not payload:
            return False
        
        return permiso_requerido in payload.get("permisos", [])
    
    def registrar_sesion(self, user_id: str, token: str) -> None:
        """Registrar sesión activa"""
        self.sesiones[user_id] = {
            "token": token,
            "inicio": datetime.utcnow(),
            "ultima_actividad": datetime.utcnow()
        }
    
    def actualizar_actividad(self, user_id: str) -> None:
        """Actualizar última actividad de la sesión"""
        if user_id in self.sesiones:
            self.sesiones[user_id]["ultima_actividad"] = datetime.utcnow()
    
    def limpiar_sesiones_expiradas(self, horas_expiracion: int = 24) -> None:
        """Limpiar sesiones expiradas"""
        ahora = datetime.utcnow()
        sesiones_a_eliminar = []
        
        for user_id, sesion in self.sesiones.items():
            tiempo_inactivo = ahora - sesion["ultima_actividad"]
            if tiempo_inactivo > timedelta(hours=horas_expiracion):
                sesiones_a_eliminar.append(user_id)
        
        for user_id in sesiones_a_eliminar:
            del self.sesiones[user_id]

def requerir_autenticacion(permiso_requerido: str = None):
    """Decorador para requerir autenticación en herramientas MCP"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # En un caso real, obtendrías el token del contexto
            # Por ahora, simulamos la verificación
            token = kwargs.get("token")
            
            if not token:
                return {"error": "Token de autenticación requerido"}
            
            autenticador = AutenticadorMCP()
            
            if permiso_requerido and not autenticador.verificar_permiso(token, permiso_requerido):
                return {"error": f"Permiso '{permiso_requerido}' requerido"}
            
            # Actualizar actividad de la sesión
            payload = autenticador.verificar_token(token)
            if payload:
                autenticador.actualizar_actividad(payload["user_id"])
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Validación de Datos

Crea el archivo `seguridad/validacion_datos.py`:

```python
#!/usr/bin/env python3
"""
Sistema de validación de datos para herramientas MCP
"""

import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, validator, Field
from datetime import datetime

class ValidacionDatos:
    """Clase para validación de datos de entrada"""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Validar formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Validar formato de teléfono"""
        # Patrón para teléfonos españoles
        pattern = r'^(\+34|0034)?[6-9]\d{8}$'
        return bool(re.match(pattern, telefono))
    
    @staticmethod
    def validar_fecha(fecha: str) -> bool:
        """Validar formato de fecha"""
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def sanitizar_texto(texto: str) -> str:
        """Sanitizar texto para prevenir inyección"""
        # Eliminar caracteres peligrosos
        caracteres_peligrosos = ['<', '>', '"', "'", '&', ';', '(', ')']
        for char in caracteres_peligrosos:
            texto = texto.replace(char, '')
        
        # Limitar longitud
        return texto[:1000]
    
    @staticmethod
    def validar_numeros_rango(valor: Union[int, float], min_valor: float, max_valor: float) -> bool:
        """Validar que un número esté en un rango específico"""
        return min_valor <= valor <= max_valor

# Modelos Pydantic para validación
class ProductoInput(BaseModel):
    """Modelo para validación de datos de producto"""
    nombre: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str = Field(..., min_length=1, max_length=50)
    
    @validator('nombre')
    def validar_nombre(cls, v):
        return ValidacionDatos.sanitizar_texto(v)
    
    @validator('precio')
    def validar_precio(cls, v):
        if not ValidacionDatos.validar_numeros_rango(v, 0.01, 10000):
            raise ValueError('Precio debe estar entre 0.01 y 10000')
        return round(v, 2)
    
    @validator('stock')
    def validar_stock(cls, v):
        if not ValidacionDatos.validar_numeros_rango(v, 0, 10000):
            raise ValueError('Stock debe estar entre 0 y 10000')
        return v

class ClienteInput(BaseModel):
    """Modelo para validación de datos de cliente"""
    nombre: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=100)
    telefono: str = Field(..., max_length=20)
    
    @validator('nombre')
    def validar_nombre(cls, v):
        return ValidacionDatos.sanitizar_texto(v)
    
    @validator('email')
    def validar_email(cls, v):
        if not ValidacionDatos.validar_email(v):
            raise ValueError('Formato de email inválido')
        return v.lower()
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if not ValidacionDatos.validar_telefono(v):
            raise ValueError('Formato de teléfono inválido')
        return v

class ConsultaInput(BaseModel):
    """Modelo para validación de consultas"""
    termino: str = Field(..., min_length=1, max_length=200)
    max_resultados: int = Field(default=10, ge=1, le=100)
    idioma: str = Field(default="es", regex="^[a-z]{2}$")
    
    @validator('termino')
    def validar_termino(cls, v):
        return ValidacionDatos.sanitizar_texto(v)

def validar_entrada(modelo: BaseModel, datos: Dict[str, Any]) -> Dict[str, Any]:
    """Validar datos de entrada usando un modelo Pydantic"""
    try:
        datos_validados = modelo(**datos)
        return {"valido": True, "datos": datos_validados.dict()}
    except Exception as e:
        return {"valido": False, "error": str(e)}
```

## 2. Optimización de Rendimiento

### Gestor de Cache

Crea el archivo `optimizacion/cache_manager.py`:

```python
#!/usr/bin/env python3
"""
Sistema de cache para optimizar rendimiento
"""

import json
import hashlib
import time
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import redis
import pickle

class CacheManager:
    def __init__(self, redis_url: Optional[str] = None):
        """Inicializar gestor de cache"""
        self.redis_url = redis_url or "redis://localhost:6379"
        self.redis_client = None
        self.cache_local = {}
        self.tiempo_expiracion_default = 3600  # 1 hora
        
        try:
            self.redis_client = redis.from_url(self.redis_url)
            self.redis_client.ping()  # Verificar conexión
        except Exception as e:
            print(f"⚠️ Redis no disponible, usando cache local: {e}")
            self.redis_client = None
    
    def generar_clave(self, *args, **kwargs) -> str:
        """Generar clave única para cache"""
        # Crear string con todos los argumentos
        contenido = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(contenido.encode()).hexdigest()
    
    def obtener(self, clave: str) -> Optional[Any]:
        """Obtener valor del cache"""
        try:
            if self.redis_client:
                # Intentar obtener de Redis
                valor = self.redis_client.get(clave)
                if valor:
                    return pickle.loads(valor)
            else:
                # Usar cache local
                if clave in self.cache_local:
                    entrada = self.cache_local[clave]
                    if datetime.now() < entrada["expiracion"]:
                        return entrada["valor"]
                    else:
                        del self.cache_local[clave]
            
            return None
            
        except Exception as e:
            print(f"Error al obtener del cache: {e}")
            return None
    
    def guardar(self, clave: str, valor: Any, tiempo_expiracion: int = None) -> bool:
        """Guardar valor en cache"""
        try:
            tiempo_expiracion = tiempo_expiracion or self.tiempo_expiracion_default
            
            if self.redis_client:
                # Guardar en Redis
                valor_serializado = pickle.dumps(valor)
                return self.redis_client.setex(clave, tiempo_expiracion, valor_serializado)
            else:
                # Guardar en cache local
                self.cache_local[clave] = {
                    "valor": valor,
                    "expiracion": datetime.now() + timedelta(seconds=tiempo_expiracion)
                }
                return True
                
        except Exception as e:
            print(f"Error al guardar en cache: {e}")
            return False
    
    def eliminar(self, clave: str) -> bool:
        """Eliminar valor del cache"""
        try:
            if self.redis_client:
                return bool(self.redis_client.delete(clave))
            else:
                if clave in self.cache_local:
                    del self.cache_local[clave]
                    return True
                return False
                
        except Exception as e:
            print(f"Error al eliminar del cache: {e}")
            return False
    
    def limpiar_cache_local(self) -> None:
        """Limpiar cache local expirado"""
        ahora = datetime.now()
        claves_a_eliminar = []
        
        for clave, entrada in self.cache_local.items():
            if ahora > entrada["expiracion"]:
                claves_a_eliminar.append(clave)
        
        for clave in claves_a_eliminar:
            del self.cache_local[clave]
    
    def estadisticas(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        if self.redis_client:
            info = self.redis_client.info()
            return {
                "tipo": "Redis",
                "conectado": True,
                "memoria_usada": info.get("used_memory_human", "N/A"),
                "claves_totales": info.get("db0", {}).get("keys", 0)
            }
        else:
            return {
                "tipo": "Local",
                "conectado": False,
                "claves_totales": len(self.cache_local),
                "memoria_estimada": f"{len(str(self.cache_local))} bytes"
            }

def cache_resultado(tiempo_expiracion: int = 3600):
    """Decorador para cachear resultados de funciones"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Crear instancia de cache
            cache = CacheManager()
            
            # Generar clave única
            clave = f"{func.__name__}:{cache.generar_clave(*args, **kwargs)}"
            
            # Intentar obtener del cache
            resultado_cache = cache.obtener(clave)
            if resultado_cache is not None:
                return resultado_cache
            
            # Ejecutar función y guardar resultado
            resultado = func(*args, **kwargs)
            cache.guardar(clave, resultado, tiempo_expiracion)
            
            return resultado
        return wrapper
    return decorator
```

### Rate Limiting

Crea el archivo `optimizacion/rate_limiting.py`:

```python
#!/usr/bin/env python3
"""
Sistema de rate limiting para APIs
"""

import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        """Inicializar rate limiter"""
        self.limites = defaultdict(list)
        self.limites_por_usuario = {}
        self.limites_por_api = {
            "openai": {"requests": 1000, "periodo": 3600},  # 1000 requests/hora
            "weather": {"requests": 100, "periodo": 3600},  # 100 requests/hora
            "news": {"requests": 100, "periodo": 3600},     # 100 requests/hora
        }
    
    def configurar_limite_usuario(self, user_id: str, requests: int, periodo: int) -> None:
        """Configurar límite específico para un usuario"""
        self.limites_por_usuario[user_id] = {
            "requests": requests,
            "periodo": periodo
        }
    
    def verificar_limite(self, identificador: str, tipo: str = "general") -> Dict[str, Any]:
        """Verificar si se puede hacer una nueva petición"""
        ahora = time.time()
        
        # Obtener límites aplicables
        if tipo in self.limites_por_api:
            limite_api = self.limites_por_api[tipo]
            requests_max = limite_api["requests"]
            periodo = limite_api["periodo"]
        elif identificador in self.limites_por_usuario:
            limite_usuario = self.limites_por_usuario[identificador]
            requests_max = limite_usuario["requests"]
            periodo = limite_usuario["periodo"]
        else:
            # Límite por defecto
            requests_max = 100
            periodo = 3600
        
        # Limpiar registros antiguos
        clave = f"{identificador}:{tipo}"
        self.limites[clave] = [
            timestamp for timestamp in self.limites[clave]
            if ahora - timestamp < periodo
        ]
        
        # Verificar si se puede hacer la petición
        requests_actuales = len(self.limites[clave])
        
        if requests_actuales < requests_max:
            # Registrar nueva petición
            self.limites[clave].append(ahora)
            return {
                "permitido": True,
                "requests_restantes": requests_max - requests_actuales - 1,
                "reset_en": periodo - (ahora % periodo)
            }
        else:
            # Calcular tiempo de espera
            tiempo_espera = periodo - (ahora - self.limites[clave][0])
            return {
                "permitido": False,
                "tiempo_espera": max(0, tiempo_espera),
                "mensaje": f"Rate limit excedido. Espera {int(tiempo_espera)} segundos."
            }
    
    def obtener_estadisticas(self, identificador: str, tipo: str = "general") -> Dict[str, Any]:
        """Obtener estadísticas de uso"""
        ahora = time.time()
        clave = f"{identificador}:{tipo}"
        
        # Obtener límites
        if tipo in self.limites_por_api:
            limite_api = self.limites_por_api[tipo]
            requests_max = limite_api["requests"]
            periodo = limite_api["periodo"]
        else:
            requests_max = 100
            periodo = 3600
        
        # Filtrar peticiones recientes
        peticiones_recientes = [
            timestamp for timestamp in self.limites[clave]
            if ahora - timestamp < periodo
        ]
        
        return {
            "identificador": identificador,
            "tipo": tipo,
            "peticiones_actuales": len(peticiones_recientes),
            "limite_maximo": requests_max,
            "periodo_segundos": periodo,
            "porcentaje_uso": (len(peticiones_recientes) / requests_max) * 100
        }
    
    def limpiar_registros_antiguos(self) -> None:
        """Limpiar registros antiguos de todos los límites"""
        ahora = time.time()
        max_periodo = max(
            [limite["periodo"] for limite in self.limites_por_api.values()] +
            [limite["periodo"] for limite in self.limites_por_usuario.values()]
        )
        
        for clave in list(self.limites.keys()):
            self.limites[clave] = [
                timestamp for timestamp in self.limites[clave]
                if ahora - timestamp < max_periodo
            ]
            
            # Eliminar claves vacías
            if not self.limites[clave]:
                del self.limites[clave]

def rate_limit(identificador: str, tipo: str = "general"):
    """Decorador para aplicar rate limiting"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            rate_limiter = RateLimiter()
            
            # Verificar límite
            resultado_limite = rate_limiter.verificar_limite(identificador, tipo)
            
            if not resultado_limite["permitido"]:
                return {
                    "error": "Rate limit excedido",
                    "detalles": resultado_limite
                }
            
            # Ejecutar función
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 3. Testing y Debugging

### Tests de Herramientas

Crea el archivo `testing/test_herramientas.py`:

```python
#!/usr/bin/env python3
"""
Tests para herramientas MCP
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

# Importar herramientas a testear
from seguridad.autenticacion import AutenticadorMCP
from seguridad.validacion_datos import ValidacionDatos, ProductoInput, ClienteInput
from optimizacion.cache_manager import CacheManager
from optimizacion.rate_limiting import RateLimiter

class TestAutenticacion:
    """Tests para sistema de autenticación"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        self.autenticador = AutenticadorMCP("test-secret-key")
    
    def test_generar_token(self):
        """Test generación de token"""
        token = self.autenticador.generar_token("user123", ["read", "write"])
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verificar_token_valido(self):
        """Test verificación de token válido"""
        token = self.autenticador.generar_token("user123", ["read"])
        payload = self.autenticador.verificar_token(token)
        
        assert payload is not None
        assert payload["user_id"] == "user123"
        assert "read" in payload["permisos"]
    
    def test_verificar_token_invalido(self):
        """Test verificación de token inválido"""
        payload = self.autenticador.verificar_token("token-invalido")
        assert payload is None
    
    def test_verificar_permiso(self):
        """Test verificación de permisos"""
        token = self.autenticador.generar_token("user123", ["read", "write"])
        
        assert self.autenticador.verificar_permiso(token, "read") is True
        assert self.autenticador.verificar_permiso(token, "write") is True
        assert self.autenticador.verificar_permiso(token, "delete") is False

class TestValidacionDatos:
    """Tests para validación de datos"""
    
    def test_validar_email(self):
        """Test validación de email"""
        assert ValidacionDatos.validar_email("test@example.com") is True
        assert ValidacionDatos.validar_email("invalid-email") is False
        assert ValidacionDatos.validar_email("test@.com") is False
    
    def test_validar_telefono(self):
        """Test validación de teléfono"""
        assert ValidacionDatos.validar_telefono("+34600123456") is True
        assert ValidacionDatos.validar_telefono("600123456") is True
        assert ValidacionDatos.validar_telefono("123456789") is False
    
    def test_sanitizar_texto(self):
        """Test sanitización de texto"""
        texto_original = "Texto con <script>alert('xss')</script>"
        texto_sanitizado = ValidacionDatos.sanitizar_texto(texto_original)
        
        assert "<script>" not in texto_sanitizado
        assert "alert" not in texto_sanitizado
        assert "Texto con" in texto_sanitizado
    
    def test_producto_input_valido(self):
        """Test modelo ProductoInput válido"""
        datos = {
            "nombre": "Laptop Pro",
            "precio": 999.99,
            "stock": 10,
            "categoria": "Tecnología"
        }
        
        producto = ProductoInput(**datos)
        assert producto.nombre == "Laptop Pro"
        assert producto.precio == 999.99
        assert producto.stock == 10
    
    def test_producto_input_invalido(self):
        """Test modelo ProductoInput inválido"""
        datos = {
            "nombre": "",  # Nombre vacío
            "precio": -10,  # Precio negativo
            "stock": 10,
            "categoria": "Tecnología"
        }
        
        with pytest.raises(Exception):
            ProductoInput(**datos)

class TestCacheManager:
    """Tests para gestor de cache"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        self.cache = CacheManager()
    
    def test_generar_clave(self):
        """Test generación de claves"""
        clave1 = self.cache.generar_clave("test", param1="value1")
        clave2 = self.cache.generar_clave("test", param1="value1")
        clave3 = self.cache.generar_clave("test", param1="value2")
        
        assert clave1 == clave2
        assert clave1 != clave3
        assert len(clave1) == 32  # MD5 hash length
    
    def test_guardar_y_obtener(self):
        """Test guardar y obtener del cache"""
        clave = "test_key"
        valor = {"data": "test_value"}
        
        # Guardar
        resultado_guardar = self.cache.guardar(clave, valor, 60)
        assert resultado_guardar is True
        
        # Obtener
        valor_obtenido = self.cache.obtener(clave)
        assert valor_obtenido == valor
    
    def test_cache_expirado(self):
        """Test expiración del cache"""
        clave = "test_expired"
        valor = "test_value"
        
        # Guardar con expiración muy corta
        self.cache.guardar(clave, valor, 1)
        
        # Esperar a que expire
        import time
        time.sleep(2)
        
        # Intentar obtener
        valor_obtenido = self.cache.obtener(clave)
        assert valor_obtenido is None

class TestRateLimiter:
    """Tests para rate limiter"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        self.rate_limiter = RateLimiter()
    
    def test_verificar_limite_dentro_limite(self):
        """Test verificación dentro del límite"""
        resultado = self.rate_limiter.verificar_limite("user123", "openai")
        
        assert resultado["permitido"] is True
        assert resultado["requests_restantes"] >= 0
    
    def test_verificar_limite_excedido(self):
        """Test verificación con límite excedido"""
        # Configurar límite muy bajo
        self.rate_limiter.configurar_limite_usuario("user123", 1, 3600)
        
        # Primera petición
        resultado1 = self.rate_limiter.verificar_limite("user123")
        assert resultado1["permitido"] is True
        
        # Segunda petición (debería ser rechazada)
        resultado2 = self.rate_limiter.verificar_limite("user123")
        assert resultado2["permitido"] is False
    
    def test_estadisticas(self):
        """Test obtención de estadísticas"""
        # Hacer algunas peticiones
        self.rate_limiter.verificar_limite("user123", "openai")
        self.rate_limiter.verificar_limite("user123", "openai")
        
        stats = self.rate_limiter.obtener_estadisticas("user123", "openai")
        
        assert stats["identificador"] == "user123"
        assert stats["tipo"] == "openai"
        assert stats["peticiones_actuales"] == 2
        assert stats["porcentaje_uso"] > 0

# Tests de integración
class TestIntegracion:
    """Tests de integración"""
    
    @pytest.mark.asyncio
    async def test_herramienta_con_cache_y_rate_limit(self):
        """Test integración de cache y rate limiting"""
        # Este test simula una herramienta MCP real
        cache = CacheManager()
        rate_limiter = RateLimiter()
        
        # Simular herramienta
        def herramienta_simulada(parametro: str) -> Dict[str, Any]:
            # Verificar rate limit
            resultado_limite = rate_limiter.verificar_limite("user123", "general")
            if not resultado_limite["permitido"]:
                return {"error": "Rate limit excedido"}
            
            # Verificar cache
            clave_cache = cache.generar_clave("herramienta_simulada", parametro)
            resultado_cache = cache.obtener(clave_cache)
            if resultado_cache:
                return {"resultado": resultado_cache, "cache": True}
            
            # Simular procesamiento
            resultado = {"datos": f"Procesado: {parametro}", "timestamp": "2024-01-01"}
            
            # Guardar en cache
            cache.guardar(clave_cache, resultado, 300)
            
            return {"resultado": resultado, "cache": False}
        
        # Ejecutar herramienta
        resultado1 = herramienta_simulada("test_param")
        resultado2 = herramienta_simulada("test_param")
        
        assert resultado1["cache"] is False
        assert resultado2["cache"] is True
        assert resultado1["resultado"] == resultado2["resultado"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## 4. Deployment y Configuración

### Dockerfile

Crea el archivo `deployment/dockerfile`:

```dockerfile
# Dockerfile para aplicación LangChain-MCP
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para datos
RUN mkdir -p /app/datos

# Crear usuario no-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "-m", "mcp.server.stdio"]
```

### Docker Compose

Crea el archivo `deployment/docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Servidor MCP
  mcp-server:
    build:
      context: .
      dockerfile: deployment/dockerfile
    container_name: langchain-mcp-server
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MCP_SECRET_KEY=${MCP_SECRET_KEY}
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./datos:/app/datos
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  # Redis para cache
  redis:
    image: redis:7-alpine
    container_name: langchain-mcp-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Cliente LangChain
  langchain-client:
    build:
      context: .
      dockerfile: deployment/dockerfile
    container_name: langchain-mcp-client
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MCP_SERVER_URL=mcp://mcp-server:8000
    volumes:
      - ./config:/app/config
    depends_on:
      - mcp-server
    command: ["python", "cliente_langchain.py"]
    restart: unless-stopped

  # Nginx para proxy reverso (opcional)
  nginx:
    image: nginx:alpine
    container_name: langchain-mcp-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - mcp-server
    restart: unless-stopped

volumes:
  redis_data:
```

### Configuración de Producción

Crea el archivo `deployment/config_produccion.py`:

```python
#!/usr/bin/env python3
"""
Configuración para entorno de producción
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings

class ConfiguracionProduccion(BaseSettings):
    """Configuración para producción"""
    
    # Configuración de la aplicación
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"
    
    # Configuración de APIs
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str = None
    OPENWEATHER_API_KEY: str = None
    NEWS_API_KEY: str = None
    
    # Configuración de seguridad
    MCP_SECRET_KEY: str
    JWT_SECRET_KEY: str
    ALLOWED_HOSTS: list = ["*"]
    
    # Configuración de base de datos
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Configuración de cache
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600
    
    # Configuración de rate limiting
    RATE_LIMIT_DEFAULT: int = 100
    RATE_LIMIT_PERIOD: int = 3600
    
    # Configuración de logging
    LOG_FILE: str = "/app/logs/app.log"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Configuración de monitoreo
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = False

def obtener_configuracion() -> ConfiguracionProduccion:
    """Obtener configuración de producción"""
    return ConfiguracionProduccion()

def configurar_logging(config: ConfiguracionProduccion) -> None:
    """Configurar logging para producción"""
    import logging
    from logging.handlers import RotatingFileHandler
    
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivo
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=config.LOG_MAX_SIZE,
        backupCount=config.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def configurar_seguridad(config: ConfiguracionProduccion) -> Dict[str, Any]:
    """Configurar parámetros de seguridad"""
    return {
        "secret_key": config.MCP_SECRET_KEY,
        "jwt_secret": config.JWT_SECRET_KEY,
        "allowed_hosts": config.ALLOWED_HOSTS,
        "cors_origins": config.ALLOWED_HOSTS,
        "rate_limiting": {
            "default_limit": config.RATE_LIMIT_DEFAULT,
            "period": config.RATE_LIMIT_PERIOD
        }
    }

def configurar_cache(config: ConfiguracionProduccion) -> Dict[str, Any]:
    """Configurar parámetros de cache"""
    return {
        "redis_url": config.REDIS_URL,
        "ttl": config.CACHE_TTL,
        "enable_local_cache": True,
        "max_local_size": 1000
    }

def configurar_monitoreo(config: ConfiguracionProduccion) -> Dict[str, Any]:
    """Configurar parámetros de monitoreo"""
    return {
        "enable_metrics": config.ENABLE_METRICS,
        "metrics_port": config.METRICS_PORT,
        "health_check_interval": 30,
        "performance_monitoring": True
    }

# Configuración por defecto
config = obtener_configuracion()

if __name__ == "__main__":
    # Configurar logging
    configurar_logging(config)
    
    # Mostrar configuración
    print("🔧 Configuración de Producción:")
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Debug: {config.DEBUG}")
    print(f"Log Level: {config.LOG_LEVEL}")
    print(f"Redis URL: {config.REDIS_URL}")
    print(f"Rate Limit: {config.RATE_LIMIT_DEFAULT} requests/{config.RATE_LIMIT_PERIOD}s")
```

## Resumen de Mejores Prácticas

### 🔒 Seguridad
- ✅ Usar autenticación JWT para APIs
- ✅ Validar todos los datos de entrada
- ✅ Sanitizar texto para prevenir inyección
- ✅ Implementar rate limiting
- ✅ Usar HTTPS en producción

### ⚡ Rendimiento
- ✅ Implementar cache (Redis o local)
- ✅ Optimizar consultas a bases de datos
- ✅ Usar conexiones persistentes
- ✅ Monitorear métricas de rendimiento

### 🧪 Testing
- ✅ Escribir tests unitarios
- ✅ Implementar tests de integración
- ✅ Usar mocks para APIs externas
- ✅ Automatizar tests en CI/CD

### 🚀 Deployment
- ✅ Usar contenedores Docker
- ✅ Configurar variables de entorno
- ✅ Implementar health checks
- ✅ Configurar logging estructurado

### 📊 Monitoreo
- ✅ Implementar métricas de aplicación
- ✅ Configurar alertas automáticas
- ✅ Monitorear logs en tiempo real
- ✅ Usar herramientas de APM

## Próximos Pasos

¡Felicidades! Has completado el tutorial completo de LangChain con MCP. Ahora tienes las herramientas y conocimientos para crear aplicaciones robustas y escalables.

**Recursos adicionales:**
- [Documentación oficial de LangChain](https://python.langchain.com/)
- [Especificación MCP](https://modelcontextprotocol.io/)
- [Comunidad de desarrolladores](https://github.com/langchain-ai/langchain)

---

**¡Gracias por completar el tutorial! 🎉** 