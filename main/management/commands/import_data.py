from collections import Counter
import csv
import os.path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = 'Import products in BookTime'

    # The add_arguement is explained in the argparse module(a python module)
    # adding positional arguements on top of all the django options
    def add_arguments(self, parser):
        # the path to the csv file to import
        parser.add_argument("csvfile", type=open)
        # the path to the images directory
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        self.stdout.write("Importing products")
        count = Counter()
        reader = csv.DictReader(options.pop("csvfile"))
        for row in reader:
            product, created = models.Product.objects.get_or_create(name=row['name'],
                                                                    price=row['price']
                                                                    )
            product.description = row["description"]
            product.slug = slugify(row["name"])
            for import_tag in row["tags"].split("|"):
                tag, tag_created = models.ProductTag.objects.get_or_create(
                    name=import_tag)
                product.tags.add(tag)
                count["tags"] += 1
                if tag_created:
                    count["tags_created"] += 1
            with open(os.path.join(options['image_basedir'], row['image_filename'],), 'rb',) as f:
                image = models.ProductImage(
                    product=product,
                    image=ImageFile(f, name=row['image_filename']),
                )
                image.save()
                count['images'] += 1
            product.save()
            count['products'] += 1
            if created:
                count['products_created'] += 1

        self.stdout.write(
            'Products processed=%d (created=%d)'
            % (count["products"], count["products_created"])
        )
        self.stdout.write(
            'Tags processed=%d (created=%d)'
            % (count["tags"], count["tags_created"])
        )

        self.stdout.write("Images processed=%d" % count["images"])
        print(
            f'image processed: {count["images"]}')
