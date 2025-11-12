from django.urls import path
from .views import create, get_orders_by_user, update

urlpatterns = [
    path('', create),                            # POST /orders
    path('<int:id_user>', get_orders_by_user),   # GET /orders/1
    path('update/<int:id_order>', update),       # PUT /orders/update/1
]