from django.core.management.base import BaseCommand
from django.db import connection


CALCULATE_GENDER_QUERY = """
SELECT gender, count(gender) FROM instances_patient GROUP BY gender;
"""

GET_TOP_PROCEDURES_QUERY = """
SELECT type_code, count(type_code) FROM instances_procedure GROUP BY type_code order by count desc limit 10;
"""

MOST_LEAST_POPULAR_DAY_QUERY = """
select extract(dow from start_date) as week_day,
 count(start_date) from instances_encounter group by week_day order by count desc;
"""

DAY_MAPPING = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}


class Command(BaseCommand):
    help = 'Get statistics of datasets'

    def handle(self, *args, **kwargs):  # noqa: unused-argument
        self.calculate_gender()
        self.get_top_procedures()
        self.get_most_least_popular_day()

    @staticmethod
    def calculate_gender():
        with connection.cursor() as cursor:
            cursor.execute(CALCULATE_GENDER_QUERY)
            response = cursor.fetchall()
            print('The number of patients by gender:')
            for gender, value in response:
                print('{}: {}'.format(gender, value))

    @staticmethod
    def get_top_procedures():
        with connection.cursor() as cursor:
            cursor.execute(GET_TOP_PROCEDURES_QUERY)
            response = cursor.fetchall()
            print('The top 10 types of procedures:')
            for procedure, value in response:
                print('{}: {}'.format(procedure, value))

    @staticmethod
    def get_most_least_popular_day():
        with connection.cursor() as cursor:
            cursor.execute(MOST_LEAST_POPULAR_DAY_QUERY)
            response = cursor.fetchall()
            print('The most and least popular days of the week when encounters occurred:')
            for day, value in response:
                print('{}: {}'.format(DAY_MAPPING[int(day)], value))
