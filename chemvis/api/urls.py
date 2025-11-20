from django.urls import path
from .views import UploadCSV, History, SummaryDetail, GeneratePDF

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload'),
    path('history/', History.as_view(), name='history'),
    path('summary/<int:pk>/', SummaryDetail.as_view(), name='summary'),
    path('report/<int:pk>/', GeneratePDF.as_view(), name='report'),
]
