from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Customer, Debt, Payment
from .forms import DebtForm, PaymentForm

# --- 1. لوحة التحكم الرئيسية (البحث والعرض) ---

def dashboard(request):
    """عرض قائمة العملاء مع ميزة البحث وإجمالي الديون المستحقة"""
    query = request.GET.get('search', '')  # الحصول على قيمة البحث من الرابط
    
    if query:
        # البحث في الاسم أو رقم الهاتف باستخدام Q objects
        customer_list = Customer.objects.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        ).order_by('-created_at')
    else:
        # عرض كل العملاء إذا لم يوجد بحث
        customer_list = Customer.objects.all().order_by('-created_at')

    # حساب إجمالي الديون بناءً على القائمة الحالية (سواء بحث أو الكل)
    total_market_debt = sum(c.total_balance for c in customer_list)
    
    # إعداد نظام الصفحات (10 عملاء لكل صفحة)
    paginator = Paginator(customer_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_market_debt': total_market_debt,
        'query': query
    }
    return render(request, 'debts/dashboard.html', context)


# --- 2. تفاصيل العميل والعمليات الممالية ---

def customer_detail(request, pk):
    """عرض كشف حساب تفصيلي للعميل (مشتريات ومدفوعات)"""
    customer = get_object_or_404(Customer, pk=pk)
    debts = customer.debts.all().order_by('-date')
    payments = customer.payments.all().order_by('-date')
    
    context = {
        'customer': customer,
        'debts': debts,
        'payments': payments,
    }
    return render(request, 'debts/customer_detail.html', context)


def add_debt(request, pk):
    """إضافة دين جديد (عملية سحب أو شراء)"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.customer = customer
            debt.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = DebtForm()
    return render(request, 'debts/add_debt.html', {'form': form, 'customer': customer})


def add_payment(request, pk):
    """إضافة مبلغ مدفوع (عملية سداد أو قبض)"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer
            payment.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = PaymentForm()
    return render(request, 'debts/add_payment.html', {'form': form, 'customer': customer})


# --- 3. الصفحات التعريفية ---

def about(request):
    """تعريف بالنظام والمبرمج"""
    return render(request, 'debts/about.html')


def contact(request):
    """معلومات التواصل والدعم الفني"""
    return render(request, 'debts/contact.html')