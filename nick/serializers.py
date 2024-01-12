from rest_framework import serializers

from .models import *

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "tmdb_id"]

class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "name", "tmdb_id"]

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name", "tmdb_id"]

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "tmdb_id"]

class TitleSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    companies = CompanySerializer(many=True)
    
    class Meta:
        model = Title
        fields = '__all__'



