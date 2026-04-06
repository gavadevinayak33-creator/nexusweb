from django.urls import path   
from .views import *

urlpatterns =[
    path('',Home_page, name='Home_page'),

    path('Conatact',Conatact_page, name='Conatact_page'),
    # path('pay',pay, name='pay'),
    path('dashboard', dashboard, name='dashboard'),
    
     path('pay/<int:booking_id>/', create_payment, name='create_payment'),
    path('payment-success/', payment_success, name='payment_success'),
    
    

]