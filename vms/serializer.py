from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,Serializer
from django.contrib.auth.models import User
from .models import VendorModel, PurchaseOrder, HistoricalPerformance

class VenderModel_serializer(serializers.ModelSerializer):
    class Meta:
        model=VendorModel
        fields="__all__"

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields="__all__"
        # read_only_fields=[
        #     "po_number",
        #     "vendor",
        #     "order_date",
        #     "delivery_date",
        #     "status",
        #     "issue_date",
        #     "acknowledgment_date"
        # ]

class Performance_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model=HistoricalPerformance
        fields="__all__"
    