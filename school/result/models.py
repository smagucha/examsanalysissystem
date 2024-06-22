from django.db import models
from student.models import Student, Klass, Stream
from django.db.models import F
from datetime import date
from django.db.models import Sum


year = str(date.today().year)


class term(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class MarkManager(models.Manager):
    def get_results_for_student(self, subject_name, term, student):
        return (
            self.prefetch_related("student", "Term", "name")
            .filter(name__name=subject_name, Term__name=term, student=student)
            .values_list("marks", flat=True)
        )

    def student_subject_ranking_per_class_or_stream(
        self, name, term, subject, stream=None
    ):
        year = str(date.today().year)
        query_params = {
            "student__class_name__name": name,
            "name__name": subject,
            "Term__name": term,
            "year": year,
        }
        if stream:
            query_params["student__stream__name"] = stream
        return (
            self.filter(**query_params)
            .order_by("-marks")
            .values_list(
                "student__first_name",
                "student__middle_name",
                "student__last_name",
                "name__name",
                "marks",
            )
        )

    def student_result_per_term_class(self, term, student, classname, stream=None):
        query_params = {
            "student__class_name__name": classname,
            "Term__name": term,
            "student": student,
        }
        if stream:
            query_params["student__stream__name"] = stream
        return (
            self.select_related("student", "Term")
            .filter(
                Term__name=term,
                student=student,
                student__class_name__name=classname,
            )
            .values_list("marks", flat=True)
        )

    def get_subject_marks_for_class_or_stream_marks(
        self, student_class_name, Term, subject_name, stream=None
    ):
        query_params = {
            "student__class_name__name": student_class_name,
            "Term__name": Term,
            "name__name": subject_name,
            "year": year,
        }
        if stream:
            query_params["student__stream__name"] = stream

        return self.select_related("student__class_name", "Term", "name").filter(
            **query_params
        )

    def get_subject_marks_for_class_or_stream(
        self, student_class_name, Term, subject_name, stream
    ):
        return self.get_subject_marks_for_class_or_stream_marks(
            student_class_name, Term, subject_name, stream
        ).values_list("marks", flat=True)

    def student_marks(self, student, term):
        query_params = {
            "student": student,
            "Term__name": term,
            "year": year,
        }
        return self.select_related("Term").filter(**query_params)


class Mark(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.ForeignKey(subject, on_delete=models.CASCADE)
    Term = models.ForeignKey(term, on_delete=models.CASCADE, blank=True, null=True)
    marks = models.PositiveIntegerField()
    year = models.CharField(
        max_length=4, default=date.today().year, blank=True, null=True
    )

    def __str__(self):
        return f"{self.student} {self.name} {self.marks}"

    class Meta:
        verbose_name = "Marks"
        verbose_name_plural = "Marks"

    objects = models.Manager()
    mark = MarkManager()


class Grading(models.Model):
    percent = models.PositiveIntegerField()
    name = models.CharField(max_length=2)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.percent}"


class EnrollStudenttosubectManager(models.Manager):
    def get_students_subject(self, name, Subject, stream=None):
        query_params = {
            "class_name__name": name,
            "subject__name": Subject,
            "year": str(date.today().year),
        }
        if stream:
            query_params["stream__name"] = stream
        return self.prefetch_related("class_name", "student", "subject").filter(
            **query_params
        )

    def get_all_students_subject(self):
        return self.prefetch_related(
            "class_name", "stream", "student", "subject"
        ).filter(year=str(date.today().year))

    def get_subjects_for_student_count(self, student):
        return self.get_all_students_subject().filter(student=student).count()

    def student_per_subject_count(self, subject, class_name, stream=None):
        query_params = {
            "class_name__name": class_name,
            "subject__name": subject,
            "year": str(date.today().year),
        }
        if stream:
            query_params["stream__name"] = stream
        return self.filter(**query_params).count()


class EnrollStudenttosubect(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True, null=True)
    class_name = models.ForeignKey(
        Klass, on_delete=models.CASCADE, blank=True, null=True
    )
    year = models.CharField(
        max_length=4, default=date.today().year, blank=True, null=True
    )

    def __str__(self):
        return f"{self.student} {self.subject}"

    objects = models.Manager()
    enroll = EnrollStudenttosubectManager()
