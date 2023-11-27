from vms import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    path("createuser/",views.userCreations),
    path('api/vendors/',views.createVendors),
    path('api/vendors/<int:vendor_id>',views.createVendors),
    path('api/purchase_orders/',views.purchaseOrderTracking),
    path('api/purchase_orders/<str:po_id>',views.purchaseOrderTracking),
    path('api/vendors/<int:vendor_id>/performance/',views.VendorPerformance.as_view()),
    path("auth/",include('rest_framework.urls',namespace='rest_framework'))
]
