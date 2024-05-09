from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard2/', views.paginator_views, name='dashboard2'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add_task/', views.add_task, name='add_task'),
    path('<uuid:pk>/details/', views.details, name='details'),
    path('<uuid:pk>/edit/', views.edit_task, name='edit'),
    path('<uuid:pk>/delete/', views.delete_task, name='delete'),
    path('<uuid:pk>/task_done/', views.mark_done, name='done'),
    path('<uuid:pk>/task_todo/', views.mark_todo, name='todo'),
]
