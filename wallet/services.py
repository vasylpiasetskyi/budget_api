import decimal

from rest_framework.exceptions import NotFound

from wallet.models import Account


def service_perform_create(self, serializer):
    from_account = None
    to_account = None
    owner = self.request.user
    category = serializer.validated_data.get('category')
    sub_category = serializer.validated_data.get('sub_category')

    if category and category.owner != owner:
        raise NotFound(detail=f"Error 403, Category does not meet the {owner.username}", code=403)

    if serializer.validated_data.get('from_account'):
        from_account = Account.objects.get(id=serializer.validated_data.get('from_account').id)
        if from_account.owner != owner:
            raise NotFound(detail=f"Error 403, Account does not meet the {owner.username}", code=403)

    if serializer.validated_data.get('to_account'):
        to_account = Account.objects.get(id=serializer.validated_data.get('to_account').id)
        if to_account.owner != owner:
            raise NotFound(detail=f"Error 403, Account does not meet the {owner.username}", code=403)

    if serializer.validated_data.get('action') == "INCOME":
        if category and category.category_type != "INCOME":
            raise NotFound(detail=f"Error 403, Category does not meet the INCOME", code=403)
        if sub_category and sub_category.category.category_type != "INCOME":
            raise NotFound(detail=f"Error 403, SubCategory does not meet the INCOME", code=403)
        to_account.balance = to_account.balance + decimal.Decimal(serializer.validated_data.get('amount'))
        to_account.save()
        serializer.save(from_account=None)

    if serializer.validated_data.get('action') == "EXPENSE":
        if category and category.category_type != "EXPENSE":
            raise NotFound(detail=f"Error 403, Category does not meet the EXPENSE", code=403)
        if sub_category and sub_category.category.category_type != "EXPENSE":
            raise NotFound(detail=f"Error 403, SubCategory does not meet the EXPENSE", code=403)
        from_account.balance = from_account.balance - decimal.Decimal(serializer.validated_data.get('amount'))
        from_account.save()
        serializer.save(to_account=None)

    if serializer.validated_data.get('action') == "TRANSFER":
        if not from_account or not to_account:
            raise NotFound(detail=f"Error 403, Transfer required FROM and TO accounts", code=403)
        if category or sub_category:
            raise NotFound(detail=f"Error 403, Transfer does not have Category or SubCategory", code=403)
        to_account.balance = to_account.balance + decimal.Decimal(serializer.validated_data.get('amount'))
        from_account.balance = from_account.balance - decimal.Decimal(serializer.validated_data.get('amount'))
        to_account.save()
        serializer.save(category=None, sub_category=None)

    return serializer
