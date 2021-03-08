"""arot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import urls as api_urls
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static


class HomeView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'index.html'


class GrowersView(TemplateView):
    template_name = 'index.html'


class BuyersView(TemplateView):
    template_name = 'index.html'


class WhyArotView(TemplateView):
    template_name = 'index.html'


class TeamView(TemplateView):
    template_name = 'index.html'


class ContactView(TemplateView):
    template_name = 'index.html'


class LoginView(TemplateView):
    template_name = 'index.html'


class OrderView(TemplateView):
    template_name = 'index.html'


class BillingView(TemplateView):
    template_name = 'index.html'


urlpatterns = [
    path('', HomeView.as_view()),
    path('about/', AboutView.as_view()),
    path('growers/', AboutView.as_view()),
    path('buyers/', AboutView.as_view()),
    path('why-arrot/', WhyArotView.as_view()),
    path('team/', TeamView.as_view()),
    path('contact/', ContactView.as_view()),
    path('login/', LoginView.as_view()),
    path('order/', OrderView.as_view()),
    path('billing/', BillingView.as_view()),
    path('profile/', HomeView.as_view()),

    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
