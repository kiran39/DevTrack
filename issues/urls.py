from django.urls import path
from .views import get_issues, post_issues

urlpatterns = [
    path("issues/", get_issues),
    path("issues/<int:id>/", get_issues),
    path("postissues/", post_issues),
]