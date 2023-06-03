from django.shortcuts import get_object_or_404, render
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from result.models import Mark, term, Grading, subject
from student.models import Student, Stream
from datetime import date
import xlwt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from result.views import streamexamanalysis


@login_required(login_url="/accounts/login/")
def report_pdf_view(request, id, name):
    student = get_object_or_404(Student, id=id)
    Getgrading = Grading.objects.all()
    getgrade = []
    getmark = Mark.objects.filter(
        student=id,
        Term__name="firstterm",
        year=student.year,
    )
    totalclass = Student.student.class_count(name=name)
    streamtotal = Student.student.stream_count(name=name, stream=student.stream)
    classnumber = None
    getidnumber = {}
    for idstudent in Student.student.get_student_list_class(name=name):
        if sum(
            list(
                Mark.objects.filter(
                    student=idstudent, Term__name="firstterm", year=student.year
                ).values_list("marks", flat=True)
            )
        ):
            getidnumber[idstudent.id] = sum(
                list(
                    Mark.objects.filter(
                        student=idstudent.id,
                        Term__name="firstterm",
                        year=student.year,
                    ).values_list("marks", flat=True)
                )
            )

    if getidnumber:
        sortedid = dict(sorted(getidnumber.items(), key=lambda item: item[1])[::-1])
        getclassrank = list(sortedid.keys())
        classnumber = getclassrank.index(student.id) + 1
    streamnumber = None
    getstreamidnumber = {}
    for idstudent in Student.objects.filter(
        class_name__name=student.class_name,
        stream__name=student.stream,
        year=student.year,
    ):
        if sum(
            list(
                Mark.objects.filter(
                    student=idstudent, Term__name="firstterm", year=student.year
                ).values_list("marks", flat=True)
            )
        ):
            getstreamidnumber[idstudent.id] = sum(
                list(
                    Mark.objects.filter(
                        student=idstudent, Term__name="firstterm", year=student.year
                    ).values_list("marks", flat=True)
                )
            )
    if getstreamidnumber:
        sortedid = dict(
            sorted(getstreamidnumber.items(), key=lambda item: item[1])[::-1]
        )
        getstreamrank = list(sortedid.keys())
        streamnumber = getstreamrank.index(student.id) + 1
    getsubjectcount = (
        Mark.objects.filter(student=student.id).values_list("marks", flat=True).count()
    )
    outsubject = getsubjectcount * 100
    totalmarks = 0
    for i in getmark:
        totalmarks += i.marks
        for j in Getgrading:
            if i.marks >= j.percent and i.marks <= 100:
                getgrade.append(j.name)
                break

    getavg = totalmarks / getsubjectcount
    Grade = None
    for j in Getgrading:
        if getavg >= j.percent and getavg <= 100:
            Grade = j.name
            break

    rankingsubject = {}
    for Subject in subject.objects.all():
        subjectname = (
            Mark.objects.filter(
                student__class_name__name=student.class_name,
                name__name=Subject,
                Term__name="firstterm",
                year=student.year,
            )
            .values_list("student", "marks")
            .order_by("-marks")
        )
        rankingsubject[Subject] = subjectname
    getsubjectrankng = {}

    for k, v in rankingsubject.items():
        q = []
        for i in v:
            q.append(i[0])
        getsubjectrankng[k] = q

    finalsub = []
    for k, v in getsubjectrankng.items():
        if student.id in v:
            getnu = v.index(student.id) + 1
            getnumbers = f"{getnu}/{totalclass}"
            finalsub.append(getnumbers)

    reportcard = zip(
        getmark,
        getgrade,
        finalsub,
    )
    template_path = "reports/reportcard.html"
    context = {
        "Grade": Grade,
        "outsubject": outsubject,
        "totalmarks": totalmarks,
        "classnumber": classnumber,
        "myvar": student,
        "streamtotal": streamtotal,
        "getmark": getmark,
        "reportcard": reportcard,
        "Term": name,
        "totalclass": totalclass,
        "streamnumber": streamnumber,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="studentreportcard.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="/accounts/login/")
def classanalysis(request, name, term):
    avgsubject = {}
    subjectavg = None
    for Subject in subject.objects.all():
        subjectname = list(
            Mark.objects.filter(
                student__class_name__name=name,
                Term__name="firstterm",
                year=2022,
                name__name=Subject,
            ).values_list("marks", flat=True)
        )
        lensubject = len(subjectname)
        sumsubect = sum(subjectname)

        try:
            subjectavg = sumsubect / lensubject
        except:
            pass
        avgsubject[Subject] = subjectavg

    beststudent = []
    getmarks = []
    getsub = []

    for Subject in subject.objects.all():
        getbest = list(
            Mark.objects.filter(
                student__class_name__name=name,
                Term__name=term,
                name__name=Subject,
                year=str(date.today().year),
            ).values_list("marks", flat=True)
        )
        if getbest:
            getmax = max(getbest)
            getstudent = Mark.objects.filter(
                student__class_name__name=name,
                Term__name=term,
                name__name=Subject,
                marks=getmax,
                year=str(date.today().year),
            )
            beststudent.append(getstudent)
            getmarks.append(getmax)
            getsub.append(Subject)
    Getgrading = Grading.objects.all()
    k = []
    for student in Student.objects.filter(class_name__name=name, year=2022):
        getstudent = Mark.objects.filter(
            Term__name=term, year=str(date.today().year), student=student
        ).values_list("marks", flat=True)
        y = [i for i in getstudent if i != ""]
        thesum = sum(y)
        calcavg = round(thesum / len(getstudent), 1)
        for j in Getgrading:
            if calcavg >= j.percent and calcavg <= 100:
                k.append(j.name)
                break
    Count = {}
    for i in Getgrading:
        Count[i.name] = k.count(i.name)
    template_path = "reports/classranalysis.html"
    context = {
        "z": beststudent,
        "name": name,
        "term": term,
        "avgsubject": avgsubject,
        "subject": subject.objects.all(),
        "Count": Count,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="/accounts/login/")
def streamanalysis(request, name, term, stream=None, template_name=None):
    # streamexamanalysis(request, name, term, stream=None, template_name=None)
    # if stream:
    # original_output = streamexamanalysis(request,name, term, stream, template_name)
    # context_data = streamexamanalysis.get_context_data()
    # print(context_data)
    view = streamexamanalysis(request, name, term, stream, template_name)
    # response = view(request, name, term, stream, template_name)
    # context_data = view.get_view_instance().get_context_data()
    print(view)
    return render(request, 'reports/streamranalysisdownload.html')
    # if stream:#
    #     print(streamexamanalysis(request, name, term, stream=None, template_name=None).context)
    
    # return streamexamanalysis(request, name, term, stream=None, template_name=None).context
    # avgsubject = {}
    # subjectavg = None
    # for Subject in subject.objects.all():
    #     subjectname = list(
    #         Mark.objects.filter(
    #             student__class_name__name=name,
    #             Term__name=term,
    #             student__stream__name=stream,
    #             year=2022,
    #             name__name=Subject,
    #         ).values_list("marks", flat=True)
    #     )
    #     lensubject = len(subjectname)
    #     sumsubect = sum(subjectname)
    #     try:
    #         subjectavg = sumsubect / lensubject
    #     except:
    #         pass
    #     avgsubject[Subject.name] = subjectavg
    # beststudent = []
    # getmarks = []
    # getsub = []

    # for Subject in subject.objects.all():
    #     getbest = list(
    #         Mark.objects.filter(
    #             student__class_name__name=name,
    #             Term__name=term,
    #             name__name=Subject,
    #             student__stream__name=stream,
    #             year=2022,
    #         ).values_list("marks", flat=True)
    #     )
    #     if getbest:
    #         getmax = max(getbest)
    #         getstudent = Mark.objects.filter(
    #             student__class_name__name=name,
    #             Term__name=term,
    #             name__name=Subject,
    #             marks=getmax,
    #             year=str(date.today().year),
    #         )
    #         beststudent.append(getstudent)
    #         getmarks.append(getmax)
    #         getsub.append(Subject)

    # Getgrading = Grading.objects.all()
    # k = []

    # for student in Student.objects.filter(
    #     class_name__name=name,
    #     stream__name=stream,
    #     year=2022,
    # ):
    #     getstudent = Mark.objects.filter(
    #         Term__name=term,
    #         year=2022,
    #         student=student,
    #         student__stream__name=stream,
    #     ).values_list("marks", flat=True)
    #     y = [i for i in getstudent if i != ""]
    #     thesum = sum(y)
    #     calcavg = round(thesum / len(getstudent), 1)
    #     for j in Getgrading:
    #         if calcavg >= j.percent and calcavg <= 100:
    #             k.append(j.name)
    #             break

    # Count = {}
    # for i in Getgrading:
    #     Count[i.name] = k.count(i.name)
    # template_path = "reports/streamranalysisdownload.html"
    # context = {
    #     "z": beststudent,
    #     "name": name,
    #     "term": term,
    #     "stream": stream,
    #     "avgsubject": avgsubject,
    #     "getstudent": getstudent,
    #     "subject": subject.objects.all(),
    #     "Count": Count,
    # }
    # # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'filename="report.pdf"'
    # # find the template and render it.
    # template = get_template(template_path)
    # html = template.render(context)

    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse("We had some errors <pre>" + html + "</pre>")
    # return response
    # return render(request, "reports/streamranalysisdownload.html", context)


@login_required(login_url="/accounts/login/")
def subjectperrankclassdownload(request, name, term, subject):

    subjectname = (
        Mark.objects.filter(
            student__class_name__name=name,
            name__name=subject,
            Term__name="firstterm",
            year=2022,
        )
        .values_list(
            "student__first_name",
            "student__middle_name",
            "student__last_name",
            "name__name",
            "marks",
        )
        .order_by("-marks")
    )
    template_path = "reports/subjectperrankclassdownload.html"
    context = {
        "subjectname": subjectname,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="/accounts/login/")
def subjectperrankstreamdownload(request, name, term, stream, subject):

    subjectname = (
        Mark.objects.filter(
            student__class_name__name=name,
            name__name=subject,
            student__stream__name=stream,
            Term__name=term,
            year=2022,
        )
        .values_list(
            "student__first_name",
            "student__middle_name",
            "student__last_name",
            "name__name",
            "marks",
        )
        .order_by("-marks")
    )
    template_path = "reports/subjectperrankstreamdownload.html"
    context = {
        "subjectname": subjectname,
        "name": name,
        "stream": stream,
        "term": term,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@login_required(login_url="/accounts/login/")
def export_users_xls(request, name, term):
    subjectname = subject.objects.all()
    getresult = []

    for student in Student.student.get_student_list_class(name=name):
        t = []
        for sub in subjectname:
            x = list(
                Mark.objects.filter(
                    name__name=sub,
                    Term__name="firstterm",
                    year=2022,
                    student=student,
                ).values_list("marks", flat=True)
            )
            if x == []:
                x = [""]
            t += x
        y = [i for i in t if i != ""]
        full_name = (
            student.first_name + " " + student.middle_name,
            " " + student.middle_name,
        )
        t.append(sum(y))
        t.append(full_name)
        getresult.append(t)
    rearranginglist = []
    for i in getresult:
        i = i[-1:] + i[:-1]
        rearranginglist.append(i)
    sorttotal = sorted(rearranginglist, key=lambda x: x[-1])[::-1]
    index = 1
    sorttotalfinal = []
    for i in sorttotal:
        t = [index] + i
        sorttotalfinal.append(t)
        index += 1
    getavg = []
    Getgrading = Grading.objects.all()
    for i in sorttotalfinal:
        c = i[2:-1]
        getallsubectwithvalue = [i for i in c if i != ""]
        Sum = sum(getallsubectwithvalue)
        length = len(getallsubectwithvalue)
        calcavg = round(Sum / length)
        getavg.append(calcavg)
        for j in Getgrading:
            if calcavg >= j.percent and calcavg <= 100:
                i.append(j.name)
                i.append(j.points)
                break

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
