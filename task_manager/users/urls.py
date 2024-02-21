from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_users'),
    path('create/', views.CreateUser.as_view(), name='create_user'),
    path('<int:id>/update/', views.UpdateUser.as_view(), name='update_user'),
    path('<int:id>/delete/', views.DeleteUser.as_view(), name='delete_user'),
]