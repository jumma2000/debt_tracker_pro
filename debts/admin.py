from django.contrib import admin
from .models import Customer, Debt, Payment

# --- 1. إعدادات لوحة الإدارة العامة ---
admin.site.site_header = "نظام إدارة ديون العملاء"
admin.site.site_title = "لوحة التحكم"
admin.site.index_title = "مرحباً بك في نظام الإدارة"

# --- 2. الجداول المتداخلة (Inlines) ---
class DebtInline(admin.TabularInline):
    """إتاحة إضافة الديون مباشرة من داخل صفحة العميل"""
    model = Debt
    extra = 1
    fields = ('amount', 'description') 

class PaymentInline(admin.TabularInline):
    """إتاحة إضافة المدفوعات مباشرة من داخل صفحة العميل"""
    model = Payment
    extra = 1
    fields = ('amount',)

# --- 3. تخصيص واجهة العميل الرئيسية (الأمان والخصوصية) ---
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # الأعمدة الظاهرة في قائمة العملاء
    list_display = ('name', 'phone', 'display_total_balance', 'created_at')
    # البحث والفلاتر
    search_fields = ('name', 'phone')
    list_filter = ('created_at',)
    # الجداول المتداخلة
    inlines = [DebtInline, PaymentInline]
    # إخفاء حقل المستخدم ليتم تعبئته تلقائياً
    exclude = ('user',)

    # تنسيق عرض الرصيد
    def display_total_balance(self, obj):
        return f"{obj.total_balance} د.ل"
    display_total_balance.short_description = 'الرصيد المتبقي'

    # أمان: حفظ العميل وربطه بالمستخدم المسجل حالياً تلقائياً
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    # خصوصية: تصفية البيانات ليرى كل مستخدم عملاءه فقط
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

# --- 4. تخصيص واجهات الديون والمدفوعات المنفصلة ---
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'description', 'date')
    list_filter = ('date', 'customer')
    readonly_fields = ('date',)

    # خصوصية: يرى المستخدم ديون عملائه فقط
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(customer__user=request.user)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'date')
    list_filter = ('date', 'customer')
    readonly_fields = ('date',)

    # خصوصية: يرى المستخدم مدفوعات عملائه فقط
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(customer__user=request.user)