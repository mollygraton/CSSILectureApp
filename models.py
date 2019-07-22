from google.appengine.ext import ndb


class Student(ndb.Model):
    email = ndb.StringProperty(required = True)
    room_code = ndb.IntegerProperty(required = False)
    user = #????

class Teacher(ndb.Model):
    room_code = ndb.IntegerProperty(required = False)
    email = ndb.StringProperty(required = True)
    user = #???

class Question(ndb.Model):
    student_key =
