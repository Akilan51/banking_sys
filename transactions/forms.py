from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(min_value=1)


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(min_value=1)


class TransferForm(forms.Form):
    account_number = forms.CharField(max_length=12)
    amount = forms.DecimalField(min_value=1)
    description = forms.CharField(required=False)