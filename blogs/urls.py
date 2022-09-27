from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.as_view()),
    # path('<int:id>', views.index.as_view()),
    path('addBlog', views.addBlog),
    path('addCategory', views.addTag),
    path('<int:id>', views.blogDetails),
    path('register', views.registerPage),
    path('login', views.loginPage),
    path('logout', views.logoutUser),
    path('<int:id>/add_comment', views.add_comment),
    path('<int:id>/delete_comment', views.delete_comment),
    path('<int:id>/edit_comment', views.edit_comment),
    path('profile', views.profile),
    path('listblogs/', views.listBlog.as_view()),
    path('dummy/<int:id>', views.dummy.as_view())
]