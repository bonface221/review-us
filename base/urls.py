from django.urls import path 
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    path('profile/<str:username>/settings',views.edit_profile,name='settings'),
    path('project/<str:post>/',views.project,name='project'),
    path('profile/<username>/', views.profile, name='profile'),

    path('login/',views.LoginInterfaceView.as_view(),name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('signup/',views.SignupView.as_view(),name='signup'),

]