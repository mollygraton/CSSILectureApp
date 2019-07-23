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

tCode=randint(100, 999)

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
        new_student.email = (users.get_current_user()).email()
        new_student.put()
        self.redirect('/studentSession')

class StudentSessionPage(webapp2.RequestHandler):
    def get(self):
        # user = users.get_current_user()
        # sCode = self.request.get('code')
        # new_student.code =
        # if (int(sCode) == int(tCode)):
            template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            print "The logic is correct"
            self.response.write(template.render())
        # elif (sCode != tCode):
        #      print "You got here"
        #      print tCode
        #      print sCode
        # print sCode
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
    #
    # def post(self):
    #     new_teacher = Teacher(parent=root_parent())
    #     # new_teacher.email =
    #     new_teacher.put()
    #     self.redirect('/studentSession')

class TeacherSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        number1 = Number.query(Number.num1to5 == 1).fetch()
        print(number1)
        number2 = Number.query(Number.num1to5 == 2).fetch()
        print(number2)
        number3 = Number.query(Number.num1to5 == 3).fetch()
        number4 = Number.query(Number.num1to5 == 4).fetch()
        number5 = Number.query(Number.num1to5 == 5).fetch()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        data = {
            "numOf1": len(number1),
            "numOf2": len(number2),
            "numOf3": len(number3),
            "numOf4": len(number4),
            "numOf5": len(number5)
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
