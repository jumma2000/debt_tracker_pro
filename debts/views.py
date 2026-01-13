from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .models import Customer, Debt, Payment
from .forms import DebtForm, PaymentForm

# --- 1. لوحة التحكم الرئيسية ---
@login_required
def dashboard(request):
    query = request.GET.get('search', '')
    
    # جلب العملاء التابعين للمستخدم الحالي فقط لضمان الخصوصية
    customers = Customer.objects.filter(user=request.user)
    
    # تصفية البحث إذا وجد
    if query:
        customers = customers.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
    
    # حساب إجمالي الديون المستحقة في السوق لهذا المستخدم فقط
    # تم تغيير الاسم لـ total_market_debt ليطابق كود القالب (Template) الخاص بك
    total_market_debt = sum(customer.total_balance for customer in customers)
    
    context = {
        'page_obj': customers,  # استخدام page_obj ليتماشى مع حلقة for في القالب
        'total_market_debt': total_market_debt,
        'query': query,
    }
    return render(request, 'debts/dashboard.html', context)

# --- 2. تفاصيل العميل وكشف الحساب ---
@login_required
def customer_detail(request, pk):
    # التأكد من أن العميل يخص المستخدم المسجل حالياً لزيادة الأمان
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    debts = customer.debts.all().order_by('-date')
    payments = customer.payments.all().order_by('-date')
    
    context = {
        'customer': customer,
        'debts': debts,
        'payments': payments,
    }
    # يجب أن يكون القالب هنا customer_detail.html وليس dashboard.html
    return render(request, 'debts/customer_detail.html', context)

# --- 3. إضافة العمليات المالية ---
@login_required
def add_debt(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
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

@login_required
def add_payment(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
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

# --- 4. الصفحات التعريفية ---
def about(request):
    return render(request, 'debts/about.html')

def contact(request):
    return render(request, 'debts/contact.html')