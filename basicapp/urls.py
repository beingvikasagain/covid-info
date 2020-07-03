from django.urls import path
from basicapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('registration',views.user_registration,name='user_registration'),
    path('login',views.user_login,name='user_login'),
    path('logout',views.user_logout,name='user_logout'),
    path('blog',views.PostListView.as_view(),name='post_list'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('blog/new',views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/publish',views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts',views.DraftList.as_view(), name='post_draft_list'),
    path('post/<int:pk>/edit',views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/comment',views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve',views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove',views.comment_delete, name='comment_delete'),
]
