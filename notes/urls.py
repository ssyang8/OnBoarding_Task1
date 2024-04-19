from . import views
from django.urls import path
from .views import edit_plain_note, edit_highlighted_note, delete_note


app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:article_id>/', views.article_view, name='article_view'),
    path('new_article/', views.new_article, name='new_article'),
    path('article/<int:article_id>/add_highlighted_note/',
         views.add_highlighted_note, name='add_highlighted_note'),
    path('delete/<int:note_id>/', delete_note, name='delete_note'),


    path('delete_highlighted_note/<int:note_id>/',
         views.delete_highlighted_note, name='delete_highlighted_note'),
    path('edit_plain_note/<int:note_id>/',
         edit_plain_note, name='edit_plain_note'),
    path('edit_highlighted_note/<int:note_id>/',
         edit_highlighted_note, name='edit_highlighted_note'),

]
