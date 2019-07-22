from google.appengine.ext import ndb
from google.appengine.api import users



class Student(ndb.Model):
    email = ndb.StringProperty(required = True)
    room_code = ndb.IntegerProperty(required = False)
    user = users.get_current_user()

class Teacher(ndb.Model):
    room_code = ndb.IntegerProperty(required = False)
    email = ndb.StringProperty(required = True)
    user = users.get_current_user()

class Question(ndb.Model):
    student_key = ndb.StringProperty(required=True)
    question_text = ndb.StringProperty(required=True)
    timestamp = ndb.IntegerProperty(required=True)
