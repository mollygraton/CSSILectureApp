import webapp2
import jinja2
import os
import time;
from google.appengine.api import users
from random import randint
from google.appengine.ext import ndb

from models import Student, Teacher, Question, Number

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
###TO DO : MAKE SURE THERE ARE NO REPEATS IN DATABASE
 ############################################################################
def root_parent():
    '''A single key to be used as the ancestor for all entries.
    Allows for strong consistency at the cost of scalability.'''
    return ndb.Key('Parent', 'default_parent')

def GetStudent(user):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = Student.query(Student.user == user, ancestor=root_parent()).fetch()
    if len(notes) > 0:
        # We found a note, return it.
        return notes[0]
    else:
        # We didn't find a note, return None
        return None

def GetTeacher(user):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = Teacher.query(Teacher.user == user, ancestor=root_parent()).fetch()
    if len(notes) > 0:
        # We found a note, return it.
        return notes[0]
    else:
        # We didn't find a note, return None
        return None


def GetCodeTeacher(student):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = Teacher.query(Teacher.code == student.code, ancestor=root_parent()).fetch()
    if len(notes) > 0:
        # We found a note, return it.
        return notes[0].code
    else:
        # We didn't find a note, return None
        return None

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        data = {
          'user': user,
          'login_url': users.create_login_url(self.request.uri),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class StudentDashboardPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/studentDashboard.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())
    def post(self):
        new_student = Student(parent=root_parent())
        new_student.user = users.get_current_user()
        new_student.code = int(self.request.get("code"))
        new_student.email = (users.get_current_user()).email()
        new_student.put()
        self.redirect('/studentSession')

class StudentSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (GetStudent(user).code == GetCodeTeacher(GetStudent(user))):
            template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            print "The logic is correct"
            self.response.write(template.render())
        elif (GetStudent(user).code != GetCodeTeacher(GetStudent(user))):
             print "You got here"

        print "THE TEACHER CODE IS: " + str(GetCodeTeacher(GetStudent(user)))
        print "THE STUDENT CODE IS: " + str(GetStudent(user).code)
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())
        self.redirect('/studentSession')

class AddQuestion(webapp2.RequestHandler):
    def post(self):
        new_question = Question(parent=root_parent())
        new_question.question_text = self.request.get('question')
        new_question.timestamp = time.time()
        new_question.student = (GetStudent(users.get_current_user())).key.urlsafe()
        new_question.put()
        self.redirect('/studentSession')

class AddNumber(webapp2.RequestHandler):
    def post(self):
        new_number = Number(parent=root_parent())
        new_number.num1to5 = int(self.request.get('understanding'))
        new_number.put()
        self.redirect('/studentSession')

class TeacherDashboardPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherDashboard.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

    def post(self):
        #if GetTeacher(user) == None:
            new_teacher = Teacher(parent=root_parent())
            new_teacher.user = users.get_current_user()
            new_teacher.email = (users.get_current_user()).email()
            new_teacher.code = randint(100,999)
            new_teacher.put()
            self.redirect('/teacherSession')
        #else:
        #    self.redirect('/teacherSession')

class TeacherSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        number1 = Number.query(Number.num1to5 == 1).fetch()
        number2 = Number.query(Number.num1to5 == 2).fetch()
        number3 = Number.query(Number.num1to5 == 3).fetch()
        number4 = Number.query(Number.num1to5 == 4).fetch()
        number5 = Number.query(Number.num1to5 == 5).fetch()
        questions = Question.query().fetch()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        data = {
            "tCode": int(GetTeacher(user).code),
            "numOf1": len(number1),
            "numOf2": len(number2),
            "numOf3": len(number3),
            "numOf4": len(number4),
            "numOf5": len(number5),
            "questions": questions
        }
        print(data)
        self.response.write(template.render(data))

def GetUserInput(user):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = UserNote.query(UserNote.user == user, ancestor=root_parent()).fetch()
    if len(notes) > 0:
        # We found a note, return it.
        return notes[0]
    else:
        # We didn't find a note, return None
        return None

class AjaxGetCurrentNote(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            # No user is logged in, so don't return any value.
            self.response.status = 401
            return
        user_note = GetUserNote(user)
        note = ''
        if user_note is not None:
            # If there was a current note, update note.
            note = user_note.note
        # build a dictionary that contains the data that we want to return.
        data = {'note': note}
        # Note the different content type.
        self.response.headers['Content-Type'] = 'application/json'
        # Turn data dict into a json string and write it to the response
        self.response.write(json.dumps(data))
#class
# The app config
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/studentDashboard', StudentDashboardPage),
    ('/studentSession', StudentSessionPage),
    ('/teacherDashboard', TeacherDashboardPage),
    ('/teacherSession', TeacherSessionPage),
    ('/addQuestion', AddQuestion),
    ('/addNumber', AddNumber),
], debug=True)
