from .views import CategoryData, ProductData
from django.urls import path


urlpatterns = [
    path('categories/', CategoryData.as_view(),
         name='transform_product_data'),
    path('products/', ProductData.as_view(),
         name='get_and_transform_products'),
    # Add other URL patterns as needed.
]
