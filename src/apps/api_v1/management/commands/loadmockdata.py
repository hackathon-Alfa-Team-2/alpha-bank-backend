import csv
import logging
import sys

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError

from src.apps.lms.models import LMS
from src.apps.tasks.models import Task
from src.apps.users.models import CustomUser, Role, Grade, Position

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s -- %(message)s",
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    MODELS_FILES_NAMES = {
        Role: "role_mock",
        Grade: "grade_mock",
        Position: "position_mock",
        CustomUser: "users_mock",
        LMS: "lms_mock",
        Task: "tasks_mock",
    }
    DATA_PATH = "src/apps/api_v1/management/mock_data/{}.csv"

    def handle(self, *args, **options):
        try:
            if self.check_models():
                logger.info("Starting to upload data.")
                for model, file_name in self.MODELS_FILES_NAMES.items():
                    self.load_csv_to_db(model=model, file_name=file_name)
                logger.info("The data has been uploaded successfully.")
            else:
                sys.exit()
        except DatabaseError as e:
            logger.error(f'An error has occurred: "{e}"')

    @classmethod
    def check_models(cls) -> bool:
        exists_objects_models = [
            m.__name__ for m in cls.MODELS_FILES_NAMES if m.objects.exists()
        ]
        if exists_objects_models:
            answer = input(
                f'В таблицах {", ".join(exists_objects_models)} '
                "уже есть данные. "
                "Продолжение операции может привести к конфликтам.\n"
                "Продолжить? y/N: "
            )
            if answer.lower() != "y":
                return False
        return True

    @classmethod
    def add_instance(cls, model, row: dict) -> dict:
        if model is CustomUser:
            supervisor_id = row.pop("supervisor")
            if supervisor_id:
                row["supervisor"] = CustomUser.objects.get(id=supervisor_id)
            row["role"] = Role.objects.get(id=row.pop("role"))
            row["position"] = Position.objects.get(id=row.pop("position"))
            row["grade"] = Grade.objects.get(id=row.pop("grade"))
        elif model is LMS:
            row["employee"] = CustomUser.objects.get(id=row.pop("employee"))
            row["supervisor"] = CustomUser.objects.get(
                id=row.pop("supervisor")
            )
        elif model is Task:
            row["lms"] = LMS.objects.get(id=row.pop("lms"))
        return row

    @classmethod
    def load_csv_to_db(cls, model, file_name):
        with open(cls.DATA_PATH.format(file_name)) as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=",")
            for row in dict_reader:
                row = cls.add_instance(model=model, row=row)
                if model == CustomUser:
                    CustomUser.objects.create_user(**row)
                else:
                    model.objects.create(**row)
            csvfile.close()
        logger.info(f"The data has been added to the table {model.__name__}.")
