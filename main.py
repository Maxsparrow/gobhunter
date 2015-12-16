import random
from collections import OrderedDict
import mechanize
from BeautifulSoup import BeautifulSoup
import re
from indeedhandler import IndeedHandler
from connections import glassdoor_p_id, glassdoor_key, email_user, email_pass
from glassdoorhandler import GlassdoorHandler
from emailsender import send_email

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
    if int(job_dict['date_posted'][:2]) < DAYS_OLD_LIMIT:
        return True
    return False

def _filter_remove_nones(jobs_list):
    return [job for job in jobs_list if job]

def pick_random(a_list):
    return random.choice(a_list)

def order_jobs_dicts(jobs_list):
    key_list = ['title', 'company', 'glassdoor_company_name', 'location',
                'glassdoor_rating', 'summary', 'glassdoor_pros', 'glassdoor_cons',
                'glassdoor_url', 'job_url', 'date_posted']
    new_job_list = []
    for job_dict in jobs_list:
        ordered_jobs_dict = OrderedDict()
        for key in key_list:
            if key in job_dict:
                ordered_jobs_dict[key] = job_dict[key]
        new_job_list.append(ordered_jobs_dict)

    return new_job_list

def order_jobs_by_rating(jobs_list):
    n = len(jobs_list)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if float(jobs_list[i-1]['glassdoor_rating']) < float(jobs_list[i]['glassdoor_rating']):
                temp = jobs_list[i-1]
                jobs_list[i-1] = jobs_list[i]
                jobs_list[i] = temp
                swapped = True
    return jobs_list

def create_email_jobs_message(jobs_list, job_title, city, number_of_jobs):
    message_body = "Today's top %s jobs for '%s' in %s: " % (number_of_jobs, job_title, city)
    for job in jobs_list[:number_of_jobs]:
        message_body += "<br>"*2
        for key, value in job.items():
            message_body += "%s: %s<br>" % (key, value)
    return message_body

def generate_jobs_list(selected_job, selected_city):
    indeedhandler = IndeedHandler()
    jobs_list = indeedhandler.check_indeed(selected_job, selected_city)

    jobs_list = filter_jobs(jobs_list)

    jobs_list = order_jobs_dicts(jobs_list)

    jobs_list = order_jobs_by_rating(jobs_list)

    return jobs_list


def start():
    jobs_list = read_jobs_list('jobslist.txt')
    selected_job = pick_random(jobs_list)

    cities = get_cities()
    selected_city = pick_random(cities.keys())

    selected_job = 'lead engineer'
    selected_city = 'Atlanta, GA'

    jobs_list = generate_jobs_list(selected_job, selected_city)

    message_body = create_email_jobs_message(jobs_list, selected_job, selected_city, 10)

    from pprint import pprint
    pprint(message_body.replace("<br>","\n"))

    send_email(email_user, ['maxsparrow@gmail.com'], "Today's jobs", message_body, email_user, email_pass)


if __name__ == '__main__':
    start()

    # print check_indeed("Developer", "Washington, DC")

    # print glassdoor.get_job_progression('plant manager')

    # print glassdoor.get_job_stats('Washington, DC')