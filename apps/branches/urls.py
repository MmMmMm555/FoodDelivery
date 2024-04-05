from django.urls import path

from apps.branches.api_endpoints.branch.views import BranchListCreateView, BranchRetrieveUpdateDestroyView
from apps.branches.api_endpoints.comments.views import CommentListCreateView, CommentRetrieveUpdateDestroyView



urlpatterns = [
    # List and Create a new branch
    path('branch/', BranchListCreateView.as_view(), name='branch_create_list'),
    path('branch/<int:pk>', BranchRetrieveUpdateDestroyView.as_view(),
         name='branch_update_retrieve_destroy'),
    
    # List and Create a new Comment
    path('comment/', CommentListCreateView.as_view(), name='comment_create_list'),
    path('comment/<int:pk>', CommentRetrieveUpdateDestroyView.as_view(),
         name='comment_update_retrieve_destroy'),
]
