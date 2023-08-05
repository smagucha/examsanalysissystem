from django.db import models
from datetime import date
from parent.models import Parent


class CommonInfo(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Klass(CommonInfo):
    pass

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Stream(CommonInfo):
    pass

    def __str__(self):
        return "%s" % (self.name)


class StudentManager(models.Manager):
    def get_total_students(self):
        return (
            self.prefetch_related("class_name", "stream")
            .filter(year=str(date.today().year))
            .count()
        )

    def get_student_list(self):
        return self.prefetch_related("class_name", "stream").filter(
            year=str(date.today().year)
        )

    def get_student_list_class_or_stream(self, name, stream=None):
        query_params = {
            "class_name__name": name,
            "year": str(date.today().year),
        }
        if stream:
            query_params["stream__name"] = stream
        return self.prefetch_related("class_name", "stream").filter(**query_params)

    def all_student_count(self):
        return self.get_student_list().count()

    def class_or_stream_count(self, name, stream=None):
        query_params = {
            "name": name,
        }
        if stream:
            query_params["stream__name"] = stream
        return self.get_student_list_class_or_stream(name, stream).count()


class Student(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Admin_no = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    date_of_admission = models.DateField()
    parent = models.CharField(max_length=50)
    class_name = models.ForeignKey(
        Klass,
        on_delete=models.CASCADE,
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
    )
    gender = models.CharField(max_length=6, choices=GENDER)
    year = models.CharField(
        max_length=4, default=str(date.today().year), blank=True, null=True
    )

    def __str__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def get_student_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    class Meta:
        verbose_name_plural = "students"
        ordering = ["id"]

    objects = models.Manager()
    student = StudentManager()


class AttendManager(models.Manager):
    def get_student_list_stream(self, name, stream):
        return self.prefetch_related("class_name", "stream").filter(
            class_name__name=name, stream__name=stream, year=str(date.today().year)
        )


class Attendance(models.Model):
    Present = (
        ("absent", "absent"),
        ("present", "present"),
    )
    class_name = models.ForeignKey(Klass, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=True)
    dateattend = models.DateField(auto_now_add=True)
    present_status = models.CharField(max_length=10, choices=Present)
    absentwhy = models.CharField(max_length=200, null=True, blank=True)
    year = models.CharField(
        max_length=4, default=str(date.today().year), blank=True, null=True
    )

    def __str__(self):
        return "%s %s %s" % (self.student, self.class_name, self.present_status)

    class Meta:
        ordering = ["id"]

    objects = models.Manager()
    attend = AttendManager()


class StudentParent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
