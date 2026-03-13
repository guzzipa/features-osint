# 🔍 Additional Data Sources - v3.1

Added 5 high-value data sources to reach **192 total features** (+62 from v3.0).

---

## 📊 Overview

| Source | Features | Cost | Implementation | Value |
|--------|----------|------|----------------|-------|
| **WHOIS/DNS** | +13 | FREE | ✅ Complete | ⭐⭐⭐⭐⭐ |
| **IPQualityScore** | +20 | 5K/month free | ✅ Complete | ⭐⭐⭐⭐⭐ |
| **LinkedIn** | +15 | FREE | ⚠️ Placeholder | ⭐⭐⭐⭐⭐ |
| **StackOverflow** | +11 | FREE | ⚠️ Placeholder | ⭐⭐⭐⭐ |
| **Twitter/X** | +13 | 500/month free | ✅ Complete | ⭐⭐⭐ |
| **TOTAL** | **+72** | | | |

**Note:** Some implementations are placeholders pending API access or require manual configuration.

---

## 1️⃣ WHOIS/DNS Analysis (✅ COMPLETE)

### Features Extracted (13)

```python
{
    "domain_age_days": 8765,              # ⭐ CRITICAL for credit scoring
    "domain_age_years": 24.01,            # Years since domain registration
    "domain_registrar": "MarkMonitor Inc.",
    "domain_creation_date": "1997-09-15",
    "domain_expiration_date": "2028-09-14",
    "domain_updated_date": "2024-01-20",
    "domain_days_until_expiration": 912,
    "domain_days_since_update": 55,
    "domain_dnssec_enabled": true,
    "domain_privacy_protected": false,
    "mx_records_count": 5,
    "spf_record_exists": true,
    "dmarc_record_exists": true
}
```

### Setup

```bash
pip install python-whois dnspython
```

No API key needed - completely FREE!

### Usage

```python
from additional_sources import WHOISAnalyzer

whois = WHOISAnalyzer()
data = whois.analyze_domain("gmail.com")
print(f"Domain age: {data['domain_age_years']} years")
```

### Importance

**Domain age is CRITICAL:**
- `startup.com` (1 month old) = HIGH RISK
- `ibm.com` (30+ years old) = LOW RISK
- Differentiates legitimate companies from new/potentially fraudulent operations

---

## 2️⃣ IPQualityScore (✅ COMPLETE)

### Features Extracted (20)

```python
{
    "ipqs_fraud_score": 15,               # ⭐ 0-100 fraud probability
    "ipqs_valid": true,
    "ipqs_disposable": false,
    "ipqs_deliverability": "high",
    "ipqs_spam_trap": false,
    "ipqs_honeypot": false,
    "ipqs_frequent_complainer": false,
    "ipqs_suspect": false,
    "ipqs_leaked": false,                 # ⭐ Credentials in leaks
    "ipqs_first_seen": "2018-03-15",
    "ipqs_domain_age_days": 9125,
    "ipqs_domain_velocity": "low",
    "ipqs_suspicious_tld": false,
    "ipqs_recent_abuse": false,
    "ipqs_overall_score": 92,
    "ipqs_suggested_domain": null,
    "ipqs_catch_all": false,
    "ipqs_smtp_score": 98,
    "ipqs_generic": false,
    "ipqs_common": true
}
```

### Setup

1. **Sign up:** https://www.ipqualityscore.com/create-account
2. **Free tier:** 5,000 requests/month (no credit card required)
3. **Get API key:** Dashboard → API Keys
4. **Add to `.env`:**
   ```bash
   IPQS_API_KEY=your_api_key_here
   ```

### Usage

```python
from additional_sources import IPQualityScore

ipqs = IPQualityScore()
data = ipqs.validate_email("test@example.com")
print(f"Fraud score: {data['ipqs_fraud_score']}/100")
```

### Importance

**Best-in-class fraud detection:**
- Professional fraud scoring (0-100)
- Leaked credentials detection
- Spam trap detection
- Disposable email detection
- Domain velocity (rapid domain creation = fraud signal)

---

## 3️⃣ LinkedIn Scraping (⚠️ PLACEHOLDER)

### Features Designed (15)

```python
{
    "linkedin_profile_exists": true,
    "linkedin_connections_count": 842,
    "linkedin_endorsements": 67,
    "linkedin_recommendations": 12,
    "linkedin_years_experience": 8.5,
    "linkedin_education_count": 2,
    "linkedin_has_profile_picture": true,
    "linkedin_headline_professional": true,
    "current_company_from_linkedin": "Tech Corp",
    "current_position_from_linkedin": "Senior Engineer",
    "linkedin_profile_completeness": 0.95,
    "linkedin_premium_account": false,
    "linkedin_verified_profile": true,
    "days_since_linkedin_update": 15,
    "linkedin_activity_score": 0.72
}
```

### Implementation Status

⚠️ **Placeholder implementation** - requires one of:

**Option A: Manual Google Custom Search API**
1. Setup: https://developers.google.com/custom-search
2. Search query: `site:linkedin.com/in "email@example.com"`
3. Parse results for profile URL
4. Scrape public profile (respecting robots.txt)

**Option B: Third-party services**
- Proxycurl (paid): https://nubela.co/proxycurl/
- RocketReach (paid): https://rocketreach.co/

**Option C: Manual lookup**
- User provides LinkedIn URL directly
- System scrapes public data only

### Why Important

**LinkedIn = #1 professional signal:**
- Connections count → network size
- Endorsements → skill validation
- Recommendations → trust from peers
- Experience years → career stability
- Profile completeness → professionalism

---

## 4️⃣ StackOverflow API (⚠️ PLACEHOLDER)

### Features Designed (11)

```python
{
    "stackoverflow_profile": true,
    "stackoverflow_reputation": 12543,    # ⭐ Developer credibility
    "stackoverflow_badges_gold": 8,
    "stackoverflow_badges_silver": 42,
    "stackoverflow_badges_bronze": 128,
    "stackoverflow_questions": 34,
    "stackoverflow_answers": 267,
    "stackoverflow_acceptance_rate": 0.78,
    "stackoverflow_member_years": 6.3,
    "stackoverflow_top_tags": ["python", "machine-learning", "aws"],
    "developer_credibility_score": 0.85
}
```

### Implementation Status

⚠️ **Placeholder implementation** - requires:

1. **Username/Profile URL** (email not directly searchable)
   - User provides StackOverflow username
   - Or: search via Google: `site:stackoverflow.com/users "email"`

2. **API Usage** (FREE, 10K requests/day)
   - Docs: https://api.stackexchange.com/docs
   - No API key required for basic calls
   - Rate limit: 300 requests/IP/day (no key) or 10K/day (with key)

### Usage (when implemented)

```python
from additional_sources import StackOverflowAPI

so = StackOverflowAPI()
# Requires username or user ID
data = so.get_user_data(user_id=123456)
print(f"Reputation: {data['stackoverflow_reputation']}")
```

### Why Important

**For tech workers/developers:**
- Reputation = proof of technical skill
- Badges = achievements and expertise
- Answer/question ratio = contribution level
- Top tags = skill areas
- High correlation with employment stability in tech

---

## 5️⃣ Twitter/X API (✅ COMPLETE)

### Features Extracted (13)

```python
{
    "twitter_account_exists": true,
    "twitter_username": "johndoe",
    "twitter_followers_count": 1842,
    "twitter_following_count": 423,
    "twitter_tweets_count": 3891,
    "twitter_account_age_days": 2184,
    "twitter_verified": false,
    "twitter_bio_length": 142,
    "twitter_has_profile_image": true,
    "twitter_engagement_rate": 0.45,
    "days_since_last_tweet": 3,
    "twitter_professional_keywords": 4,
    "twitter_sentiment_score": 0.0
}
```

### Setup

1. **Apply for Developer Account:** https://developer.twitter.com/
2. **Create Project + App**
3. **Get Bearer Token** from dashboard
4. **Add to `.env`:**
   ```bash
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   ```

**Free Tier Limits:**
- 500 tweets/month (Twitter API v2 Essential)
- User lookups count toward quota
- Rate limit: 15 requests/15 minutes

### Usage

```python
from additional_sources import TwitterAPI

twitter = TwitterAPI()
# Searches for username extracted from email
data = twitter.search_user("johndoe@example.com")
print(f"Followers: {data['twitter_followers_count']}")
```

### Limitations

- Email → username mapping is heuristic (extracts username from email)
- Only finds accounts where username matches email prefix
- May miss accounts with different usernames

### Why Important

**Social presence indicators:**
- Followers count → influence/reach
- Account age → established identity
- Engagement rate → active vs dormant
- Professional keywords in bio → career focus

---

## 🎯 Total Feature Count Evolution

| Version | Features | Sources | Comments |
|---------|----------|---------|----------|
| v1.0 | 30 | OSINT basic | Initial release |
| v2.0 | 78 | OSINT advanced + NLP | Temporal analysis |
| v3.0 | 130 | + Hunter.io/EmailRep/Clearbit | Commercial APIs |
| **v3.1** | **202** | **+ WHOIS/IPQS/LinkedIn/SO/Twitter** | **High-value additions** |

**+572% features vs v1.0**
**+55% features vs v3.0**

---

## 📦 Installation

```bash
# Install new dependencies
pip install -r requirements.txt

# Includes:
# - python-whois (WHOIS lookups)
# - dnspython (DNS records)
# - requests (HTTP)
# - python-dotenv (.env management)
```

---

## 🚀 Usage

### Standalone Testing

```bash
# Test all additional sources
python additional_sources.py test@example.com

# Output: additional_sources_test_at_example.com.json
```

### Integrated Pipeline

Will be integrated into `full_enrichment.py` in next update to provide all 202 features in one call.

---

## ✅ Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **WHOIS/DNS** | ✅ Complete | Fully functional, no API key needed |
| **IPQualityScore** | ✅ Complete | Requires free API key (5K/month) |
| **LinkedIn** | ⚠️ Placeholder | Requires Google CSE or manual config |
| **StackOverflow** | ⚠️ Placeholder | Requires username/profile URL |
| **Twitter** | ✅ Complete | Requires free developer account |

**Currently functional:** WHOIS, IPQS, Twitter = **+46 features**
**Pending implementation:** LinkedIn, StackOverflow = **+26 features**

---

## 🔑 API Keys Setup Guide

### 1. IPQualityScore (FREE 5K/month)

```bash
# 1. Sign up
https://www.ipqualityscore.com/create-account

# 2. Get API key
Dashboard → API → Private Key

# 3. Add to .env
IPQS_API_KEY=abc123...
```

### 2. Twitter Developer (FREE 500/month)

```bash
# 1. Apply for developer account
https://developer.twitter.com/en/portal/petition/essential/basic-info

# 2. Create project + app
# 3. Generate Bearer Token
# 4. Add to .env
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxx...
```

### 3. LinkedIn/StackOverflow

No API keys required, but:
- **LinkedIn:** Needs implementation (Google CSE or manual)
- **StackOverflow:** Needs username/user_id input

---

## 🎯 Next Steps

1. ✅ **WHOIS + IPQS implemented** - can use immediately
2. ⏳ **Twitter** - get free developer account
3. ⏳ **LinkedIn** - implement Google Custom Search
4. ⏳ **StackOverflow** - add username input option
5. 🔄 **Integration** - merge into main pipeline (full_enrichment.py)

---

## 📊 Expected Impact on Credit Scoring

| Feature | Impact | Reason |
|---------|--------|--------|
| `domain_age_days` | ⭐⭐⭐⭐⭐ | Differentiates established from new companies |
| `ipqs_fraud_score` | ⭐⭐⭐⭐⭐ | Professional fraud detection |
| `ipqs_leaked` | ⭐⭐⭐⭐⭐ | Credential security signal |
| `linkedin_connections_count` | ⭐⭐⭐⭐ | Network = stability |
| `stackoverflow_reputation` | ⭐⭐⭐⭐ | Tech skill proof (for dev roles) |
| `twitter_followers_count` | ⭐⭐⭐ | Social influence |
| `domain_dnssec_enabled` | ⭐⭐⭐ | Security posture |
| `linkedin_years_experience` | ⭐⭐⭐⭐ | Employment stability |

---

## 📝 Notes

- WHOIS/DNS data is cached (changes infrequently)
- IPQualityScore has 5K/month free tier - sufficient for most use cases
- LinkedIn/StackOverflow placeholders return zero values - safe for ML models
- Twitter rate limits: be mindful when doing batch processing
- All features have safe defaults (0, false, null) when data unavailable

---

**Version:** 3.1.0
**Last Updated:** 2026-03-13
**Author:** Feature Generation Email Contributors
