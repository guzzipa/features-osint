#!/usr/bin/env python3
"""
Commercial API Integrations for Feature Generation

Integrates with paid/commercial services:
- Hunter.io: Email verification, deliverability, corporate data
- EmailRep.io: Reputation scoring, malicious activity detection
- Clearbit: Company and person enrichment

Author: Feature Generation Email
Version: 3.0.0
"""

import os
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HunterIO:
    """
    Hunter.io API integration for email verification and corporate data.

    Features extracted:
    - Email deliverability status
    - Email type (webmail vs corporate)
    - Accept-all domain detection
    - Risk score
    - Domain employee count
    - Department information

    API Limits:
    - Free: 25 requests/month
    - Starter: $49/mo for 500 requests
    - Growth: $99/mo for 5,000 requests

    Docs: https://hunter.io/api-documentation
    """

    BASE_URL = "https://api.hunter.io/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUNTER_API_KEY")
        if not self.api_key:
            logger.warning("Hunter.io API key not found. Set HUNTER_API_KEY in .env")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FeatureGenerationEmail/3.0'
        })

    def verify_email(self, email: str) -> Dict[str, Any]:
        """
        Verify email address deliverability and extract metadata.

        Args:
            email: Email address to verify

        Returns:
            Dictionary with verification results and metadata
        """
        if not self.api_key:
            logger.warning("Hunter.io API key not configured, skipping")
            return self._empty_response()

        try:
            url = f"{self.BASE_URL}/email-verifier"
            params = {
                'email': email,
                'api_key': self.api_key
            }

            logger.info(f"[Hunter.io] Verifying email: {email}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json().get('data', {})

            return {
                'hunter_status': data.get('status'),  # valid, invalid, accept_all, webmail, disposable, unknown
                'hunter_result': data.get('result'),  # deliverable, undeliverable, risky, unknown
                'hunter_score': data.get('score', 0),  # 0-100 (confidence)
                'hunter_regexp': data.get('regexp', False),
                'hunter_gibberish': data.get('gibberish', False),
                'hunter_disposable': data.get('disposable', False),
                'hunter_webmail': data.get('webmail', False),
                'hunter_mx_records': data.get('mx_records', False),
                'hunter_smtp_server': data.get('smtp_server', False),
                'hunter_smtp_check': data.get('smtp_check', False),
                'hunter_accept_all': data.get('accept_all', False),
                'hunter_block': data.get('block', False),
                'hunter_sources_count': len(data.get('sources', [])),
                'hunter_first_seen': data.get('first_seen'),
                'hunter_last_seen': data.get('last_seen'),
            }

        except requests.RequestException as e:
            logger.error(f"[Hunter.io] API error: {e}")
            return self._empty_response()
        except Exception as e:
            logger.error(f"[Hunter.io] Unexpected error: {e}")
            return self._empty_response()

    def get_domain_search(self, domain: str) -> Dict[str, Any]:
        """
        Get information about a domain (employee count, department info).

        Args:
            domain: Domain to search (e.g., 'google.com')

        Returns:
            Dictionary with domain metadata
        """
        if not self.api_key:
            return {'domain_emails_found': 0, 'domain_pattern': None}

        try:
            url = f"{self.BASE_URL}/domain-search"
            params = {
                'domain': domain,
                'api_key': self.api_key,
                'limit': 10  # Don't need all emails, just metadata
            }

            logger.info(f"[Hunter.io] Searching domain: {domain}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json().get('data', {})

            return {
                'domain_emails_found': data.get('emails', 0),
                'domain_pattern': data.get('pattern'),  # e.g., "{first}.{last}@domain.com"
                'domain_organization': data.get('organization'),
                'domain_description': data.get('description'),
                'domain_twitter': data.get('twitter'),
                'domain_facebook': data.get('facebook'),
                'domain_linkedin': data.get('linkedin'),
            }

        except requests.RequestException as e:
            logger.error(f"[Hunter.io] Domain search error: {e}")
            return {'domain_emails_found': 0, 'domain_pattern': None}

    def _empty_response(self) -> Dict[str, Any]:
        """Return empty response when API is not available."""
        return {
            'hunter_status': None,
            'hunter_result': None,
            'hunter_score': 0,
            'hunter_regexp': False,
            'hunter_gibberish': False,
            'hunter_disposable': False,
            'hunter_webmail': False,
            'hunter_mx_records': False,
            'hunter_smtp_server': False,
            'hunter_smtp_check': False,
            'hunter_accept_all': False,
            'hunter_block': False,
            'hunter_sources_count': 0,
            'hunter_first_seen': None,
            'hunter_last_seen': None,
        }


class EmailRepIO:
    """
    EmailRep.io API integration for email reputation and security.

    Features extracted:
    - Reputation score (high, medium, low, none)
    - Suspicious activity flags
    - Malicious activity detection
    - Credential leaks
    - Data breach presence
    - First/last seen dates
    - Spam probability

    API Limits:
    - Free: 300 requests/day
    - Basic: $20/mo for 10,000 requests
    - Pro: $100/mo for 100,000 requests

    Docs: https://docs.emailrep.io/
    """

    BASE_URL = "https://emailrep.io"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("EMAILREP_API_KEY")
        if not self.api_key:
            logger.warning("EmailRep.io API key not found. Set EMAILREP_API_KEY in .env")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Key': self.api_key,
                'User-Agent': 'FeatureGenerationEmail/3.0'
            })

    def check_reputation(self, email: str) -> Dict[str, Any]:
        """
        Check email reputation and security flags.

        Args:
            email: Email address to check

        Returns:
            Dictionary with reputation data
        """
        if not self.api_key:
            logger.warning("EmailRep.io API key not configured, skipping")
            return self._empty_response()

        try:
            url = f"{self.BASE_URL}/{email}"

            logger.info(f"[EmailRep.io] Checking reputation: {email}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'emailrep_email': data.get('email'),
                'emailrep_reputation': data.get('reputation'),  # high, medium, low, none
                'emailrep_suspicious': data.get('suspicious', False),
                'emailrep_references': data.get('references', 0),
                'emailrep_blacklisted': data.get('details', {}).get('blacklisted', False),
                'emailrep_malicious_activity': data.get('details', {}).get('malicious_activity', False),
                'emailrep_malicious_activity_recent': data.get('details', {}).get('malicious_activity_recent', False),
                'emailrep_credentials_leaked': data.get('details', {}).get('credentials_leaked', False),
                'emailrep_credentials_leaked_recent': data.get('details', {}).get('credentials_leaked_recent', False),
                'emailrep_data_breach': data.get('details', {}).get('data_breach', False),
                'emailrep_first_seen': data.get('details', {}).get('first_seen'),
                'emailrep_last_seen': data.get('details', {}).get('last_seen'),
                'emailrep_domain_exists': data.get('details', {}).get('domain_exists', False),
                'emailrep_domain_reputation': data.get('details', {}).get('domain_reputation'),
                'emailrep_new_domain': data.get('details', {}).get('new_domain', False),
                'emailrep_days_since_domain_creation': data.get('details', {}).get('days_since_domain_creation'),
                'emailrep_suspicious_tld': data.get('details', {}).get('suspicious_tld', False),
                'emailrep_spam': data.get('details', {}).get('spam', False),
                'emailrep_free_provider': data.get('details', {}).get('free_provider', False),
                'emailrep_disposable': data.get('details', {}).get('disposable', False),
                'emailrep_deliverable': data.get('details', {}).get('deliverable', False),
                'emailrep_accept_all': data.get('details', {}).get('accept_all', False),
                'emailrep_valid_mx': data.get('details', {}).get('valid_mx', False),
                'emailrep_spoofable': data.get('details', {}).get('spoofable', False),
                'emailrep_spf_strict': data.get('details', {}).get('spf_strict', False),
                'emailrep_dmarc_enforced': data.get('details', {}).get('dmarc_enforced', False),
                'emailrep_profiles': len(data.get('details', {}).get('profiles', [])),
            }

        except requests.RequestException as e:
            logger.error(f"[EmailRep.io] API error: {e}")
            return self._empty_response()
        except Exception as e:
            logger.error(f"[EmailRep.io] Unexpected error: {e}")
            return self._empty_response()

    def _empty_response(self) -> Dict[str, Any]:
        """Return empty response when API is not available."""
        return {
            'emailrep_email': None,
            'emailrep_reputation': 'none',
            'emailrep_suspicious': False,
            'emailrep_references': 0,
            'emailrep_blacklisted': False,
            'emailrep_malicious_activity': False,
            'emailrep_malicious_activity_recent': False,
            'emailrep_credentials_leaked': False,
            'emailrep_credentials_leaked_recent': False,
            'emailrep_data_breach': False,
            'emailrep_first_seen': None,
            'emailrep_last_seen': None,
            'emailrep_domain_exists': False,
            'emailrep_domain_reputation': None,
            'emailrep_new_domain': False,
            'emailrep_days_since_domain_creation': None,
            'emailrep_suspicious_tld': False,
            'emailrep_spam': False,
            'emailrep_free_provider': False,
            'emailrep_disposable': False,
            'emailrep_deliverable': False,
            'emailrep_accept_all': False,
            'emailrep_valid_mx': False,
            'emailrep_spoofable': False,
            'emailrep_spf_strict': False,
            'emailrep_dmarc_enforced': False,
            'emailrep_profiles': 0,
        }


class Clearbit:
    """
    Clearbit API integration for company and person enrichment.

    Features extracted:
    - Company name, domain, size, employees
    - Funding information
    - Industry and category
    - Technology stack
    - Person job title, role, seniority
    - LinkedIn URL

    API Limits:
    - Free: 20 requests/month (trial)
    - Starter: $99/mo for 1,000 requests
    - Growth: $299/mo for 10,000 requests

    Docs: https://clearbit.com/docs
    """

    BASE_URL = "https://person.clearbit.com/v2"
    COMPANY_URL = "https://company.clearbit.com/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLEARBIT_API_KEY")
        if not self.api_key:
            logger.warning("Clearbit API key not found. Set CLEARBIT_API_KEY in .env")
        self.session = requests.Session()
        if self.api_key:
            self.session.auth = (self.api_key, '')
        self.session.headers.update({
            'User-Agent': 'FeatureGenerationEmail/3.0'
        })

    def enrich_person(self, email: str) -> Dict[str, Any]:
        """
        Enrich person and company data from email.

        Args:
            email: Email address to enrich

        Returns:
            Dictionary with person and company data
        """
        if not self.api_key:
            logger.warning("Clearbit API key not configured, skipping")
            return self._empty_response()

        try:
            url = f"{self.BASE_URL}/combined/find"
            params = {'email': email}

            logger.info(f"[Clearbit] Enriching email: {email}")
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 404:
                logger.info(f"[Clearbit] No data found for {email}")
                return self._empty_response()

            response.raise_for_status()
            data = response.json()

            person = data.get('person', {})
            company = data.get('company', {})

            return {
                # Person data
                'clearbit_person_name': person.get('name', {}).get('fullName'),
                'clearbit_person_location': person.get('location'),
                'clearbit_person_title': person.get('employment', {}).get('title'),
                'clearbit_person_role': person.get('employment', {}).get('role'),  # engineering, sales, marketing, etc.
                'clearbit_person_sub_role': person.get('employment', {}).get('subRole'),
                'clearbit_person_seniority': person.get('employment', {}).get('seniority'),  # executive, manager, individual
                'clearbit_person_linkedin': person.get('linkedin', {}).get('handle'),
                'clearbit_person_twitter': person.get('twitter', {}).get('handle'),
                'clearbit_person_github': person.get('github', {}).get('handle'),
                'clearbit_person_avatar': person.get('avatar'),
                'clearbit_person_email_provider': person.get('emailProvider', False),

                # Company data
                'clearbit_company_name': company.get('name'),
                'clearbit_company_domain': company.get('domain'),
                'clearbit_company_category_sector': company.get('category', {}).get('sector'),
                'clearbit_company_category_industry': company.get('category', {}).get('industry'),
                'clearbit_company_category_sub_industry': company.get('category', {}).get('subIndustry'),
                'clearbit_company_tags': ','.join(company.get('tags', [])),
                'clearbit_company_description': company.get('description'),
                'clearbit_company_founded_year': company.get('foundedYear'),
                'clearbit_company_location': company.get('location'),
                'clearbit_company_employees': company.get('metrics', {}).get('employees'),
                'clearbit_company_employees_range': company.get('metrics', {}).get('employeesRange'),
                'clearbit_company_estimated_revenue': company.get('metrics', {}).get('estimatedAnnualRevenue'),
                'clearbit_company_raised': company.get('metrics', {}).get('raised'),
                'clearbit_company_tech': ','.join(company.get('tech', [])),
                'clearbit_company_linkedin': company.get('linkedin', {}).get('handle'),
                'clearbit_company_twitter': company.get('twitter', {}).get('handle'),
                'clearbit_company_facebook': company.get('facebook', {}).get('handle'),
                'clearbit_company_alexa_us_rank': company.get('metrics', {}).get('alexaUsRank'),
                'clearbit_company_alexa_global_rank': company.get('metrics', {}).get('alexaGlobalRank'),
            }

        except requests.RequestException as e:
            logger.error(f"[Clearbit] API error: {e}")
            return self._empty_response()
        except Exception as e:
            logger.error(f"[Clearbit] Unexpected error: {e}")
            return self._empty_response()

    def _empty_response(self) -> Dict[str, Any]:
        """Return empty response when API is not available."""
        return {
            'clearbit_person_name': None,
            'clearbit_person_location': None,
            'clearbit_person_title': None,
            'clearbit_person_role': None,
            'clearbit_person_sub_role': None,
            'clearbit_person_seniority': None,
            'clearbit_person_linkedin': None,
            'clearbit_person_twitter': None,
            'clearbit_person_github': None,
            'clearbit_person_avatar': None,
            'clearbit_person_email_provider': False,
            'clearbit_company_name': None,
            'clearbit_company_domain': None,
            'clearbit_company_category_sector': None,
            'clearbit_company_category_industry': None,
            'clearbit_company_category_sub_industry': None,
            'clearbit_company_tags': None,
            'clearbit_company_description': None,
            'clearbit_company_founded_year': None,
            'clearbit_company_location': None,
            'clearbit_company_employees': None,
            'clearbit_company_employees_range': None,
            'clearbit_company_estimated_revenue': None,
            'clearbit_company_raised': None,
            'clearbit_company_tech': None,
            'clearbit_company_linkedin': None,
            'clearbit_company_twitter': None,
            'clearbit_company_facebook': None,
            'clearbit_company_alexa_us_rank': None,
            'clearbit_company_alexa_global_rank': None,
        }


class CommercialAPIsEnricher:
    """
    Unified interface to all commercial APIs.

    Usage:
        enricher = CommercialAPIsEnricher()
        data = enricher.enrich_email("user@example.com")
    """

    def __init__(self):
        self.hunter = HunterIO()
        self.emailrep = EmailRepIO()
        self.clearbit = Clearbit()

    def enrich_email(self, email: str) -> Dict[str, Any]:
        """
        Run all commercial API enrichments for an email.

        Args:
            email: Email address to enrich

        Returns:
            Combined dictionary with all API results
        """
        logger.info(f"[CommercialAPIs] Starting enrichment for: {email}")

        results = {
            'email': email,
            'enrichment_timestamp': datetime.now().isoformat(),
        }

        # Hunter.io - Email verification
        hunter_data = self.hunter.verify_email(email)
        results.update(hunter_data)

        # Extract domain for domain search
        domain = email.split('@')[1] if '@' in email else None
        if domain:
            hunter_domain = self.hunter.get_domain_search(domain)
            results.update(hunter_domain)

        # EmailRep.io - Reputation
        emailrep_data = self.emailrep.check_reputation(email)
        results.update(emailrep_data)

        # Clearbit - Person + Company
        clearbit_data = self.clearbit.enrich_person(email)
        results.update(clearbit_data)

        logger.info(f"[CommercialAPIs] Enrichment completed for: {email}")
        return results


def main():
    """Test the commercial APIs."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python commercial_apis.py email@example.com")
        sys.exit(1)

    email = sys.argv[1]

    print(f"\n🔍 Testing Commercial APIs for: {email}\n")

    enricher = CommercialAPIsEnricher()
    data = enricher.enrich_email(email)

    import json
    print(json.dumps(data, indent=2, default=str))

    # Save to file
    output_file = f"commercial_api_results_{email.replace('@', '_at_')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\n✅ Results saved to: {output_file}")


if __name__ == "__main__":
    main()
