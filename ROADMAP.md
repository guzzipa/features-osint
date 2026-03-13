# 🗺️ Roadmap - OSINT Feature Engineering

**Estado Actual:** v3.0 funcionando, 130 features (78 OSINT + 52 Commercial APIs), publicado en GitHub
**Última actualización:** 2026-03-13

---

## 🎯 Objetivos por Camino

Hay **3 caminos posibles** dependiendo de tu objetivo:

### Camino A: Producción (Fintech/Crédito Real)
→ Usar el sistema para aprobar/rechazar créditos reales

### Camino B: Research/Portfolio (Mostrar capacidades)
→ Demo técnico, caso de estudio, portfolio profesional

### Camino C: ML Training (Entrenar modelos)
→ Crear dataset, entrenar modelo predictivo, A/B testing

---

# 📅 ROADMAP POR CAMINO

---

## 🏢 CAMINO A: PRODUCCIÓN

### 🔴 Fase 1: Fixes Críticos (1-2 semanas)

**Objetivo:** Resolver issues P0 que bloquean precisión

#### 1.1 Fix GitHub Activity Temporal
```
PROBLEMA: days_since_last_github_update = 9999 (placeholder)
IMPACTO: recency_score = 0.0 (incorrecto)
```

**Solución:**
- Agregar llamada a GitHub Commits API
- Extraer fecha del último commit real
- Calcular days_since correctamente

**Código estimado:**
```python
def _get_last_commit_date(username: str) -> Optional[datetime]:
    url = f"https://api.github.com/users/{username}/events"
    # Buscar último PushEvent
    # Retornar fecha real
```

**Tiempo:** 2-3 días
**Prioridad:** 🔴 CRÍTICA

---

#### 1.2 Parse Breach Dates (HIBP)
```
PROBLEMA: days_since_most_recent_breach = null
IMPACTO: No detecta breach reciente vs viejo
```

**Solución:**
- Parsear campo `BreachDate` de HIBP API
- Calcular días desde breach más reciente
- Agregar flags temporales

**Tiempo:** 1-2 días
**Prioridad:** 🔴 CRÍTICA

---

#### 1.3 Domain Age (WHOIS)
```
PROBLEMA: No valida antigüedad del dominio corporativo
IMPACTO: Email @startup.com (creado hace 1 mes) = igual score que @ibm.com
```

**Solución:**
```python
import whois

def get_domain_age(domain: str) -> int:
    try:
        w = whois.whois(domain)
        created = w.creation_date
        age_days = (datetime.now() - created).days
        return age_days
    except:
        return None
```

**Dependencia:** `pip install python-whois`
**Tiempo:** 1 día
**Prioridad:** 🟡 ALTA

---

#### 1.4 Stars/Forks por Repo
```
PROBLEMA: avg_stars_per_repo = 0.0 (no consultado)
IMPACTO: Pierde señal de calidad de código
```

**Solución:**
- Loop por repos del usuario
- Sumar stars/forks
- Calcular promedios

**Costo:** +N requests (rate limit consideration)
**Tiempo:** 2 días
**Prioridad:** 🟡 MEDIA

---

### 🟢 Fase 2: Production Ready (2-3 semanas)

#### 2.1 API REST
**Framework:** FastAPI

```python
# api.py
from fastapi import FastAPI
from pydantic import EmailStr

app = FastAPI()

@app.post("/enrich")
async def enrich_email(email: EmailStr):
    # Run OSINT pipeline
    # Return features
    return {"features": {...}, "trust_score": 0.8}

@app.post("/score")
async def score_credit(email: EmailStr):
    # Get features
    # Apply model
    # Return decision
    return {"decision": "APPROVE", "limit": 5000}
```

**Features:**
- Rate limiting (per IP)
- API key authentication
- Async processing
- Response caching

**Tiempo:** 1 semana
**Prioridad:** 🟢 ALTA

---

#### 2.2 Redis Caching
**TTL:** 30-90 días para datos estáticos

```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_features(email: str):
    key = f"osint:{email}"
    cached = cache.get(key)
    if cached:
        return json.loads(cached)

    # Fetch fresh data
    features = enrich(email)

    # Cache for 30 days
    cache.setex(key, 30*24*60*60, json.dumps(features))
    return features
```

**Tiempo:** 2-3 días
**Prioridad:** 🟢 ALTA

---

#### 2.3 Logging & Monitoring
**Stack:** Structlog + Prometheus + Grafana

```python
import structlog

log = structlog.get_logger()

def enrich_email(email: str):
    log.info("enrichment_started", email=email)

    try:
        features = extract_features(email)
        log.info("enrichment_success",
                 email=email,
                 trust_score=features['trust_score'])
        return features
    except Exception as e:
        log.error("enrichment_failed",
                  email=email,
                  error=str(e))
        raise
```

**Métricas a trackear:**
- Enrichment duration (p50, p95, p99)
- API calls per source
- Trust score distribution
- Error rates

**Tiempo:** 3-4 días
**Prioridad:** 🟢 MEDIA

---

#### 2.4 Testing Suite
**Framework:** pytest

```python
# tests/test_features.py
def test_email_entropy():
    assert calculate_entropy("random123") > 3.5
    assert calculate_entropy("juan.perez") < 3.0

def test_trust_score_no_github():
    data = {"github": {"github_found": False}}
    score = calculate_trust(data)
    assert score < 0.5  # Sin GitHub = bajo score

@mock.patch('requests.get')
def test_github_api_down(mock_get):
    mock_get.side_effect = Timeout()
    result = fetch_github("test@email.com")
    assert result["github_found"] == False
```

**Coverage target:** 80%+
**Tiempo:** 1 semana
**Prioridad:** 🟢 ALTA

---

### 🔵 Fase 3: Scale & Optimize (1-2 meses)

#### 3.1 Async Processing
**Framework:** Celery + RabbitMQ

```python
# tasks.py
from celery import Celery

app = Celery('osint', broker='amqp://localhost')

@app.task
def enrich_email_async(email: str):
    features = run_enrichment(email)
    save_to_db(email, features)
    return features

# Usage
result = enrich_email_async.delay("user@example.com")
```

**Beneficios:**
- No bloquea HTTP request
- Retry automático
- Queue management

**Tiempo:** 1 semana

---

#### 3.2 Database Integration
**Stack:** PostgreSQL + SQLAlchemy

```python
# models.py
class EnrichmentResult(Base):
    __tablename__ = 'enrichments'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    trust_score = Column(Float)
    features = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

**Queries necesarias:**
- Get by email
- Trust score distribution
- Bulk insert (batch processing)

**Tiempo:** 3-4 días

---

#### 3.3 Feature Store Integration
**Opciones:** Feast, Tecton, Hopsworks

```python
# feast/features.py
from feast import FeatureView, Entity, Field
from feast.types import Float32, Int64

user = Entity(name="user", join_keys=["email"])

osint_features = FeatureView(
    name="osint_features",
    entities=[user],
    schema=[
        Field(name="trust_score", dtype=Float32),
        Field(name="account_age_years", dtype=Float32),
        Field(name="github_repos", dtype=Int64),
    ],
)
```

**Tiempo:** 1-2 semanas

---

## 🎓 CAMINO B: RESEARCH/PORTFOLIO

### Objetivo: Demostrar capacidades técnicas

#### B.1 Blog Post / Case Study (1 semana)
**Título:** "Building a Credit Scoring System with OSINT: From 30 to 78 Features"

**Secciones:**
1. Problema: Scoring crediticio sin historial bancario
2. Solución: OSINT + Feature Engineering
3. Technical Deep Dive:
   - Email pattern analysis (entropía)
   - Temporal features (decay functions)
   - Anomaly detection
4. Results:
   - Comparación v1.0 vs v2.0
   - Caso real (anonymizado)
   - ROI estimado
5. Lessons Learned

**Publicar en:**
- Medium / Dev.to
- LinkedIn
- Personal blog

---

#### B.2 Demo Video/Notebook (2-3 días)

**Jupyter Notebook:**
```python
# demo.ipynb

# 1. Setup
from osint_email_enrichment import EmailOSINT

# 2. Analyze sample email
osint = EmailOSINT("demo@example.com")
features = osint.enrich()

# 3. Visualizaciones
import seaborn as sns
sns.barplot(trust_scores)

# 4. Model training example
from sklearn.ensemble import RandomForestClassifier
model.fit(X, y)
```

**Video:** Loom/YouTube (5-10 min)
- Quick walkthrough
- Feature highlights
- Use cases

---

#### B.3 Documentation Improvements (1 semana)

**Agregar:**
- API documentation (OpenAPI/Swagger)
- Architecture diagrams (draw.io)
- Sequence diagrams para flows
- Performance benchmarks
- Comparison table vs competitors

---

## 🤖 CAMINO C: ML TRAINING

### Objetivo: Entrenar modelo predictivo

#### C.1 Data Collection (2-4 semanas)

**Necesitas:**
- 1,000+ emails con labels
- Labels = {1: "buen pagador", 0: "mal pagador"}
- Idealmente 50/50 balance

**Opciones:**
1. **Datos históricos** (si tienes acceso)
   - Extraer emails de usuarios pasados
   - Label = si pagaron o no

2. **Synthetic data** (para POC)
   - Generar emails variados
   - Aplicar reglas heurísticas para labels

3. **Kaggle datasets** (aproximados)
   - Credit card default datasets
   - Agregar emails sintéticos

---

#### C.2 Feature Selection (1 semana)

**Proceso:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV

# Train base model
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Feature importance
importances = rf.feature_importances_
top_features = sorted(zip(feature_names, importances),
                      key=lambda x: x[1], reverse=True)[:30]

# Recursive feature elimination
selector = RFECV(rf, cv=5)
X_selected = selector.fit_transform(X_train, y_train)
```

**Target:** 20-30 features más predictivos

---

#### C.3 Model Training (2-3 semanas)

**Modelos a probar:**
1. **RandomForest** (baseline)
2. **XGBoost** (mejor performance)
3. **LightGBM** (más rápido)
4. **Logistic Regression** (interpretable)

**Pipeline:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.05
    ))
])

# Cross-validation
from sklearn.model_selection import cross_val_score
scores = cross_val_score(pipeline, X, y, cv=5, scoring='roc_auc')
```

**Métricas objetivo:**
- AUC: 0.80+ (bueno), 0.85+ (excelente)
- Precision: 0.75+
- Recall: 0.70+

---

#### C.4 Model Deployment (1-2 semanas)

**MLflow para tracking:**
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 8)

    model.fit(X_train, y_train)

    auc = roc_auc_score(y_test, y_pred_proba)
    mlflow.log_metric("auc", auc)

    mlflow.sklearn.log_model(model, "model")
```

**Serving:**
```python
# serve_model.py
import mlflow.sklearn

model = mlflow.sklearn.load_model("runs:/abc123/model")

@app.post("/predict")
def predict(features: dict):
    X = prepare_features(features)
    proba = model.predict_proba([X])[0][1]

    if proba >= 0.7:
        return {"decision": "APPROVE", "confidence": proba}
    else:
        return {"decision": "REJECT", "confidence": 1-proba}
```

---

## 📊 DECISIÓN: ¿Qué camino tomar?

### 🤔 Matriz de Decisión

| Factor | Producción | Portfolio | ML Training |
|--------|-----------|-----------|-------------|
| **Tiempo requerido** | 2-3 meses | 2-3 semanas | 1-2 meses |
| **Complejidad** | Alta | Baja | Media-Alta |
| **Requiere datos** | Opcional | No | Sí (crítico) |
| **ROI inmediato** | Alto | Bajo | Medio |
| **Riesgo técnico** | Alto | Bajo | Medio |
| **Aprendizaje** | Infra/DevOps | Marketing | ML/Data Science |

### 💡 Recomendaciones

**Si tienes datos históricos:**
→ **CAMINO C** (ML Training)
- Máximo valor técnico
- Demuestra todo el stack (data → model → deploy)
- Portfolio impresionante

**Si NO tienes datos:**
→ **CAMINO B** (Portfolio) → **CAMINO A** (Producción simplificada)
- Primero documenta bien
- Luego implementa API básica
- Escala según necesidad

**Si trabajas en fintech real:**
→ **CAMINO A** (Producción completa)
- Prioriza robustez
- Implementa monitoreo pesado
- Compliance crítico

---

## 🎯 RECOMENDACIÓN ESPECÍFICA PARA TI

Basado en lo que veo:

### ✅ Hacer AHORA (próximas 2 semanas):

1. **Fix P0 issues** (3-4 días)
   - GitHub activity temporal
   - Breach dates
   - Stars/forks

2. **Escribir blog post** (2-3 días)
   - Documenta el proceso
   - Muestra comparación v1 vs v2
   - Comparte en LinkedIn

3. **Crear Jupyter notebook demo** (1 día)
   - Análisis interactivo
   - Visualizaciones
   - Publicar en GitHub

4. **Mejorar README con ejemplos reales** (1 día)
   - GIFs/screenshots
   - Quick start mejorado
   - Badge de "live demo"

### 🔜 Hacer DESPUÉS (1-2 meses):

5. **API REST básica** (1 semana)
   - FastAPI simple
   - Deploy a Render/Railway (gratis)
   - Live demo accesible

6. **Colectar datos sintéticos** (1-2 semanas)
   - Generar 1000 emails variados
   - Labels heurísticos
   - Entrenar modelo baseline

7. **Dashboard de métricas** (1 semana)
   - Streamlit/Gradio
   - Visualizaciones interactivas
   - Deploy público

---

## 🚀 Quick Wins (Hacer en 1 día cada uno)

### 1. GitHub Topics
Agregar en repo settings:
- `machine-learning`
- `credit-scoring`
- `osint`
- `feature-engineering`
- `python`
- `fintech`

### 2. Shields.io Badges
Agregar a README:
```markdown
![GitHub stars](https://img.shields.io/github/stars/guzzipa/feature-generation-email)
![Code size](https://img.shields.io/github/languages/code-size/guzzipa/feature-generation-email)
![Last commit](https://img.shields.io/github/last-commit/guzzipa/feature-generation-email)
```

### 3. CONTRIBUTING.md
Guía para contribuidores externos

### 4. requirements.txt actualizado
```
# Production
fastapi==0.104.1
uvicorn==0.24.0
redis==5.0.1
python-whois==0.8.0

# ML (optional)
scikit-learn==1.3.2
xgboost==2.0.1
```

### 5. Docker support
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api.py"]
```

---

## 📅 Timeline Sugerido (60 días)

**Semana 1-2:** Fixes P0 + Blog post
**Semana 3-4:** API REST + Deploy
**Semana 5-6:** Data collection + Feature selection
**Semana 7-8:** Model training + Evaluation

**Resultado:** Sistema completo end-to-end deployado

---

## ❓ FAQ

**P: ¿Necesito TODOS los fixes P0?**
R: No, pero GitHub activity es crítico (impacta 30% del score)

**P: ¿Cuál es el MVP mínimo para producción?**
R: API REST + Cache + Logging + Tests = 2-3 semanas

**P: ¿Puedo entrenar modelo sin datos reales?**
R: Sí, con datos sintéticos puedes demostrar el pipeline completo

**P: ¿Qué tecnologías aprender primero?**
R: FastAPI + Redis + Docker (cubren 80% de needs)

---

**Última actualización:** 2026-03-13
**Versión:** 1.0
**Autor:** Sistema OSINT Feature Engineering
