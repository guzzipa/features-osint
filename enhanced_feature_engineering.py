#!/usr/bin/env python3
"""
Enhanced Feature Engineering with Commercial APIs
Extends advanced features (78) with commercial API data (+40) = 118 total features

Combines:
- Public OSINT data (GitHub, Gravatar, HIBP)
- Commercial APIs (Hunter.io, EmailRep.io, Clearbit)

Version: 3.0.0
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from advanced_feature_engineering import AdvancedFeatureEngineer, AdvancedMLFeatures


@dataclass
class EnhancedMLFeatures(AdvancedMLFeatures):
    """
    Extended features including commercial API data.
    Inherits all 78 features from AdvancedMLFeatures + adds ~40 more.
    """

    # ========== HUNTER.IO FEATURES ==========
    # Email verification (10 features)
    hunter_deliverable: int  # 1=deliverable, 0=undeliverable/unknown
    hunter_score: int  # 0-100 confidence score
    hunter_disposable: int  # Disposable email detector
    hunter_webmail: int  # Is webmail (vs corporate)
    hunter_accept_all: int  # Domain accepts all emails
    hunter_mx_records: int  # Has MX records
    hunter_smtp_check: int  # SMTP validation passed
    hunter_gibberish: int  # Username is gibberish
    hunter_block: int  # Email is blocked
    hunter_sources_count: int  # Times seen online

    # Domain intelligence (3 features)
    domain_emails_found: int  # Emails found in domain
    domain_has_pattern: int  # Domain has email pattern
    domain_has_social: int  # Domain has social profiles

    # ========== EMAILREP.IO FEATURES ==========
    # Reputation (15 features)
    emailrep_reputation_score: float  # Converted: high=1.0, medium=0.5, low=0.2, none=0.0
    emailrep_suspicious: int  # Flagged as suspicious
    emailrep_references: int  # Times referenced online
    emailrep_blacklisted: int  # On blacklist
    emailrep_malicious_activity: int  # Known malicious activity
    emailrep_malicious_recent: int  # Malicious activity in last 90 days
    emailrep_credentials_leaked: int  # Credentials leaked
    emailrep_credentials_leaked_recent: int  # Leaked in last year
    emailrep_spam: int  # Associated with spam
    emailrep_spoofable: int  # Domain is spoofable
    emailrep_domain_exists: int  # Domain exists
    emailrep_domain_age_days: Optional[int]  # Days since domain creation
    emailrep_new_domain: int  # Domain < 1 year old
    emailrep_valid_mx: int  # Valid MX records
    emailrep_profiles_count: int  # Associated profiles

    # ========== CLEARBIT FEATURES ==========
    # Person data (8 features)
    clearbit_person_found: int  # Person data available
    clearbit_has_title: int  # Has job title
    clearbit_has_role: int  # Has defined role
    clearbit_seniority_level: int  # 0=individual, 1=manager, 2=executive
    clearbit_has_linkedin: int  # LinkedIn profile exists
    clearbit_has_github: int  # GitHub handle found (cross-validation)
    clearbit_email_is_personal: int  # Using personal email for work
    clearbit_person_score: float  # Composite person data quality (0-1)

    # Company data (12 features)
    clearbit_company_found: int  # Company data available
    clearbit_company_employees: Optional[int]  # Number of employees
    clearbit_company_size_score: float  # 0-1 based on employee range
    clearbit_company_founded_year: Optional[int]  # Year founded
    clearbit_company_age_years: float  # Years since founding
    clearbit_has_funding: int  # Has raised funding
    clearbit_funding_amount: Optional[float]  # Total raised (if available)
    clearbit_has_tech_stack: int  # Technology stack documented
    clearbit_tech_count: int  # Number of technologies used
    clearbit_alexa_rank: Optional[int]  # Global Alexa rank (lower = better)
    clearbit_has_social: int  # Has social profiles
    clearbit_company_score: float  # Composite company quality (0-1)

    # ========== CROSS-SOURCE VALIDATION ==========
    # Consistency checks across multiple sources
    github_clearbit_match: int  # GitHub handle matches across sources
    email_consistency_score: float  # Consistency of email data across APIs
    identity_cross_validation_score: float  # Cross-API identity validation

    # Version tracking
    commercial_apis_version: str = "3.0.0"


class EnhancedFeatureEngineer(AdvancedFeatureEngineer):
    """
    Enhanced feature engineering combining OSINT + Commercial APIs.

    Usage:
        # First collect all data
        osint_data = run_osint_enrichment(email)
        commercial_data = run_commercial_enrichment(email)

        # Combine and engineer features
        engineer = EnhancedFeatureEngineer(osint_data, commercial_data)
        features = engineer.generate_all_features()
    """

    FEATURE_VERSION = "3.0.0"

    def __init__(self, osint_data: Dict[str, Any], commercial_data: Optional[Dict[str, Any]] = None):
        """
        Initialize with both OSINT and commercial API data.

        Args:
            osint_data: Output from osint_email_enrichment.py
            commercial_data: Output from commercial_apis.py (optional)
        """
        super().__init__(osint_data)
        self.commercial = commercial_data or {}

    def _extract_hunter_features(self) -> Dict[str, Any]:
        """Extract features from Hunter.io data."""
        return {
            'hunter_deliverable': 1 if self.commercial.get('hunter_result') == 'deliverable' else 0,
            'hunter_score': self.commercial.get('hunter_score', 0),
            'hunter_disposable': 1 if self.commercial.get('hunter_disposable') else 0,
            'hunter_webmail': 1 if self.commercial.get('hunter_webmail') else 0,
            'hunter_accept_all': 1 if self.commercial.get('hunter_accept_all') else 0,
            'hunter_mx_records': 1 if self.commercial.get('hunter_mx_records') else 0,
            'hunter_smtp_check': 1 if self.commercial.get('hunter_smtp_check') else 0,
            'hunter_gibberish': 1 if self.commercial.get('hunter_gibberish') else 0,
            'hunter_block': 1 if self.commercial.get('hunter_block') else 0,
            'hunter_sources_count': self.commercial.get('hunter_sources_count', 0),
            'domain_emails_found': self.commercial.get('domain_emails_found', 0),
            'domain_has_pattern': 1 if self.commercial.get('domain_pattern') else 0,
            'domain_has_social': 1 if any([
                self.commercial.get('domain_twitter'),
                self.commercial.get('domain_linkedin'),
                self.commercial.get('domain_facebook')
            ]) else 0,
        }

    def _extract_emailrep_features(self) -> Dict[str, Any]:
        """Extract features from EmailRep.io data."""
        # Convert reputation string to score
        rep = self.commercial.get('emailrep_reputation', 'none')
        rep_score = {'high': 1.0, 'medium': 0.5, 'low': 0.2, 'none': 0.0}.get(rep, 0.0)

        # Calculate domain age
        domain_age = self.commercial.get('emailrep_days_since_domain_creation')

        return {
            'emailrep_reputation_score': rep_score,
            'emailrep_suspicious': 1 if self.commercial.get('emailrep_suspicious') else 0,
            'emailrep_references': self.commercial.get('emailrep_references', 0),
            'emailrep_blacklisted': 1 if self.commercial.get('emailrep_blacklisted') else 0,
            'emailrep_malicious_activity': 1 if self.commercial.get('emailrep_malicious_activity') else 0,
            'emailrep_malicious_recent': 1 if self.commercial.get('emailrep_malicious_activity_recent') else 0,
            'emailrep_credentials_leaked': 1 if self.commercial.get('emailrep_credentials_leaked') else 0,
            'emailrep_credentials_leaked_recent': 1 if self.commercial.get('emailrep_credentials_leaked_recent') else 0,
            'emailrep_spam': 1 if self.commercial.get('emailrep_spam') else 0,
            'emailrep_spoofable': 1 if self.commercial.get('emailrep_spoofable') else 0,
            'emailrep_domain_exists': 1 if self.commercial.get('emailrep_domain_exists') else 0,
            'emailrep_domain_age_days': domain_age,
            'emailrep_new_domain': 1 if self.commercial.get('emailrep_new_domain') else 0,
            'emailrep_valid_mx': 1 if self.commercial.get('emailrep_valid_mx') else 0,
            'emailrep_profiles_count': self.commercial.get('emailrep_profiles', 0),
        }

    def _extract_clearbit_features(self) -> Dict[str, Any]:
        """Extract features from Clearbit data."""
        # Person features
        person_found = 1 if self.commercial.get('clearbit_person_name') else 0
        has_title = 1 if self.commercial.get('clearbit_person_title') else 0
        has_role = 1 if self.commercial.get('clearbit_person_role') else 0

        # Seniority mapping
        seniority = self.commercial.get('clearbit_person_seniority') or ''
        seniority = seniority.lower() if seniority else ''
        seniority_level = 2 if 'executive' in seniority else (1 if 'manager' in seniority else 0)

        # Person score (0-1 based on data completeness)
        person_score = sum([
            person_found,
            has_title,
            has_role,
            1 if self.commercial.get('clearbit_person_linkedin') else 0,
            1 if self.commercial.get('clearbit_person_location') else 0,
        ]) / 5.0

        # Company features
        company_found = 1 if self.commercial.get('clearbit_company_name') else 0
        employees = self.commercial.get('clearbit_company_employees')

        # Company size score
        if employees:
            if employees < 10:
                size_score = 0.2
            elif employees < 50:
                size_score = 0.4
            elif employees < 200:
                size_score = 0.6
            elif employees < 1000:
                size_score = 0.8
            else:
                size_score = 1.0
        else:
            size_score = 0.0

        # Company age
        founded = self.commercial.get('clearbit_company_founded_year')
        company_age = (datetime.now().year - founded) if founded else 0.0

        # Tech stack
        tech_str = self.commercial.get('clearbit_company_tech', '')
        tech_count = len(tech_str.split(',')) if tech_str else 0

        # Funding
        raised = self.commercial.get('clearbit_company_raised')
        has_funding = 1 if raised and raised > 0 else 0

        # Company score
        company_score = sum([
            company_found,
            1 if employees and employees > 10 else 0,
            1 if founded and founded > 0 else 0,
            1 if tech_count > 0 else 0,
            1 if self.commercial.get('clearbit_company_linkedin') else 0,
        ]) / 5.0

        return {
            'clearbit_person_found': person_found,
            'clearbit_has_title': has_title,
            'clearbit_has_role': has_role,
            'clearbit_seniority_level': seniority_level,
            'clearbit_has_linkedin': 1 if self.commercial.get('clearbit_person_linkedin') else 0,
            'clearbit_has_github': 1 if self.commercial.get('clearbit_person_github') else 0,
            'clearbit_email_is_personal': 1 if self.commercial.get('clearbit_person_email_provider') else 0,
            'clearbit_person_score': round(person_score, 3),
            'clearbit_company_found': company_found,
            'clearbit_company_employees': employees,
            'clearbit_company_size_score': size_score,
            'clearbit_company_founded_year': founded,
            'clearbit_company_age_years': company_age,
            'clearbit_has_funding': has_funding,
            'clearbit_funding_amount': raised,
            'clearbit_has_tech_stack': 1 if tech_count > 0 else 0,
            'clearbit_tech_count': tech_count,
            'clearbit_alexa_rank': self.commercial.get('clearbit_company_alexa_global_rank'),
            'clearbit_has_social': 1 if any([
                self.commercial.get('clearbit_company_linkedin'),
                self.commercial.get('clearbit_company_twitter'),
                self.commercial.get('clearbit_company_facebook'),
            ]) else 0,
            'clearbit_company_score': round(company_score, 3),
        }

    def _calculate_cross_validation(self) -> Dict[str, Any]:
        """Cross-validate data across multiple sources."""
        # GitHub handle consistency
        github_from_osint = self.github.get('login', '').lower()
        github_from_clearbit = (self.commercial.get('clearbit_person_github') or '').lower()
        github_match = 1 if (github_from_osint and github_from_osint == github_from_clearbit) else 0

        # Email consistency (Hunter + EmailRep agreement)
        hunter_valid = self.commercial.get('hunter_result') == 'deliverable'
        emailrep_deliverable = self.commercial.get('emailrep_deliverable', False)
        email_consistency = 1.0 if hunter_valid == emailrep_deliverable else 0.5

        # Identity cross-validation score
        # Higher score = more sources agree
        identity_signals = [
            1 if self.github.get('login') else 0,
            1 if self.gravatar.get('profile_url') else 0,
            1 if self.commercial.get('clearbit_person_name') else 0,
            1 if self.commercial.get('hunter_sources_count', 0) > 0 else 0,
            1 if self.commercial.get('emailrep_profiles', 0) > 0 else 0,
        ]
        identity_score = sum(identity_signals) / len(identity_signals)

        return {
            'github_clearbit_match': github_match,
            'email_consistency_score': email_consistency,
            'identity_cross_validation_score': round(identity_score, 3),
        }

    def generate_all_features(self) -> EnhancedMLFeatures:
        """
        Generate all 118+ features combining OSINT + Commercial APIs.

        Returns:
            EnhancedMLFeatures dataclass with all features
        """
        # First get base 78 features from parent class
        base_features_dict = super().generate_features()
        base_dict = asdict(base_features_dict)

        # Extract commercial API features
        hunter_features = self._extract_hunter_features()
        emailrep_features = self._extract_emailrep_features()
        clearbit_features = self._extract_clearbit_features()
        cross_validation = self._calculate_cross_validation()

        # Combine all features
        all_features = {
            **base_dict,
            **hunter_features,
            **emailrep_features,
            **clearbit_features,
            **cross_validation,
            'commercial_apis_version': self.FEATURE_VERSION,
            'feature_version': self.FEATURE_VERSION,  # Override parent version
        }

        return EnhancedMLFeatures(**all_features)

    def to_ml_ready(self) -> Dict[str, Any]:
        """
        Convert to ML-ready format (numerical + categorical separated).

        Returns:
            Dictionary with 'numerical_features', 'categorical_features', 'metadata'
        """
        features = self.generate_all_features()
        features_dict = asdict(features)

        # Categorical fields
        categorical_fields = {
            'account_age_category', 'email_structure_type', 'domain_tld',
            'email_provider_type', 'location_country', 'profile_completeness',
            'account_maturity'
        }

        # Metadata fields
        metadata_fields = {
            'enrichment_timestamp', 'feature_version', 'commercial_apis_version'
        }

        # Split features
        numerical = {}
        categorical = {}
        metadata = {}

        for key, value in features_dict.items():
            if key in metadata_fields:
                metadata[key] = value
            elif key in categorical_fields:
                categorical[key] = value
            elif value is None:
                numerical[key] = None  # Keep None for missing values
            else:
                numerical[key] = value

        return {
            'numerical_features': numerical,
            'categorical_features': categorical,
            'metadata': metadata,
        }


def main():
    """Test enhanced feature engineering."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python enhanced_feature_engineering.py <osint_file.json> [commercial_file.json]")
        sys.exit(1)

    # Load OSINT data
    with open(sys.argv[1], 'r') as f:
        osint_data = json.load(f)

    # Load commercial data (optional)
    commercial_data = None
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            commercial_data = json.load(f)

    # Generate features
    engineer = EnhancedFeatureEngineer(osint_data, commercial_data)
    features = engineer.generate_all_features()

    # Print summary
    print(f"\n🎯 Enhanced Feature Generation v{EnhancedFeatureEngineer.FEATURE_VERSION}")
    print(f"   Total features: {len(asdict(features))}")
    print(f"\n📊 Key Scores:")
    print(f"   Overall Trust: {features.overall_trust_score:.3f}")
    print(f"   Identity: {features.identity_strength_score:.3f}")
    print(f"   Security Risk: {features.security_risk_score:.3f}")

    if commercial_data:
        print(f"\n💼 Commercial API Features:")
        print(f"   Hunter Score: {features.hunter_score}/100")
        print(f"   EmailRep Reputation: {features.emailrep_reputation_score:.2f}")
        print(f"   Clearbit Person: {features.clearbit_person_score:.2f}")
        print(f"   Clearbit Company: {features.clearbit_company_score:.2f}")

    # Save to file
    ml_ready = engineer.to_ml_ready()
    email = osint_data.get('validation', {}).get('email', 'unknown')
    output_file = f"enhanced_features_{email.replace('@', '_at_')}.json"

    with open(output_file, 'w') as f:
        json.dump({
            'all_features': asdict(features),
            'ml_ready': ml_ready,
            'feature_count': len(asdict(features)),
            'version': EnhancedFeatureEngineer.FEATURE_VERSION
        }, f, indent=2, default=str)

    print(f"\n✅ Features saved to: {output_file}")


if __name__ == "__main__":
    main()
