from django import forms
from .models import Customer, Debt, Payment



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم العميل'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل رقم الهاتف'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'أدخل العنوان (اختياري)'}),
        }



class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'بيان العملية'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ المدفوع'}),
        }



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'أدخل المبلغ المدفوع (مثلاً: 100)',
                'step': '0.01'
            }),
        }
        labels = {
            'amount': 'المبلغ المستلم',
        }