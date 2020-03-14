from django.urls import path
from webapp.views import FileCreate, FileList, FileDelete, FileDetail
urlpatterns = [
    path('', FileList.as_view(), name='file_list'),
    path('file/add', FileCreate.as_view(), name='file_add'),
    path('file/delete/<int:pk>', FileDelete.as_view(), name='file_delete'),
    path('file/detail/<int:pk>', FileDetail.as_view(), name='file_detail')
]