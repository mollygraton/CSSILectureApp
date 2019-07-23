import webapp2
import jinja2
import os
import time;
from google.appengine.api import users
from random import randint
from google.appengine.ext import ndb

from models import Student, Teacher, Question

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

 ############################################################################
def root_parent():
    '''A single key to be used as the ancestor for all dog entries.
    Allows for strong consistency at the cost of scalability.'''
    return ndb.Key('Parent', 'default_parent')

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
        new_student.email = users.get_current_user().email
        #new_student.code =
        new_student.put()
        self.redirect('/studentSession')

class StudentSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        sCode = self.request.get('code')
        if (int(sCode) == int(tCode)):
            template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            print "The logic is correct"
            self.response.write(template.render())
        elif (sCode != tCode):
             print "You got here"
             print tCode
             print sCode
        print sCode
    def post(self):
        numOf1 = self.request.get('numOf1')
        numOf2 = self.request.get('numOf2')
        numOf3 = self.request.get('numOf3')
        numOf4 = self.request.get('numOf4')
        numOf5 = self.request.get('numOf5')
        template = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())
        self.redirect('/studentSession')

class AddQuestion(webapp2.RequestHandler):
    def post(self):
        new_question = Question(parent=root_parent())
        new_question.question_text = self.request.get('question')
        new_question.timestamp = time.time()
        #new_question.student_key =
        new_question.put()
        self.redirect('/studentSession')

class TeacherDashboardPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherDashboard.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

    def post(self):
        new_teacher = Teacher(parent=root_parent())
        new_teacher.teacher_code = random.randint(100,999)
        # new_teacher.email =
        new_teacher.put()
        self.redirect('/studentSession')

class TeacherSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render({'tCode': tCode}))
#class
# The app config
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/studentDashboard', StudentDashboardPage),
    ('/studentSession', StudentSessionPage),
    ('/teacherDashboard', TeacherDashboardPage),
    ('/teacherSession', TeacherSessionPage),
    ('/addQuestion', AddQuestion),
], debug=True)
