from django.urls import path

from apps.branches.api_endpoints.branch.views import BranchListCreateView, BranchRetrieveUpdateDestroyView



urlpatterns = [
    path('', BranchListCreateView.as_view(), name='branch_create_list'),
    path('<int:pk>', BranchRetrieveUpdateDestroyView.as_view(),
         name='branch_update_retrieve_destroy'),
]
