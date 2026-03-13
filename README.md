# 🔍 OSINT Feature Store Enrichment

Sistema de enriquecimiento de feature stores usando datos públicos (OSINT) basados en emails.

## 🎯 Objetivo

Enriquecer un feature store con información pública adicional sobre usuarios, usando su email como punto de partida. Útil para:

- Scoring de usuarios
- Detección de fraude
- Personalización
- Segmentación
- Modelos de ML

## 🚀 Quick Start

```bash
# Ejecutar análisis de un email
python osint_email_enrichment.py tu@email.com
```

## 📊 Features Generados

- ✅ Validación de email (formato, tipo, dominio)
- 👤 Gravatar (avatar, perfil público)
- 💻 GitHub (perfil, repos, actividad)
- 🔒 Brechas de seguridad (HIBP)
- 🌐 Análisis de dominio
- 📈 Scores derivados (trust, online presence)

## 📝 Ejemplo de Output

```json
{
  "feature_vector": {
    "email_valid": 1,
    "is_free_email": 0,
    "is_corporate_email": 1,
    "has_gravatar": 1,
    "has_github": 1,
    "github_public_repos": 42,
    "breach_count": 0,
    "trust_score": 0.95,
    "online_presence_score": 0.87
  }
}
```

## ⚠️ Consideraciones

- APIs gratuitas tienen rate limits
- HIBP requiere API key para producción
- Cachear resultados (TTL 30-90 días recomendado)
- Ejecutar en batch/async para múltiples usuarios
- Considerar privacidad y GDPR

## 📚 Documentación

Ver [CLAUDE.md](CLAUDE.md) para contexto completo del proyecto.

## 🔐 Privacy & Compliance

- Solo datos públicamente disponibles
- Respetar GDPR/CCPA
- Informar a usuarios sobre enriquecimiento
- Permitir opt-out
