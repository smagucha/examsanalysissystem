from django.shortcuts import render, redirect, get_object_or_404
from .models import EnrollStudenttosubect, Mark, subject, term, Grading
from student.models import Student, Klass, Stream, Attendance
from parent.models import Parent
from .forms import subjectForm, TermForm, GradeForm, EnrollForm
from django.contrib.auth.decorators import login_required
from datetime import date
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import xlwt
from student.views import (
    database_operation,
    delete_database_operation,
)

year = str(date.today().year)


def generate_excel(name, term, subjectname, sorttotalfinal, stream=None):
    name = f"{name} {term} result"
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=results.xls "

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Users")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Rank", "Student"]
    for xubject in subjectname:
        columns.append(xubject.name)
    columns.append("Total")
    columns.append("Grade")
    columns.append("Points")
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = sorttotalfinal
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def generate_pdf(template_name, context):
    template_path = template_name
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="/accounts/login/")
def getsubjects(request, classname, term=None, streamname=None, template_name=None):
    context = {
        "subjects": subject.objects.all(),
        "classname": classname,
        "streamname": streamname,
        "term": term,
    }
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def terms(request, classname, streamname=None, subject=None, template_name=None):
    context = {
        "allterms": term.objects.all(),
        "classname": classname,
        "streamname": streamname,
        "subject": subject,
    }
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def student_view(request, id, name, format=None, template_name=None):
    student = get_object_or_404(Student, id=id)
    totalclass = Student.student.class_or_stream_count(name)
    streamtotal = Student.student.class_or_stream_count(name, student.stream)
    subjectname = subject.objects.all()
    terms = term.objects.all()
    student_stream = Student.student.get_student_list_class_or_stream(
        name=student.class_name, stream=student.stream
    )
    Getgrading = getgrade()
    student_class = Student.student.get_student_list_class_or_stream(
        name=student.class_name
    )
    getterm = {}
    getclassrankid = []
    getstreamrankid = []
    streamnumber = None
    classnumber = None
    getavg = None
    Gradeterm = None
    points = []
    totalmarks = 0
    getsubjectcount = EnrollStudenttosubect.enroll.get_subjects_for_student_count(
        student=student
    )
    outsubject = getsubjectcount * 100
    q = []

    for getterms in terms:
        termresults = []
        for sub in subjectname:
            studentmarks = list(
                Mark.objects.filter(
                    Term__name=getterms, name__name=sub, student=student, year=year
                ).values_list("marks", flat=True)
            )
            if not studentmarks:
                studentmarks = [""]
            termresults.extend(studentmarks)
        getmark = get_student_marks(student, getterms, year)
        totalmarks = sum([i for i in termresults if i != ""])
        getavg, Gradeterm = calculate_average_and_get_grades(
            getmark, id, student, Getgrading, totalmarks, getsubjectcount
        )
        termresults.append(totalmarks)
        getterm[getterms] = termresults
        getclassnumber, getstreamnumber = get_all_student_result_for_class_and_stream(
            student_stream, student_class, getterms
        )

        classnumber = calculate_class_rank(
            getclassnumber, student, totalclass, getclassrankid
        )
        streamnumber = calculate_stream_rank(getstreamnumber, student, getstreamrankid)
        getterm, q = update_term_results(
            getterm,
            getterms,
            getclassrankid,
            getstreamrankid,
            totalmarks,
            getsubjectcount,
            Getgrading,
            getmark,
            student,
            totalclass,
            q,
        )
    context = {
        "Grade": Gradeterm,
        "outsubject": outsubject,
        "totalmarks": totalmarks,
        "classnumber": classnumber,
        "streamtotal": streamtotal,
        "classname": name,
        "totalclass": totalclass,
        "streamnumber": streamnumber,
        "getterm": getterm,
        "title": "student details",
        "subject": subjectname,
        "terms": terms,
        "points": points,
        "student": student,
        "q": q,
    }

    if format == "pdf":
        return generate_pdf(template_name, context)

    return render(request, "result/student.html", context)


@login_required(login_url="/accounts/login/")
def enteresult(request, name, stream, Term, Subject):
    exam = EnrollStudenttosubect.enroll.get_students_subject(
        name=name, stream=stream, Subject=Subject
    )
    result = [[] for _ in range(4)]
    if request.method == "POST":
        getmarks = request.POST.getlist("subjectname")
        result[0] = [i.student.id for i in exam]
        result[1] = [subject.objects.get(name=Subject).id for i in exam]
        result[2] = [term.objects.get(name=Term).id for i in exam]
        result[3] = getmarks
        for j in range(len(result[0])):
            Marks = Mark.objects.create(
                student_id=result[0][j],
                name_id=result[1][j],
                Term_id=result[2][j],
                marks=int(result[3][j]),
            )
            Marks.save()
        return redirect("student:home")
    context = {
        "exam": exam,
        "name": name,
        "stream": stream,
        "term": term,
        "subject": Subject,
    }
    return render(request, "result/enterresult.html", context)


@login_required(login_url="/accounts/login/")
def streamexamanalysis(
    request, name, term, stream=None, template_name=None, format=None
):
    subjects = subject.objects.all()
    avg_subject = get_average_subject_marks(name, term, stream, subjects)
    best_students_data = get_best_students_data(name, term, stream, subjects)
    grades_count = get_grades_count(name, term, stream)

    context = {
        "z": best_students_data,
        "name": name,
        "term": term,
        "avgsubject": avg_subject,
        "subject": subjects,
        "Count": grades_count,
    }

    if stream:
        context["stream"] = stream

    if format == "pdf":
        return generate_pdf(template_name, context)

    return render(request, template_name, context)


def get_marks_for_class_or_stream(name, term, stream, subject):
    marks = Mark.mark.get_subject_marks_for_class_or_stream(
        student_class_name=name, Term=term, subject_name=subject.name, stream=stream
    )
    return marks


def get_average_subject_marks(name, term, stream, subjects):
    avg_subject = {}
    for subject in subjects:
        marks = get_marks_for_class_or_stream(name, term, stream, subject)
        student_count = EnrollStudenttosubect.enroll.student_per_subject_count(
            subject=subject, class_name=name
        )
        subject_marks = list(marks)
        if subject_marks:
            avg_subject[subject.name] = calculate_average(
                sum(subject_marks), student_count
            )
    return avg_subject


# reuse function  from line 304
def get_best_students_data(name, term, stream, subjects):
    best_students_data = []
    for subject in subjects:
        marks = get_marks_for_class_or_stream(name, term, stream, subject)
        if not marks:
            continue

        max_mark = max(marks)
        best_student = Mark.objects.get(
            student__class_name__name=name,
            Term__name=term,
            name__name=subject.name,
            marks=max_mark,
            year=year,
        )
        best_students_data.append(
            (best_student.student.get_student_name(), subject.name, max_mark)
        )

    return best_students_data


def get_grades_count(name, term, stream):
    Getgrading = Grading.objects.all()
    students = get_students_by_class_and_stream(name, stream)
    grades = []
    for student in students:
        marks = Mark.objects.filter(Term__name=term, student=student).values_list(
            "marks", flat=True
        )
        marks = [int(m) for m in marks if m != ""]
        if not marks:
            continue
        avg_mark = round(calculate_average(sum(marks), len(marks)), 1)
        grades.append(get_grade(Getgrading, avg_mark).name)
    grades_count = {}
    for grading in Getgrading:
        grades_count[grading.name] = grades.count(grading.name)

    return grades_count


# test done
@login_required(login_url="/accounts/login/")
def addsubject(request):
    return database_operation(request, subjectForm)


# test done
@login_required(login_url="/accounts/login/")
def AddTerm(request):
    return database_operation(request, TermForm)


# test done
@login_required(login_url="/accounts/login/")
def addGrade(request):
    return database_operation(request, GradeForm)


@login_required(login_url="/accounts/login/")
def allGrade(request):
    return render(
        request,
        "result/allgrading.html",
        context={"allgrade": Grading.objects.all().order_by("name")},
    )


# remove this is a duplicate
@login_required(login_url="/accounts/login/")
def allsubject(request):
    return render(
        request,
        "result/subjectall.html",
        context={"allsubjects": subject.objects.all()},
    )


@login_required(login_url="/accounts/login/")
def allterm(request):
    return render(
        request,
        "result/allterm.html",
        context={"allterm": term.objects.all()},
    )


@login_required(login_url="/accounts/login/")
def deleteterm(request, id):
    return delete_database_operation(request, term, id)


@login_required(login_url="/accounts/login/")
def enrollStudenttosubectall(request):
    allenroll = EnrollStudenttosubect.enroll.get_all_students_subject()
    context = {
        "title": "allenrollsubject",
        "allenroll": allenroll,
    }
    return render(request, "result/allenroll.html", context)


@login_required(login_url="/accounts/login/")
def deletegrade(request):
    return delete_database_operation(request, Grading, id)


@login_required(login_url="/accounts/login/")
def updatesubject(request):
    return database_operation(request, subjectForm, id)


@login_required(login_url="/accounts/login/")
def subjectdelete(request):
    return delete_database_operation(request, subject, id)


@login_required(login_url="/accounts/login/")
def Enrollupdate(request, id):
    return database_operation(request, EnrollForm, id)


@login_required(login_url="/accounts/login/")
def enrolldelete(request, id):
    return delete_database_operation(request, EnrollStudenttosubect, id)


@login_required(login_url="/accounts/login")
def enrollstudentstosubject(request, name, stream):
    getstudents = get_students_by_class_and_stream(name, stream)
    getsubjects = subject.objects.all()
    if request.method == "POST":
        getsubjectid = request.POST.getlist("subjectid")
        getstudentsub = []
        for i in getstudents:
            getstudentsub.append(i.id)
        for i in range(len(getstudents)):
            if getsubjectid[i]:
                enrolltosubject = EnrollStudenttosubect.objects.create(
                    student_id=getstudentsub[i],
                    subject_id=subject.objects.get(name=getsubjectid[i]).id,
                    stream_id=Stream.objects.get(name=stream).id,
                    class_name_id=Klass.objects.get(name=name).id,
                )
                enrolltosubject.save()
    context = {"getstudents": getstudents, "getsubjects": getsubjects}
    return render(request, "result/studentenroll.html", context)


# reuse function  from line 304
@login_required(login_url="/accounts/login/")
def subjectperrank(
    request, name, term, subject, stream=None, template_name=None, format=None
):
    rankings_data = Mark.mark.student_subject_ranking_per_class_or_stream(
        name, term, subject, stream
    )
    context = {
        "name": name,
        "term": term,
        "stream": stream,
        "subject": subject,
        "rankings_data": rankings_data,
    }

    if format == "pdf":
        return generate_pdf(template_name, context)
    else:
        return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def getresultstreamterm(
    request, name, term, stream=None, template_name=None, format=None
):
    subjects = subject.objects.all()
    students = get_students_by_class_and_stream(name, stream)
    results = collect_student_marks(students, subjects, term)
    sorted_results = sort_results_by_total_marks(results)
    indexed_results = add_index_to_results(sorted_results)

    avg_marks = calculate_average_marks_and_grading(indexed_results)

    context = {
        "page_obj": indexed_results,
        "subject_list": subjects,
        "class_name": name,
        "term": term,
    }
    if stream:
        context["stream"] = stream

    if format == "ms-excel":
        return generate_excel(name, term, subjects, indexed_results, stream=None)

    return render(request, template_name, context)


def get_students_by_class_and_stream(name, stream):
    query_params = {"class_name__name": name}
    if stream:
        query_params["stream__name"] = stream
    return Student.objects.filter(**query_params)


def collect_student_marks(students, subjects, term):
    results = []
    for student in students:
        marks = []
        for subjectname in subjects:
            marks_list = list(
                Mark.objects.filter(
                    student=student, name=subjectname, Term__name=term
                ).values_list("marks", flat=True)
            )
            if not marks_list:
                marks_list = [""]
            marks += marks_list
        marks_sum = sum([int(mark) for mark in marks if mark != ""])
        marks.append(str(marks_sum))
        marks.insert(0, str(student))
        results.append(marks)
    return results


def sort_results_by_total_marks(results):
    return sorted(results, key=lambda x: x[-1], reverse=True)


def add_index_to_results(results):
    return [[index] + result for index, result in enumerate(results, start=1)]


def calculate_average_marks_and_grading(indexed_results):
    avg_marks = []
    grading_system = Grading.objects.all()
    for result in indexed_results:
        subject_marks = result[2:-2]
        subject_marks_with_value = [int(mark) for mark in subject_marks if mark != ""]
        total_marks = sum(subject_marks_with_value)
        num_subjects = len(subject_marks_with_value)
        avg_mark = calculate_average(total_marks, num_subjects)
        avg_marks.append(avg_mark)
        result.append(get_grade(grading_system, avg_mark).name)
        result.append(get_grade(grading_system, avg_mark).points)
    return avg_marks


def error_404(request, exception):
    return render(request, "student/404.html")


def calculate_average_and_get_grades(
    getmark, id, student, Getgrading, totalmarks, getsubjectcount
):
    getavg = calculate_average(totalmarks, getsubjectcount)
    Gradeterm = None
    Gradeterm = get_grade(Getgrading, getavg)
    return getavg, Gradeterm


def get_all_student_result_for_class_and_stream(
    student_stream, student_class, getterms
):
    getclassnumber, getstreamnumber = {}, {}
    for idstudent in student_class:
        marks = list(
            Mark.objects.filter(student=idstudent, Term__name=getterms).values_list(
                "marks", flat=True
            )
        )
        if sum(marks):
            getclassnumber[idstudent.id] = sum(marks)

    for idstudent in student_stream:
        marks = list(
            Mark.objects.filter(student=idstudent, Term__name=getterms).values_list(
                "marks", flat=True
            )
        )
        if sum(marks):
            getstreamnumber[idstudent.id] = sum(marks)

    return getclassnumber, getstreamnumber


def get_student_marks(student, getterms, year):
    getmark = Mark.objects.filter(
        student=student, Term__name=getterms, year=student.year
    )
    return getmark


def calculate_class_rank(getclassnumber, student, totalclass, getclassrankid):
    if getclassnumber:
        sortedid = dict(sorted(getclassnumber.items(), key=lambda item: item[1])[::-1])
        getclassrank = list(sortedid.keys())
        classnumber = getclassrank.index(student.id) + 1
        getnumbers = f"{classnumber}/{totalclass}"
        getclassrankid.append(getnumbers)
        return classnumber


def calculate_stream_rank(getstreamnumber, student, getstreamrankid):
    if getstreamnumber:
        sorted_id = dict(
            sorted(getstreamnumber.items(), key=lambda item: item[1], reverse=True)
        )
        getstreamrank = list(sorted_id.keys())
        streamnumber = getstreamrank.index(student.id) + 1
        getnumbers = f"{streamnumber}/{len(getstreamrank)}"
        getstreamrankid.append(getnumbers)
        return streamnumber


def update_term_results(
    getterm,
    getterms,
    getclassrankid,
    getstreamrankid,
    totalmarks,
    getsubjectcount,
    Getgrading,
    getmark,
    student,
    totalclass,
    q,
):
    a = 0
    if getterm:
        try:
            getterm[getterms] = (
                [getstreamrankid[a]] + [getclassrankid[a]] + getterm[getterms]
            )
            a += 1
            calcavg = round(calculate_average(totalmarks, getsubjectcount))
            getterm[getterms].append(get_grade(Getgrading, calcavg).name)
            getterm[getterms].append(get_grade(Getgrading, calcavg).points)

        except IndexError:
            pass
        q = subject_ranking_per_class_and_stream(
            getmark, student, Getgrading, totalclass, q
        )
    return getterm, q


def subject_ranking_per_class_and_stream(getmark, student, Getgrading, totalclass, q):
    for i in getmark:
        subjectrank = []
        subjectrank.append(i.name.name)
        subjectrank.append(i.marks)
        subjectrank.append(get_grade(Getgrading, i.marks).name)
        subjectrankclass = list(
            Mark.objects.filter(
                student__class_name__name=student.class_name,
                name__name=i.name,
                Term__name=i.Term,
                year=student.year,
            )
            .values_list("student", flat=True)
            .order_by("-marks")
        )
        getnu = f"{subjectrankclass.index(student.id)+1}/{totalclass}"
        subjectrank.append(getnu)
        q.append(subjectrank)
    return q


def getgrade():
    return Grading.objects.all()


def get_grade(grades, percent_or_marks):
    grade_name = None
    for grade in grades:
        if percent_or_marks >= grade.percent and percent_or_marks <= 100:
            grade_name = grade
            break
    return grade_name


def calculate_average(totalmarks, divider):
    try:
        getaverage = totalmarks / divider
    except ZeroDivisionError:
        getaverage = 0
    return getaverage
