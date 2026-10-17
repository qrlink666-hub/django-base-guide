from django.urls import path
from .import views 

app_name = 'catr'

urlpatterns = [
    path('', views.catr_detail, name='catr_detail'), 
    path('add/<int:product_id>/', views.catr_add, name='catr_add'), 
    path('remove/<int:product_id>/', views.catr_remove, name='catr_remove'), 

]
