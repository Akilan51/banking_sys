from django import forms
from .models import Beneficiary

class BeneficiaryForm(forms.ModelForm):

    class Meta:

        model = Beneficiary

        fields = [
            "beneficiary_name",
            "beneficiary_account",
            "beneficiary_ifsc"
        ]