from peewee import *

database = SqliteDatabase("data.db", pragmas={'foreign_keys': 1})


class LOJProblem(Model):
    id = IntegerField()
    name = CharField(622535)
    accepted_count = IntegerField()
    submit_count = IntegerField()
    problem_type = CharField()
    time_limit = IntegerField()
    memory_limit = IntegerField()
    body = TextField()
    tags = CharField(622535)
    fastest_code = TextField()
    fastest_language = CharField(622535)
    fastest_submitter = CharField(622535)
    score = TextField()

    class Meta:
        database = database
        primary_key = CompositeKey('id')


def first_use():
    database.create_tables([LOJProblem])


first_use()
