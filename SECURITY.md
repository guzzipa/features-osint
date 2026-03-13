# Security Policy

## Privacy & Data Protection

Este proyecto está diseñado para procesar datos OSINT (Open Source Intelligence) de forma ética y responsable.

### 🔒 Datos Personales

**NUNCA incluir en el repositorio:**
- Archivos de resultados con emails reales (`osint_results_*.json`)
- Reportes personales (`REPORTE_*.md`)
- Archivos `.env` con API keys
- CSVs con datos de usuarios reales
- Cualquier información identificable

### ✅ Verificado

El repositorio ha sido limpiado de:
- ❌ Paths hardcodeados con nombres de usuario
- ❌ Datos personales en ejemplos
- ❌ Resultados de análisis reales
- ❌ API keys o tokens

### 🛡️ Recomendaciones de Uso

1. **Ejecuta siempre en local** - No subas resultados al repo
2. **Usa .env para secrets** - Nunca commits tu `.env`
3. **Respeta rate limits** - No abuses de APIs públicas
4. **GDPR/Compliance** - Solo procesa datos con consentimiento
5. **Datos de prueba** - Usa emails ficticios en ejemplos

### 📋 Checklist Antes de Commit

Antes de hacer `git add`, verifica:
- [ ] No hay archivos `osint_results_*.json`
- [ ] No hay datos personales en CSVs
- [ ] `.env` no está en staging
- [ ] Paths son genéricos (sin usernames)
- [ ] Ejemplos usan datos ficticios

### 🚨 Reportar Vulnerabilidades

Si encuentras datos sensibles accidentalmente expuestos:
1. **NO** abras un issue público
2. Contacta directamente al maintainer
3. Describe qué datos encontraste (sin incluirlos)

## Responsible Use

Este proyecto es para:
- ✅ Scoring crediticio legítimo
- ✅ Investigación académica
- ✅ Detección de fraude autorizada
- ✅ Evaluación de riesgo con consentimiento

NO usar para:
- ❌ Stalking o acoso
- ❌ Recopilación no autorizada de datos
- ❌ Violación de privacidad
- ❌ Scraping masivo sin throttling

## License

MIT License - Ver [LICENSE](LICENSE)
