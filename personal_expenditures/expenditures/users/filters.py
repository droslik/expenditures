import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='gte'
    )
    end_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='lte'
    )
    min_amount = django_filters.Filter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.Filter(field_name='amount', lookup_expr='lte')
    start_time = django_filters.IsoDateTimeFilter(
        field_name='transaction_date',
        lookup_expr='gte'
    )
    end_time = django_filters.IsoDateTimeFilter(
        field_name='transaction_date',
        lookup_expr='lte'
    )

    class Meta:

        model = Transaction
        fields = [
            'amount',
            'start_date',
            'end_date',
            'min_amount',
            'max_amount',
            'start_time',
            'end_time'
        ]

        def list(self, request):
            user = request.user
            transactions = Transaction.objects.filter(user_id=user.id)
            return transactions

