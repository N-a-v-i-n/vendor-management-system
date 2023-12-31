# vendor-management-system

1. install all modules and libraries on requirement.txt
        -> pip install -r requirements.txt
2. to create db 
        -> python .\manage.py makemigrations vms
        -> python .\manage.py migrate
3. to create superuser
        -> python .\manage.py createsuperuser

4. to run the server app 
        -> python .\manage.py runserver 


API's Working:- (note :- all apis are token authentication)
-------------------
1. Create User to get token, to access all api's

        curl  -X POST \
          'http://127.0.0.1:8000/createuser/' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Content-Type: application/json' \
          --data-raw '{
          "Username":"naveenkumar",
          "Password":1234
        }'

        o/p res:-
        -----------------
        {
          "mgs": "User Created",
          "token": "1f352ab9ef86f9b6861b73ac397bd631a0bca16b"
        }

2. Create Vendor on passing Token, got by user creation

        curl  -X POST \
          'http://127.0.0.1:8000/api/vendors/' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b' \
          --header 'Content-Type: application/json' \
          --data-raw '{
          "name":"naveen",
          "contact_details":"Ascahcunlw",
          "address":2
        }'

        o/p res:-
        -----------------
        {
          "msg": "Vender creation Success"
        }


3. To purchase order, on passing fields, and token got by user creation

        curl  -X POST \
          'http://127.0.0.1:8000/api/purchase_orders/' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b' \
          --header 'Content-Type: application/json' \
          --data-raw '{
          "vendor":"naveen",
          "items":"Ascahcunlw",
          "quantity":2,
          "quality_rating":2
        }'



        o/p res:-
        -----------------
       {
          "msg": "purchased success"
        }


4. To get all vendor details, token got by user creation

        curl  -X GET \
          'http://127.0.0.1:8000/api/vendors/' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b'

        o/p res:-
        --------------

        {
          "vendors": [
            {
              "id": 1,
              "name": "naveen",
              "contact_details": "Ascahcunlw",
              "address": "2",
              "vendor_code": "naveend6ddbbf6",
              "on_time_delivery_rate": null,
              "quality_rating_avg": null,
              "average_response_time": null,
              "fulfillment_rate": null
            },
            {
              "id": 2,
              "name": "kumar",
              "contact_details": "Ascahcunlw",
              "address": "2",
              "vendor_code": "kumard3be7a24",
              "on_time_delivery_rate": null,
              "quality_rating_avg": null,
              "average_response_time": null,
              "fulfillment_rate": null
            },
            {
              "id": 3,
              "name": "nk",
              "contact_details": "Ascahcunlw",
              "address": "2",
              "vendor_code": "nkaac2d7ad",
              "on_time_delivery_rate": null,
              "quality_rating_avg": null,
              "average_response_time": null,
              "fulfillment_rate": null
            }
          ]
        }



5. get purchase order through po-number

        curl  -X GET \
          'http://127.0.0.1:8000/api/purchase_orders/80785ccc' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b'


        o/p res:-
        -----------------

        {
          "vendor-naveen": {
            "id": 1,
            "po_number": "80785ccc",
            "order_date": "2023-11-27T15:51:42.244677Z",
            "delivery_date": "2023-11-29T15:51:42.244677Z",
            "items": "Ascahcunlw",
            "quantity": 2,
            "status": "placed",
            "quality_rating": 2.0,
            "issue_date": "2023-11-27T21:21:42.244677Z",
            "acknowledgment_date": "2023-11-27T21:21:42.244677Z",
            "vendor": 1
          }
        }



6. update purchase order

        curl  -X PUT \
          'http://127.0.0.1:8000/api/purchase_orders/80785ccc' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b' \
          --header 'Content-Type: application/json' \
          --data-raw '{
            "items": "frame",
            "quantity": 5,
            "status": "placed",
            "quality_rating": 3.0
          }'


        o/p res:-
        -----------------

        {
          "msg": "Purchase order updated"
        }


7. get performance for a particular vendor

        curl  -X GET \
          'http://127.0.0.1:8000/api/vendors/1/performance/' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)'



        o/p res:-
        -----------------

        {
          "Performance": {
            "id": 1,
            "date": "2023-11-27T16:03:13.506185Z",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 3.0,
            "average_response_time": 0.0,
            "fulfillment_rate": 25.0,
            "vendor": 1
          }
        }



8. Delete purchase order

        curl  -X DELETE \
          'http://127.0.0.1:8000/api/purchase_orders/80785ccc' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b'


        o/p res:-
        -----------------

        {
          "msg": "Purchasen order deleted"
        }


9. update purchase status

        curl  -X PUT \
          'http://127.0.0.1:8000/api/purchase_orders/d487ab1f' \
          --header 'Accept: */*' \
          --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
          --header 'Authorization: Token 1f352ab9ef86f9b6861b73ac397bd631a0bca16b' \
          --header 'Content-Type: application/json' \
          --data-raw '{
          "quality_rating":4.9,
          "status":"completed"
        }'


        o/p res:-
        -----------------
        {
          "msg": "Purchase order updated"
        }



Project details :-
----------------------------------
----------------------------------

Vendor Management System with Performance Metrics
Objective
---------------
Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

Core Features 
----------------
1. Vendor Profile Management:
    ● Model Design: Create a model to store vendor information including name, contact
    details, address, and a unique vendor code.
    ● API Endpoints:
    ● POST /api/vendors/: Create a new vendor.
    ● GET /api/vendors/: List all vendors.
    ● GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    ● PUT /api/vendors/{vendor_id}/: Update a vendor's details.
    ● DELETE /api/vendors/{vendor_id}/: Delete a vendor.

2. Purchase Order Tracking:
    ● Model Design: Track purchase orders with fields like PO number, vendor reference,
    order date, items, quantity, and status.
    ● API Endpoints:
    ● POST /api/purchase_orders/: Create a purchase order.
    ● GET /api/purchase_orders/: List all purchase orders with an option to filter by
    vendor.
    ● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
    ● PUT /api/purchase_orders/{po_id}/: Update a purchase order.
    ● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

3. Vendor Performance Evaluation:
    ● Metrics:
    ● On-Time Delivery Rate: Percentage of orders delivered by the promised date.
    ● Quality Rating: Average of quality ratings given to a vendor’s purchase orders.
    ● Response Time: Average time taken by a vendor to acknowledge or respond to
    purchase orders.
    ● Fulfilment Rate: Percentage of purchase orders fulfilled without issues.
    ● Model Design: Add fields to the vendor model to store these performance metrics.
    ● API Endpoints:
    ● GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
    metrics.

Data Models
1. Vendor Model
This model stores essential information about each vendor and their performance metrics.
    ● Fields:
    ● name: CharField - Vendor's name.
    ● contact_details: TextField - Contact information of the vendor.
    ● address: TextField - Physical address of the vendor.
    ● vendor_code: CharField - A unique identifier for the vendor.
    ● on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
    ● quality_rating_avg: FloatField - Average rating of quality based on purchase
    orders.
    ● average_response_time: FloatField - Average time taken to acknowledge
    purchase orders.
    ● fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

2. Purchase Order (PO) Model
This model captures the details of each purchase order and is used to calculate various
performance metrics.
    ● Fields:
    ● po_number: CharField - Unique number identifying the PO.
    ● vendor: ForeignKey - Link to the Vendor model.
    ● order_date: DateTimeField - Date when the order was placed.
    ● delivery_date: DateTimeField - Expected or actual delivery date of the order.
    ● items: JSONField - Details of items ordered.
    ● quantity: IntegerField - Total quantity of items in the PO.
    ● status: CharField - Current status of the PO (e.g., pending, completed, canceled).
    ● quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
    ● issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
    ● acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor
    acknowledged the PO.
3. Historical Performance Model
This model optionally stores historical data on vendor performance, enabling trend analysis.
    ● Fields:
    ● vendor: ForeignKey - Link to the Vendor model.
    ● date: DateTimeField - Date of the performance record.
    ● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
    ● quality_rating_avg: FloatField - Historical record of the quality rating average.
    ● average_response_time: FloatField - Historical record of the average response
    time.
    ● fulfillment_rate: FloatField - Historical record of the fulfilment rate.
    These models form the backbone of the Vendor Management System, enabling
    comprehensive tracking and analysis of vendor performance over time. The performance
    metrics are updated based on interactions recorded in the Purchase Order model

Backend Logic
-----------------
Backend Logic for Performance Metrics
On-Time Delivery Rate:
    ● Calculated each time a PO status changes to 'completed'.
    ● Logic: Count the number of completed POs delivered on or before
    delivery_date and divide by the total number of completed POs for that vendor.

Quality Rating Average:
    ● Updated upon the completion of each PO where a quality_rating is provided.
    ● Logic: Calculate the average of all quality_rating values for completed POs of
    the vendor.
Average Response Time:
    ● Calculated each time a PO is acknowledged by the vendor.
    ● Logic: Compute the time difference between issue_date and
    acknowledgment_date for each PO, and then find the average of these times
    for all POs of the vendor.

Fulfilment Rate:
    ● Calculated upon any change in PO status.
    ● Logic: Divide the number of successfully fulfilled POs (status 'completed'
    without issues) by the total number of POs issued to the vendor.

API Endpoint Implementation
    ● Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):
    ● Retrieves the calculated performance metrics for a specific vendor.
    ● Should return data including on_time_delivery_rate, quality_rating_avg,
    average_response_time, and fulfillment_rate.

    ● Update Acknowledgment Endpoint:
    ● While not explicitly detailed in the previous sections, consider an endpoint like
    POST /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge
    POs.
    ● This endpoint will update acknowledgment_date and trigger the recalculation
    of average_response_time.
    Additional Technical Considerations
    ● Efficient Calculation: Ensure that the logic for calculating metrics is optimised to
    handle large datasets without significant performance issues.
    ● Data Integrity: Include checks to handle scenarios like missing data points or division
    by zero in calculations.
    ● Real-time Updates: Consider using Django signals to trigger metric updates in
    real-time when related PO data is modified.
    Technical Requirements
    ● Use the latest stable version of Django and Django REST Framework.
    ● Adhere to RESTful principles in API design.
    ● Implement comprehensive data validations for models.
    ● Utilise Django ORM for database interactions.
    ● Secure API endpoints with token-based authentication.
    ● Follow PEP 8 style guidelines for Python code.
    ● Document each API endpoint thoroughly.
