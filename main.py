import webapp2
import jinja2
import os
import time;
from google.appengine.api import users
from random import randint

import json
from google.appengine.ext import ndb

from models import Student, Teacher, Question, Number

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
###TO DO : TeacherSession HTML and Python for OpenForm/CloseForm ADD to Teacher model?
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

def GetUserInput(user):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = Question.query(Question.student == GetStudent(user), ancestor=root_parent()).fetch()
    if len(notes) > 0:
        # We found a note, return it.
        return notes
    else:
        # We didn't find a note, return None
        return None

def GetTeacherFromStudent(student):
    '''Queries datastore to get the current value of the note associated with this user.'''
    notes = Teacher.query(Teacher.code == student.code, ancestor=root_parent()).fetch()
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

def GetBoolTeacher(student):
    notes = Teacher.query(Teacher.formBool, ancestor=root_parent()).fetch()
    if notes:
        # We found a note, return it.
        return True
    else:
        # We didn't find a note, return None
        return False

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
        if GetStudent(users.get_current_user()) == None:
            new_student = Student(parent=root_parent())
            new_student.user = users.get_current_user()
            new_student.code = int(self.request.get("code"))
            new_student.email = (users.get_current_user()).email()
            new_student.put()
            self.redirect('/studentSession')
        else :
            newCode = int(self.request.get("code"))
            currentStudent = GetStudent(users.get_current_user())
            currentStudent.code = newCode
            currentStudent.put()
            self.redirect('/studentSession')


class StudentSessionPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (GetStudent(user).code == GetCodeTeacher(GetStudent(user))):
            template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            print "The logic is correct"
            # Open Close visual for StudentSession html
            data = {
            "open_closed" : "Open"
            }
            if GetTeacherFromStudent(GetStudent(user)).formProperty == True:
                data["open_closed"] = "Open"
            else:
                data["open_closed"] = "Closed"

            self.response.write(template.render(data))
        elif (GetStudent(user).code != GetCodeTeacher(GetStudent(user))):
             template = JINJA_ENVIRONMENT.get_template('templates/studentDashboard.html')
             self.response.headers['Content-Type'] = 'text/html'
             self.response.write(template.render({"notCorrect": "Sorry, that's not a valid code. Try again!"}))

        print "THE TEACHER CODE IS: " + str(GetCodeTeacher(GetStudent(user)))
        print "THE STUDENT CODE IS: " + str(GetStudent(user).code)
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())
        self.redirect('/studentSession')

class StudentFeedbackPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if (GetBoolTeacher(user)):
            template = JINJA_ENVIRONMENT.get_template('templates/studentFeedback.html')
            self.response.headers['Content-Type'] = 'text/html'
            print "The logic is correct"
            self.response.write(template.render())
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/studentSession.html')
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(template.render({"noInput": "The teacher is not allowing feedback at this time."}))

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
        if GetTeacher(users.get_current_user()) == None:
            new_teacher = Teacher(parent=root_parent())
            new_teacher.user = users.get_current_user()
            new_teacher.email = (users.get_current_user()).email()
            new_teacher.code = randint(100,999)
            new_teacher.put()
            self.redirect('/teacherSession')
        else:
            newCode = randint(100,999)
            currentTeacher = GetTeacher(users.get_current_user())
            currentTeacher.code = newCode
            currentTeacher.put()
            self.redirect('/teacherSession')

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
            "open_close" : "Open",
            "tCode": int(GetTeacher(user).code),
            "numOf1": len(number1),
            "numOf2": len(number2),
            "numOf3": len(number3),
            "numOf4": len(number4),
            "numOf5": len(number5),
            "questions": questions
        }
        if GetTeacher(users.get_current_user()).formProperty == True:
            data["open_close"] = "Open"
        else:
            data["open_close"] = "Closed"

        print(data)
        self.response.write(template.render(data))

class DeleteNames(webapp2.RequestHandler):
    def post(self):
        to_delete = self.request.get('to_delete', allow_multiple=True)
        for entry in to_delete:
            key = ndb.Key(urlsafe=entry)
            key.delete()
        self.redirect('/teacherSession')

class FormBool(webapp2.RequestHandler):
    def post(self):
        if GetTeacher(users.get_current_user()).formProperty == True:
            currentTeacher = GetTeacher(users.get_current_user())
            currentTeacher.formProperty = False
            currentTeacher.put()
            #Delete the fist of five from datastore
            to_delete = Number.query(ancestor=root_parent()).fetch()
            for entry in to_delete:
                key = ndb.Key(urlsafe=entry.key.urlsafe())
                key.delete()
            self.redirect('/teacherSession')
        else:
            currentTeacher = GetTeacher(users.get_current_user())
            currentTeacher.formProperty = True
            currentTeacher.put()
            #Delete the fist of five from datastore
            to_delete = Number.query(ancestor=root_parent()).fetch()
            for entry in to_delete:
                key = ndb.Key(urlsafe=entry.key.urlsafe())
                key.delete()
            self.redirect('/teacherSession')

class AjaxGetCurrentChat(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        student = GetStudent(user)
        if student is None:
            # No user is logged in, so don't return any value.
            self.response.status = 401
            return
        chat = GetChats(student)
        all_chat = []
        if chat is not None:
            # If there was a current note, update note.
            all_chat.append(chat)
        # build a dictionary that contains the data that we want to return.
        data = {'chat': all_chat}
        # Note the different content type.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(data))
#class
# The app config
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/studentDashboard', StudentDashboardPage),
    ('/studentSession', StudentSessionPage),
    ('/feedback', StudentFeedbackPage),
    ('/teacherDashboard', TeacherDashboardPage),
    ('/teacherSession', TeacherSessionPage),
    ('/addQuestion', AddQuestion),
    ('/addNumber', AddNumber),
    ('/ajax/get_current_chat',AjaxGetCurrentChat),
    ('/deleteNames', DeleteNames),
    ('/formBool', FormBool),

], debug=True)
