from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
import secrets
from datetime import timedelta
import datetime
from django.db.models import Q


# function to generate uniue hex 4 codes
def generate():
    return secrets.token_hex(4)

# Creation of venders (unique)
class VendorModel(models.Model):
    name=models.CharField(max_length=100, blank=True, null=True,unique=True)
    contact_details=models.TextField()
    address=models.TextField()
    vendor_code=models.CharField(max_length=100,blank=True, null=True)
    on_time_delivery_rate=models.FloatField(blank=True, null=True)
    quality_rating_avg=models.FloatField(blank=True, null=True)
    average_response_time=models.FloatField(blank=True, null=True)
    fulfillment_rate=models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name
    


# signaling, default performance history when vendor model created
@receiver(post_save,sender=VendorModel)
def Cal_performance(sender, instance,**kwargs):
    update_performance=HistoricalPerformance.objects.create(
        vendor=instance,
        on_time_delivery_rate=0,
        quality_rating_avg=0,
        average_response_time=0,
        fulfillment_rate =0,
        date=timezone.now()
    )



# signaling, applied when vendor create and assign unique code 
@receiver(pre_save,sender=VendorModel)
def vender_post_save(sender, instance,**kwargs):
    instance.vendor_code=f"{instance.name}{secrets.token_hex(4)}"


# signaling, to create token when user created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None , created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)



# creating purchase order table
class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=2000,unique=True, default= generate, editable=False)
    vendor=models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=timezone.now(),editable=False)
    delivery_date=models.DateTimeField(default=timezone.now() + timedelta(days=2))
    items=models.JSONField()
    quantity=models.IntegerField()
    status=models.CharField(default="placed", max_length=100)
    quality_rating=models.FloatField(blank=True,null=True)

    issue_date=models.DateTimeField(default=timezone.datetime.now())
    acknowledgment_date=models.DateTimeField(default=timezone.datetime.now())




# signaling, applied when any fields are getting updated
@receiver(post_save,sender=PurchaseOrder)
def improve_performance(sender,instance,**kwargs):
     # Avg on-time delivery
    update_perfomance=HistoricalPerformance.objects.get(vendor=VendorModel.objects.get(id=instance.vendor.id))
    get_all_completed_purchase_order=PurchaseOrder.objects.filter(vendor=VendorModel.objects.get(id=instance.vendor.id)).filter(status="completed")
    update_perfomance=HistoricalPerformance.objects.get(vendor=instance.vendor.id)
    print("checec : ",get_all_completed_purchase_order, "vender id : ",instance.vendor.id)
    if instance.status=="completed":
       
        print("updating performance of Avg on-time delivery !!!")
        total_completed_delivery=get_all_completed_purchase_order.count()
        total_on_time_completed_delivery=get_all_completed_purchase_order.filter(delivery_date__lte=timezone.now()).count()

        # updating on db
        if total_on_time_completed_delivery > 0:
            update_perfomance.on_time_delivery_rate=(total_on_time_completed_delivery/total_completed_delivery)*100
            update_perfomance.date=timezone.now()
            update_perfomance.save()
            print("Avg on-time delivery : ",update_perfomance.on_time_delivery_rate)

    # Quality rating
    if instance.quality_rating:
        
        print("updating performance of Quality rating !!!")
        get_all_completed_purchase_order=PurchaseOrder.objects.filter(Q(vendor=VendorModel.objects.get(id=instance.vendor.id)) & Q(status="completed"))
        total_completed_quality_rate=[x for x in get_all_completed_purchase_order.exclude(quality_rating=None).values_list('quality_rating')]
        print(total_completed_quality_rate)
        total_sum_rating=sum([x[0] for x in total_completed_quality_rate])
        
        if total_sum_rating > 0:
            update_perfomance.quality_rating_avg=(total_sum_rating/len(total_completed_quality_rate))
            update_perfomance.date=timezone.now()
            update_perfomance.save()
            print("Quality rating : ",update_perfomance.quality_rating_avg)

    # Average Response Time in days
    if instance.acknowledgment_date:
        print("updating performance of Average Response Time !!!")
        vendor_data = [x for x in PurchaseOrder.objects.filter(Q(vendor=VendorModel.objects.get(id=instance.vendor.id)) & ~Q(acknowledgment_date = None))]
        from .serializer import PurchaseOrderSerializer
        time_differences=list(map(lambda x,y : (x.acknowledgment_date-y.issue_date).total_seconds(),vendor_data,vendor_data))
        if len(time_differences) > 0:
            update_perfomance.average_response_time = (sum(time_differences)/len(time_differences))/60/60/24
            update_perfomance.save()
            print("Average Response Time in days : ",update_perfomance.average_response_time)

    # Fulfilment Rate:
    if instance.status:
        get_total_po_placed=PurchaseOrder.objects.filter(vendor=VendorModel.objects.get(id=instance.vendor.id))
        
        if len(get_total_po_placed) > 0:
            cal_rate=len(get_all_completed_purchase_order)/len(get_total_po_placed)
            update_perfomance.fulfillment_rate=cal_rate*100
            update_perfomance.save()
            print("Fulfilment Rate : ",update_perfomance.fulfillment_rate)



    
# This model optionally stores historical data on vendor performance, enabling trend analysis.
class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date=models.DateTimeField(timezone.datetime.now())
    on_time_delivery_rate=models.FloatField()
    quality_rating_avg=models.FloatField()
    average_response_time=models.FloatField()
    fulfillment_rate=models.FloatField()
