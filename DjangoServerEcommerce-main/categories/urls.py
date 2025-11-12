from django.urls import path
from .views import create, get_categories, delete, update

urlpatterns = [
    path('', create),                                    # POST /categories
    path('getCategories', get_categories),               # GET /categories/getCategories
    path('delete/<int:id_category>', delete),            # DELETE /categories/delete/1
    path('update/<int:id_category>', update),            # PUT /categories/update/1
]