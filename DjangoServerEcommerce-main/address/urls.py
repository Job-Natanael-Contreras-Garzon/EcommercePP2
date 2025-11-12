from django.urls import path
from .views import create, get_address_by_user, delete, update

urlpatterns = [
    path('', create),                                    # POST /address
    path('user/<int:id_user>', get_address_by_user),     # GET /address/user/1
    path('<int:id_address>', delete),                    # DELETE /address/1
    path('update/<int:id_address>', update),             # PUT /address/update/1
]