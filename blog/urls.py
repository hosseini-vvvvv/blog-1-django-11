from django.urls import path
# from .views import home, detail, category, index, PostListView,site,UserAccount,ContactUs,SharePost
from .views import *
# from . import views
app_name = "blog"
urlpatterns = [
    path('post/index', index, name="index"),
    path('', home, name="home"),
    
    
    
    path('post/contact-us',ContactUs,name="contact_us"),
    # path('post/users', PostListView.as_view(), name="users"),
    path('post/userAccount',UserAccount, name="userAccount"),
    
    
    path('post/users', users, name="users"),  #for TAG
    path('post/users/<slug:tag_slug>/',users,name="users_tag"),  #for TAG
    
    path('post/users/<slug:slug>/<int:pk>/', site, name="site"),
    
    
    path('share_post/<int:post_id>/',SharePost,name="share_post"),
    path('search',search,name="search"),
    path('login',user_login,name="login"),
    path('logout',user_logout,name="logout"),
    path('change_password',change_password,name="change_password"),
    
    
    
    
    path('post/<slug:slug>', detail, name="detail"),
    path('category/<slug:slug>', category, name="category"),
   

]
