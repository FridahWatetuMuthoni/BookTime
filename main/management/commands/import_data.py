from collections import Counter
import csv
import os.path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = 'Import products in BookTime'

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=open)
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Importing products")
