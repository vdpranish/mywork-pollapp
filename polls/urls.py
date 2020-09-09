from django.urls import path
from . import views

app_name = 'p'
urlpatterns = [
    path('polls/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('adminview/', views.AdminView.as_view(), name='adminview'),
    path('', views.user_login, name='login'),
    path('<int:user_id>/edit/', views.edit, name='edit'),
    path('<int:user_id>/delete/', views.delete_user, name='delete')
]
