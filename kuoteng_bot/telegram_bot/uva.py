import requests

from bs4 import BeautifulSoup

import json
##import pprint
##pp = pprint.PrettyPrinter(indent=4)

USERNAME = 'rapirent'
PASSWD = 'ddddfvgc'

URL = 'https://uva.onlinejudge.org/'
session = requests.session()

GET = '0'
POST = '1'

def get_params(form):
    params = {}
    inputs = form.find_all('input')
    for i in inputs:
        name = i.get('name')
        value = i.get('value')
        if name: 
            params[name] = value if value else '' 

    return params

def get_soup(url, action = GET, params = {}):
    request = None

    if action == GET: 
        request = session.get(url)
                                               
    elif action == POST: 
        request = session.post(url, params) 
    
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup 

def make_login():
    soup = get_soup(URL)
    form = soup.find(id = "mod_loginform")
    if not form:
        return False
    url = form['action']
    params = get_params(form)

    params['username'] = USERNAME 
    params['passwd'] = PASSWD
    
    soup = get_soup(url, action = POST, params = params)
    if soup.find(id = "mod_loginform"): 
        return False 
    else: 
        return True

def get_problem(number):
    get_url = 'http://uhunt.felix-halim.net/api/p/num/' + str(number)
    res = requests.get(get_url)
    data = json.loads(res.text)
    return data

def set_account(uva_id, uva_passwd):
    USERNAME = uva_id
    PASSWD = uva_passwd



def submit(uva_id, uva_passwd, number, file_path):
    set_account(uva_id,uva_passwd)
#    print(number)
    problem = get_problem(number)
#    print(problem)
    if problem == {}:
        return False
    else:
        problem_id = int(problem[u'pid'])
        base_url = 'http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=submit_problem&problemid=' + str(problem_id) + '&category='

        code = requests.get(file_path).content
        login = make_login()

        if login:
            soup = get_soup(base_url)
            form = soup.find_all('form')[1]
            params = get_params(form)
            name = form.textarea['name']
            params[name] = code
            params['language'] = '3'
            params['localid'] = str(number)
            
            headers = {
                'Referer': URL
            }
            r = session.post(URL + form['action'], data=params)
            print(r)
            # soup = get_soup(URL + 'option=com_onlinejudge&Itemid=8&page=save_submission', action = POST, params = params)
            return True
        else:
            print('Error login')
            return False

