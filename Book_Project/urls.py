# urls.py
from django.urls import path
from Book_Management import views as book

urlpatterns = [
    path('users/', book.get_all_users),
    path('user/register/', book.user_register),
    path('user/login/', book.user_login),
    path('book/', book.create_book),
    path('book/<int:pk>/', book.book_detail),
    path('book/<int:reading_list_id>/add_book/<int:book_id>/', book.add_book_to_reading_list),
    path('book/<int:reading_list_id>/remove_book/<int:book_id>/', book.remove_book_from_reading_list),
]
