import webapp2
import jinja2
import os
from google.appengine.api import users
from random import randint

from models import Student, Teacher, Question

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

 ############################################################################

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

class StudentSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        sCode = self.request.get('code')
        tCode = randint(100, 999)
        if (sCode==tCode):
            template = JINJA_ENVIRONMENT.get_template('templates/StudentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(template.render())
    def post(self):
         numOf1 = self.request.get('numof1')
         numOf2 = self.request.get('numOf2')
         numOf3 = self.request.get('numOf3')
         numOf4 = self.request.get('numOf4')
         numOf5 = self.request.get('numOf5')
         template2 = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
         self.response.headers['Content-Type'] = 'text/html'
         self.response.write(template.render())

class TeacherDashboardPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherDashboard.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())

class TeacherSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/teacherSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())
#class
# The app config
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/studentDashboard', StudentDashboardPage),
    ('/studentSession', StudentSessionPage),
    ('/teacherDashboard', TeacherDashboardPage),
    ('/teacherSession', TeacherSessionPage),
], debug=True)
