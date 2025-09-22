#!/usr/bin/env python3
"""
Real AI Visibility Checker - Works without Airtop
Uses direct API calls to get real data
"""

import requests
import json
import time
import random
from datetime import datetime
from typing import List, Dict
import os

class RealVisibilityChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def check_perplexity(self, query: str) -> Dict:
        """Check Perplexity for real responses"""
        try:
            # Perplexity API endpoint (public)
            url = "https://www.perplexity.ai/api/chat"
            
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            response = self.session.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'response': data.get('choices', [{}])[0].get('message', {}).get('content', ''),
                    'sources': data.get('choices', [{}])[0].get('message', {}).get('sources', []),
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response_time': response.elapsed.total_seconds()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': 0
            }
    
    def check_web_search(self, query: str) -> Dict:
        """Use a web search API to get real results"""
        try:
            # Using a free search API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'response': data.get('Abstract', ''),
                    'sources': [data.get('AbstractURL', '')] if data.get('AbstractURL') else [],
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response_time': response.elapsed.total_seconds()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': 0
            }
    
    def analyze_brand_mentions(self, text: str, brand_name: str, competitors: List[str]) -> Dict:
        """Analyze real text for brand mentions"""
        import re
        
        result = {
            'brand_mentioned': False,
            'mention_type': 'none',
            'competitors_mentioned': [],
            'sentiment': 'neutral'
        }
        
        # Check for brand mentions
        brand_pattern = re.compile(r'\b' + re.escape(brand_name) + r'\b', re.IGNORECASE)
        if brand_pattern.search(text):
            result['brand_mentioned'] = True
            
            # Determine sentiment
            text_lower = text.lower()
            positive_words = ['best', 'top', 'leading', 'excellent', 'recommended', 'premier', 'outstanding']
            negative_words = ['worst', 'bad', 'poor', 'avoid', 'problem', 'issue', 'terrible']
            
            if any(word in text_lower for word in positive_words):
                result['sentiment'] = 'positive'
                result['mention_type'] = 'positive'
            elif any(word in text_lower for word in negative_words):
                result['sentiment'] = 'negative'
                result['mention_type'] = 'negative'
            else:
                result['mention_type'] = 'mentioned'
        
        # Check for competitor mentions
        for competitor in competitors:
            if re.search(r'\b' + re.escape(competitor) + r'\b', text, re.IGNORECASE):
                result['competitors_mentioned'].append(competitor)
        
        return result
    
    def run_real_check(self, brand_name: str, competitors: List[str], queries: List[str]) -> Dict:
        """Run real visibility check"""
        print(f"🔍 Running REAL visibility check for: {brand_name}")
        print(f"🏢 Competitors: {', '.join(competitors)}")
        print(f"❓ Queries: {len(queries)}")
        
        results = []
        
        for query in queries:
            print(f"\n🔍 Checking: {query}")
            
            # Try Perplexity first
            perplexity_result = self.check_perplexity(query)
            
            if perplexity_result['success']:
                print(f"✅ Perplexity: Got real response ({perplexity_result['response_time']:.2f}s)")
                
                # Analyze the real response
                analysis = self.analyze_brand_mentions(
                    perplexity_result['response'], 
                    brand_name, 
                    competitors
                )
                
                results.append({
                    'platform': 'Perplexity',
                    'query': query,
                    'response': perplexity_result['response'][:500] + "..." if len(perplexity_result['response']) > 500 else perplexity_result['response'],
                    'brand_mentioned': analysis['brand_mentioned'],
                    'mention_type': analysis['mention_type'],
                    'competitors_mentioned': analysis['competitors_mentioned'],
                    'sentiment': analysis['sentiment'],
                    'sources': perplexity_result['sources'],
                    'response_time': perplexity_result['response_time'],
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            else:
                print(f"❌ Perplexity failed: {perplexity_result['error']}")
                
                # Fallback to web search
                web_result = self.check_web_search(query)
                
                if web_result['success']:
                    print(f"✅ Web Search: Got real response ({web_result['response_time']:.2f}s)")
                    
                    analysis = self.analyze_brand_mentions(
                        web_result['response'], 
                        brand_name, 
                        competitors
                    )
                    
                    results.append({
                        'platform': 'Web Search',
                        'query': query,
                        'response': web_result['response'][:500] + "..." if len(web_result['response']) > 500 else web_result['response'],
                        'brand_mentioned': analysis['brand_mentioned'],
                        'mention_type': analysis['mention_type'],
                        'competitors_mentioned': analysis['competitors_mentioned'],
                        'sentiment': analysis['sentiment'],
                        'sources': web_result['sources'],
                        'response_time': web_result['response_time'],
                        'success': True,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    print(f"❌ Web Search failed: {web_result['error']}")
            
            # Rate limiting
            time.sleep(2)
        
        # Generate summary
        successful_results = [r for r in results if r['success']]
        brand_mentions = len([r for r in successful_results if r['brand_mentioned']])
        
        summary = {
            'total_queries': len(queries),
            'successful_queries': len(successful_results),
            'brand_mentions': brand_mentions,
            'mention_rate': brand_mentions / len(successful_results) if successful_results else 0,
            'average_response_time': sum(r['response_time'] for r in successful_results) / len(successful_results) if successful_results else 0
        }
        
        return {
            'success': True,
            'demo_mode': False,  # This is REAL data!
            'brand_monitored': brand_name,
            'competitors_tracked': competitors,
            'results': results,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Test the real visibility checker"""
    checker = RealVisibilityChecker()
    
    results = checker.run_real_check(
        brand_name="AIO Search",
        competitors=["Clearscope", "MarketMuse", "Surfer SEO"],
        queries=[
            "What are the best AI content optimization tools?",
            "AI tools for SEO content optimization",
            "Content optimization software for AI search engines"
        ]
    )
    
    print("\n" + "=" * 60)
    print("📊 REAL VISIBILITY RESULTS")
    print("=" * 60)
    
    if results['success']:
        print(f"✅ Brand: {results['brand_monitored']}")
        print(f"📈 Mention Rate: {results['summary']['mention_rate']:.1%}")
        print(f"⏱️ Avg Response Time: {results['summary']['average_response_time']:.2f}s")
        
        for result in results['results']:
            if result['success']:
                status = "✅" if result['brand_mentioned'] else "❌"
                print(f"\n{status} {result['platform']}: {result['query'][:50]}...")
                print(f"   📝 Brand Mentioned: {result['brand_mentioned']}")
                print(f"   🎭 Sentiment: {result['sentiment']}")
                print(f"   📚 Sources: {len(result['sources'])} found")
                print(f"   ⏱️ Response Time: {result['response_time']:.2f}s")
    else:
        print("❌ Check failed")

if __name__ == "__main__":
    main() 