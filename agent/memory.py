import json
import os

class Memory:
    def __init__(self, filepath='data/used_topics.txt'):
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def load_all(self):
        """قراءة كل البوستات السابقة"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def get_style_references(self):
        """استخراج أول عنصرين فقط للمرجع الأسلوبي"""
        all_posts = self.load_all()
        return all_posts[:2] if len(all_posts) >= 2 else all_posts
    
    def is_topic_used(self, new_topic, new_summary):
        """التحقق من عدم تكرار الموضوع"""
        all_posts = self.load_all()
        
        new_topic_lower = new_topic.lower()
        new_summary_lower = new_summary.lower()
        
        for post in all_posts:
            existing_title = post.get('title', '').lower()
            existing_summary = post.get('summary', '').lower()
            
            # مقارنة دقيقة للعناوين والملخصات
            if new_topic_lower in existing_title or existing_title in new_topic_lower:
                return True
            if new_summary_lower in existing_summary or existing_summary in new_summary_lower:
                return True
            
            # مقارنة الكلمات المفتاحية
            new_words = set(new_topic_lower.split() + new_summary_lower.split())
            existing_words = set(existing_title.split() + existing_summary.split())
            
            # لو فيه تطابق أكتر من 60% في الكلمات المفتاحية
            common_words = new_words.intersection(existing_words)
            if len(common_words) > 0:
                similarity = len(common_words) / min(len(new_words), len(existing_words))
                if similarity > 0.6:
                    return True
        
        return False
    
    def add_entry(self, title, summary):
        """إضافة بوست جديد للذاكرة"""
        all_posts = self.load_all()
        
        new_entry = {
            'post_number': len(all_posts) + 1,
            'title': title,
            'summary': summary
        }
        
        all_posts.append(new_entry)
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)
        
        return new_entry
    
    def get_all_topics(self):
        """استخراج كل العناوين والملخصات السابقة"""
        all_posts = self.load_all()
        topics = []
        for post in all_posts:
            topics.append(f"{post.get('title', '')} - {post.get('summary', '')}")
        return topics