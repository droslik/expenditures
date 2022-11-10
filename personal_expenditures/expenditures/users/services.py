from rest_framework import serializers
from rest_framework.response import Response
from users.models import Transaction, User, Category, Account


basic_list_of_categories = [
    {'name': "Забота о себе", 'is_basic': True, 'is_income': False},
    {'name': "Зарплата", 'is_basic': True, 'is_income': True},
    {'name': "Здоровье и фитнес", 'is_basic': True, 'is_income': False},
    {'name': "Кафе и рестораны", 'is_basic': True, 'is_income': False},
    {'name': "Машина", 'is_basic': True, 'is_income': False},
    {'name': "Образование", 'is_basic': True, 'is_income': False},
    {'name': "Отдых и развлечения", 'is_basic': True, 'is_income': False},
    {'name': "Платежи, комиссии", 'is_basic': True, 'is_income': False},
    {'name': "Покупки: одежда, техника", 'is_basic': True, 'is_income': False},
    {'name': "Продукты", 'is_basic': True, 'is_income': False},
    {'name': "Проезд", 'is_basic': True, 'is_income': False}
]


def perform_create_basic_categories(validated_data):
    basic_categories = []
    for category in basic_list_of_categories:
        category_db = Category.objects.filter(name=category['name'])
        if not category_db:
            category_cr = Category.objects.create(**category)
            basic_categories.append(category_cr)
    if len(basic_categories) == 0:
        raise serializers.ValidationError(
            'basic categories have been already created'
        )
    return basic_categories


def create_user(validated_data):
    user = User.objects.create_user(**validated_data)
    if user:
        return create_account_and_categories(user)


def create_account_and_categories(user):
    category = Category.objects.filter(is_basic=True)
    account_number = f'3014{(13 - 4 - len(str(user.id))) * str(0)}' \
                     f'{str(user.id)}'
    Account.objects.create(number=account_number, user_id=user.id)
    user.categories.add(*(cat.id for cat in category))
    return user


def create_categories(user, validated_data):
    name = validated_data.get('name')
    category_in_db = Category.objects.filter(name=name)
    if category_in_db:
        if category_in_db[0] not in user.categories.all():
            user.categories.add(category_in_db[0].id)
            return category_in_db[0]
        raise serializers.ValidationError(
            f'category {category_in_db[0].name} '
            f'is already in your category list'
        )
    category = Category.objects.create(**validated_data)
    user.categories.add(category.id)
    return category


def perform_update_own_categories(self, request):
    user = request.user
    user_categories = user.categories.all()
    category = request.data['category_id']
    serializer = self.serializer_class(instance=user, data=request.data)
    serializer.is_valid(raise_exception=True)
    for cat in user_categories:
        if cat.id == int(category):
            user.categories.remove(category)
            user.save()
            return Response(serializer.data)
    return Response({'message': 'category not found'})


def perform_outcome_transaction(user, validated_data):
    user_account = user.accounts.get(user_id=user.id)
    transaction_amount = validated_data['amount']
    validated_data['category_id'] = validated_data['category_id'].id
    validated_data['user_id'] = user.id
    if user_account.amount >= transaction_amount:
        user_account.amount = user_account.amount - transaction_amount
        transaction = Transaction.objects.create(**validated_data)
        if transaction:
            user_account.save()
        return transaction
    raise serializers.ValidationError('Not enough money on your account')


def perform_income_transaction(user, validated_data):
    user_account = user.accounts.get(user_id=user.id)
    transaction_amount = validated_data['amount']
    validated_data['category_id'] = validated_data['category_id'].id
    validated_data['user_id'] = user.id
    user_account.amount = user_account.amount + transaction_amount
    transaction = Transaction.objects.create(**validated_data)
    if transaction:
        user_account.save()
        return transaction
    raise serializers.ValidationError('Can not perform transaction')
