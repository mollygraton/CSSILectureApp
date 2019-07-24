from google.appengine.ext import ndb
from google.appengine.api import users



class Student(ndb.Model):
    email = ndb.StringProperty()
    code = ndb.IntegerProperty()
    user = ndb.UserProperty()
    num1to5 = ndb.IntegerProperty()

class Teacher(ndb.Model):
    code = ndb.IntegerProperty()
    email = ndb.StringProperty()
    user = ndb.UserProperty()
    formProperty = ndb.BooleanProperty()

class Question(ndb.Model):
    code = ndb.IntegerProperty()
    student = ndb.StringProperty()
    question_text = ndb.StringProperty()
    timestamp = ndb.FloatProperty()
