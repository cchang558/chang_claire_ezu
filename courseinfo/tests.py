from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Semester, Section, Course, Instructor, Student, Registration, Period, Year


# Create your tests here.
class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='tester', email='test@email.com', password='{iSchoolUI}'
        )
        cls.period = Period.objects.create(
            period_sequence=1, period_name='Spring'
        )
        cls.year = Year.objects.create(
            year=2023
        )
        cls.semester = Semester.objects.create(
            year=cls.year, period=cls.period
        )
        cls.course = Course.objects.create(
            course_number='IS327', course_name='Concepts of Machine Learning'
        )
        cls.instructor = Instructor.objects.create(
            first_name='Bob', last_name='Adams', disambiguator='UPenn'
        )
        cls.student = Student.objects.create(
            first_name='Martin', last_name='Cooper', disambiguator='Waterloo'
        )
        cls.section = Section.objects.create(
            section_name='AOG/AOG', semester=cls.semester, course=cls.course, instructor=cls.instructor
        )
        cls.registration = Registration.objects.create(
            student=cls.student, section=cls.section
        )

    def test_period_model(self):
        self.assertEqual(self.period.period_sequence, 1)
        self.assertEqual(self.period.period_name, 'Spring')
        self.assertEqual(self.period.__str__(), 'Spring')

    def test_year_model(self):
        self.assertEqual(self.year.year, 2023)
        self.assertEqual(self.year.__str__(), '2023')

    def test_semester_model(self):
        self.assertEqual(self.semester.year.__str__(), '2023')
        self.assertEqual(self.semester.period.__str__(), 'Spring')
        self.assertEqual(self.semester.__str__(), '2023 - Spring')

    def test_course_model(self):
        self.assertEqual(self.course.course_number, 'IS327')
        self.assertEqual(self.course.course_name, 'Concepts of Machine Learning')
        self.assertEqual(self.course.__str__(), 'IS327 - Concepts of Machine Learning')

    def test_instructor_model(self):
        self.assertEqual(self.instructor.first_name, 'Bob')
        self.assertEqual(self.instructor.last_name, 'Adams')
        self.assertEqual(self.instructor.disambiguator, 'UPenn')
        self.assertEqual(self.instructor.__str__(), 'Adams, Bob (UPenn)')

    def test_student_model(self):
        self.assertEqual(self.student.first_name, 'Martin')
        self.assertEqual(self.student.last_name, 'Cooper')
        self.assertEqual(self.student.disambiguator, 'Waterloo')
        self.assertEqual(self.student.__str__(), 'Cooper, Martin (Waterloo)')

    def test_section_model(self):
        self.assertEqual(self.section.section_name, 'AOG/AOG')
        self.assertEqual(self.section.semester.__str__(), '2023 - Spring')
        self.assertEqual(self.section.course.course_number, 'IS327')
        self.assertEqual(self.section.__str__(), 'IS327 - AOG/AOG (2023 - Spring)')

    def test_registration_model(self):
        self.assertEqual(self.registration.student.__str__(), 'Cooper, Martin (Waterloo)')
        self.assertEqual(self.registration.section.__str__(), 'IS327 - AOG/AOG (2023 - Spring)')
        self.assertEqual(self.registration.__str__(), 'IS327 - AOG/AOG (2023 - Spring) / Cooper, Martin (Waterloo)')

    def test_url_exists_at_correct_location_instructor_list(self):
        response = self.client.get('/instructor/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_section_list(self):
        response = self.client.get('/section/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_course_list(self):
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_semester_list(self):
        response = self.client.get('/semester/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_student_list(self):
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_registration_list(self):
        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 200)

    def test_instructor_list_view(self):
        response = self.client.get(reverse('courseinfo_instructor_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Adams, Bob (UPenn)')
        self.assertTemplateUsed(response, 'courseinfo/instructor_list.html')
        self.assertContains(response, '<h1>EZ University</h1>')
        self.assertContains(response, '<h2>Course Information System</h2>')
        self.assertContains(response, '<h2>Instructor List</h2>')

        # Base Links
        urls = ['courseinfo_instructor_list_urlpattern', 'courseinfo_section_list_urlpattern',
                'courseinfo_course_list_urlpattern', 'courseinfo_semester_list_urlpattern',
                'courseinfo_student_list_urlpattern', 'courseinfo_registration_list_urlpattern']

        for url in urls:
            type_url = reverse(url)
            self.assertContains(response, f'href="{type_url}"')

        # Type Links
        self.assertContains(response, self.instructor.get_absolute_url())

    def test_section_list_view(self):
        response = self.client.get(reverse('courseinfo_section_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IS327 - AOG/AOG (2023 - Spring)')
        self.assertTemplateUsed(response, 'courseinfo/section_list.html')
        self.assertContains(response, '<h2>Section List</h2>')

        # Links
        self.assertContains(response, self.section.get_absolute_url())

    def test_course_list_view(self):
        response = self.client.get(reverse('courseinfo_course_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IS327 - Concepts of Machine Learning')
        self.assertTemplateUsed(response, 'courseinfo/course_list.html')
        self.assertContains(response, '<h2>Course List</h2>')

        # Links
        self.assertContains(response, self.course.get_absolute_url())

    def test_semester_list_view(self):
        response = self.client.get(reverse('courseinfo_semester_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2023 - Spring')
        self.assertTemplateUsed(response, 'courseinfo/semester_list.html')
        self.assertContains(response, '<h2>Semester List</h2>')

        # Links
        self.assertContains(response, self.semester.get_absolute_url())

    def test_student_list_view(self):
        response = self.client.get(reverse('courseinfo_student_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cooper, Martin (Waterloo)')
        self.assertTemplateUsed(response, 'courseinfo/student_list.html')
        self.assertContains(response, '<h2>Student List</h2>')

        # Links
        self.assertContains(response, self.student.get_absolute_url())

    def test_registration_list_view(self):
        response = self.client.get(reverse('courseinfo_registration_list_urlpattern'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IS327 - AOG/AOG (2023 - Spring) / Cooper, Martin (Waterloo)')
        self.assertTemplateUsed(response, 'courseinfo/registration_list.html')
        self.assertContains(response, '<h2>Registration List</h2>')

        # Links
        self.assertContains(response, self.registration.get_absolute_url())

    def test_url_exists_at_correct_location_instructor_detail(self):
        response = self.client.get('/instructor/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_section_detail(self):
        response = self.client.get('/section/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_course_detail(self):
        response = self.client.get('/course/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_semester_detail(self):
        response = self.client.get('/semester/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_student_detail(self):
        response = self.client.get('/student/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_registration_detail(self):
        response = self.client.get('/registration/1/')
        self.assertEqual(response.status_code, 200)

    def test_instructor_detail_view(self):
        response = self.client.get(reverse('courseinfo_instructor_detail_urlpattern',
                                           kwargs={'pk': self.instructor.pk}))
        no_response = self.client.get('/instructor/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Adams, Bob (UPenn)')
        self.assertTemplateUsed(response, 'courseinfo/instructor_detail.html')
        self.assertContains(response, '<h1>EZ University</h1>')
        self.assertContains(response, '<h2>Course Information System</h2>')

        # Base Links
        urls = ['courseinfo_instructor_list_urlpattern', 'courseinfo_section_list_urlpattern',
                'courseinfo_course_list_urlpattern', 'courseinfo_semester_list_urlpattern',
                'courseinfo_student_list_urlpattern', 'courseinfo_registration_list_urlpattern']

        for url in urls:
            type_url = reverse(url)
            self.assertContains(response, f'href="{type_url}"')

        # Type Links
        self.assertContains(response, self.section.get_absolute_url())

    def test_section_detail_view(self):
        response = self.client.get(reverse('courseinfo_section_detail_urlpattern',
                                           kwargs={'pk': self.section.pk}))
        no_response = self.client.get('/section/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'IS327 - AOG/AOG (2023 - Spring)')
        self.assertTemplateUsed(response, 'courseinfo/section_detail.html')

        # Links
        self.assertContains(response, self.course.get_absolute_url())
        self.assertContains(response, self.semester.get_absolute_url())
        self.assertContains(response, self.instructor.get_absolute_url())

    def test_course_detail_view(self):
        response = self.client.get(reverse('courseinfo_course_detail_urlpattern',
                                           kwargs={'pk': self.course.pk}))
        no_response = self.client.get('/course/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'IS327 - Concepts of Machine Learning')
        self.assertTemplateUsed(response, 'courseinfo/course_detail.html')

        # Links
        self.assertContains(response, self.section.get_absolute_url())

    def test_semester_detail_view(self):
        response = self.client.get(reverse('courseinfo_semester_detail_urlpattern',
                                           kwargs={'pk': self.semester.pk}))
        no_response = self.client.get('/semester/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, '2023 - Spring')
        self.assertTemplateUsed(response, 'courseinfo/semester_detail.html')

        # Links
        self.assertContains(response, self.section.get_absolute_url())

    def test_student_detail_view(self):
        response = self.client.get(reverse('courseinfo_student_detail_urlpattern',
                                           kwargs={'pk': self.student.pk}))
        no_response = self.client.get('/student/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Cooper, Martin (Waterloo)')
        self.assertTemplateUsed(response, 'courseinfo/student_detail.html')

        # Links
        self.assertContains(response, self.registration.get_absolute_url())

    def test_registration_detail_view(self):
        response = self.client.get(reverse('courseinfo_registration_detail_urlpattern',
                                           kwargs={'pk': self.registration.pk}))
        no_response = self.client.get('/registration/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'IS327 - AOG/AOG (2023 - Spring) / Cooper, Martin (Waterloo)')
        self.assertTemplateUsed(response, 'courseinfo/registration_detail.html')

        # Links
        self.assertContains(response, self.student.get_absolute_url())
        self.assertContains(response, self.section.get_absolute_url())
