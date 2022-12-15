import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from api.models import Ingredients

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class ExistsError(Exception):
    pass


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    Ingredients.objects.create(name=ingredient["name"],
                                                  measurement_unit=ingredient[
                                                      "measurement_unit"])
                    if Ingredients.objects.filter(name=ingredient["name"],
                                                  measurement_unit=ingredient[
                                                      "measurement_unit"]).exists():
                        raise  ExistsError(f'Ingredient {ingredient["name"]} '
                                           f'{ingredient["measurement_unit"]} '
                                           f'already exists')

        except FileNotFoundError:
            raise CommandError('There is not file in directory data')