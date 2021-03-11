from django.urls import path, include
from api.views import ProductViewSet, LogoutView, LoginView, OrderViewSet, OrderSearchView, \
    MerchantUserPermissionViewSet, ChangePasswordView, BillingViewSet, ProfileViewSet, BillingSearchView, BuyerViewSet,PaymentViewSet
from api.views.order import cancel_order, confirm_order
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('products', ProductViewSet, basename='product_api')
router.register('orders', OrderViewSet, basename='order_api')
router.register('merchant_user_permission', MerchantUserPermissionViewSet, basename='merchant_user_permission_api')
router.register('billing', BillingViewSet, basename='billing_api')
router.register('buyer', BuyerViewSet, basename='buyer_api')
router.register('payments',PaymentViewSet,basename='payment_api')

urlpatterns = [
    # path('', RootView.as_view()),
    path('', include(router.urls)),
    path('orders/<order_id>/cancel/', cancel_order),
    path('orders/<order_id>/confirm/', confirm_order),
    path('orders/search', OrderSearchView.as_view()),
    path('billing/search', BillingSearchView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('profile/', ProfileViewSet.as_view({
        'get': 'list',
        'put': 'update',
        # 'patch': 'partial_update'
    })),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
