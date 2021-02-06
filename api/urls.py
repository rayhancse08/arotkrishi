from django.urls import path, include
from api.views import ProductViewSet, LogoutView, LoginView,OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('products', ProductViewSet, basename='product_api')
router.register('orders',OrderViewSet,basename='order_api')

urlpatterns = [
    # path('', RootView.as_view()),
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
