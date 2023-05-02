from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
from apps.receipts.models import ReceiptImage, Vendor, Receipt, ReceiptItem


class AccountAdmin(UserAdmin):
    """
    Model for account admin.
    """
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ReceiptAdmin(admin.ModelAdmin):
    """
    Model for receipt admin.
    """
    readonly_fields = ('id',)


admin.site.register(Account, AccountAdmin)

admin.site.register(ReceiptImage, ReceiptAdmin)

admin.site.register(Vendor, ReceiptAdmin)

admin.site.register(Receipt, ReceiptAdmin)

admin.site.register(ReceiptItem, ReceiptAdmin)