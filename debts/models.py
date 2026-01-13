from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User # استيراد نظام المستخدمين الافتراضي

class Customer(models.Model):
    # ربط العميل بالمستخدم الذي أنشأه
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم صاحب الحساب")
    name = models.CharField(max_length=200, verbose_name="اسم العميل")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name

    @property
    def total_balance(self):
        debts = self.debts.aggregate(Sum('amount'))['amount__sum'] or 0
        payments = self.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        return debts - payments

class Debt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='debts', verbose_name="العميل")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مبلغ الدين")
    description = models.CharField(max_length=255, verbose_name="بيان الدين (بضاعة/خدمة)")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ الدين")

    class Meta:
        verbose_name = "دين"
        verbose_name_plural = "الديون"

class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments', verbose_name="العميل")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المدفوع")
    date = models.DateField(auto_now_add=True, verbose_name="تاريخ الدفع")

    class Meta:
        verbose_name = "عملية دفع"
        verbose_name_plural = "المدفوعات"