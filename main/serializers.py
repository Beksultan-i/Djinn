from rest_framework import serializers
from .models import Category, Post, PostImage, Comment, Like


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
         model = PostImage
         fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super(PostImageSerializer, self).to_representation(instance)
        representation['images'] = self._get_image_url(instance)
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created_at = serializers.DateTimeField(format='%d/%m%Y %H:%M:%S', read_only=True)
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        post = Post.objects.create(author=author, **validated_data)
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=instance, image=image)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comments = CommentSerializer(instance.comments.all(), many=True).data
        likes = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data
        representation['comments'] = comments
        representation['likes'] = likes

        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post', 'like')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('like')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')
        like = Like.objects.get_or_create(user=user, post=post)[0]
        like.like = True if like.like is False else False
        like.save()
        return like

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['like'] = instance.like
        representation['user'] = instance.user.email
        return representation
