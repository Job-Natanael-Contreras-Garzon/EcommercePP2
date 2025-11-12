from django.urls import path
from .views import create, get_products_by_category, delete, update

urlpatterns = [
    path('', create),                                        # POST /products
    path('category/<int:id_category>', get_products_by_category), # GET /products/category/1
    path('<int:id_product>', delete),                        # DELETE /products/1
    path('upload/<int:id_product>', update),                 # PUT /products/upload/1
]