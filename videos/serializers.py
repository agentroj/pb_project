from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
    source_post_id = serializers.CharField()
    post_url = serializers.URLField()
    post_description = serializers.CharField()
    post_created = serializers.DateField(format="%m/%d/%y", input_formats=["%m/%d/%y"])
    likes_count = serializers.IntegerField(min_value=0)
    shares_count = serializers.IntegerField(min_value=0)
    views_count = serializers.IntegerField(min_value=0)
    comments_count = serializers.IntegerField(min_value=0)
