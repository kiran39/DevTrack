from django.urls import path
from .views import get_issues, post_issues, get_Reporter,post_reporter

urlpatterns = [
    path("issues/", get_issues),
    path("issues/<int:id>/", get_issues),
    path("postissues/", post_issues),
    path("reporters/", get_Reporter),
    path("reporter/<int:id>/", get_Reporter),
    path("create-reporter/",post_reporter ),
]