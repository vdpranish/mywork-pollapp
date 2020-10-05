from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('polls/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:pk>/adminview/', views.AdminView.as_view(), name='adminview'),
    path('table/', views.TableView.as_view(), name='table'),
    path('calender/', views.CalenderView.as_view(), name='calender'),
    path('', views.user_login, name='login'),
    path('<int:user_id>/edit/', views.edit, name='edit'),
    path('delete/', views.delete_user, name='delete'),
    path('ajaxaction/', views.ajax_request, name='ajaxaction'),
    path('square/', views.SquareForm.as_view(), name='square'),
    path('pdf/', views.pdf_file, name='pdf'),
    path('pdf/<int:pdf_id>', views.pdf_view, name='pdfview'),
    path('create_square_customer',views.square_customer_form,name='create_square_customer')
]
