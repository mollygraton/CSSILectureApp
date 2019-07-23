from google.appengine.ext import ndb
from google.appengine.api import users



class Student(ndb.Model):
    email = ndb.StringProperty(required = True)
    code = ndb.IntegerProperty(required = False)
    user = users.get_current_user() #not sure

class Teacher(ndb.Model):
    code = ndb.IntegerProperty(required = False)
    email = ndb.StringProperty(required = True)
    user = users.get_current_user() #not sure

class Question(ndb.Model):
    student_key = ndb.StringProperty(required=True)
    question_text = ndb.StringProperty(required=True)
    timestamp = ndb.FloatProperty(required=True)
