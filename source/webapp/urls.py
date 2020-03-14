from django.urls import path
from webapp.views import FileCreate, FileList, FileDelete, FileDetail, FileUpdate, FileDownload,PrivateUserDelete
urlpatterns = [
    path('', FileList.as_view(), name='file_list'),
    path('file/add', FileCreate.as_view(), name='file_add'),
    path('file/delete/<int:pk>', FileDelete.as_view(), name='file_delete'),
    path('file/detail/<int:pk>', FileDetail.as_view(), name='file_detail'),
    path('file/update/<int:pk>', FileUpdate.as_view(), name='file_update'),
    path('file_downloaded/', FileDownload.as_view(), name='file_downloaded'),
    path('user_private_delete/', PrivateUserDelete.as_view(), name='user_private_delete' )
]