import os
import requests

class ContentWriter:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', '').strip().strip('"').strip("'")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        # استخدام موديل Gemini الصحيح
        self.model = "google/gemini-3-flash-preview"
    
    def create_prompt(self, topic_title, topic_snippet, source_link, style_refs):
        """بناء البرومبت الصارم"""
        
        # استخراج ملخصات البوستات السابقة للمرجع الأسلوبي
        post_summary_1 = ""
        post_summary_2 = ""
        
        if len(style_refs) >= 1:
            post_summary_1 = style_refs[0].get('summary', '')
        if len(style_refs) >= 2:
            post_summary_2 = style_refs[1].get('summary', '')
        
        prompt = f"""You have one task only
Write a LinkedIn post

Rules you must follow strictly
Write only in Egyptian Arabic
Mix technical English terms naturally with Arabic text
Match exactly the users thinking style
No punctuation marks at all
No dots
No commas
No semicolons
No brackets
No parentheses
No emojis
No explanations
No extra text
No formatting
No marketing tone

Content rules
Write about the provided topic only
Focus on technical details and new technologies
Go deeper into how things work
Use English technical terms like: model architecture, training, inference, parameters, tokens, embeddings, fine-tuning, etc
Explain the technical innovation or breakthrough
Make it feel like an engineer talking to engineers
Do not repeat any idea from previous posts
The post must feel human confident and practical
Write 4-5 short paragraphs with technical depth

Post structure
Main content with technical details
Empty line
Source link
Empty line
Hashtags line only

Hashtags
#AI #NLP #LLMs #MachineLearning

Previous posts context
Use only the following summaries to understand the users thinking style
Do not mention them

{post_summary_1}
{post_summary_2}

Topic
{topic_title}
{topic_snippet}

Source link
{source_link}

Output
Return only the final post text
Nothing else"""

        return prompt
    
    def generate_post(self, topic_title, topic_snippet, source_link, style_refs):
        """توليد البوست النهائي"""
        
        prompt = self.create_prompt(topic_title, topic_snippet, source_link, style_refs)
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 800
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                post_content = data['choices'][0]['message']['content'].strip()
                return post_content
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            print(f"Error generating post: {e}")
            return None
    
    def generate_summary(self, post_content, topic_title):
        """توليد ملخص قصير للبوست"""
        
        summary_prompt = f"""أنت محلل محتوى
اكتب ملخص قصير جدا من سطر واحد يوضح الزاوية الأساسية للبوست ده
الملخص لازم يكون:
- بالعربي
- واضح ومحدد
- يوضح الفكرة الرئيسية فقط

البوست:
{post_content}

الملخص (سطر واحد فقط):"""

        try:
            response = requests.post(
                self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [
                        {
                            'role': 'user',
                            'content': summary_prompt
                        }
                    ],
                    'temperature': 0.5,
                    'max_tokens': 100
                },
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data['choices'][0]['message']['content'].strip()
                return summary
            else:
                # لو فشل توليد الملخص، نستخدم العنوان
                return topic_title
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return topic_title
