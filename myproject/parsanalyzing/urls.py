from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from parsanalyzing import views


urlpatterns = [
    path('', views.api_root),
    # path('parsanalyzing/<int:pk>/highlight/', views.ParsanalyzingHighlight.as_view(),
    #     name='snippet-highlight'),
    path('parsanalyze/', views.ParsanalyzeList.as_view(),
         name='parsanalyze-list'),
    path('parsanalyze/<int:pk>/', views.ParsanalyzeDetail.as_view(),
         name='parsanalyze-detail'),
    path('bestforbuying/', views.BestForBuyingList.as_view(),
         name='bestforbuying-list'),
    path('bestforbuying/<int:pk>/', views.BestForBuyingDetail.as_view(),
         name='bestforbuying-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
