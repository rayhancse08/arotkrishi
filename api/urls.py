from django.urls import path, include
from api.views import ProductViewSet, LogoutView, LoginView, OrderViewSet, OrderSearchView
from api.views.order import cancel_order, confirm_order
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('products', ProductViewSet, basename='product_api')
router.register('orders', OrderViewSet, basename='order_api')

urlpatterns = [
    # path('', RootView.as_view()),
    path('', include(router.urls)),
    path('orders/<order_id>/cancel/', cancel_order),
    path('orders/<order_id>/confirm/', confirm_order),
    path('orders/search', OrderSearchView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
