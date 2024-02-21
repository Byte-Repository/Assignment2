from django.test import TestCase

# Create your tests here.

from catalog.models import Author


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(author.last_name, author.first_name)

        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

from django.test import TestCase
from django.utils import timezone
from catalog.models import Book, BookInstance
from django.contrib.auth.models import User

class BookInstanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        book = Book.objects.create(
            title='Test Book',
            summary='Test summary',
            isbn='1234567890123',
        )
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        BookInstance.objects.create(
            book=book,
            imprint='Test Imprint',
            due_back=timezone.now() + timezone.timedelta(days=7),
            borrower=user,
            status='o',  # 'On loan' status for testing
        )

    def test_imprint_label(self):
        book_instance = BookInstance.objects.get(id=1)
        field_label = book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_due_back_label(self):
        book_instance = BookInstance.objects.get(id=1)
        field_label = book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_borrower_label(self):
        book_instance = BookInstance.objects.get(id=1)
        field_label = book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_status_label(self):
        book_instance = BookInstance.objects.get(id=1)
        field_label = book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_imprint_max_length(self):
        book_instance = BookInstance.objects.get(id=1)
        max_length = book_instance._meta.get_field('imprint').max_length
        self.assertEqual(max_length, 200)

    def test_is_overdue(self):
        book_instance = BookInstance.objects.get(id=1)
        # The due_back date is set to 7 days from now, so it should not be overdue
        self.assertFalse(book_instance.is_overdue)

    def test_str_representation(self):
        book_instance = BookInstance.objects.get(id=1)
        expected_str = f'{book_instance.id} ({book_instance.book.title})'
        self.assertEqual(str(book_instance), expected_str)
