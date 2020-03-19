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
from webpanel.views import index, seller, transporter
from webpanel.views.manager import index as manager_index
from webpanel.views.manager import products as manager_products
from webpanel.views.manager import sellers as manager_sellers
from webpanel.views.manager import transporters as manager_tr
from webpanel.views.manager import buyers as manager_buyers
from webpanel.views.manager import messages

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
    # TRANSPORTER
    path('tr/', transporter.index, name='tr_index'),
    path('tr/requisites/', transporter.requisites, name='tr_requisites'),
    path('tr/payment/', transporter.payment, name='tr_payment'),
    path('tr/dlvrs/', transporter.delivery_list, name='tr_dlvrs'),
    path('tr/about/<int:order_number>', transporter.about, name='tr_about'),
    path('tr/confirmed/<int:order_number>', transporter.confirmed_order, name='tr_confirmed'),
    path('tr/close/<int:order_number>', transporter.close_order, name='tr_close'),
    # MANAGER
    path('manager/', manager_index.index, name='m_index'),
    path('manager/categories/', manager_products.categories, name='m_categories'),
    path('manager/categories/add', manager_products.add_new_category, name='m_add_cat'),
    path('manager/units/', manager_products.units, name='m_units'),
    path('manager/products/', manager_products.products, name='m_products'),

    path('manager/sellers/', manager_sellers.index, name='m_sellers'),
    path('manager/sellers/deactivate/<int:uid>', manager_sellers.deactivate, name='m_deactivate'),
    path('manager/sellers/activate/<int:uid>', manager_sellers.activate, name='m_activate'),
    path('manager/sellers/prolong/<int:uid>', manager_sellers.prolong, name='m_prolong'),

    path('manager/tr/', manager_tr.index, name='m_transporters'),
    path('manager/tr/deactivate/<int:uid>', manager_tr.deactivate, name='tr_deactivate'),
    path('manager/tr/activate/<int:uid>', manager_tr.activate, name='tr_activate'),
    path('manager/tr/prolong/<int:uid>', manager_tr.prolong, name='tr_prolong'),

    path('manager/buyers/', manager_buyers.index, name='m_buyers'),
    path('manager/buyers/deactivate/<int:uid>', manager_buyers.deactivate, name='b_deactivate'),
    path('manager/buyers/activate/<int:uid>', manager_buyers.activate, name='b_activate'),
    path('manager/buyers/prolong/<int:uid>', manager_buyers.prolong, name='b_prolong'),
    # MESSAGES
    path('manager/messages/', messages.index, name='m_messages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)