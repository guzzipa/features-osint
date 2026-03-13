# OSINT Feature Store Enrichment

## Descripción del Proyecto

Sistema de enriquecimiento de feature store basado en OSINT (Open Source Intelligence) usando emails de usuarios como punto de partida. El objetivo es obtener información pública adicional para mejorar modelos de ML, scoring, y personalización.

## Estructura del Proyecto

```
features-osint/
├── CLAUDE.md              # Este archivo - contexto del proyecto
├── osint_email_enrichment.py  # Script principal de enriquecimiento
├── requirements.txt       # Dependencias Python
├── .env.example          # Template de variables de entorno
└── examples/             # Ejemplos de uso y resultados
```

## Fuentes de Datos OSINT

### Implementadas
1. **Validación de Email** - Formato, tipo de proveedor, dominio
2. **Gravatar** - Avatar y perfil público
3. **GitHub** - Perfil, repos, actividad
4. **Have I Been Pwned** - Brechas de seguridad
5. **Domain Analysis** - Tipo de dominio, disposable detection

### Por Implementar
- Hunter.io - Información corporativa y verificación
- EmailRep.io - Reputación del email
- Clearbit - Enriquecimiento empresarial
- FullContact - Perfil social agregado
- Lookup de redes sociales (LinkedIn, Twitter vía scraping)

## Features Generados

El sistema genera un vector de features que incluye:

- **Validación**: `email_valid`, `is_free_email`, `is_corporate_email`, `is_disposable_email`
- **Presencia Online**: `has_gravatar`, `has_github`, `github_public_repos`, `github_followers`
- **Seguridad**: `breach_count`, `has_breaches`
- **Scores Derivados**: `online_presence_score`, `trust_score`

## Consideraciones de Producción

### Rate Limits
- GitHub API: 60 req/hora (sin auth), 5000/hora (con token)
- HIBP: Requiere API key para producción
- Gravatar: Sin límites conocidos

### Caching
- TTL recomendado: 30-90 días para datos estáticos (Gravatar, GitHub profile)
- TTL recomendado: 7 días para breach checks

### Privacidad y Compliance
- Solo usar datos públicamente disponibles
- Respetar GDPR/CCPA - informar a usuarios sobre enriquecimiento
- No almacenar datos sensibles
- Permitir opt-out

### Arquitectura para Escala
- Ejecutar en batch asíncrono (Celery, Airflow, etc)
- No ejecutar en tiempo real de registro
- Usar queue system para procesamiento
- Implementar retry logic con exponential backoff

## Instrucciones para Claude

### Estilo de Código
- Python 3.8+
- Type hints donde sea relevante
- Docstrings para funciones públicas
- Manejo de errores graceful (no fallar por una API caída)
- Logging estructurado

### Testing
- Crear unit tests para cada fuente de datos
- Mock APIs externas en tests
- Test cases para emails válidos/inválidos
- Test error handling

### Seguridad
- Nunca hardcodear API keys
- Usar .env para configuración sensible
- Rate limiting local para evitar bans
- Timeout en todas las requests HTTP

### Próximos Pasos Sugeridos
1. Agregar más fuentes de datos (Hunter.io, EmailRep)
2. Implementar sistema de caching (Redis)
3. Crear API REST para servir features
4. Integración con feature stores populares (Feast, Tecton)
5. Dashboard de métricas y coverage

## Variables de Entorno

```bash
# APIs (opcionales, mejoran resultados)
GITHUB_TOKEN=          # Token de GitHub para mayor rate limit
HIBP_API_KEY=          # API key de Have I Been Pwned
HUNTER_API_KEY=        # API key de Hunter.io
CLEARBIT_API_KEY=      # API key de Clearbit

# Configuración
CACHE_TTL_DAYS=30      # TTL para cache de resultados
MAX_RETRIES=3          # Reintentos en caso de fallo
REQUEST_TIMEOUT=10     # Timeout de requests en segundos
```

## Uso

```bash
# Análisis individual
python osint_email_enrichment.py usuario@ejemplo.com

# Batch processing (por implementar)
python batch_enrichment.py --input usuarios.csv --output features.json
```

## Notas Adicionales

- El proyecto está en fase de POC/evaluación
- Los resultados se guardan en JSON para análisis
- Considerar costos de APIs pagas antes de escalar
- Algunas APIs públicas pueden cambiar sin previo aviso
