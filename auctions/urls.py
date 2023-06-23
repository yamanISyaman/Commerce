from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("close/<str:id>", views.close_auction, name="close_auction"),
    path("listing/<str:id>", views.listing_view, name="listing"),
    path("bid/<str:id>", views.add_bid, name="bid"),
path("commemt/<str:id>", views.add_comment, name="comment")
]
