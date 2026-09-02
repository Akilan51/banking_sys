from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "transaction_type",
        "amount",
        "status",
        "approved",
        "date"
    )

    list_filter = (
        "status",
        "approved"
    )

    search_fields = (
        "sender__account_number",
        "receiver__account_number"
    )