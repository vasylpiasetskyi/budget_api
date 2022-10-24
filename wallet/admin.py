from django.contrib import admin

from wallet.models import Currency, Account, Category, SubCategory, Transaction


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "exchange", "created_at", "updated_at")


class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_type", "name", "balance", "owner", "currency",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_type", "name", "owner", "is_active", "created_at", "updated_at")


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_active", "created_at", "updated_at")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("action", "category", "sub_category", "amount", "description",
                    "date", "owner", "from_account", "to_account", "created_at", "updated_at")


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
