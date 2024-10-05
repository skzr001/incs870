from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('book/', views.book,name='book'),
    path('booking/<int:id>/',views.booking,name='booking'),
    path('booking/',views.booking,name='booking'),
    path('pay/<int:id>/',views.Pay,name='pay'),
    path('pay/',views.Pay,name='pay'),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout_user,name='logout_user'),  

    # path('', home_view, name='home_view')
    # path('login', auth_view, name='login_view')
    path('verify/', views.verify_view, name='verify-view'),
]
