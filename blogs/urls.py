from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.as_view(template_name="blogs"), name="blogs"),
    path('addBlog', views.add_blog, name="add-blog"),
    path('addCategory', views.add_tag, name="add-category"),
    path('<int:id>', views.blog_details, name="blog-details"),
    path('register', views.register_page, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('<int:blog_id>/add_comment/<int:id>', views.add_comment, name="add-comment"),
    path('<int:blog_id>/delete_comment/<int:id>', views.delete_comment, name="delete-comment"),
    path('<int:blog_id>/edit_comment/<int:id>', views.edit_comment, name="edit-comment"),
    path('profile', views.profile),
    path('listblogs/', views.ListBlog.as_view(template_name="list-blog")),
    path('dummy/<int:id>', views.dummy.as_view(template_name="dummy"))
]