from django.urls import path
from .views import (
    UserAPIRegistration,
    CategoryBasicCreateListAPI,
    UserListAPI,
    UserRetrieveUpdateAPI,
    CategoryCreateListAPI,
    OutcomeTransactionCreateAPI,
    IncomeTransactionCreateAPI,
    TransactionListAPI,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("users/create/", UserAPIRegistration.as_view(), name="create-user"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "create_basic_category/",
        CategoryBasicCreateListAPI.as_view(),
        name="create-basic",
    ),
    path(
        "create_category/", CategoryCreateListAPI.as_view(), name="create-view-category"
    ),
    path("users/", UserListAPI.as_view(), name="users"),
    path(
        "users/<int:pk>/",
        UserRetrieveUpdateAPI.as_view({"get": "retrieve", "patch": "update"}),
        name="user-view-update",
    ),
    path(
        "transactions/outcome/",
        OutcomeTransactionCreateAPI.as_view(),
        name="outcome_view_create",
    ),
    path(
        "transactions/income/",
        IncomeTransactionCreateAPI.as_view(),
        name="income_view_create",
    ),
    path("transactions/", TransactionListAPI.as_view(), name="transactions-list"),
]
