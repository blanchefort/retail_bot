"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from webpanel.views import index, seller

urlpatterns = [
    # ENTER
    path('', index.index, name='index'),
    # ADMIN
    path('admin/', admin.site.urls, name='admin'),
    # AUTH
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', index.select_profile, name='select_profile'),
    path('select_registration/', index.select_registration, name='select_registration'),
    path('registration/<int:type>', index.registration, name='registration'),
    # SELLER
    path('seller/', seller.index, name='seller_index'),
    path('seller/upload_price/', seller.upload_price, name='seller_upload_price'),
    path('seller/pricelists/', seller.pricelists, name='seller_pricelists'),
    path('seller/products/', seller.products, name='seller_products'),
    path('seller/orders/', seller.orders, name='seller_orders'),
    path('seller/order/<int:user_id>/<int:status>', seller.confirm_order, name='seller_confirm_order'),
    path('seller/download_order_as_xsls/<int:user_id>', seller.download_order_as_xsls, name='seller_download_order_as_xsls'),
    path('seller/order_details/<int:order_number>', seller.order_details, name='seller_order_details'),
    path('seller/requisites/', seller.requisites, name='seller_requisites'),
    path('seller/payment/', seller.payment, name='seller_payment'),
    path('seller/closed_orders/<int:order_number>', seller.closed_orders, name='seller_closed_orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)