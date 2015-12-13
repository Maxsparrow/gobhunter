import mechanize
from BeautifulSoup import BeautifulSoup
import re
from indeedhandler import IndeedHandler
from connections import glassdoor_p_id, glassdoor_key
from glassdoorhandler import GlassdoorHandler
from emailsender import send_email
import random

DAYS_OLD_LIMIT = 20
MINIMUM_COMPANY_RATING = 3.0

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

def read_jobs_list(file_name):
    with open(file_name) as f:
        results = f.readlines()

    return [result[:-1] for result in results]

def filter_jobs(jobs_list):
    new_jobs_list = []
    for job_dict in jobs_list:
        job_dict = _add_glassdoor_company_rating(job_dict)
        if job_dict and _filter_job_days(job_dict) and _filter_job_company_rating(job_dict):
            new_jobs_list.append(job_dict)

    new_jobs_list = _filter_remove_nones(new_jobs_list)
    return new_jobs_list

def _add_glassdoor_company_rating(job_dict):
    glassdoor = GlassdoorHandler(glassdoor_p_id, glassdoor_key, '73.209.138.204')
    glassdoor_results = glassdoor.get_company_rating(job_dict['company'])
    if glassdoor_results:
        job_dict.update(glassdoor_results)
        return job_dict

def _filter_job_company_rating(job_dict):
    if float(job_dict['glassdoor_rating']) > MINIMUM_COMPANY_RATING:
        return True
    return False

def _filter_job_days(job_dict):
    if int(job_dict['date'][:2]) < DAYS_OLD_LIMIT:
        return True
    return False

def _filter_remove_nones(jobs_list):
    return [job for job in jobs_list if job]

def pick_random(a_list):
    return random.choice(a_list)

def create_email_jobs_message(jobs_list):
    # TODO Implement this
    pass

def start():
    jobs_list = read_jobs_list('jobslist.txt')

    selected_job = pick_random(jobs_list)

    cities = get_cities()
    selected_city = pick_random(cities.keys())

    indeedhandler = IndeedHandler()

    jobs_list = indeedhandler.check_indeed(selected_job, selected_city)

    from pprint import pprint
    pprint(filter_jobs(jobs_list))


if __name__ == '__main__':
    start()

    # print check_indeed("Developer", "Washington, DC")

    # print glassdoor.get_job_progression('plant manager')

    # print glassdoor.get_job_stats('Washington, DC')