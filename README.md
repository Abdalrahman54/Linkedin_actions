# AI LinkedIn Agent

Agent ذكي لإنتاج محتوى LinkedIn تلقائيًا باللهجة المصرية

## المميزات

- توليد بوست يومي تلقائي عن NLP/LLMs
- محتوى باللهجة المصرية
- عدم تكرار المواضيع
- الحفاظ على أسلوب المستخدم
- تشغيل مجاني بالكامل عبر GitHub Actions

## البنية

```
ai_linkedin_agent/
│
├── data/
│   └── used_topics.txt          # ذاكرة النظام الوحيدة
│
├── agent/
│   ├── search.py                # البحث عن المواضيع
│   ├── writer.py                # كتابة المحتوى
│   └── memory.py                # إدارة الذاكرة
│
├── main.py                      # الملف الرئيسي
├── requirements.txt
└── .github/workflows/daily.yml  # التشغيل التلقائي
```

## الإعداد

### 1. Fork المشروع على GitHub

### 2. إضافة Secrets في GitHub

اذهب إلى Settings → Secrets and variables → Actions → New repository secret

أضف المتغيرات التالية:

- `SERPER_API_KEY`: مفتاح API من [serper.dev](https://serper.dev)
- `OPENROUTER_API_KEY`: مفتاح API من [openrouter.ai](https://openrouter.ai)
- `SENDER_EMAIL`: بريد Gmail الخاص بك
- `SENDER_PASSWORD`: App Password من Gmail ([كيفية إنشائه](https://support.google.com/accounts/answer/185833))
- `RECEIVER_EMAIL`: البريد الذي تريد استقبال البوستات عليه

### 3. تعديل ملف الذاكرة

افتح `data/used_topics.txt` وعدل البوستين المثاليين:

- البوست الأول والثاني يمثلان أسلوبك في الكتابة
- يجب أن تكون ملخصات حقيقية لبوستات كتبتها أنت
- النظام يستخدمهم كمرجع فقط لفهم أسلوبك

### 4. تفعيل GitHub Actions

- اذهب إلى تبويب Actions في الريبو
- اضغط "I understand my workflows, go ahead and enable them"

## التشغيل

النظام يعمل تلقائيًا كل يوم الساعة 5:30 مساءً بتوقيت القاهرة

للتشغيل اليدوي:
- Actions → Daily LinkedIn Agent → Run workflow

## آلية العمل

1. قراءة أول بوستين من الذاكرة كمرجع أسلوبي
2. البحث عن أحدث مواضيع AI/NLP/LLMs
3. التحقق من عدم تكرار الموضوع
4. توليد بوست بنفس أسلوب المستخدم
5. حفظ الموضوع في الذاكرة
6. إرسال البوست عبر Email

## قواعد الكتابة

- لهجة مصرية فقط
- بدون علامات ترقيم نهائيًا
- بدون emojis
- فقرات قصيرة
- أسلوب عملي ومباشر

## البنية النهائية للبوست

```
محتوى البوست

[لينك المصدر]

#AI #NLP #LLMs #MachineLearning
```

## التكلفة

**مجاني 100%**

- GitHub Actions: مجاني للريبوهات العامة
- Serper API: 2500 بحث مجاني شهريًا
- OpenRouter: أسعار رمزية جدًا ($0.000075 لكل 1K token)
- Gmail: مجاني

## الدعم الفني

لو عندك مشكلة، افتح Issue في الريبو
