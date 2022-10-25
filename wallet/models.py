from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=5)
    exchange = models.DecimalField(decimal_places=6, max_digits=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Account(models.Model):
    ACCOUNT_OPTIONS = [
        ('REGULAR', 'Regular'),
        ('DEBT', 'Debt'),
        ('SAVINGS', 'Savings'),
    ]
    account_type = models.CharField(choices=ACCOUNT_OPTIONS, max_length=45)
    name = models.CharField(max_length=45)
    balance = models.DecimalField(decimal_places=2, max_digits=12)
    owner = models.ForeignKey(User, related_name="accounts_user", on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, related_name="accounts_currency", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_OPTIONS = [
        ('INCOME', 'Income'),
        ('EXPENSES', 'Expenses')
    ]
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="category_user", on_delete=models.CASCADE)
    category_type = models.CharField(choices=CATEGORY_OPTIONS, max_length=45)
    currency = models.ForeignKey(Currency, related_name="category_currency", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category_type} - {self.name} - {self.owner}"


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="sub_category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.category}"


class Transaction(models.Model):
    TRANSACTION_OPTIONS = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer')
    ]
    action = models.CharField(choices=TRANSACTION_OPTIONS, max_length=45)
    category = models.ForeignKey(Category, related_name="transactions_category", on_delete=models.CASCADE,
                                 blank=True,
                                 null=True
                                 )
    sub_category = models.ForeignKey(SubCategory, related_name="transactions_sub_category", on_delete=models.SET_NULL,
                                     blank=True,
                                     null=True)
    from_amount = models.DecimalField(decimal_places=2, max_digits=12)
    to_amount = models.DecimalField(decimal_places=2, max_digits=12)

    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="transactions_user", on_delete=models.CASCADE)
    from_account = models.ForeignKey(Account, related_name="transactions_from", on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)
    to_account = models.ForeignKey(Account, related_name="transactions_to", on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return str(self.owner) + f"s {self.action}"
