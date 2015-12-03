import mechanize
from BeautifulSoup import BeautifulSoup
from bs4.diagnose import diagnose
import re
from connections import glassdoor_p_id, glassdoor_key
from glassdoorhandler import GlassdoorHandler

def get_cities():
    br = mechanize.Browser()

    cities_url = 'http://greatist.com/health/20-best-cities-20-somethings'

    response = br.open(cities_url)
    html = response.read()

    soup = BeautifulSoup(html)

    h4results = soup.findAll('h4')

    print diagnose(html)

    cities = {}
    for item in h4results:
        if re.findall('[0-9]\.', item.text):
            city = " ".join(item.text.split()[1:])
            description = item.findNext('p').text
            cities[city] = description

    return cities

def check_indeed(title, city):
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)

    indeed_url = 'http://www.indeed.com'

    br.open(indeed_url)

    br.form = list(br.forms())[0]

    br["q"] = title # The What id
    br["l"] = city # The Where id
    response = br.submit()
    print br.geturl()
    return response.read()


if __name__ == '__main__':
    cities = get_cities()
    print cities

    # print check_indeed("Developer", "Washington, DC")

    glassdoor = GlassdoorHandler(glassdoor_p_id, glassdoor_key, '73.209.138.204')
    print glassdoor.get_company_rating('IBM')

    print glassdoor.get_job_progression('plant manager')

    # print glassdoor.get_job_stats('Washington, DC')