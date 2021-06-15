from django.urls import path

from . import views
app_name="encyclopedia"

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("new/",views.new, name="new"),
    path("wiki/<str:page>",views.entry_page,name="entry_page"),
    path("editpage/<str:title>",views.editpage,name="editpage"),
    path("edit/",views.edit,name="edit"),
    path("randompage/",views.randompage,name="randompage"),
    path("search/",views.search,name="search"),
    path("index/",views.index,name="index")
]
