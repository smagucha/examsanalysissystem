# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from .views import getsubjects


# # Mock user for testing login
# def create_test_user(email="testuser", password="testpassword"):
#     return User.objects.create_user(email=email, password=password)


# class GetSubjectsViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.user = create_test_user()
#         cls.url = reverse(
#             "get_subjects", args=["Class 10"]
#         )  # Change 'Class 10' to your desired classname

#     def test_login_required(self):
#         """
#         Test if the view redirects to the login page when an unauthenticated user tries to access it.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 302
#         )  # 302 is the HTTP status code for redirection

#     def test_get_subjects_authenticated(self):
#         """
#         Test if the view works as expected when accessed by an authenticated user.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 200
#         )  # 200 is the HTTP status code for successful response

#     def test_template_used(self):
#         """
#         Test if the view uses the correct template to render the response.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(
#             response, "your_template_name.html"
#         )  # Change 'your_template_name.html' to your actual template name

#     def test_context_data(self):
#         """
#         Test if the context data contains the correct values.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.context["classname"], "Class 10"
#         )  # Change 'Class 10' to your desired classname
#         # Test other context data, such as subjects, streamname, and term, if applicable

#     # Add more test cases as needed for different scenarios


# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from .views import terms


# # Mock user for testing login
# def create_test_user(username="testuser", password="testpassword"):
#     return User.objects.create_user(username=username, password=password)


# class TermsViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.user = create_test_user()
#         cls.url = reverse(
#             "terms", args=["Class 10"]
#         )  # Change 'Class 10' to your desired classname

#     def test_login_required(self):
#         """
#         Test if the view redirects to the login page when an unauthenticated user tries to access it.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 302
#         )  # 302 is the HTTP status code for redirection

#     def test_terms_authenticated(self):
#         """
#         Test if the view works as expected when accessed by an authenticated user.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 200
#         )  # 200 is the HTTP status code for successful response

#     def test_template_used(self):
#         """
#         Test if the view uses the correct template to render the response.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(
#             response, "your_template_name.html"
#         )  # Change 'your_template_name.html' to your actual template name

#     def test_context_data(self):
#         """
#         Test if the context data contains the correct values.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.context["classname"], "Class 10"
#         )  # Change 'Class 10' to your desired classname
#         # Test other context data, such as allterms, streamname, and subject, if applicable

#     # Add more test cases as needed for different scenarios


# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from .models import Student, subject, term
# from .views import student_view


# # Mock user for testing login
# def create_test_user(username="testuser", password="testpassword"):
#     return User.objects.create_user(username=username, password=password)


# class StudentViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.user = create_test_user()
#         cls.student = Student.objects.create(
#             # Your student object data here
#             # Example: first_name='John', last_name='Doe', ...
#         )
#         cls.url = reverse(
#             "student_view", args=[cls.student.id, "Class 10"]
#         )  # Change 'Class 10' to your desired classname

#     def test_login_required(self):
#         """
#         Test if the view redirects to the login page when an unauthenticated user tries to access it.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 302
#         )  # 302 is the HTTP status code for redirection

#     def test_student_view_authenticated(self):
#         """
#         Test if the view works as expected when accessed by an authenticated user.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 200
#         )  # 200 is the HTTP status code for successful response

#     def test_template_used(self):
#         """
#         Test if the view uses the correct template to render the response.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(
#             response, "your_template_name.html"
#         )  # Change 'your_template_name.html' to your actual template name

#     def test_context_data(self):
#         """
#         Test if the context data contains the correct values.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         student = get_object_or_404(Student, id=self.student.id)
#         # Test if the context contains the expected data, e.g., student, subjectname, terms, etc.
#         self.assertEqual(response.context["student"], student)
#         # Test other context data as applicable

#     def test_pdf_format(self):
#         """
#         Test if the view generates a PDF format response when requested.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url, {"format": "pdf"})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response["Content-Type"], "application/pdf")

#     # Add more test cases as needed for different scenarios


# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from .models import EnrollStudenttosubect, subject, term, Mark
# from .views import enteresult


# # Mock user for testing login
# def create_test_user(username="testuser", password="testpassword"):
#     return User.objects.create_user(username=username, password=password)


# class EnterResultViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.user = create_test_user()
#         cls.url = reverse(
#             "enteresult", args=["Class 10", "Science", "Fall", "Math"]
#         )  # Change the args to your desired values

#     def test_login_required(self):
#         """
#         Test if the view redirects to the login page when an unauthenticated user tries to access it.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 302
#         )  # 302 is the HTTP status code for redirection

#     def test_enter_result_authenticated_get(self):
#         """
#         Test if the view works as expected when accessed by an authenticated user with a GET request.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code, 200
#         )  # 200 is the HTTP status code for successful response

#     def test_enter_result_authenticated_post(self):
#         """
#         Test if the view saves the result correctly when accessed by an authenticated user with a POST request.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user

#         # Assuming you have a setup to create exam and subject objects for the test.
#         # Replace the below lines with the appropriate objects according to your test setup.

#         exam = EnrollStudenttosubect.enroll.get_students_subject(
#             name="Class 10", stream="Science", Subject="Math"
#         )

#         # Populate request.POST data with valid marks for each student in the exam
#         # Ensure the order of students in exam and the corresponding marks in request.POST match

#         marks_list = [90, 85, 95]  # Replace with valid marks

#         data = {
#             "subjectname": marks_list,
#         }

#         response = self.client.post(self.url, data)
#         self.assertEqual(
#             response.status_code, 302
#         )  # 302 is the HTTP status code for redirection

#         # Verify that the marks are saved in the database
#         for i in range(len(exam)):
#             student_id = exam[i].student.id
#             subject_id = subject.objects.get(name="Math").id
#             term_id = term.objects.get(name="Fall").id

#             mark = Mark.objects.get(
#                 student_id=student_id, name_id=subject_id, Term_id=term_id
#             )
#             self.assertEqual(mark.marks, marks_list[i])

#     def test_template_used(self):
#         """
#         Test if the view uses the correct template to render the response.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(
#             response, "your_template_name.html"
#         )  # Change 'your_template_name.html' to your actual template name

#     def test_context_data(self):
#         """
#         Test if the context data contains the correct values.
#         """
#         self.client.login(
#             username="testuser", password="testpassword"
#         )  # Log in the user
#         response = self.client.get(self.url)
#         # Test if the context contains the expected data, e.g., exam, name, stream, term, subject, etc.
#         # Replace the below lines with your expected values based on your test setup
#         self.assertEqual(response.context["exam"], [])
#         self.assertEqual(response.context["name"], "Class 10")
#         self.assertEqual(response.context["stream"], "Science")
#         self.assertEqual(response.context["term"], "Fall")
#         self.assertEqual(response.context["subject"], "Math")
#         # Test other context data as applicable

#     # Add more test cases as needed for different scenarios


# from django.test import TestCase, RequestFactory
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from .models import Mark, EnrollStudenttosubect, subject, term, Grading, Student
# from .views import streamexamanalysis

# # Mock user for testing login
# def create_test_user(username='testuser', password='testpassword'):
#     return User.objects.create_user(username=username, password=password)

# class StreamExamAnalysisViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.user = create_test_user()
#         cls.url = reverse('streamexamanalysis', args=['Class 10', 'Fall'])  # Change the args to your desired values

#     def test_login_required(self):
#         """
#         Test if the view redirects to the login page when an unauthenticated user tries to access it.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 302)  # 302 is the HTTP status code for redirection

#     def test_stream_exam_analysis_authenticated(self):
#         """
#         Test if the view works as expected when accessed by an authenticated user.
#         """
#         self.client.login(username='testuser', password='testpassword')  # Log in the user
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)  # 200 is the HTTP status code for successful response

#     def test_template_used(self):
#         """
#         Test if the view uses the correct template to render the response.
#         """
#         self.client.login(username='testuser', password='testpassword')  # Log in the user
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(response, 'your_template_name.html')  # Change 'your_template_name.html' to your actual template name

#     def test_context_data(self):
#         """
#         Test if the context data contains the correct values.
#         """
#         self.client.login(username='testuser', password='testpassword')  # Log in the user
#         response = self.client.get(self.url)
#         # Test if the context contains the expected data, e.g., z, name, term, avgsubject, subject, Count, etc.
#         # Replace the below lines with your expected values based on your test setup
#         self.assertEqual(response.context['name'], 'Class 10')
#         self.assertEqual(response.context['term'], 'Fall')
#         # Test other context data as applicable

#     def test_pdf_format(self):
#         """
#         Test if the view generates a PDF format response when requested.
#         """
#         self.client.login(username='testuser', password='testpassword')  # Log in the user
#         response = self.client.get(self.url, {'format': 'pdf'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response['Content-Type'], 'application/pdf')

#     # Add more test cases as needed for different scenarios


from django.test import TestCase, RequestFactory
from django.urls import reverse
from useraccounts.models import MyUser
from result.models import term
from django.contrib.auth.decorators import login_required
from result.views import addsubject, AddTerm
from student.views import database_operation
from ..forms import subjectForm
from django.urls import resolve


# Mock user for testing login
def create_test_user(email="testuser@gmail.com", password="testpassword"):
    return MyUser.objects.create_user(
        email=email,
        first_name="sam",
        last_name="magucha",
        country="",
        date_of_birth="1999-01-01",
        phone="+254707181264",
        city="Nairobi",
        password=password,
    )


class AddSubjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = create_test_user()
        cls.url_addsubject = reverse("result:addsubject")
        cls.url_addterm = reverse("result:addterm")
        cls.url_addgrade = reverse("result:addgrade")
        cls.login_url = reverse("login")
        cls.url_delete_term = reverse("result:deleteterm", kwargs={"id": 1})

    def get_authenticated_response(self, url):
        self.client.login(email="testuser@gmail.com", password="testpassword")
        return self.client.get(url)

    def get_unauthenticated_response(self, url):
        return self.client.post(url)

    def test_login_required_addsubject(self):
        response = self.client.get(self.url_addsubject)
        self.assertEqual(response.status_code, 302)

    def test_add_subject_authenticated(self):
        response = self.get_authenticated_response(self.url_addsubject)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(self.url_addsubject).func.__name__, "addsubject")

    def test_add_subject_unauthenticated_user(self):
        response = self.get_unauthenticated_response(self.url_addsubject)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.url_addsubject}"
        self.assertRedirects(response, expected_redirect_url)

    def test_template_used_addsubject(self):
        response = self.get_authenticated_response(self.url_addsubject)
        self.assertTemplateUsed(response, "student/generalform.html")

    def test_login_required_addterm(self):
        response = self.client.get(self.url_addterm)
        self.assertEqual(response.status_code, 302)

    def test_addterm_authenticated_user(self):
        response = self.get_authenticated_response(self.url_addterm)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(self.url_addterm).func.__name__, "AddTerm")

    def test_addterm_unauthenticated_user(self):
        response = response = self.get_unauthenticated_response(self.url_addterm)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.url_addterm}"
        self.assertRedirects(response, expected_redirect_url)

    def test_template_used_addterm(self):
        response = self.get_authenticated_response(self.url_addterm)
        self.assertTemplateUsed(response, "student/generalform.html")

    def test_login_required_addgrade(self):
        response = self.get_authenticated_response(self.url_addgrade)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resolve(self.url_addgrade).func.__name__, "addGrade")

    def test_addgrade_unauthenticated_user(self):
        response = self.get_unauthenticated_response(self.url_addgrade)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.url_addgrade}"
        self.assertRedirects(response, expected_redirect_url)

    def test_addgrade_templateduser(self):
        response = self.get_authenticated_response(self.url_addgrade)
        self.assertTemplateUsed(response, "student/generalform.html")

    def test_login_required_delete_term(self):
        term_name = term.objects.create(name="Test Term")
        response = self.client.get(self.url_delete_term)
        self.assertTrue(term.objects.filter(id=term_name.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_redirect_unauthenticated_user(self):
        response = response = self.get_unauthenticated_response(self.url_delete_term)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = f"{self.login_url}?next={self.url_delete_term}"
        self.assertRedirects(response, expected_redirect_url)

    # work invalid id
    # def test_delete_term_invalid_id(self):
    #     term_name = term.objects.create(name="Test Term")
    #     url = reverse("result:deleteterm", kwargs={"id": 548415})
    #     response = self.client.delete(url)
    #     # self.assertEqual(response.status_code, 404)
    #     print(response)
