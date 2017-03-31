from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$',views.register),
    # url(r'^reviews/destroy/(?P<reviewid>\d+)$',views.destroyReview),
    url(r'^login$',views.login),
    url(r'^user/(?P<userid>\d+)$',views.user),
    url(r'^logout$',views.logout),
    url(r'^quotes$',views.quotes),
    url(r'^quote/create$',views.create),
    url(r'^favorite/add/(?P<quoteid>\d+)$',views.addFavorite),
    url(r'^favorite/destroy/(?P<favoriteid>\d+)$',views.destroyFavorite),
    # url(r'^books$', views.books),
    # url(r'^books/add$', views.addBook),
    # url(r'^book/create$', views.createBook),
    # url(r'^books/(?P<bookid>\d+)$', views.oneBook),
    # url(r'^review/create/(?P<bookid>\d+)$', views.createReview),
]
