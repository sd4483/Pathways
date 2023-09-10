from django.urls import path, include
from . import views
from .plan_revise_view import planning_view, complete_task_view, revision_view, mark_revision_completed, delete_task_view
from .resources_view import resource_archive_view, image_resource_view, text_resource_view, link_resource_view, file_resource_view, resource_sorted_view, text_resource_delete_view, image_resource_delete_view, link_resource_delete_view, file_resource_delete_view

urlpatterns = [
    path('', views.view_pathway_view, name='view_pathway'),
    path('create/', views.create_pathway_view, name='create_pathway'),
    path('tinymce/', include('tinymce.urls')),
    path('pathway/<int:pathway_id>/', views.single_pathway_view, name='single_pathway'),
    path('pathway/<int:pathway_id>/resources/', resource_archive_view, name='resource_archive'),
    path('pathway/<int:pathway_id>/resources-sorted/', resource_sorted_view, name='resource_sorted'),
    path('pathway/<int:pathway_id>/settings/', views.pathway_settings_view, name='pathway_settings'),
    path('pathway/<int:pathway_id>/discussion/', views.pathway_comments_view, name='pathway_comments'),
    path('pathway/discussion/replies/<int:comment_id>/', views.pathway_reply_view, name='pathway_comments_replies'),
    path('pathway/<int:pathway_id>/upvote/', views.upvote_pathway_view, name='upvote_pathway'),
    path('pathway/<int:pathway_id>/downvote/', views.downvote_pathway_view, name='downvote_pathway'),
    path('pathway/<int:pathway_id>/add-text', text_resource_view, name='text_resource'),
    path('pathway/<int:pathway_id>/add-link', link_resource_view, name='link_resource'),
    path('pathway/<int:pathway_id>/add-image', image_resource_view, name='image_resource'),
    path('pathway/<int:pathway_id>/add-file', file_resource_view, name='file_resource'),
    path('<int:pathway_id>/text-resource/<int:resource_id>/delete/', text_resource_delete_view, name='delete_text_resource'),
    path('<int:pathway_id>/image-resource/<int:resource_id>/delete/', image_resource_delete_view, name='delete_image_resource'),
    path('<int:pathway_id>/link-resource/<int:resource_id>/delete/', link_resource_delete_view, name='delete_link_resource'),
    path('<int:pathway_id>/file-resource/<int:resource_id>/delete/', file_resource_delete_view, name='delete_file_resource'),
    path('delete_pathway/<int:pathway_id>/', views.delete_pathway_view, name='delete_pathway'),
    path('pathway/<int:pathway_id>/planning/', planning_view, name='planning'),
    path('pathway/<int:pathway_id>/planning/<int:task_id>/delete', delete_task_view, name='delete_task'),
    path('pathway/<int:pathway_id>/revision/', revision_view, name='revision'),
    path('pathway/<int:pathway_id>/complete-task/<int:task_id>/', complete_task_view, name='complete_task'),
    path('mark_revision_completed/<int:revision_id>/', mark_revision_completed, name='mark_revision_completed'),
    path('pathways/<int:pathway_id>/follow/', views.follow_pathway, name='follow_pathway'),
    path('unfollow_pathway/<int:pathway_id>/', views.unfollow_pathway, name='unfollow_pathway'),
]