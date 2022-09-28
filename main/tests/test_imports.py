from io import StringIO
import tempfile
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from main import models


class TestImport(TestCase):
    # The purpose of this override is to override the django setting for a specific test
    # in this case, we are creating a temporary folder as MEDIA_ROOT because we are dealing
    # with potentially many uploaded files. Django, unlike the database, does
    # not clean these files. Using a temporary folder makes sure this will be eventually cleaned by the operating system.
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        # Creates a new file like object that has nothing
        out = StringIO()
        args = ['main/fixtures/product-sample.csv',
                'main/fixtures/product-sampleimages/']
        # it runs the import_data command and passes the csv and image  path arguement
        # call_command() function is used to invoke management commands
        call_command('import_data', *args, stdout=out)
        # the stdout.write statements
        expected_out = ("Importing products\n"
                        "Products processed=3 (created=3)\n"
                        "Tags processed=6 (created=6)\n"
                        "Images processed=3\n")
        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.ProductTag.objects.count(), 6)
        self.assertEqual(models.ProductImage.objects.count(), 3)
