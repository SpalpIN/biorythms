from django.urls import path, re_path
from . import views

urlpatterns = [

    path('main', views.start),
    path('', views.start),
    re_path('biorythms/', views.Biorhythms.as_view()),
    path('ivents', views.Ivent.as_view()),
    re_path('register/', views.RegisterForm.as_view()),
    re_path('auth/', views.AuthForm.as_view()),
    re_path('logout/', views.LogoutForm.as_view()),
    re_path('account/', views.Account.as_view()),
    re_path('changeData/',views.account_form),
    re_path('changeAccData/',views.ChangeAccData.as_view()),
    re_path('reduct/',views.Reduct.as_view()),
    re_path('bioresult/', views.Bioresult.as_view()),
    re_path('circad/', views.CircadeRythm.as_view()),
    re_path('hronoTest/', views.HronoTest.as_view()),





]
