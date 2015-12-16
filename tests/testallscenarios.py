from main import generate_jobs_list, create_email_jobs_message, read_jobs_list, get_cities

cities = get_cities()
jobs = read_jobs_list('jobslist.txt')

for selected_city in cities:
    for selected_job in jobs:
        jobs_list = generate_jobs_list(selected_job, selected_city)

        message_body = create_email_jobs_message(jobs_list, selected_job, selected_city, 10)

        from pprint import pprint
        print message_body.replace("<br>","\n")
