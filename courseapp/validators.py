
from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, url):
        self.url = url

    def __call__(self, obj):
        url = dict(obj).get(self.url)
        if "youtube.com" not in url:
            raise ValidationError("Пчел, здесь котируется только youtube.com")
