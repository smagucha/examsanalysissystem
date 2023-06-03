from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa # for generating PDFs

class MyView(View):
    def get(self, request):
        # Check if the request is for a PDF
        if request.GET.get('format') == 'pdf':
            # Generate the PDF
            template = get_template('my_template.html')
            html = template.render({'my_data': 'some data'})
            pdf = generate_pdf(html)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="my_file.pdf"'
            return response
        else:
            # Generate the regular web page
            my_data = 'some data'
            return render(request, 'my_template.html', {'my_data': my_data})

def generate_pdf(html):
    # Generate a PDF from the given HTML using xhtml2pdf
    result = io.BytesIO()
    pdf = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return result.getvalue()
    else:
        raise Exception('PDF generation failed')
