#!/usr/bin/env python3
"""
Free Data Sources for Email Enrichment
100% gratis - No API keys required (or free tier available)

Features extracted: +50
- IP Intelligence (15 features)
- Advanced Email Pattern Analysis (20 features)
- Username Search across platforms (10 features)
- Google Search presence (5 features)

Version: 3.2.0
"""

import os
import re
import logging
import requests
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IPIntelligence:
    """
    IP Geolocation and Intelligence (FREE).

    Features extracted: +15
    - Country, city, region
    - ISP, connection type
    - Timezone, coordinates
    - VPN/Proxy detection

    API: ipapi.co (30,000 requests/month FREE)
    Alternative: ip-api.com (45/min FREE)
    """

    def __init__(self):
        self.base_url = "https://ipapi.co"

    def analyze_ip(self, ip_address: str) -> Dict[str, Any]:
        """
        Analyze IP address for geolocation and risk.

        Args:
            ip_address: IP address to analyze

        Returns:
            Dictionary with IP intelligence features
        """
        try:
            logger.info(f"[IP Intel] Analyzing IP: {ip_address}")

            url = f"{self.base_url}/{ip_address}/json/"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()

                return {
                    'ip_address': ip_address,
                    'ip_country': data.get('country_name'),
                    'ip_country_code': data.get('country_code'),
                    'ip_region': data.get('region'),
                    'ip_city': data.get('city'),
                    'ip_postal_code': data.get('postal'),
                    'ip_latitude': data.get('latitude'),
                    'ip_longitude': data.get('longitude'),
                    'ip_timezone': data.get('timezone'),
                    'ip_utc_offset': data.get('utc_offset'),
                    'ip_isp': data.get('org'),
                    'ip_asn': data.get('asn'),
                    'ip_connection_type': self._classify_connection(data.get('org', '')),
                    'ip_is_eu': data.get('in_eu', False),
                    'ip_continent': data.get('continent_code'),
                }
            else:
                logger.warning(f"[IP Intel] API returned {response.status_code}")
                return self._empty_response(ip_address)

        except Exception as e:
            logger.error(f"[IP Intel] Error: {e}")
            return self._empty_response(ip_address)

    def _classify_connection(self, org: str) -> str:
        """Classify connection type from organization name."""
        org_lower = org.lower()

        if any(x in org_lower for x in ['google', 'amazon', 'microsoft', 'digitalocean', 'linode']):
            return 'datacenter'
        elif any(x in org_lower for x in ['mobile', 'wireless', 'cellular']):
            return 'mobile'
        elif any(x in org_lower for x in ['vpn', 'proxy']):
            return 'vpn_proxy'
        else:
            return 'residential'

    def _empty_response(self, ip_address: str) -> Dict[str, Any]:
        """Return empty response when IP lookup fails."""
        return {
            'ip_address': ip_address,
            'ip_country': None,
            'ip_country_code': None,
            'ip_region': None,
            'ip_city': None,
            'ip_postal_code': None,
            'ip_latitude': None,
            'ip_longitude': None,
            'ip_timezone': None,
            'ip_utc_offset': None,
            'ip_isp': None,
            'ip_asn': None,
            'ip_connection_type': 'unknown',
            'ip_is_eu': False,
            'ip_continent': None,
        }


class EmailPatternAnalyzer:
    """
    Advanced Email Pattern Analysis (FREE - pure code).

    Features extracted: +20
    - Name extraction from email
    - Professional pattern detection
    - Randomness/entropy analysis
    - Common patterns (year, numbers, etc)
    """

    PROFESSIONAL_PATTERNS = [
        r'^[a-z]+\.[a-z]+@',           # john.doe@
        r'^[a-z]+_[a-z]+@',            # john_doe@
        r'^[a-z]\.[a-z]+@',            # j.doe@
        r'^[a-z]+\.[a-z]\.[a-z]+@',    # john.m.doe@
    ]

    RANDOM_PATTERNS = [
        r'^[a-z0-9]{10,}@',            # longrandomemail@
        r'^[0-9]+[a-z]+[0-9]+@',       # 123abc456@
        r'[a-z]{3}[0-9]{3,}',          # abc12345
    ]

    COMMON_NAMES = {
        'john', 'jane', 'test', 'admin', 'info', 'contact', 'support',
        'noreply', 'no-reply', 'postmaster', 'webmaster', 'hello', 'hi'
    }

    def analyze_email(self, email: str) -> Dict[str, Any]:
        """
        Analyze email structure and patterns.

        Args:
            email: Email address to analyze

        Returns:
            Dictionary with email pattern features
        """
        username, domain = email.split('@')
        username_lower = username.lower()

        # Name extraction
        name_parts = self._extract_names(username_lower)
        has_full_name = len(name_parts) >= 2

        # Pattern detection
        is_professional = self._is_professional_pattern(username_lower)
        is_random = self._is_random_pattern(username_lower)

        # Separators
        separators = self._detect_separators(username)

        # Numbers analysis
        numbers = re.findall(r'\d+', username)
        has_numbers = len(numbers) > 0
        numeric_ratio = sum(len(n) for n in numbers) / len(username) if username else 0

        # Year extraction
        year_match = re.search(r'(19|20)\d{2}', username)
        year_value = int(year_match.group()) if year_match else None
        age_from_year = datetime.now().year - year_value if year_value else None

        # Entropy (randomness)
        entropy = self._calculate_entropy(username_lower)

        # Common patterns
        is_role_account = username_lower in self.COMMON_NAMES

        return {
            'email_username': username,
            'email_username_length': len(username),
            'email_has_full_name': has_full_name,
            'email_has_first_name': len(name_parts) >= 1,
            'email_has_last_name': len(name_parts) >= 2,
            'email_name_parts_count': len(name_parts),
            'email_is_professional_pattern': is_professional,
            'email_is_random_pattern': is_random,
            'email_has_separator': len(separators) > 0,
            'email_separator_type': separators[0] if separators else None,
            'email_separator_count': len(separators),
            'email_has_numbers': has_numbers,
            'email_numeric_ratio': round(numeric_ratio, 3),
            'email_numbers_count': len(numbers),
            'email_has_year': year_value is not None,
            'email_year_value': year_value,
            'email_age_from_year': age_from_year,
            'email_entropy': round(entropy, 3),
            'email_is_role_account': is_role_account,
            'email_readability_score': self._calculate_readability(username_lower),
        }

    def _extract_names(self, username: str) -> List[str]:
        """Extract potential name parts from username."""
        # Split by common separators
        parts = re.split(r'[._\-]', username)
        # Remove numbers and short parts
        names = [p for p in parts if p.isalpha() and len(p) > 1]
        return names

    def _is_professional_pattern(self, username: str) -> bool:
        """Check if email follows professional naming pattern."""
        return any(re.match(pattern, username + '@') for pattern in self.PROFESSIONAL_PATTERNS)

    def _is_random_pattern(self, username: str) -> bool:
        """Check if email appears to be randomly generated."""
        return any(re.search(pattern, username + '@') for pattern in self.RANDOM_PATTERNS)

    def _detect_separators(self, username: str) -> List[str]:
        """Detect separators used in username."""
        separators = []
        if '.' in username:
            separators.append('dot')
        if '_' in username:
            separators.append('underscore')
        if '-' in username:
            separators.append('hyphen')
        return separators

    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy (randomness measure)."""
        if not text:
            return 0.0

        from collections import Counter
        import math

        counts = Counter(text)
        length = len(text)
        entropy = -sum((count/length) * math.log2(count/length) for count in counts.values())
        return entropy

    def _calculate_readability(self, username: str) -> float:
        """Calculate readability score (0-1, higher = more readable)."""
        # Factors that increase readability
        score = 0.5  # baseline

        # Has separators
        if any(sep in username for sep in ['.', '_', '-']):
            score += 0.2

        # Not too long
        if len(username) < 15:
            score += 0.1

        # Low numbers
        numeric_ratio = sum(c.isdigit() for c in username) / len(username) if username else 0
        if numeric_ratio < 0.3:
            score += 0.1

        # Pronounceable (has vowels)
        vowels = sum(c in 'aeiou' for c in username.lower())
        if vowels >= len(username) * 0.2:
            score += 0.1

        return min(score, 1.0)


class UsernameSearch:
    """
    Username search across public platforms (FREE).

    Features extracted: +10
    - Checks if username exists on major platforms
    - Uses public APIs and endpoints

    Platforms: Instagram, YouTube, TikTok, Pinterest, etc.
    """

    def __init__(self):
        self.platforms = {
            'instagram': 'https://www.instagram.com/{}/?__a=1',
            'youtube': 'https://www.youtube.com/@{}',
            'tiktok': 'https://www.tiktok.com/@{}',
            'pinterest': 'https://www.pinterest.com/{}/',
            'reddit': 'https://www.reddit.com/user/{}',
            'medium': 'https://medium.com/@{}',
            'spotify': 'https://open.spotify.com/user/{}',
            'twitch': 'https://www.twitch.tv/{}',
        }

    def search_username(self, email: str) -> Dict[str, Any]:
        """
        Search for username across platforms.

        Args:
            email: Email address (username extracted)

        Returns:
            Dictionary with platform presence
        """
        username = email.split('@')[0]

        logger.info(f"[Username Search] Checking platforms for: {username}")

        results = {
            'username_searched': username,
            'platforms_found_count': 0,
        }

        found_platforms = []

        for platform, url_template in self.platforms.items():
            try:
                url = url_template.format(username)
                response = requests.head(url, timeout=3, allow_redirects=True)

                exists = response.status_code == 200
                results[f'has_{platform}'] = exists

                if exists:
                    found_platforms.append(platform)

            except Exception as e:
                logger.debug(f"[Username Search] {platform} check failed: {e}")
                results[f'has_{platform}'] = False

        results['platforms_found_count'] = len(found_platforms)
        results['platforms_found'] = found_platforms

        return results


class GoogleSearchPresence:
    """
    Google Search presence check (FREE - scraping).

    Features extracted: +5
    - Number of results for email
    - Appears in LinkedIn, GitHub, etc.
    """

    def search_email(self, email: str) -> Dict[str, Any]:
        """
        Check Google search results for email.

        Note: This is basic scraping. For production, use Google Custom Search API.

        Args:
            email: Email address to search

        Returns:
            Dictionary with search presence features
        """
        logger.info(f"[Google Search] Searching for: {email}")

        try:
            # Simple check - in production use Google Custom Search API
            query = quote(f'"{email}"')
            url = f"https://www.google.com/search?q={query}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=5)
            content = response.text.lower()

            # Check for platform mentions
            has_linkedin_mention = 'linkedin.com' in content
            has_github_mention = 'github.com' in content
            has_twitter_mention = 'twitter.com' in content or 'x.com' in content

            # Rough estimate of results (not accurate without API)
            has_results = email.lower() in content

            return {
                'google_search_has_results': has_results,
                'google_linkedin_mention': has_linkedin_mention,
                'google_github_mention': has_github_mention,
                'google_twitter_mention': has_twitter_mention,
                'google_search_count': int(has_linkedin_mention) + int(has_github_mention) + int(has_twitter_mention),
            }

        except Exception as e:
            logger.error(f"[Google Search] Error: {e}")
            return {
                'google_search_has_results': False,
                'google_linkedin_mention': False,
                'google_github_mention': False,
                'google_twitter_mention': False,
                'google_search_count': 0,
            }


class FreeSourcesEnricher:
    """
    Main enricher combining all free sources.
    """

    def __init__(self, ip_address: Optional[str] = None):
        """
        Initialize free sources enricher.

        Args:
            ip_address: Optional IP address for geolocation
        """
        self.ip_address = ip_address
        self.ip_intel = IPIntelligence()
        self.email_analyzer = EmailPatternAnalyzer()
        self.username_search = UsernameSearch()
        self.google_search = GoogleSearchPresence()

    def enrich_email(self, email: str, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """
        Run all free enrichment sources.

        Args:
            email: Email address to enrich
            ip_address: Optional IP address for geolocation

        Returns:
            Dictionary with all free source features
        """
        logger.info(f"[FreeSources] Starting enrichment for: {email}")

        results = {
            'email': email,
            'enrichment_timestamp': datetime.now().isoformat(),
        }

        # IP Intelligence (if IP provided)
        if ip_address or self.ip_address:
            ip_to_check = ip_address or self.ip_address
            try:
                ip_data = self.ip_intel.analyze_ip(ip_to_check)
                results.update(ip_data)
            except Exception as e:
                logger.error(f"[FreeSources] IP Intel error: {e}")

        # Email Pattern Analysis
        try:
            email_patterns = self.email_analyzer.analyze_email(email)
            results.update(email_patterns)
        except Exception as e:
            logger.error(f"[FreeSources] Email analysis error: {e}")

        # Username Search
        try:
            username_data = self.username_search.search_username(email)
            results.update(username_data)
        except Exception as e:
            logger.error(f"[FreeSources] Username search error: {e}")

        # Google Search Presence
        try:
            google_data = self.google_search.search_email(email)
            results.update(google_data)
        except Exception as e:
            logger.error(f"[FreeSources] Google search error: {e}")

        logger.info(f"[FreeSources] Enrichment completed for: {email}")
        return results


def main():
    """CLI for testing."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python free_sources.py <email> [ip_address]")
        sys.exit(1)

    email = sys.argv[1]
    ip_address = sys.argv[2] if len(sys.argv) > 2 else None

    enricher = FreeSourcesEnricher(ip_address=ip_address)
    results = enricher.enrich_email(email)

    # Save results
    filename = f"free_sources_{email.replace('@', '_at_')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"FREE SOURCES ENRICHMENT RESULTS")
    print(f"{'='*60}\n")
    print(json.dumps(results, indent=2))
    print(f"\n{'='*60}")
    print(f"Results saved to: {filename}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
