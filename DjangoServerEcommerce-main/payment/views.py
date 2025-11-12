from django.shortcuts import render
import mercadopago
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status

from MyDjangoProjectServer.settings import NGROK_URL
from django.shortcuts import redirect

from orders.models import OrderHasProducts
from orders.serializers import OrderSerializer
from products.models import Product


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def create_checkout_preference(request):
    sdk = mercadopago.SDK("ACCESS_TOKEN")  # usa sandbox o prod según tu ambiente
    print(f'DATA PAYMENT: {request.data}')
    products = request.data.get('products', [])
    id_user = request.data.get('id_client')
    id_address = request.data.get('id_address')
    preference_data = {
        "items": [
            {
                "title": product["name"],
                "quantity": product["quantity"],
                "currency_id": "COP",
                "unit_price": product["price"]
            }
            for product in products
        ],
        "back_urls": {
            "success": f"https://{NGROK_URL}/payment/success",
            "failure": f"https://{NGROK_URL}/payment/failure",
            "pending": f"https://{NGROK_URL}/payment/pending"
            
        },
        # "back_urls": {
        #     "success": "myapp://payment-success",
        #     "failure": "myapp://payment-failure",
        #     "pending": "myapp://payment-pending"
        # },
        "auto_return": "approved",
        "notification_url": "https://tusitio.com/webhooks/mercadopago/"
    }

    preference_response = sdk.preference().create(preference_data)

    order_data = {
        'id_user': id_user,
        'id_address': id_address,
        'status': 'PAGADO',
    }

    serializer = OrderSerializer(data=order_data)
    if not serializer.is_valid():
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        error_response = {
            "message": error_messages,
            "statusCode": status.HTTP_400_BAD_REQUEST
        }

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    order = serializer.save()
    
    if not products:
        return Response(
            {
                "message": 'Debes enviar al menos un producto',
                "statusCode": status.HTTP_400_BAD_REQUEST
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    for product_data in products:
        try:
            product = Product.objects.get(id=product_data['id'])
            quantity = product_data['quantity']
            OrderHasProducts.objects.create(
                id_order=order,
                id_product=product,
                quantity = quantity
            )
        except Product.DoesNotExist:
            order.delete()
            return Response(
                {
                    "message": f'El producto con id: ${product_data["id"]} no existe',
                    "statusCode": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            order.delete()
            return Response(
                {
                    "message": f'Error al crear el producto ${str(e)}',
                    "statusCode": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
    

    if preference_response["status"] == 201:
        return Response({
            "init_point": preference_response["response"]["init_point"]
        })
    else:
        return Response({
            "error": "No se pudo generar la preferencia",
            "details": preference_response
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_success(request):
    return render(request, 'redirect.html')

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def payment_success(request):
#     data = request.query_params
#     print(f'Data Success: ${data}')
#     return Response({
#         "message": "Pago exitoso",
#         "data": data
#     })

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_failure(request):
   
    data = request.query_params
    print(f'Data failure: ${data}')
    return Response({
        "message": "Pago fallido",
        "data": data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_pending(request):
    
    data = request.query_params
    print(f'Data pending: ${data}')
    return Response({
        "message": "Pago pendiente",
        "data": data
    })
