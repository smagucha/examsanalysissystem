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
    getterms = term.objects.all()
    context = {
        "allterms": getterms,
        "classname": classname,
        "streamname": streamname,
        "subject": subject,
    }
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def student_view(request, id, name, format=None, template_name=None):
    student = get_object_or_404(Student, id=id)
    totalclass = Student.student.class_count(name=name)
    streamtotal = Student.student.stream_count(name=name, stream=student.stream)
    subjectname = subject.objects.all()
    terms = term.objects.all()
    student_stream = Student.student.get_student_list_stream(
        name=student.class_name, stream=student.stream
    )
    Getgrading = Grading.objects.all()
    student_class = Student.student.get_student_list_class(name=student.class_name)
    getterm = {}
    getclassrankid = []
    getstreamrankid = []
    streamnumber = None
    classnumber = None
    getavg = None
    Gradeterm = None
    points = []
    totalmarks = 0
    finalsub = []
    a = 0
    getsubjectcount = EnrollStudenttosubect.enroll.get_subjects_for_student_count(
        student=student
    )
    outsubject = getsubjectcount * 100
    q = []

    for getterms in terms:
        termreuslts = []
        getidnumber = {}
        getstreamidnumber = {}
        rankingsubject = {}

        for sub in subjectname:
            studentmarks = list(
                Mark.objects.filter(
                    student=student, Term__name=getterms, name__name=sub
                ).values_list("marks", flat=True)
            )
            termreuslts.extend(studentmarks)

        getmark = Mark.objects.filter(
            student=student, Term__name=getterms, year=student.year
        )
        totalmarks = sum(
            list(getmark.filter(Term__name=getterms).values_list("marks", flat=True))
        )

        try:
            getavg = totalmarks / getsubjectcount
        except ZeroDivisionError:
            getavg = 0

        for j in Getgrading:
            if getavg >= j.percent and getavg <= 100:
                Gradeterm = j.name
                break

        getdonesubects = [i for i in termreuslts if i != ""]
        if getdonesubects:
            termreuslts.append(sum(getdonesubects))
            getterm[getterms] = termreuslts

        for idstudent in student_class:
            marks = list(
                Mark.objects.filter(student=idstudent, Term__name=getterms).values_list(
                    "marks", flat=True
                )
            )
            if sum(marks):
                getidnumber[idstudent.id] = sum(marks)

        for idstudent in student_stream:
            marks = list(
                Mark.objects.filter(student=idstudent, Term__name=getterms).values_list(
                    "marks", flat=True
                )
            )
            if sum(marks):
                getstreamidnumber[idstudent.id] = sum(marks)

        if getidnumber:
            sortedid = dict(sorted(getidnumber.items(), key=lambda item: item[1])[::-1])
            getclassrank = list(sortedid.keys())
            classnumber = getclassrank.index(student.id) + 1
            getnumbers = f"{classnumber}/{totalclass}"
            getclassrankid.append(getnumbers)

        if getstreamidnumber:
            sortedid = dict(
                sorted(getstreamidnumber.items(), key=lambda item: item[1])[::-1]
            )
            getstreamrank = list(sortedid.keys())
            streamnumber = getstreamrank.index(student.id) + 1
            getnumbers = f"{streamnumber}/{streamtotal}"
            getstreamrankid.append(getnumbers)

        if getterm:
            getterm[getterms] = (
                [getstreamrankid[a]] + [getclassrankid[a]] + getterm[getterms]
            )
            a += 1
            calcavg = round(totalmarks / getsubjectcount)
            for j in Getgrading:
                if calcavg >= j.percent and calcavg <= 100:
                    getterm[getterms].append(j.name)
                    getterm[getterms].append(j.points)
                    break

        for i in getmark:
            subjectrank = []
            subjectrank.append(i.name.name)
            Grade = None
            subjectrank.append(i.marks)
            for j in Getgrading:
                if i.marks >= j.percent and i.marks <= 100:
                    Grade = j.name
                    subjectrank.append(Grade)
                    break
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
            getnu = f"{subjectrankclass.index(student.id)}/{totalclass}"
            subjectrank.append(getnu)
            q.append(subjectrank)

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
        "getmark": getmark,
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
    avg_subject = {}
    subject_marks = {}
    subjects = subject.objects.all()
    for Subject in subjects:
        if stream:
            marks = Mark.mark.get_results_stream(
                student_class_name=name, term=term, name=Subject.name, stream=stream
            )
            student_count = EnrollStudenttosubect.enroll.student_per_subject_count(
                subject=Subject, class_name=name
            )
        else:
            marks = Mark.mark.get_subject_marks(
                student_class_name=name, Term=term, subject_name=Subject.name
            )
            student_count = EnrollStudenttosubect.enroll.student_per_subject_count(
                subject=Subject, class_name=name
            )
        subject_marks[Subject.name] = list(marks)
        if subject_marks:
            try:
                avg_subject[Subject.name] = (
                    sum(subject_marks[Subject.name]) / student_count
                )
            except:
                avg_subject[Subject.name] = 0

    best_students = []
    best_marks = []
    best_subjects = []

    filter_kwargs = {"student__class_name__name": name, "Term__name": term}
    if stream:
        filter_kwargs["student__stream__name"] = stream
    for Subject in subjects:
        subject_filter_kwargs = {"name__name": Subject}
        marks = Mark.objects.filter(
            **filter_kwargs, **subject_filter_kwargs
        ).values_list("marks", flat=True)
        if not marks:
            continue
        max_mark = max(marks)
        best_student = Mark.objects.get(
            student__class_name__name=name,
            Term__name=term,
            name__name=Subject.name,
            marks=max_mark,
            year=year,
        )
        best_students.append(best_student.student.get_student_name())
        best_marks.append(max_mark)
        best_subjects.append(Subject.name)

    z = zip(best_students, best_subjects, best_marks)

    Getgrading = Grading.objects.all()
    if stream:
        students = Student.student.get_student_list_stream(name=name, stream=stream)
    else:
        students = Student.student.get_student_list_class(name=name)

    grades = []
    for student in students:
        marks = Mark.objects.filter(Term__name=term, student=student).values_list(
            "marks", flat=True
        )
        marks = [int(m) for m in marks if m != ""]
        if not marks:
            continue
        avg_mark = round(sum(marks) / len(marks), 1)
        for grading in Getgrading:
            if avg_mark >= grading.percent and avg_mark <= 100:
                grades.append(grading.name)
                break

    Count = {}
    for i in Getgrading:
        Count[i.name] = grades.count(i.name)
    context = {
        "z": z,
        "name": name,
        "term": term,
        "avgsubject": avg_subject,
        "subject": subject.objects.all(),
        "Count": Count,
    }
    if stream:
        context["stream"] = stream

    if format == "pdf":
        return generate_pdf(template_name, context)
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def addsubject(request):
    if request.method == "POST":
        form = subjectForm(request.POST)
        if form.is_valid():
            form.save()
            form = subjectForm()
    else:
        form = subjectForm()
    context = {"form": form, "title": "add subjects"}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def AddTerm(request):
    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("result:allterm")
    else:
        form = TermForm()
    context = {"form": form, "title": "add term"}

    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def AddGrade(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            form = GradeForm()
            return redirect("student:home")
    else:
        form = GradeForm()
    context = {"form": form, "title": "add Grade"}

    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def allGrade(request):
    return render(
        request,
        "result/allgrading.html",
        context={"allgrade": Grading.objects.all().order_by("name")},
    )


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
def enrollStudenttosubectall(request):
    allenroll = EnrollStudenttosubect.enroll.get_all_students_subject()
    context = {
        "title": "allenrollsubject",
        "allenroll": allenroll,
    }
    return render(request, "result/allenroll.html", context)


@login_required(login_url="/accounts/login/")
def updategrade(request, id):
    grade = Grading.objects.get(id=id)
    form = GradeForm()
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade or None)
        if form.is_valid:
            form.save()
        return redirect("allGrade")
    else:
        form = GradeForm(instance=grade or None)

    context = {
        "grade": grade,
        "form": form,
    }
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def deletegrade(request, id):
    grade = Grading.objects.get(id=id)
    if request.method == "POST":
        grade.delete()
        return redirect("allGrade")
    context = {
        "grade": grade,
    }
    return render(request, "result/deletegrade.html", context)


@login_required(login_url="/accounts/login/")
def updatesubject(request, id):
    getsubject = subject.objects.get(id=id)
    form = subjectForm()
    if request.method == "POST":
        form = subjectForm(request.POST or None, instance=getsubject)
        if form.is_valid():
            form.save()
            return redirect("allsubject")
    else:
        form = subjectForm(instance=getsubject)
    context = {"title": "update subject", "getsubject": getsubject, "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def subjectdelete(request, id):
    getsubject = subject.objects.get(id=id)
    if request.method == "POST":
        getsubject.delete()
        return redirect("allsubject")
        print(getsubject)
    context = {
        "getsubject": getsubject,
    }
    return render(request, "result/subjectdelete.html", context)


@login_required(login_url="/accounts/login/")
def Enrollupdate(request, id):
    enroll = EnrollStudenttosubect.objects.get(id=id)
    if request.method == "POST":
        form = EnrollForm(request.POST or None, instance=enroll)
        if form.is_valid():
            form.save()
            return redirect("enrollStudenttosubectall")
    else:
        form = EnrollForm(instance=enroll)
    context = {"title": "update enroll", "enroll": enroll, "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def enrolldelete(request, id):
    enroll = EnrollStudenttosubect.objects.get(id=id)
    if request.method == "POST":
        enroll.delete()
        return redirect("enrollStudenttosubectall")
    context = {"enroll": enroll}
    return render(request, "result/enrolldelete.html", context)


@login_required(login_url="/accounts/login")
def enrollstudentstosubject(request, name, stream):
    getstudents = Student.objects.filter(class_name__name=name, stream__name=stream)
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


@login_required(login_url="/accounts/login/")
def subjectperrank(
    request, name, term=None, stream=None, subject=None, template_name=None, format=None
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
    rankings = Mark.objects.filter(**query_params).order_by("-marks")
    rankings_data = rankings.values_list(
        "student__first_name",
        "student__middle_name",
        "student__last_name",
        "name__name",
        "marks",
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
    results = []
    if stream:
        students = Student.objects.filter(class_name__name=name, stream__name=stream)
    else:
        students = Student.objects.filter(class_name__name=name)
    # Iterate over all the students and their subjects and collect their marks
    for student in students:
        marks = []
        for subjectname in subjects:
            marks_list = list(
                Mark.objects.filter(
                    student=student, name=subjectname, Term__name=term
                ).values_list("marks", flat=True)
            )
            if marks_list == []:
                marks_list = [
                    ""
                ]  # Replace empty list with a list containing empty string
            marks += marks_list
        # Sum up the marks and add to the end of the marks list
        marks_sum = sum([int(mark) for mark in marks if mark != ""])
        marks.append(str(marks_sum))
        # Insert the student name at the beginning of the marks list
        marks.insert(0, str(student))
        # Add the marks list to the results list
        results.append(marks)

    # Sort the results list based on the total marks in descending order
    sorted_results = sorted(results, key=lambda x: x[-1], reverse=True)
    # Add index number to each result row and create a new list
    indexed_results = [
        [index] + result for index, result in enumerate(sorted_results, start=1)
    ]

    # Calculate average marks for each student and add grading
    avg_marks = []
    grading_system = Grading.objects.all()
    for result in indexed_results:
        subject_marks = result[2:-2]  # Get all subject marks
        subject_marks_with_value = [
            int(mark) for mark in subject_marks if mark != ""
        ]  # Get only marks with value
        total_marks = sum(subject_marks_with_value)
        num_subjects = len(subject_marks_with_value)
        try:
            avg_mark = round(total_marks / num_subjects)
        except ZeroDivisionError:
            avg_mark = 0
        avg_marks.append(avg_mark)
        for grading in grading_system:
            if avg_mark >= grading.percent and avg_mark <= 100:
                result.append(grading.name)
                result.append(grading.points)
                break
        # Create context dictionary for rendering template
    context = {
        "page_obj": indexed_results,
        "subject_list": subjects,
        "class_name": name,
        "term": term,
    }
    if stream:
        context["stream"] = stream

    # Generate Excel file if requested
    if format == "ms-excel":
        return generate_excel(name, term, subjects, indexed_results, stream=None)

    # Render the template with the context dictionary
    return render(request, template_name, context)


def error_404(request, exception):
    return render(request, "student/404.html")
