from django.contrib import admin
from .models import Customer, Debt, Payment

# --- 1. إعدادات لوحة الإدارة العامة ---
admin.site.site_header = "نظام إدارة ديون العملاء"
admin.site.site_title = "لوحة التحكم"
admin.site.index_title = "مرحباً بك في نظام الإدارة"

# --- 2. الجداول المتداخلة (Inlines) ---
class DebtInline(admin.TabularInline):
    model = Debt
    extra = 1
    fields = ('amount', 'description') 

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    fields = ('amount',)

# --- 3. تخصيص واجهة العميل ---
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # تم إزالة الأقواس من total_balance لحل مشكلة 'Decimal object is not callable'
    list_display = ('name', 'phone', 'user', 'display_total_balance', 'created_at')
    
    # إظهار الحقول المطلوبة في صفحة التعديل
    fields = ('user', 'name', 'phone', 'address') 
    
    search_fields = ('name', 'phone')
    list_filter = ('user', 'created_at')
    inlines = [DebtInline, PaymentInline]

    # التصحيح هنا: استخدام obj.total_balance بدون أقواس ()
    def display_total_balance(self, obj):
        return f"{obj.total_balance} د.ل"
    display_total_balance.short_description = 'الرصيد المتبقي'

    # ربط العميل بالمستخدم الحالي تلقائياً عند الإضافة
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    # خصوصية البيانات
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

# --- 4. تخصيص واجهات الديون والمدفوعات ---
@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'description', 'date')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(customer__user=request.user)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'date')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(customer__user=request.user)
    
    