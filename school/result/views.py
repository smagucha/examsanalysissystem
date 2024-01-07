from django.shortcuts import render, redirect, get_object_or_404
from .models import EnrollStudenttosubect, Mark, subject, term, Grading
from student.models import Student, Klass, Stream, Attendance
from .forms import subjectForm, TermForm, GradeForm, EnrollForm, UpdateMarksForm
from django.contrib.auth.decorators import login_required
from datetime import date
from io import BytesIO


from student.views import (
    database_operation,
    delete_database_operation,
)
from student.views import get_class, get_stream
from twilio.rest import Client
from django.conf import settings
from .utils import (
    get_student,
    all_terms,
    all_subjects,
    generate_excel,
    generate_pdf,
    class_stream_count,
    student_stream_class,
    student_subject_count,
    get_average_subject_marks,
    get_best_students_data,
    get_marks_for_class_or_stream,
    get_grades_count,
    calculate_class_rank,
    calculate_stream_rank,
    calculate_average_and_get_grades,
    get_all_student_result_for_class_and_stream,
    update_term_results,
    getgrade,
    get_grade,
    calculate_average,
    get_student_avg_and_class_average,
    get_student_result,
    subject_ranking_per_class_and_stream,
    get_students_by_class_and_stream,
    collect_student_marks,
    sort_results_by_total_marks,
    add_index_to_results,
    calculate_average_marks_and_grading,
    send_sms,
)


year = str(date.today().year)


@login_required(login_url="/accounts/login/")
def student_view(request, id, name, format=None, template_name=None):
    student = get_object_or_404(Student, id=id)
    totalclass = class_stream_count(name=name)
    subjectname = all_subjects()
    terms = all_terms()
    streamtotal = class_stream_count(name=name, stream=student.stream)
    student_stream = student_stream_class(
        name=student.class_name, stream=student.stream
    )
    Getgrading = getgrade()
    student_class = student_stream_class(name=student.class_name)
    getterm = {}
    getavg = {}
    totalmarks = {}
    getclassrankid = []
    getstreamrankid = []
    getsubjectcount = student_subject_count(student)
    outsubject = getsubjectcount * 100
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
        totalmarks[getterms.name] = sum([i for i in termresults if i != ""])
        studenttotalmarks = totalmarks[getterms.name]
        if totalmarks[getterms.name]:
            termresults.append(studenttotalmarks)
        if sum([i for i in termresults if i != ""]):
            getterm[getterms.name] = termresults

            (
                getclassnumber,
                getstreamnumber,
            ) = get_all_student_result_for_class_and_stream(
                student_stream, student_class, getterms
            )
            _, getclassrankid = calculate_class_rank(
                getclassnumber, student, totalclass, getclassrankid
            )

            _, getstreamrankid = calculate_stream_rank(
                getstreamnumber, student, getstreamrankid
            )
            getterm = update_term_results(
                getterm,
                getterms,
                getclassrankid,
                getstreamrankid,
                studenttotalmarks,
                getsubjectcount,
                subjectname,
                Getgrading,
            )
    context = {
        "classname": name,
        "getterm": getterm,
        "title": "student details",
        "subject": subjectname,
        "student": student,
    }

    return render(request, "result/student.html", context)


@login_required(login_url="/accounts/login/")
def enteresult(request, name, Term, Subject, stream=None):
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
        "term": Term,
        "subject": Subject,
    }
    return render(request, "result/enterresult.html", context)


@login_required(login_url="/accounts/login/")
def streamexamanalysis(
    request, name, term, stream=None, template_name=None, format=None
):
    subjects = subject.objects.all()
    avg_subject = get_average_subject_marks(name, term, stream, subjects, term)
    best_students_data = get_best_students_data(name, term, stream, subjects)
    grades_count = get_grades_count(name, term, stream)

    context = {
        "z": best_students_data,  # use a good variable name for key
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


@login_required(login_url="/accounts/login/")
def addsubject(request):
    return database_operation(request, subjectForm)


@login_required(login_url="/accounts/login/")
def AddTerm(request):
    return database_operation(request, TermForm)


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
    getsubjects = all_subjects()
    if request.method == "POST":
        getsubjectid = request.POST.getlist("subjectid")
        getstudentsub = []
        for i in getstudents:
            getstudentsub.append(i.id)
        for i in range(len(getstudents)):
            if getsubjectid[i]:
                enrolltosubject_data = {
                    "student_id": getstudentsub[i],
                    "subject_id": subject.objects.get(name=getsubjectid[i]).id,
                    "class_name_id": Klass.objects.get(name=name).id,
                }
                if stream:
                    enrolltosubject_data["stream_id"] = Stream.objects.get(
                        name=stream
                    ).id
                enrolltosubject = EnrollStudenttosubect.objects.create(
                    **enrolltosubject_data
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
    subjects = all_subjects()
    students = get_students_by_class_and_stream(name, stream)
    results = collect_student_marks(students, subjects, term)
    sorted_results = sort_results_by_total_marks(results)
    indexed_results = add_index_to_results(sorted_results)

    avg_marks = calculate_average_marks_and_grading(indexed_results, term)

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


def error_404(request, exception):
    return render(request, "student/404.html")


def reportbook(request, name, id, termname):
    student = get_student(Student, id)
    totalclass = class_stream_count(name=name)
    streamtotal = class_stream_count(name=name, stream=student.stream)
    terms = all_terms()
    Getgrading = getgrade()
    classnumber = {}
    streamnumber = {}
    Gradeterm = {}
    totalmarks = {}
    subjectname = all_subjects()
    student_stream = student_stream_class(
        name=student.class_name, stream=student.stream
    )
    student_class = student_stream_class(name=student.class_name)
    getsubjectcount = EnrollStudenttosubect.enroll.get_subjects_for_student_count(
        student=student
    )
    getavg = {}
    getclassrankid = []
    getstreamrankid = []
    getsubjectcount = EnrollStudenttosubect.enroll.get_subjects_for_student_count(
        student=student
    )
    outsubject = getsubjectcount * 100
    q = {}  # use a good variable name
    for gettermname in terms:
        getclassnumber, getstreamnumber = get_all_student_result_for_class_and_stream(
            student_stream, student_class, gettermname
        )
        classnumber[gettermname.name], _ = calculate_class_rank(
            getclassnumber, student, totalclass, getclassrankid
        )
        streamnumber[gettermname.name], _ = calculate_stream_rank(
            getstreamnumber, student, getstreamrankid
        )

        q = subject_ranking_per_class_and_stream(
            student, subjectname, Getgrading, totalclass, q, gettermname
        )
        getmarks = list(
            Mark.objects.filter(student=student, Term__name=gettermname).values_list(
                "marks", flat=True
            )
        )

        if getmarks:
            studenttotalmarks = sum(getmarks)
            totalmarks[gettermname.name] = studenttotalmarks
        else:
            totalmarks[gettermname.name] = 0

        (
            getavg[gettermname.name],
            Gradeterm[gettermname.name],
        ) = calculate_average_and_get_grades(
            Getgrading,
            totalmarks[gettermname.name],
            getsubjectcount,
        )
    context = {
        "Grade": Gradeterm,
        "totalmarks": totalmarks,
        "classnumber": classnumber,
        "streamtotal": streamtotal,
        "classname": name,
        "totalclass": totalclass,
        "streamnumber": streamnumber,
        "title": "report card",
        "terms": terms,
        "student": student,
        "q": q,
        "termname": termname,
        "outsubject": outsubject,
    }
    return generate_pdf("result/reportcard.html", context)


@login_required(login_url="/accounts/login/")
def class_subject_ranking(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_term = request.POST.get("selected_term")
        selected_subject = request.POST.get("selected_subject")
        if get_stream:
            selected_stream = request.POST.get("selected_stream")
        if selected_stream:
            return redirect(
                "result:subjectperrankstreamterm",
                name=selected_class,
                stream=selected_stream,
                term=selected_term,
                subject=selected_subject,
            )

        return redirect(
            "result:subjectperrankclass",
            name=selected_class,
            term=selected_term,
            subject=selected_subject,
        )
    context = {
        "getclasses": get_class(),
        "getsubjects": all_subjects(),
        "getterms": all_terms(),
    }
    if get_stream():
        context["getstream"] = get_stream()
    return render(request, "result/class_subject_ranking.html", context)


@login_required(login_url="/accounts/login/")
def result_stream_or_term(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_term = request.POST.get("selected_term")
        if get_stream:
            selected_stream = request.POST.get("selected_stream")

        if selected_stream:
            return redirect(
                "result:resultstreamterm",
                name=selected_class,
                stream=selected_stream,
                term=selected_term,
            )
        return redirect(
            "result:resultperterm",
            name=selected_class,
            term=selected_term,
        )

    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
    }
    if get_stream():
        context["getstream"] = get_stream()
    return render(request, "result/result_stream_or_term.html", context)


@login_required(login_url="/accounts/login/")
def enter_result_for_stream_or_class(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_term = request.POST.get("selected_term")
        selected_subject = request.POST.get("selected_subject")
        selected_stream = request.POST.get("selected_stream")
        if selected_stream:
            return redirect(
                "result:enterexam",
                name=selected_class,
                stream=selected_stream,
                Term=selected_term,
                Subject=selected_subject,
            )
        else:
            return redirect(
                "result:enterexamforclass",
                name=selected_class,
                Term=selected_term,
                Subject=selected_subject,
            )
    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
        "getsubjects": all_subjects(),
        "getstream": get_stream(),
    }
    return render(request, "result/enter_result.html", context)


@login_required(login_url="/accounts/login/")
def enroll_students_to_student(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_stream = request.POST.get("selected_stream")
        return redirect(
            "result:enrollstudentstosubject",
            name=selected_class,
            stream=selected_stream,
        )
    context = {
        "getclasses": get_class(),
        "getstream": get_stream(),
    }
    return render(request, "result/enrollstudentstosubject.html", context)


@login_required(login_url="/accounts/login/")
def subjects_enrolled_y_student(request):
    allsubjectsbystudent = EnrollStudenttosubect.objects.filter(year=year)
    context = {"allsubjectsbystudent": allsubjectsbystudent}
    return render(request, "result/allsubjectsbystudent.html", context)


@login_required(login_url="/accounts/login/")
def update_subjects_enrolled_y_student(request, id):
    return database_operation(request, EnrollForm, id)


@login_required(login_url="/accounts/login/")
def delete_subjects_enrolled_y_student(request, id):
    return delete_database_operation(request, EnrollStudenttosubect, id)


@login_required(login_url="/accounts/login/")
def class_and_stream_ranking(request):
    return render(request, "result/class_and_stream_ranking.html")


@login_required(login_url="/accounts/login/")
def stream_ranking(request, name, term):
    streams = get_stream()
    grades = getgrade()
    stream_ranks = {}
    get_avg = {}
    for stream in streams:
        students = Student.student.get_student_list_class_or_stream(
            name=name, stream=stream.name
        )
        get_avg[stream.name] = get_student_avg_and_class_average(students, term)
        stream_ranks[stream.name] = get_grade(
            grades,
            calculate_average(sum(get_avg[stream.name]), len(get_avg[stream.name])),
        ).points
    sorted_dict = dict(
        sorted(stream_ranks.items(), key=lambda item: item[1], reverse=True)
    )
    print(sorted_dict)
    context = {"stream_ranks": sorted_dict, "name": name}

    return render(request, "result/stream_ranking.html", context)


@login_required(login_url="/accounts/login/")
def calculate_class_ranks(request, term):
    classes = get_class()
    grades = getgrade()
    class_ranks = {}
    stream = None
    for class_name in classes:
        students = Student.student.get_student_list_class_or_stream(
            name=class_name, stream=stream
        )
        get_avg = get_student_avg_and_class_average(students, term)
        class_ranks[class_name.name] = get_grade(
            grades,
            calculate_average(sum(get_avg), len(get_avg)),
        ).points
    sorted_dict = dict(
        sorted(class_ranks.items(), key=lambda item: item[1], reverse=True)
    )
    context = {"class_ranks": sorted_dict}
    return render(request, "result/class_ranks.html", context)


@login_required(login_url="/accounts/login/")
def select_class_for_stream_ranking(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_term = request.POST.get("selected_term")

        return redirect("result:streamranking", name=selected_class, term=selected_term)
    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
    }
    return render(request, "result/select_class_for_stream_ranking.html", context)


@login_required(login_url="/accounts/login/")
def select_stream_for_subject_ranking(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_subject = request.POST.get("selected_subject")
        selected_term = request.POST.get("selected_term")
        return redirect(
            "result:subjectrankingstream",
            class_name=selected_class,
            term=selected_term,
            subject=selected_subject,
        )

    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
        "getsubjects": all_subjects(),
    }
    return render(request, "result/select_stream_ranking.html", context)


@login_required(login_url="/accounts/login/")
def class_stream_subject_ranking(request, class_name, term, subject):
    stream = Stream.objects.all()
    grades = getgrade()
    streamsubjectrank = {}
    for streams in stream:
        subjectclass = list(
            Mark.mark.get_subject_marks_for_class_or_stream(
                student_class_name=class_name,
                Term=term,
                subject_name=subject,
                stream=stream,
            )
        )
        studentpersubject = EnrollStudenttosubect.enroll.student_per_subject_count(
            subject=subject, class_name=class_name, stream=stream
        )
        if subjectclass:
            avg = sum(subjectclass) / studentpersubject
            streamsubjectrank[streams.name] = get_grade(grades, avg).points
    sorted_subject_ranking = dict(
        sorted(streamsubjectrank.items(), key=lambda item: item[1], reverse=True)
    )
    context = {
        "subject_ranking": sorted_subject_ranking,
        "subject": subject,
        "class": class_name,
    }
    return render(request, "result/streamsubjectranking.html", context)


@login_required(login_url="/accounts/login/")
def select_term_for_class_ranking(request):
    if request.method == "POST":
        selected_term = request.POST.get("selected_term")
        return redirect(
            "result:classranking",
            term=selected_term,
        )

    context = {
        "getterms": all_terms(),
    }
    return render(request, "result/select_term_for_class_ranking.html", context)


@login_required(login_url="/accounts/login/")
def select_result_to_update(request):
    if request.method == "POST":
        selected_term = request.POST.get("selected_term")
        selected_class = request.POST.get("selected_class")
        selected_subject = request.POST.get("selected_subject")
        selected_stream = request.POST.get("selected_stream")
        return redirect(
            "result:sujectresults",
            class_name=selected_class,
            term=selected_term,
            subject=selected_subject,
            stream=selected_stream,
        )

    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
        "getsubjects": all_subjects(),
        "getstream": get_stream(),
    }
    return render(request, "result/select_result_to_update.html", context)


@login_required(login_url="/accounts/login/")
def subject_results_class(request, class_name, term, subject, stream):
    subject_results = Mark.mark.get_subject_marks_for_class_or_stream_marks(
        student_class_name=class_name,
        Term=term,
        subject_name=subject,
        stream=stream,
    )
    context = {"subject_results": subject_results}
    return render(request, "result/subject_results.html", context)


@login_required(login_url="/accounts/login/")
def updatemarks(request, id):
    return database_operation(request, UpdateMarksForm, id)


@login_required(login_url="/accounts/login/")
def select_class_to_sent_result(request):
    if request.method == "POST":
        selected_term = request.POST.get("selected_term")
        selected_class = request.POST.get("selected_class")
        return redirect(
            "result:sentresultspage",
            class_name=selected_class,
            term=selected_term,
        )

    context = {
        "getclasses": get_class(),
        "getterms": all_terms(),
    }
    return render(request, "result/select_class_to_sent_result.html", context)


@login_required(login_url="/accounts/login/")
def sent_results(request, class_name, term):
    student = student_stream_class(name=class_name)
    parent_message = {}
    if request.method == "POST":
        selected_parent = request.POST.getlist("parent_phone_number")
        selected_message = request.POST.getlist("message")
        for i in range(len(selected_message)):
            to = selected_parent[i]
            body = selected_message[i]
            send_sms(to, body)
        return redirect("result:messagesuccess")
    else:
        for i in student:
            parent_message[i] = ", ".join(
                [
                    f"{key}: {value}"
                    for key, value in get_student_result(
                        student=i, term=term, class_name=class_name
                    ).items()
                ]
            )
        selected_parent = request.POST.getlist("parent_phone_number")
        selected_message = request.POST.getlist("message")
    context = {"parent_message": parent_message}
    return render(request, "result/sent_results.html", context)


def send_sms_view(request):
    return render(request, "result/sms_sent.html")
