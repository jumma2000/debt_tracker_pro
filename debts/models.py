import re
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# استيراد الدالة المساعدة من ملف utils
try:
    from .utils import get_whatsapp_link
except ImportError:
    # دالة احتياطية في حال لم يتم إنشاء ملف utils.py بعد
    def get_whatsapp_link(phone, message):
        import urllib.parse
        clean_phone = phone.lstrip('0')
        return f"https://api.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(message)}"

# --- 1. دالة التحقق من رقم الهاتف ---
def validate_phone(value):
    """التأكد من أن الرقم يتبع التنسيق الليبي الدولي (00218)"""
    if not re.match(r'^00218\d{9}$', value):
        raise ValidationError("خطأ: يجب أن يبدأ الرقم بـ 00218 ويتبعه 9 أرقام.")

# --- 2. موديل العملاء ---
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم صاحب الحساب")
    name = models.CharField(max_length=200, verbose_name="اسم العميل")
    phone = models.CharField(
        max_length=20, 
        validators=[validate_phone], 
        verbose_name="رقم الهاتف (00218...)"
    )
    address = models.TextField(blank=True, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    debt_duration_limit = models.IntegerField(default=30, verbose_name="مدة الدين المسموحة (أيام)")

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name

    @property
    def total_balance(self):
        """حساب الرصيد الصافي للعميل"""
        debts = self.debts.aggregate(Sum('amount'))['amount__sum'] or 0
        payments = self.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        return debts - payments

# --- 3. موديل الديون ---
class Debt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='debts', verbose_name="العميل")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ الدين")
    description = models.CharField(max_length=255, verbose_name="بيان الدين")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ الدين")

    class Meta:
        verbose_name = "دين"
        verbose_name_plural = "الديون"

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"

# --- 4. موديل المدفوعات ---
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments', verbose_name="العميل")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المدفوع")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ الدفع")

    class Meta:
        verbose_name = "عملية دفع"
        verbose_name_plural = "المدفوعات"

# --- 5. نظام التنبيهات (Signals) ---
@receiver(post_save, sender=Debt)
def notify_customer_on_new_debt(sender, instance, created, **kwargs):
    """إرسال تنبيه واتساب آلي عند إضافة دين جديد"""
    if created:
        customer = instance.customer
        message = (
            f"مرحباً سيد {customer.name}،\n"
            f"تم تسجيل دين جديد عليك بقيمة: {instance.amount} د.ل\n"
            f"البيان: {instance.description}\n"
            f"إجمالي رصيدك الحالي لدينا هو: {customer.total_balance} د.ل.\n"
            f"يرجى العلم أن مدة السداد المتفق عليها هي {customer.debt_duration_limit} يوماً.\n"
            f"شكراً لتعاملكم معنا."
        )
        
        whatsapp_url = get_whatsapp_link(customer.phone, message)
        
        # طباعة الرابط في الـ Terminal للمبرمج للمتابعة
        print("\n" + "*"*60)
        print(f"إشعار: تم تجهيز رابط واتساب للعميل {customer.name}")
        print(f"الرابط: {whatsapp_url}")
        print("*"*60 + "\n")