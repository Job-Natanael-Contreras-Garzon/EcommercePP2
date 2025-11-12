from django.urls import path
from .views import create_checkout_preference, payment_success, payment_pending, payment_failure

urlpatterns = [
    path('create', create_checkout_preference),  # POST /payment/create
    path('success', payment_success),            # GET /payment/success
    path('failure', payment_failure),            # GET /payment/failure
    path('pending', payment_pending),            # GET /payment/pending
]