from rest_framework import serializers
from .models import User, Category, Account, Transaction
from .services import (
    perform_outcome_transaction,
    perform_income_transaction,
    create_user,
    create_categories,
    perform_create_basic_categories,
)


class CreateBasicCategoriesSerializer(serializers.ModelSerializer):
    """Serializer to create basic categories by admin"""

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("name",)

    def create(self, validated_data):
        return perform_create_basic_categories(validated_data)


class CreateCategoriesSerializer(serializers.ModelSerializer):
    """Serializer for creating the categories and
    adding categories to user's list of categories"""

    name = serializers.CharField(read_only=False)
    is_income = serializers.BooleanField(read_only=False)
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "is_income"
        )

    def create(self, validated_data):
        user = self.context["request"].user
        return create_categories(user, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "is_income"
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "number",
            "amount",
            "id"
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for registration of users with creation
    of an account and adding of basic set of categories"""

    role = serializers.HiddenField(default="user")
    password = serializers.CharField(write_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    accounts = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "role",
            "categories",
            "accounts"
        )

    def create(self, validated_data, *args, **kwargs):
        return create_user(validated_data)


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving of all users"""

    categories = CategorySerializer
    accounts = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "categories",
            "accounts"
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users to view own profile users"""

    accounts = AccountSerializer(read_only=True, many=True)
    user = serializers.CurrentUserDefault()
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Category.objects.filter()
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "categories",
            "accounts",
            "category_id",
        )
        read_only_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "categories",
            "accounts",
        )


class OutcomeTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating outcome transactions"""

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_income=False)
    )
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "organization",
            "description",
            "category_id",
            "user_id",
            "transaction_date",
        )
        read_only_fields = ("transaction_date",)

    def create(self, validated_data, *args, **kwargs):
        user = self.context["request"].user
        return perform_outcome_transaction(user, validated_data)


class IncomeTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating income transactions"""

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_income=True)
    )
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "organization",
            "description",
            "category_id",
            "user_id",
            "transaction_date",
        )
        read_only_fields = ("transaction_date",)

    def create(self, validated_data, *args, **kwargs):
        user = self.context["request"].user
        return perform_income_transaction(user, validated_data)


class TransactionListSerializer(serializers.ModelSerializer):
    """Serializer for creating income transactions"""

    class Meta:
        model = Transaction
        fields = "__all__"
