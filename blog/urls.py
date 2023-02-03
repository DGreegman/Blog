from django.urls import path
from . import views


app_name = 'blog' #This allows you to organize URLs by application and use the name when referring to them

urlpatterns = [
    #post views
    path('', views.PostListView.as_view(), name='post_list'),
    #path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
