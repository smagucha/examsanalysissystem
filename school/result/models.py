from django.db import models
from student.models import Student, Klass, Stream
from django.db.models import F
from datetime import date

year=str(date.today().year)

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
    def get_results(self, name, term, student):
        return (
            self.select_related("student", "Term", "name")
            .filter(name__name=name, Term__name=term, student=student)
            .values_list("marks", flat=True)
        )

    def get_results_stream(self, name, term, student_class_name, stream):
        return (
            self.select_related("student", "Term", "name")
            .filter(
                name__name=name,
                Term__name=term,
                student__class_name__name=student_class_name,
                student__stream__name=stream,
            )
            .values_list("marks", flat=True)
        )

    def student_result_per_term_class(self, term, student, classname):
        return self.select_related("student", "Term").filter(
            Term__name=term, 
            student=student,
            student__class_name__name = classname,
            ).values_list(
                "marks", 
                flat=True
                )
    def get_subject_marks_stream(self, student_class_name, Term, subject_name, stream):
        return (
            self.select_related("student__class_name", "Term", "name")
            .filter(
                student__class_name__name=student_class_name,
                Term__name=Term,
                subject_name__name=name,
                student__stream__name= stream,
            )
            .values_list("marks", flat=True)
        )

    def get_subject_marks(self, student_class_name, Term, subject_name):
        return (
            self.select_related("student__class_name", "Term", "name")
            .filter(
                student__class_name__name=student_class_name,
                Term__name=Term,
                name__name=subject_name,
            )
            .values_list("marks", flat=True)
        )


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
    def get_students_subject(self, name, stream, Subject):
        return self.select_related("class_name", "stream", "student", "subject").filter(
            class_name__name=name,
            stream__name=stream,
            subject__name=Subject,
            year=str(date.today().year),
        )

    def get_all_students_subject(self):
        return self.select_related("class_name", "stream", "student", "subject").filter(
            year=str(date.today().year)
        )

    def get_subjects_for_student_count(self, student):
        return self.get_all_students_subject().filter(student=student).count()

    def student_per_subject_count(self, subject, class_name):
        return (
            self.select_related()
            .filter(subject__name=subject, class_name__name=class_name)
            .count()
        )


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
