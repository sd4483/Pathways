from django.urls import path, include
from . import views

urlpatterns = [
    path('view/', views.view_pathway_view, name='view_pathway'),
    path('create/', views.create_pathway_view, name='create_pathway'),
    path('tinymce/', include('tinymce.urls')),
    path('pathway/<int:pathway_id>/', views.single_pathway_view, name='single_pathway'),
    path('pathway/<int:pathway_id>/resources', views.resource_archive_view, name='resource_archive'),
    path('pathway/<int:pathway_id>/settings/', views.pathway_settings_view, name='pathway_settings'),
    path('pathway/<int:pathway_id>/discussion/', views.pathway_comments_view, name='pathway_comments'),
    path('pathway/discussion/replies/<int:comment_id>/', views.pathway_reply_view, name='pathway_comments_replies'),
    path('pathway/<int:pathway_id>/upvote/', views.upvote_pathway_view, name='upvote_pathway'),
    path('pathway/<int:pathway_id>/downvote/', views.downvote_pathway_view, name='downvote_pathway'),
    path('pathway/<int:pathway_id>/add-text', views.text_resource_view, name='text_resource'),
    path('pathway/<int:pathway_id>/add-link', views.link_resource_view, name='link_resource'),
    path('pathway/<int:pathway_id>/add-image', views.image_resource_view, name='image_resource'),
    path('pathway/<int:pathway_id>/add-file', views.file_resource_view, name='file_resource'),
    path('delete_pathway/<int:pathway_id>/', views.delete_pathway_view, name='delete_pathway'),
]