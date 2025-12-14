from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('pages/<int:doc_id>/', views.view_pages, name='view_pages'),
]
