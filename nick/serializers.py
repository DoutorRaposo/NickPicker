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


"""All the serializers for many to many are just so we can show in the title serializer, that will be used for fetching data from the movies"""

class TitleSerializer(serializers.HyperlinkedModelSerializer):
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(many=True)
    keywords = KeywordSerializer(many=True)
    companies = CompanySerializer(many=True)
    # This one here is just so we can also use the ID in the model serializer
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"
