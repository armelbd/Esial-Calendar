'''
Created on Sep 20, 2011
@author: Armel Bourgon Drouot (armel.bourgon-drouot@esial.net)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from google.appengine.ext import db
from datetime import date

MAX_REQUEST_COUNT = 10

class Request(db.Model):
    
    studentId = db.IntegerProperty()
    calSring = db.TextProperty()
    counterDate = db.DateProperty()
    count = db.IntegerProperty()
    
    @classmethod
    def pushCalendar(cls,studentId,calString):
        """
        For a given student id and a calendar string,
        store this informations in the database.
        """
        
        #check if we have a calendar for this id
        q = db.GqlQuery("SELECT * FROM Request WHERE studentId = :1",int(studentId))
        request = q.get()
        if request is None :
            #It's the first time that this request is made
            #add it to the database
            request = Request()
            request.studentId = int(studentId)
            request.calSring = calString.decode("utf-8")
            request.counterDate = date.today()
            request.count = 1
            request.put()
        else :
            #Update request info
            request.calSring = calString.decode("utf-8")
            request.count += 1
            request.put()
            
    @classmethod
    def pullCalendar(cls,studentId,increment):
        """
        For a given student id return the last saved calendar
        or None if any calendar save.
        If increment is True increment request count.
        """
        q = db.GqlQuery("SELECT * FROM Request WHERE studentId = :1",int(studentId))
        request = q.get()
        
        if request is None :
            return None
        else :
            if increment :
                request.count += 1
                request.put()
            return request.calSring
        
    @classmethod
    def isRequestAuthorized(cls,studentId):
        """
        Return true if the request is authorized
        A request is authorized if less than MAX_REQUEST_COUNT of the same request
        have been made today
        """
        
        q = db.GqlQuery("SELECT * FROM Request WHERE studentId = :1",int(studentId))
        request = q.get()
        
        if request is None :
            #It's the first time that this request is made
            return True
        else :
            if request.counterDate == date.today() :
                return (request.count < MAX_REQUEST_COUNT)
            else :
                #No requests of this kind have been made today
                #Update the counter
                request.counterDate = date.today()
                request.count = 0
                request.put()
                return True 
        