"""djangoshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from djangoshop import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.product_view),
    path('addpro/',views.add_product_view),
    re_path('checkout/(?P<pk>\d+)/$',views.checkout_view),
    re_path('checkout1/',views.checkout),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/',views.signup_view),
    re_path('delete/(?P<id>\d+)/$',views.del_checkout),
    path('payments/',views.homepage),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
    


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
