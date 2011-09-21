'''
Created on Sep 8, 2011
@author: Armel Bourgon Drouot (armel.bourgon-drouot@esial.net)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from esialCalendar import app
from esialCalendar.data.request import Request
from random import choice
import urllib2
import re

#A list of browser user agents
USER_AGENTS = ['Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.24 \
                    (KHTML, like Gecko) Chrome/11.0.696.60 Safari/534.24',
                'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.4 \
                    (KHTML, like Gecko) Chrome/5.0.375.125 Safari/533.4',
                'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.4 \
                    (KHTML, like Gecko) Chrome/5.0.375.125 Safari/533.4'
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.2 \
                    (KHTML, like Gecko) Chrome/15.0.874.5 Safari/535.2',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20051111 Firefox/1.5 BAVM/1.0.0',
                'Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.1.14) Gecko/20080821 Firefox/2.0.0.14',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 \
                    (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
                'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 \
                    (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; \
                     .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; \
                     .NET4.0C; .NET4.0E; InfoPath.3; Creative AutoUpdate v1.40.02)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; \
                    .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; \
                    .NET4.0C; .NET4.0E; InfoPath.3; Creative AutoUpdate v1.40.02)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; GTB6.5; Mozilla/4.0 \
                    (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; \
                    Media Center PC 5.0; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; \
                     .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; \
                     .NET CLR 1.1.4322; .NET CLR 3.0.04506; eMusic DLM/4; OfficeLiveConnector.1.3; \
                     OfficeLiveConnector.1.4; OfficeLivePatch.0.0; \
                     OfficeLivePatch.1.3; SLCC1; .NET4.0C; .NET4.0E; InfoPath.3; Zune 4.7; MS-RTC LM 8; yie8)'
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; FunWebProducts; SLCC1; \
                    .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; \
                    Windows-Media-Player/10.00.00.3990)'
                ]
    
@app.route('/<id>',methods=['GET'])
def main(id):
    
    #Check that the given parameter is a student id
    if id == None or not re.match('[0-9]{8}',id):
        return 'Bad Request' , 400
    
    #check if the request is authorized
    if not Request.isRequestAuthorized(id) :
        #if credit exceed return the saved calendar
        calString = Request.pullCalendar(id)
        if calString is not None :
            return calString
        else :
            return 'Request credit exceeded for this student id', 401 
    
    #ADE requires a cookie handler
    cookieprocessor = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler, cookieprocessor)
    urllib2.install_opener(opener)
    
    #Build a request that looks like a browser one
    request = urllib2.Request('https://synchro-edt.uhp-nancy.fr/synchroZimbra/synchro?code=' + 
                              id +'&projectId=2')
    request.add_header('user-agent' , choice(USER_AGENTS))
    request.add_header('Connection', 'keep-alive')
    request.add_header('accept-encoding','gzip,deflate,sdch')
    request.add_header('accept-language','en-US,en,q=0.8')
    request.add_header('accept-charset','ISO-8859-1,utf-8;q=0.7,*,q=0.3')
    request.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    
    #Call ADE
    try :
        response = opener.open(request)
        calString = response.read()
    except Exception :
        #ADE is down, try to get the lastest saved calendar from database
        calString = Request.pullCalendar(id)
        if calString is not None :
            return calString
        else :
            #We have any calendar save for this student
            return 'ADE is Down', 502
        
    #Check if the respond is a calendar
    if not re.search("BEGIN:VCALENDAR", calString) :
        return "can't retrieve calendar for student " + id , 502 
    
    #save the calendar into the database
    Request.pushCalendar(id, calString)
    
    return calString
        
