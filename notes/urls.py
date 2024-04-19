from . import views
from django.urls import path
from .views import article_view, delete_note


app_name = 'notes'  # Namespace for the notes app

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:article_id>/', views.article_view, name='article_view'),
    path('new_article/', views.new_article, name='new_article'),
    path('delete_note/<str:note_type>/<int:note_id>/',
         views.delete_note, name='delete_note'),

    path('article/<int:article_id>/add_highlighted_note/',
         views.add_highlighted_note, name='add_highlighted_note'),
]
