import os
import requests
from datetime import datetime, timedelta

class SearchEngine:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY', '').strip().strip('"').strip("'")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")
        
        self.base_url = "https://google.serper.dev/search"
    
    def search_ai_topics(self):
        """البحث عن أحدث مواضيع AI و NLP و LLMs"""
        
        queries = [
            "new NLP models",
            "LLMs breakthrough",
            "AI Agents updates",
            "tokens",
            "transformer models",
            "large language models",
            "embeddings",
            "fine tuning LLMs",
            "generative AI news"
        ]
        
        all_results = []
        
        for query in queries:
            try:
                response = requests.post(
                    self.base_url,
                    headers={
                        'X-API-KEY': self.api_key,
                        'Content-Type': 'application/json'
                    },
                    json={
                        'q': query,
                        'num': 5,
                        'gl': 'us',
                        'hl': 'en'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'organic' in data:
                        for result in data['organic']:
                            all_results.append({
                                'title': result.get('title', ''),
                                'snippet': result.get('snippet', ''),
                                'link': result.get('link', ''),
                                'source': result.get('source', '')
                            })
            
            except Exception as e:
                print(f"Error searching for {query}: {e}")
                continue
        
        return all_results
    
    def filter_quality_sources(self, results):
        """تصفية المصادر الموثوقة فقط"""
        
        trusted_domains = [
            'arxiv.org',
            'github.com',
            'openai.com',
            'anthropic.com',
            'google.com',
            'microsoft.com',
            'research.',
            'papers.',
            'blog.',
            'techcrunch.com',
            'theverge.com',
            'venturebeat.com',
            'mit.edu',
            'stanford.edu'
        ]
        
        filtered = []
        
        for result in results:
            link = result.get('link', '').lower()
            
            # التحقق من المصدر الموثوق
            is_trusted = any(domain in link for domain in trusted_domains)
            
            # التحقق من وجود محتوى تقني
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            tech_keywords = ['ai', 'model', 'llm', 'nlp', 'machine learning', 
                           'neural', 'research', 'algorithm', 'data', 'training']
            
            has_tech_content = any(keyword in title or keyword in snippet 
                                  for keyword in tech_keywords)
            
            if is_trusted and has_tech_content:
                filtered.append(result)
        
        return filtered
    
    def get_best_topic(self):
        """البحث واختيار أفضل موضوع"""
        
        results = self.search_ai_topics()
        
        if not results:
            return None
        
        filtered = self.filter_quality_sources(results)
        
        if not filtered:
            return results[0] if results else None
        
        return filtered[0]
