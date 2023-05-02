"""neatreceipt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.receipts.views import home_view
from neatreceipt import settings
from accounts.views import login_view
from accounts.views import register_view
from accounts.views import logout_view
from apps.receipts.views import image_upload_view
from apps.receipts.views import receipt_view
from apps.receipts.views import receipts_view
from apps.receipts.views import receipt_delete
from apps.receipts.views import reports_view

urlpatterns = []

# Accounts

urlpatterns += [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout', logout_view, name='logout'),
    path('accounts/register/', register_view, name='register'),
]

# Admin

urlpatterns += [
    path('admin/', admin.site.urls),
]

# Index

urlpatterns += [
    path('', home_view, name='home'),
]

# Receipts

urlpatterns += [
    path('receipts/<int:receipt_id>', receipt_view),
    path('receipts/', receipts_view),
    path('receipts/delete/<int:receipt_id>', receipt_delete, name='delete'),
    path('upload/', image_upload_view, name='image_upload'),
]

# Reports

urlpatterns += [
    path('reports/', reports_view, name='reports'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
