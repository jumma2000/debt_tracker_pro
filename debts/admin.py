from django.contrib import admin
from .models import Customer, Debt, Payment

# --- 1. إعدادات الإضافة السريعة داخل صفحة العميل ---

class DebtInline(admin.TabularInline):
    """إتاحة إضافة الديون مباشرة من صفحة العميل"""
    model = Debt
    extra = 1  # عدد الأسطر الفارغة الجاهزة للإدخال
    # استبعاد 'date' لأنها حقل تلقائي (auto_now_add) لمنع خطأ FieldError
    fields = ('amount', 'description') 

class PaymentInline(admin.TabularInline):
    """إتاحة إضافة المدفوعات مباشرة من صفحة العميل"""
    model = Payment
    extra = 1
    # استبعاد 'date' لتجنب أخطاء حقول القراءة فقط
    fields = ('amount',)

# --- 2. تخصيص واجهة العميل الرئيسية ---

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # الأعمدة الظاهرة في قائمة العملاء
    list_display = ('name', 'phone', 'display_total_balance', 'created_at')
    
    # خيارات البحث والفلاتر
    search_fields = ('name', 'phone')
    list_filter = ('created_at',)
    
    # دمج جداول العمليات داخل صفحة العميل (Inlines)
    inlines = [DebtInline, PaymentInline]

    # عرض الرصيد بتنسيق جميل في جدول الإدارة
    def display_total_balance(self, obj):
        return f"{obj.total_balance} د.ل"
    
    display_total_balance.short_description = 'الرصيد المتبقي'

# --- 3. تخصيص واجهات الديون والمدفوعات (للمراجعة المنفصلة) ---

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'description', 'date')
    list_filter = ('date', 'customer')
    # جعل التاريخ للقراءة فقط لأنه تلقائي
    readonly_fields = ('date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'date')
    list_filter = ('date', 'customer')
    readonly_fields = ('date',)