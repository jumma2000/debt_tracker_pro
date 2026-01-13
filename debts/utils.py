import urllib.parse

def get_whatsapp_link(phone, message):
    """توليد رابط واتساب جاهز للإرسال"""
    # تنظيف رقم الهاتف من الأصفار الزائدة في البداية إذا وجدت
    clean_phone = phone.lstrip('0') 
    encoded_message = urllib.parse.quote(message)
    # استخدام رابط api.whatsapp لتسهيل الفتح على المتصفح والهاتف
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"