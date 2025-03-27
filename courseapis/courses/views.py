# from crypt import methods
from calendar import c
from threading import activeCount
# import bcrypt
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from  courses import  serializers, paginators
from courses.models import Category, Course, Lesson, User


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active = True)
    serializer_class =  serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True )
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePagination

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q :
            queryset = queryset.filter(subject__icontains = q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id = cate_id )
        return queryset

    @action(methods=['get'], detail = True, url_path = 'lessons')
    def get_lesson(self,request,pk):
        lessons = self.get_object().lesson_set.filter(active = True)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status= status.HTTP_200_OK)

class LessonViewSet(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailSerializer

    @action(methods=['get'], detail = True, url_path = 'comments')
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').filter(active = True)
        return Response(serializers.CommentSerializer(comments, many=True).data, status= status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]
