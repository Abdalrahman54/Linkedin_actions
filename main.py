import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from agent.memory import Memory
from agent.search import SearchEngine
from agent.writer import ContentWriter

def send_email(post_content, topic_title):
    """إرسال البوست عبر البريد الإلكتروني"""
    
    sender_email = os.getenv('SENDER_EMAIL', '').strip().strip('"').strip("'")
    sender_password = os.getenv('SENDER_PASSWORD', '').strip().strip('"').strip("'")
    receiver_email = os.getenv('RECEIVER_EMAIL', '').strip().strip('"').strip("'")
    
    if not all([sender_email, sender_password, receiver_email]):
        print("Email credentials not configured")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"LinkedIn Post: {topic_title}"
        
        body = f"""🔥 بوست LinkedIn الجديد جاهز للنشر:

{post_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 الملخص (للذاكرة فقط):
{topic_title}

🤖 تم الإنشاء بواسطة AI LinkedIn Agent
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # استخدام Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print("✓ Email sent successfully")
        return True
    
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False

def main():
    """الدالة الرئيسية للنظام"""
    
    print("=" * 60)
    print("AI LinkedIn Agent - Starting")
    print("=" * 60)
    
    try:
        # 1. تهيئة الذاكرة
        print("\n[1/7] Initializing memory...")
        memory = Memory()
        
        # 2. قراءة المرجع الأسلوبي
        print("[2/7] Loading style references...")
        style_refs = memory.get_style_references()
        print(f"      Found {len(style_refs)} reference post(s)")
        
        # 3. البحث عن موضوع جديد
        print("[3/7] Searching for new AI topics...")
        search_engine = SearchEngine()
        
        # جلب كل المواضيع مرة واحدة
        all_topics = search_engine.search_ai_topics()
        filtered_topics = search_engine.filter_quality_sources(all_topics)
        
        # لو مافيش مواضيع
        if not filtered_topics:
            filtered_topics = all_topics
        
        if not filtered_topics:
            print("✗ No topics found from search")
            sys.exit(1)
        
        print(f"      Found {len(filtered_topics)} topics")
        
        # البحث عن موضوع فريد
        selected_topic = None
        
        for i, topic in enumerate(filtered_topics):
            print(f"      Checking topic {i+1}/{len(filtered_topics)}")
            
            topic_title = topic.get('title', '')
            topic_snippet = topic.get('snippet', '')
            
            # التحقق من عدم التكرار
            is_used = memory.is_topic_used(topic_title, topic_snippet)
            
            if not is_used:
                selected_topic = topic
                print(f"      ✓ Found unique topic: {topic_title[:60]}...")
                break
            else:
                print(f"      ✗ Already used: {topic_title[:40]}...")
        
        if not selected_topic:
            print("\n✗ All topics were already used")
            sys.exit(1)
        
        # 4. توليد المحتوى
        print("[4/7] Generating LinkedIn post...")
        writer = ContentWriter()
        
        post_content = writer.generate_post(
            topic_title=selected_topic['title'],
            topic_snippet=selected_topic['snippet'],
            source_link=selected_topic['link'],
            style_refs=style_refs
        )
        
        if not post_content:
            print("✗ Failed to generate post")
            sys.exit(1)
        
        print("      ✓ Post generated successfully")
        
        # 6. توليد الملخص
        print("[5/7] Generating summary...")
        summary = writer.generate_summary(post_content, selected_topic['title'])
        print(f"      Summary: {summary[:50]}...")
        
        # 7. حفظ في الذاكرة
        print("[6/7] Saving to memory...")
        memory.add_entry(selected_topic['title'], summary)
        print("      ✓ Saved successfully")
        
        # 8. إرسال البريد الإلكتروني
        print("[7/7] Sending email...")
        email_sent = send_email(post_content, selected_topic['title'])
        
        # عرض النتيجة النهائية
        print("\n" + "=" * 60)
        print("FINAL POST")
        print("=" * 60)
        print(post_content)
        print("=" * 60)
        
        if email_sent:
            print("\n✓ Agent completed successfully")
        else:
            print("\n⚠ Agent completed but email sending failed")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
