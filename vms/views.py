from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from rest_framework.decorators import permission_classes,authentication_classes,api_view
import json,io
from rest_framework.parsers import JSONParser
from .serializer import VenderModel_serializer,PurchaseOrderSerializer,Performance_Update_Serializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import VendorModel,PurchaseOrder,HistoricalPerformance
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.views import View
from django.utils import timezone


# Vendor render function base VIEW
@api_view(['PUT','POST','GET','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createVendors(request,vendor_id=None):

    # User to create vendors
    if request.method=='POST':
        
        json_data=request.body
        py_data=JSONParser().parse(io.BytesIO(json_data))  # Converting json to native Python data
        serialize=VenderModel_serializer(data=py_data)   
        if serialize.is_valid():   # check for valid data 
            serialize.save()  
            return JsonResponse({'msg':'Vender creation Success'},status=status.HTTP_201_CREATED)
        return JsonResponse({'msg':serialize.errors})
    
    # User to update vendors details
    if request.method=="PUT":
        try:   
            get_vendor_details=VendorModel.objects.get(id=vendor_id)
            print(get_vendor_details)
            if get_vendor_details:
            
                json_data=request.body
                py_data=JSONParser().parse(io.BytesIO(json_data))  # Converting json to native Python data
                serialize=VenderModel_serializer(get_vendor_details,data=py_data , partial=True )
                if serialize.is_valid():   # check for valid data
                    serialize.save()
                    return JsonResponse({'msg':"Vendor details Updated"})
        
        except:
            return JsonResponse({'msg':"Please enter valid vendor ID"})
        
    # Getting all vendors details
    if request.method =="GET":

        get_all_venders=VendorModel.objects.all()  
        serialize=VenderModel_serializer(get_all_venders,many=True) 
        return JsonResponse({"vendors":serialize.data})
    
    # Getting Deleted for the selected ID's
    if request.method =="DELETE":   
        try:   
            get_details=VendorModel.objects.get(id=vendor_id)
            if get_details:
                get_details.delete()
                return JsonResponse({'msg':"Vendor Deleted"})
        except:
            return JsonResponse({'msg':"Please enter valid vendor ID"})
        
    
    return JsonResponse({'mgs':'None'})

# User render function based VIEW
@csrf_exempt
def userCreations(request):
    print(request.headers)
    if request.method=="POST":
        data_json=request.body
        if data_json:
            
            stream=io.BytesIO(data_json)
            py_data=JSONParser().parse(stream)  # Converting json to native Python data
            u_name=py_data.get('Username')
            u_password=py_data.get('Password')
            try:
                create_user=User.objects.create(username=u_name,password=u_password)
                create_user.save()
            except Exception as error:
                return HttpResponse(json.dumps({'msg':f"{error}"}))
            
            get_user_token=Token.objects.get(user=create_user)
            print("get_user_token : ",get_user_token)
            
            return JsonResponse({'mgs':'User Created','token':f"{get_user_token}"})
    return JsonResponse({'msg':'Username and Password is required '})


# purchaseOrderTracking render function based VIEW

@api_view(['POST','GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchaseOrderTracking(request,po_id=None):
    if request.method=='POST':
        json_data=request.body
        
        py_data=JSONParser().parse(io.BytesIO(json_data))  # Converting json to native Python data
        try:    
            
            py_data['vendor']=VendorModel.objects.get(name=py_data['vendor']).id
            print("vendor : ",py_data)
        except:
            return Response({'Error':'Vendor Not Found'},status=status.HTTP_404_NOT_FOUND)
        serialize=PurchaseOrderSerializer(data=py_data)
        if serialize.is_valid():   # check for valid data
            serialize.save()
            return JsonResponse({'msg':'purchased success'},status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'msg':serialize.errors},status=status.HTTP_400_BAD_REQUEST)
        
       

    # User to get purchase details by PO-ID
    if request.method=="GET" and po_id:
        try:
            vendor_data=PurchaseOrder.objects.get(po_number=po_id) 
        except:
            return JsonResponse({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND)
        serialize_vendor_data=PurchaseOrderSerializer(vendor_data)
        return JsonResponse({f"vendor-{vendor_data.vendor.name}":serialize_vendor_data.data })      

    # User to update purchase details by PO-ID : note only can change fields like "items","quantity","quality_rating"
    if request.method=="PUT" and po_id:
        try:
            vendor_purchase_data=PurchaseOrder.objects.get(po_number=po_id) 
        except:
            return JsonResponse({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND)
        json_data=request.body
        py_data=JSONParser().parse(io.BytesIO(json_data))  # Converting json to native Python data
        serialize_update=PurchaseOrderSerializer(vendor_purchase_data,data=py_data,partial=True)
        if serialize_update.is_valid():
            serialize_update.save()

            return JsonResponse({'msg':"Purchase order updated"})
        return JsonResponse({'msg':"Bad Data"},status=status.HTTP_400_BAD_REQUEST)
    

    # User to Delete Purchase order by PO-ID
    if request.method=="DELETE" and po_id:
        try:
            vendor_purchase_data=PurchaseOrder.objects.get(po_number=po_id) 
        except:
            return JsonResponse({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND)        
        vendor_purchase_data.delete()
        return JsonResponse({'msg':'Purchasen order deleted'})

    # # Getting all vendors details

    get_all_venders=PurchaseOrder.objects.all()  
    serialize=PurchaseOrderSerializer(get_all_venders,many=True) 

    return JsonResponse({"Purchases":serialize.data})


# VendorPerformance render class based view
class VendorPerformance(View):
    def get(self,request,vendor_id):
        try:
            vendor_data=VendorModel.objects.get(id=vendor_id)
        except:
            return JsonResponse({'msg':'vendor not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if vendor_data:
            serialize=Performance_Update_Serializer(HistoricalPerformance.objects.get(vendor=VendorModel.objects.get(id=vendor_id)))
            return JsonResponse({"Performance":serialize.data})
    



