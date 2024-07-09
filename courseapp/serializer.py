from rest_framework import serializers

from courseapp.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def create(self, validated_data):
        lessons = validated_data.pop('lesson')

        course = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(course=course, **lesson)
        return course
