from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .filters import TransactionFilter
from .models import Category, User, Transaction
from .serializers import (
    UserCreateSerializer,
    CreateCategoriesSerializer,
    UserListSerializer,
    UserSerializer,
    OutcomeTransactionCreateSerializer,
    IncomeTransactionCreateSerializer,
    CreateBasicCategoriesSerializer,
    TransactionListSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .services import perform_update_own_categories


class UserAPIRegistration(generics.CreateAPIView):
    """Class for registrations of users. Allowed for any user"""

    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class CategoryBasicCreateListAPI(generics.ListCreateAPIView):
    """Class for creating of basic categories"""

    serializer_class = CreateBasicCategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        categories = Category.objects.filter(is_basic=True)
        serializer = self.serializer_class(categories, many=True)
        return Response({"categories": serializer.data})


class CategoryCreateListAPI(generics.ListCreateAPIView):
    """Class for creating and viewing own categories by users"""

    serializer_class = CreateCategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = request.user
        categories = user.categories
        serializer = self.serializer_class(categories, many=True)
        return Response({"user_categories": serializer.data})


class UserListAPI(generics.ListAPIView):
    """Class to view all users by admin"""

    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)


class UserRetrieveUpdateAPI(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    """Class to view self user info and update category list"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None, username=None):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({"user": serializer.data})

    def update(self, request, *args, **kwargs):
        return perform_update_own_categories(self, request)


class OutcomeTransactionCreateAPI(generics.ListCreateAPIView):
    """Class for creating and viewing outcome transactions"""

    queryset = Transaction.objects.all()
    serializer_class = OutcomeTransactionCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        transactions = Transaction.objects.filter(
            user_id=user.id, category_id__is_income=False
        )
        return transactions


class IncomeTransactionCreateAPI(generics.ListCreateAPIView):
    """Class for creating and viewing income transactions"""

    queryset = Transaction.objects.all()
    serializer_class = IncomeTransactionCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        transactions = Transaction.objects.filter(
            user_id=user.id, category_id__is_income=True
        )
        return transactions


class TransactionListAPI(generics.ListAPIView):
    """Class for creating and viewing all transactions"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        user = self.request.user
        transactions = Transaction.objects.filter(user_id=user.id)
        return transactions
