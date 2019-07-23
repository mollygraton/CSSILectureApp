from google.appengine.ext import ndb
from google.appengine.api import users



class Student(ndb.Model):
    email = ndb.StringProperty()
    code = ndb.IntegerProperty()
    user = users.get_current_user() #not sure

class Teacher(ndb.Model):
    code = ndb.IntegerProperty()
    email = ndb.StringProperty()
    user = users.get_current_user() #not sure

class Question(ndb.Model):
    student_key = ndb.StringProperty()
    question_text = ndb.StringProperty()
    timestamp = ndb.FloatProperty()
