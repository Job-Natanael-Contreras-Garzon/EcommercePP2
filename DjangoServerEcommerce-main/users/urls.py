from django.urls import path
from .views import update, updateWithImage, get_user_by_id, get_all_users

urlpatterns = [
    path('', get_all_users),                      # GET /users/
    path('<int:id_user>', update),                # PUT /users/1
    path('findById/<int:id_user>', get_user_by_id), # GET /users/findById/1
    path('upload/<int:id_user>', updateWithImage), # PUT /users/upload/1
]