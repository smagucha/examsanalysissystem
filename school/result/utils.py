from student.models import Student, Klass, Stream, Attendance
from .models import EnrollStudenttosubect, Mark, subject, term, Grading
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import xlwt

year = str(date.today().year)


def get_student(Student, id):
    return get_object_or_404(Student, id=id)


def all_terms():
    return term.objects.all()


def all_subjects():
    return subject.objects.all()


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


def class_stream_count(name, stream=None):
    if stream:
        return Student.student.class_or_stream_count(name, stream)
    return Student.student.class_or_stream_count(name)


def student_stream_class(name, stream=None):
    if stream:
        return Student.student.get_student_list_class_or_stream(name, stream)
    return Student.student.get_student_list_class_or_stream(name)


def student_subject_count(student):
    return EnrollStudenttosubect.enroll.get_subjects_for_student_count(student=student)


def get_average_subject_marks(name, term, stream, subjects, getterms):
    avg_subject = {}
    for subject in subjects:
        marks = get_marks_for_class_or_stream(name, term, stream, subject)
        student_count = EnrollStudenttosubect.enroll.student_per_subject_count(
            subject=subject, class_name=name, stream=stream
        )
        subject_marks = list(marks)
        if subject_marks:
            avg_subject[subject.name] = calculate_average(
                sum(subject_marks),
                student_count,
            )

    return avg_subject


def get_best_students_data(name, term, stream, subjects):
    best_students_data = []
    for subject in subjects:
        marks = get_marks_for_class_or_stream(name, term, stream, subject)
        if not marks:
            continue

        max_mark = max(marks)
        best_student = Mark.objects.filter(
            student__class_name__name=name,
            Term__name=term,
            name__name=subject.name,
            marks=max_mark,
            year=year,
        )
        for i in best_student:
            best_students_data.append(
                (i.student.get_student_name(), subject.name, max_mark)
            )

    return best_students_data


def get_marks_for_class_or_stream(name, term, stream, subject):
    marks = Mark.mark.get_subject_marks_for_class_or_stream(
        student_class_name=name, Term=term, subject_name=subject.name, stream=stream
    )
    return marks


def get_grades_count(name, term, stream):
    Getgrading = Grading.objects.all()
    students = get_students_by_class_and_stream(name, stream)
    grades = []
    grades_count = {}
    for student in students:
        marks = list(
            Mark.objects.filter(Term__name=term, student=student).values_list(
                "marks", flat=True
            )
        )
        avg_mark = round(calculate_average(sum(marks), len(marks)), 1)
        grades.append(get_grade(Getgrading, avg_mark).name)
    for grading in Getgrading:
        grades_count[grading.name] = grades.count(grading.name)
    return grades_count


def calculate_class_rank(getclassnumber, student, totalclass, getclassrankid):
    if getclassnumber:
        sortedid = dict(sorted(getclassnumber.items(), key=lambda item: item[1])[::-1])
        getclassrank = list(sortedid.keys())
        classnumber = getclassrank.index(student.id) + 1
        getnumbers = f"{classnumber}/{totalclass}"
        getclassrankid.append(getnumbers)
        return classnumber, getclassrankid
    else:
        return


def calculate_stream_rank(getstreamnumber, student, getstreamrankid):
    if getstreamnumber:
        sorted_id = dict(
            sorted(getstreamnumber.items(), key=lambda item: item[1], reverse=True)
        )
        getstreamrank = list(sorted_id.keys())
        streamnumber = getstreamrank.index(student.id) + 1
        getnumbers = f"{streamnumber}/{len(getstreamrank)}"
        getstreamrankid.append(getnumbers)
        return streamnumber, getstreamrankid


def calculate_average_and_get_grades(Getgrading, totalmarks, getsubjectcount):
    getavg = calculate_average(totalmarks, getsubjectcount)
    Gradeterm = None
    if getavg:
        Gradeterm = get_grade(Getgrading, getavg).name
    return getavg, Gradeterm


def get_all_student_result_for_class_and_stream(student_stream, student_class, getterm):
    getclassnumber, getstreamnumber = {}, {}
    for idstudent in student_class:
        marks = list(
            Mark.objects.filter(student=idstudent, Term__name=getterm).values_list(
                "marks", flat=True
            )
        )
        if marks:
            if sum(marks):
                getclassnumber[idstudent.id] = sum(marks)
        else:
            getclassnumber[idstudent.id] = 0

    for idstudent in student_stream:
        marks = list(
            Mark.objects.filter(student=idstudent, Term__name=getterm).values_list(
                "marks", flat=True
            )
        )
        if marks:
            if sum(marks):
                getstreamnumber[idstudent.id] = sum(marks)
        else:
            getstreamnumber[idstudent.id] = 0

    return getclassnumber, getstreamnumber


def update_term_results(
    getterm,
    getterms,
    getclassrankid,
    getstreamrankid,
    totalmarks,
    getsubjectcount,
    subjectname,
    Getgrading,
):
    a = 0
    if getterm:
        try:
            getterm[getterms.name] = (
                [getstreamrankid[a]] + [getclassrankid[a]] + getterm[getterms.name]
            )
            a += 1

            calcavg = round(calculate_average(totalmarks, getsubjectcount))
            if calcavg:
                getterm[getterms.name].append(get_grade(Getgrading, calcavg).name)
                getterm[getterms.name].append(get_grade(Getgrading, calcavg).points)
            else:
                getterm[getterms.name].append("")
                getterm[getterms.name].append("")
        except IndexError:
            pass
    return getterm


def getgrade():
    return Grading.objects.all()


def get_grade(grades, percent_or_marks):
    grade_name = None
    for grade in grades:
        if (
            percent_or_marks >= grade.percent
            and percent_or_marks >= 0
            and percent_or_marks <= 100
        ):
            grade_name = grade
            break
    return grade_name


def calculate_average(totalmarks, divider):
    try:
        getaverage = totalmarks / divider
    except ZeroDivisionError:
        getaverage = 0
    return getaverage


def get_student_avg_and_class_average(students, term):
    get_avg = []
    for student in students:
        query_params = {
            "student": student.id,
            "Term__name": term,
            "year": 2023,
        }
        get_marks = list(
            Mark.objects.filter(**query_params).values_list("marks", flat=True)
        )
        if get_marks:
            get_avg.append(calculate_average(sum(get_marks), len(get_marks)))
        else:
            get_avg = [0]

    return get_avg


def get_student_result(student, term, class_name):
    grades = getgrade()
    get_marks = Mark.mark.student_marks(student=student.id, term=term)
    student_class = Student.student.get_student_list_class_or_stream(name=class_name)
    student_stream = Student.student.get_student_list_class_or_stream(
        name=class_name, stream=student.stream
    )
    subjectcount = getsubjectcount = student_subject_count(student)
    totalmarks = subjectcount * 100
    totalclass = Student.student.class_or_stream_count(name=class_name)
    streamtotal = Student.student.class_or_stream_count(
        name=class_name, stream=student.stream
    )
    getclassnumber, getstreamnumber = get_all_student_result_for_class_and_stream(
        student_stream, student_class, term
    )
    _, getclassrankid = calculate_class_rank(getclassnumber, student, totalclass, [])
    result_for_student = {}
    sum = 0
    result_for_student["student"] = student.get_student_name()
    for i in get_marks:
        result_for_student[i.name.name] = i.marks
        sum += i.marks
    result_for_student["total marks"] = f"{sum}/{totalmarks}"
    result_for_student["position"] = getclassrankid[0]
    result_for_student["Grade"] = get_grade(
        grades, calculate_average(sum, subjectcount)
    ).name

    return result_for_student


def subject_ranking_per_class_and_stream(
    student, subjectname, Getgrading, totalclass, q, getterms
):
    subjectrankdetail = []
    for eachsubject in subjectname:
        eachsubjectrank = []
        eachsubjectrank.append(eachsubject.name)
        getmark = list(
            Mark.objects.filter(
                student=student,
                name__name=eachsubject.name,
                Term__name=getterms,
                year=student.year,
            ).values_list("marks", flat=True)
        )
        eachsubjectrank += getmark
        if len(eachsubjectrank) >= 2:
            eachsubjectrank.append(get_grade(Getgrading, eachsubjectrank[1]).name)
        subjectrankclass = list(
            Mark.objects.filter(
                student__class_name__name=student.class_name,
                name__name=eachsubject,
                Term__name=getterms.name,
                year=student.year,
            )
            .values_list("student", flat=True)
            .order_by("-marks")
        )

        if student.id in subjectrankclass:
            getnu = f"{subjectrankclass.index(student.id)+1}/{totalclass}"
            eachsubjectrank.append(getnu)
            subjectrankdetail.append(eachsubjectrank)
            q[getterms.name] = subjectrankdetail
    return q


def get_students_by_class_and_stream(name, stream):
    query_params = {
        "class_name__name": name,
        "year": year,
    }
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
        marks.append(marks_sum)
        marks.insert(0, str(student))
        results.append(marks)
    return results


def sort_results_by_total_marks(results):
    return sorted(results, key=lambda x: x[-1], reverse=True)


def add_index_to_results(results):
    return [[index] + result for index, result in enumerate(results, start=1)]


def calculate_average_marks_and_grading(indexed_results, getterms):
    avg_marks = []
    grading_system = getgrade()
    for result in indexed_results:
        subject_marks = result[2:-1]
        subject_marks_with_value = [int(mark) for mark in subject_marks if mark != ""]
        total_marks = sum(subject_marks_with_value)
        num_subjects = len(subject_marks_with_value)
        avg_mark = calculate_average(total_marks, num_subjects)
        if avg_mark:
            result.append(get_grade(grading_system, avg_mark).name)
            result.append(get_grade(grading_system, avg_mark).points)
    return avg_marks
