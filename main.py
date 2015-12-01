import mechanize
from BeautifulSoup import BeautifulSoup
import re
import requests
from connections import *

def get_cities():
    br = mechanize.Browser()

    cities_url = 'http://greatist.com/health/20-best-cities-20-somethings'

    response = br.open(cities_url)
    html = response.read()

    soup = BeautifulSoup(html)

    h4results = soup.findAll('h4')

    raw_cities = [r.text for r in h4results if re.findall('[0-9]\.', r.text)]

    cities = [" ".join(city.split()[1:]) for city in raw_cities]

    return cities


def get_glassdoor_rating(company):
    query = company
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
               'content-type': 'application/json',
               'accept-language': 'en-US'
              }
    user_ip = '73.209.138.204'
    api_url = 'http://api.glassdoor.com/api/api.htm?t.p=%s&t.k=%s&userip=%s&useragent=&format=json&v=1&action=employers&q=%s' % (glassdoor_p_id, glassdoor_key, user_ip, query)
    print api_url
    print headers
    response = requests.get(api_url, headers=headers)
    print response.text
    
def check_indeed(title, city):
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)

    indeed_url = 'http://www.indeed.com'

    response = br.open(indeed_url)
    html = response.read()

    br.form = list(br.forms())[0]

    br["q"] = "Developer" # The What id
    br["l"] = "Washington, DC" # The Where id
    response = br.submit()
    print br.geturl()
    return response.read()
