from indeedhandler import IndeedHandler
from connections import glassdoor_p_id, glassdoor_key, email_user, email_pass
from glassdoorhandler import GlassdoorHandler
from emailsender import send_email
from calendarhandler import get_events

DAYS_OLD_LIMIT = 20
MINIMUM_COMPANY_RATING = 3.0
NUMBER_OF_JOBS_TO_RETURN = 10
TO_ADDRESSES = ['maxsparrow@gmail.com', 'mjohnson7215@gmail.com']


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
    
def create_email_jobs_message(jobs_list, number_of_jobs):
    message_body = ""
    for job in jobs_list[:number_of_jobs]:
        if 'glassdoor_pros' in job and 'glassdoor_cons' in job:
            glassdoor_pros = job['glassdoor_pros']
            glassdoor_cons = job['glassdoor_cons']
        else:
            glassdoor_pros = glassdoor_cons = "NOT LISTED"

        job_html = """
        <h3><b>{title}</b></h3>
        <h4>{company} - <i>{location}</i><b><font size="0.8">    (Glassdoor Rating: {glassdoor_rating})</font></b></h4>
        {summary}<br><br>
        <b>Glassdoor Pros:</b> {glassdoor_pros}<br>
        <b>Glassdoor Cons:</b> {glassdoor_cons}<br>
        <a href='{glassdoor_url}'><b>Glassdoor URL</b></a><br><br>
        <a href='{job_url}'><b><font size="2">APPLY HERE</font></b></a> (job posted {date_posted})<br>
        <br>
        ------------------------------------------------------------------------------------
        """.format(title=job['title'], company=job['company'], location=job['location'], glassdoor_rating=job['glassdoor_rating'],
        summary=job['summary'], glassdoor_company_name=job['glassdoor_company_name'],
        glassdoor_pros=glassdoor_pros, glassdoor_cons=glassdoor_cons, glassdoor_url=job['glassdoor_url'],
        job_url=job['job_url'], date_posted=job['date_posted'])

        message_body += job_html
    return message_body

def generate_jobs_list(selected_job, selected_city):
    indeedhandler = IndeedHandler()
    try:
        jobs_list = indeedhandler.check_indeed(selected_job, selected_city)
    except IndexError:
        return

    jobs_list = filter_jobs(jobs_list)

    jobs_list = order_jobs_by_rating(jobs_list)

    return jobs_list


def start():
    selected_city = selected_job = None
    events = get_events()
    for event in events:
        summary = event['summary']
        if summary == "Initial Email":
            send_initial_email()
        else:
            itemtype, itemvalue = summary.split(": ")
            if itemtype == "City":
                selected_city = itemvalue
            if itemtype == "Job":
                selected_job = itemvalue
    
    if selected_city and selected_job:
        jobs_list = generate_jobs_list(selected_job, selected_city)

        subject = "Today's top %s jobs for %s in %s: " % (NUMBER_OF_JOBS_TO_RETURN, selected_job, selected_city)
        message_body = create_email_jobs_message(jobs_list, NUMBER_OF_JOBS_TO_RETURN)

        from pprint import pprint
        pprint(message_body.replace("<br>","\n"))
    
        send_email(email_user, TO_ADDRESSES, subject, message_body, email_user, email_pass)

def send_initial_email():
    message_body = """Merry Christmas, and welcome to Gobhunter! You will now receive daily job digests by email from Gobhunter.<br><br>
    The schedule can be found in another email inviting you to view gobhunter's calendar.<br>
    You can also modify the schedule yourself by modifying, deleting, or creating new events.<br><br>
    Guidelines: Each day should only have two events, one starting with "City: ", and another with "Job: "<br>
    For best results make the events 'whole day' events.<br><br>
    The default cities are chosen from this link: <a href="http://greatist.com/health/20-best-cities-20-somethings">Best cities for twenty somethings</a>.
    Extended descriptions for the cities are available there.<br><br>
    <br>Reply STOP to stop messages. Just kidding, that won't work, just ask Chris to stop the messages.<br>
    <br>My code can be found on github here. Not my best work, but still pretty cool: https://github.com/maxsparrow/gobhunter<br>
    """
    send_email(email_user, TO_ADDRESSES, "Welcome to Gobhunter!", message_body, email_user, email_pass)

if __name__ == '__main__':
    start()

    # print check_indeed("Developer", "Washington, DC")

    # print glassdoor.get_job_progression('plant manager')

    # print glassdoor.get_job_stats('Washington, DC')
