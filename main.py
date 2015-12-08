import mechanize
from BeautifulSoup import BeautifulSoup
import re
from connections import glassdoor_p_id, glassdoor_key
from glassdoorhandler import GlassdoorHandler
import random

def get_cities():
    br = mechanize.Browser()

    cities_url = 'http://greatist.com/health/20-best-cities-20-somethings'

    response = br.open(cities_url)
    html = response.read()

    soup = BeautifulSoup(html)

    h4results = soup.findAll('h4')

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


def read_jobs_list(file_name):
    with open(file_name) as f:
        results = f.readlines()

    return [result[:-1] for result in results]

def pick_random(a_list):
    return random.choice(a_list)

def start():
    jobs_list = read_jobs_list('jobslist.txt')

    selected_job = pick_random(jobs_list)

    cities = get_cities()
    selected_city = pick_random(cities.keys())

    print check_indeed(selected_job, selected_city)


if __name__ == '__main__':
    start()

    # print check_indeed("Developer", "Washington, DC")

    # glassdoor = GlassdoorHandler(glassdoor_p_id, glassdoor_key, '73.209.138.204')
    # print glassdoor.get_company_rating('IBM')

    # print glassdoor.get_job_progression('plant manager')

    # print glassdoor.get_job_stats('Washington, DC')