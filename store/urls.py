from django.urls import path
from . import views

# Set namespace for this app's URLs
app_name = 'store'

urlpatterns = [
    # Main store page showing all products (e.g., http://127.0.0.1:8000/)
    path('', views.product_list, name='product_list'),
    
    # Detail page for a specific product using its slug (e.g., http://127.0.0.1:8000/laptop/)
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]