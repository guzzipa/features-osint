# 🚀 Quick Start - v3.0 (Commercial APIs)

## Instalación

```bash
# 1. Clonar repo
git clone https://github.com/guzzipa/feature-generation-email.git
cd feature-generation-email

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API keys
cp .env.example .env
# Editar .env con tus API keys
```

## Obtener API Keys

### Free Tier (para pruebas)

1. **Hunter.io**: https://hunter.io/users/sign_up
   - Free: 25 requests/month
   - Después login: API → Your API Keys

2. **EmailRep.io**: https://emailrep.io/key
   - Free: 300 requests/day
   - Click "Get Free API Key"

3. **Clearbit**: https://dashboard.clearbit.com/signup
   - Trial: 20 requests
   - Después login: Settings → API Keys

### Opcional (mejoran resultados)

4. **GitHub Token**: https://github.com/settings/tokens
   - New token (classic) → Scope: `public_repo, read:user`

5. **HIBP**: https://haveibeenpwned.com/API/Key
   - $3.50/mes

## Uso Básico

### Opción 1: Full Pipeline (OSINT + Commercial)

```bash
# Con commercial APIs
python full_enrichment.py test@example.com

# Output:
# 📧 EMAIL: test@example.com
# 🎯 RISK ASSESSMENT: MEDIUM RISK
#    Trust Score: 0.623
# 📊 CORE SCORES:
#    Identity Strength:    0.450
#    Security Risk:        0.120
# 💼 COMMERCIAL API SCORES:
#    Hunter Verification:  0.850
#    EmailRep Reputation:  0.500
# ✅ Full results saved to: results/full_enrichment_test_at_example.com.json
```

### Opción 2: Solo OSINT (sin APIs pagas)

```bash
# Sin commercial APIs (gratis)
python full_enrichment.py test@example.com --skip-commercial
```

### Opción 3: Paso a paso

```bash
# Paso 1: OSINT data
python osint_email_enrichment.py test@example.com

# Paso 2: Commercial APIs (opcional)
python commercial_apis.py test@example.com

# Paso 3: Enhanced features
python enhanced_feature_engineering.py \
  results/osint_results_test_at_example.com.json \
  commercial_api_results_test_at_example.com.json
```

## Output Generado

```json
{
  "email": "test@example.com",
  "pipeline_version": "3.0.0",
  "features": {
    "feature_count": 118,
    "ml_ready": {
      "numerical_features": {
        "overall_trust_score": 0.623,
        "hunter_score": 85,
        "emailrep_reputation_score": 0.5,
        "clearbit_person_score": 0.8,
        // ... 110+ more features
      },
      "categorical_features": {
        "email_provider_type": "corporate",
        "profile_completeness": "full"
      }
    }
  },
  "summary": {
    "risk_classification": {
      "level": "MEDIUM RISK",
      "recommendation": "REVIEW",
      "trust_score": 0.623
    }
  }
}
```

## Comparación de Features

| Versión | Features | Fuentes de Datos | Costo |
|---------|----------|------------------|-------|
| **v1.0** | 30 | OSINT básico | Gratis |
| **v2.0** | 78 | OSINT avanzado + NLP + temporal | Gratis |
| **v3.0** | 118+ | OSINT + Hunter + EmailRep + Clearbit | $150-200/mes |

## Costos Estimados (Producción)

Para **1,000 emails/mes**:

| API | Plan | Costo | Features Aportados |
|-----|------|-------|-------------------|
| Hunter.io | Growth ($99) | $99/mes | 13 email verification features |
| EmailRep.io | Basic ($20) | $20/mes | 15 reputation features |
| Clearbit | Starter ($99) | $99/mes | 20 company/person features |
| **TOTAL** | | **$218/mes** | **+48 features comerciales** |

**ROI**: Si mejora precisión 5% → reduce pérdidas por default ~$10K/mes (para portfolio $1M)

## Testing

```bash
# Test con email público
python full_enrichment.py john.doe@company.com

# Test batch (3 emails)
python full_enrichment.py test1@example.com
python full_enrichment.py test2@gmail.com
python full_enrichment.py test3@startup.io
```

## Troubleshooting

### Error: API key not configured

```
[Hunter.io] API key not configured, skipping
```

**Solución**: Asegurate de tener el `.env` configurado:

```bash
cp .env.example .env
nano .env  # Agregar tus API keys
```

### Error: Rate limit exceeded

```
[Hunter.io] API error: 429 Too Many Requests
```

**Solución**:
- Hunter free tier = 25 req/mes, upgrade a paid plan
- O esperar reset mensual
- O usar `--skip-commercial` para OSINT only

### Error: Import error

```
ImportError: No module named 'requests'
```

**Solución**:

```bash
pip install -r requirements.txt
```

## Próximos Pasos

1. ✅ Probaste el pipeline → Leer [README.md](README.md) para uso avanzado
2. ✅ Funciona bien → Ver [ROADMAP.md](ROADMAP.md) para siguientes features
3. ✅ Querés integrar → Ver ejemplos de integración con ML en `examples/`
