from .models import Klass, Stream


def get_class():
    return Klass.objects.all()


def get_stream():
    return Stream.objects.all()
