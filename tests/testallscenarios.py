from main import generate_jobs_list, create_email_jobs_message, read_jobs_list

cities = ['Chicago, IL', 'Washington, DC', 'Baltimore, MD', 'San Francisco, CA', 'Denver, CO', 'Portland, OR',
          'Boston, MA', 'Seattle, WA', 'New York, NY', 'Austin, TX', 'Minneapolis, MN', 'Oklahoma City, OK',
          'Cleveland, OH', 'Cincinnati, OH', 'Atlanta, GA', 'Detroit MI', 'Memphis, TN', 'Saint Paul, MN', 'Omaha, NE']
jobs = read_jobs_list('jobslist.txt')

for selected_city in cities:
    for selected_job in jobs:
        jobs_list = generate_jobs_list(selected_job, selected_city)

        message_body = create_email_jobs_message(jobs_list, selected_job, selected_city, 10)

        from pprint import pprint
        print message_body.replace("<br>","\n")
