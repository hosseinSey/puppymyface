from web_engine import app

# for running on the local machine: 
if __name__ == '__main__': 
    from flask import Flask
    app = Flask('web_engine') #app = Flask('web_engine')

from time import localtime, strftime
from redis import Redis 
from flask import session, request, redirect
from flask.templating import render_template
from .config import BaseConfig

app.config.from_object(BaseConfig)

redis = Redis(host = app.config['REDIS_HOST'], port = app.config['REDIS_PORT'])

def site_analytics():
    '''
    perform  the analytics of the website including: 
        - number of visits to the the home page
        - 
    '''
    if not redis.get('first_visit'): 
        redis.set('first_visit', strftime("%a, %d %b %Y %H:%M:%S", localtime()))    
    if not redis.get('first_visit_dat'): 
        redis.set('first_visit_day', strftime("%d %b %Y", localtime()))    
    redis.incr('hits')

@app.route('/')
def home_page():
    site_analytics()
    
    searchword = request.args.get('q', '')
    results = ''
    if searchword.lower() == 'test' or searchword.lower() == 't': 
        pass 

    return render_template('first_page.html', 
                           search_results = results, 
                           search_expr = searchword,
                           visit_number = redis.get('hits').decode(),
                           since = redis.get('first_visit_day').decode())


@app.route('/test')
def test():
    output = ''
    output += 'Hey There!'
    output += '<hr>'
    output += '<br>'
    output += 'The time is now: '
    output += strftime("%a, %d %b %Y %H:%M:%S", localtime())
    output += '<br>'
    output += strftime("%d %b %Y", localtime())
    output += '<br>'

    return output 


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
