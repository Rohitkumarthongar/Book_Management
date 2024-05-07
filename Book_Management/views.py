# views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book, ReadingList
from .serializers import UserSerializer, BookSerializer, ReadingListSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({"message": "Username, email, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"token": token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book_to_reading_list(request, reading_list_id, book_id):
    try:
        reading_list = ReadingList.objects.get(id=reading_list_id)
    except ReadingList.DoesNotExist:
        return Response({"message": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    reading_list.books.add(book)
    serializer = ReadingListSerializer(reading_list)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_book_from_reading_list(request, reading_list_id, book_id):
    try:
        reading_list = ReadingList.objects.get(id=reading_list_id)
    except ReadingList.DoesNotExist:
        return Response({"message": "Reading list not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    reading_list.books.remove(book)
    serializer = ReadingListSerializer(reading_list)
    return Response(serializer.data)
