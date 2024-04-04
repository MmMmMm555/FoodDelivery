from django.urls import path

from apps.foods.api_endpoints.category.views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView)
from apps.foods.api_endpoints.foods.views import (
    FoodListCreateView, FoodRetrieveUpdateDestroyView)
from apps.foods.api_endpoints.food_images.views import (
    FoodImagesListCreateView, FoodImagesRetrieveUpdateDestroyView)


urlpatterns = [
    # categories
    path('category/', CategoryListCreateView.as_view(),
         name='category_list_create'),
    path('category/<int:pk>', CategoryRetrieveUpdateDestroyView.as_view(),
         name='category_retrieve_update_delete'),

    # foods
    path('food/', FoodListCreateView.as_view(), name='food_list_create'),
    path('food/<int:pk>', FoodRetrieveUpdateDestroyView.as_view(), name='food_retrieve_update_delete'),

    # food images
    path('images/', FoodImagesListCreateView.as_view(), name='food_list_create'),
    path('images/<int:pk>', FoodImagesRetrieveUpdateDestroyView.as_view(), name='food_retrieve_update_delete'),
]
