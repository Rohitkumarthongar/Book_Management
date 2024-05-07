from rest_framework import serializers
from .models import User, Book, ReadingList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = '__all__'