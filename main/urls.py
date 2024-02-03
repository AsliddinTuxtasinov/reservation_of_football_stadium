from django.urls import path

from main import views

urlpatterns = [
    # Admin and stadium owner apps
    path('stadiums', views.StadiumsListCreateViews.as_view()),
    path('stadiums/update/<str:pk>', views.StadiumsUpdateViews.as_view()),
    path('booked/list/', views.StadiumsBookedListView.as_view()),
    path('booked/delete/<str:booked_id>', views.StadiumsBookedDeleteView.as_view()),

    # Admin and User apps
    path('stadiums/detail/<str:pk>', views.StadiumsDetailViews.as_view()),
    path('booked/create/<str:stadium_id>', views.StadiumsBookedCreateViews.as_view()),
    path('stadiums/list', views.StadiumsListForUserViews.as_view()),
]
