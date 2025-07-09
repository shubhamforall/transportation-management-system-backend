from django.core.management.base import BaseCommand
from utils.logger import log_msg, logging
from utils.load_data.load import load_data


class Command(BaseCommand):
    help = "Load data from files into the database."

    def handle(self, *args, **kwargs):
        log_msg(logging.INFO, "Loading data from files...")
        load_data()
        log_msg(logging.INFO, "Data loaded successfully.")
