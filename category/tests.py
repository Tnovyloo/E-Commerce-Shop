from django.test import TestCase
from category.models import Category

# Create your tests here.
class CategoryTestCase(TestCase):
    def create_category(self, name="Test category", desc="Lorem ipsum dipsum lipsum ipusm trum trum", slug="test-category"):
        return Category.objects.create(category_name=name,
                                       slug=slug,
                                       description=desc)

    def test_category_object(self):
        obj = self.create_category()
        self.assertTrue(isinstance(obj, Category))
        self.assertEqual(obj.__str__(), obj.category_name)
