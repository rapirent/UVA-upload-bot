import requests

from bs4 import BeautifulSoup

USERNAME = 'rapirent'
PASSWD = 'ddddfvgc'

URL = 'http://uva.onlinejudge.org/'
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
    soup = BeautifulSoup(html)
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
    get_url = 'http://uhunt.felix-halim.net/api/p/num/' + str(problem_number)
    res = requests.get(get_url)
    data = json.loads(resp.text)
    return data


def submit(number, file_path):
    promblem = get_problem(number)
    if problem == {}:

        return False
    else:
        problem_id = str(problem[u'pid'])

        base_url = 'http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=submit_problem&problemid=' + str(problem_id) + '%category='
#        base_url += str(problem_id)
#        base_url += '&category='

        code = requests.get(file_path)
        print(code)
        login = make_login()

        if login:
            soup = get_soup(base_url)
            form = soup.find_all('form')[1]

            params = get_params(form)
            name = form.textarea['area']
            params[name] = code
            params['language'] = 3
            get_soup(URL + form['action'], action = POST, params = params)

        else:
            print('Error login')

