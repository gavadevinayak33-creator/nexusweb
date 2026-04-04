from django.urls import path   
from .views import *

urlpatterns =[
    path('',Home_page, name='Home_page'),

    path('Conatact',Conatact_page, name='Conatact_page'),
    # path('pay',pay, name='pay'),
    path('dashboard', dashboard, name='dashboard'),
    
    

]