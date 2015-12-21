import requests
import json
import time

class GlassdoorHandler:
    def __init__(self, api_p_id, api_key, user_ip):
        self._headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
                        'content-type': 'application/json',
                        'accept-language': 'en-US'
                         }

        self._api_p_id = api_p_id
        self._api_key = api_key
        self._base_uri = 'http://api.glassdoor.com/api/api.htm'
        self._user_ip = user_ip

    def _get(self, action, **kwargs):
        api_url = self._base_uri + '?t.p=%s&t.k=%s&userip=%s&useragent=&format=json&v=1&action=%s' % (self._api_p_id, self._api_key, self._user_ip, action)
        for k, v in kwargs.items():
            api_url += '&%s=%s' % (k, v)

        num_attempts = 0
        valid_response = False
        while not valid_response:
            response = requests.get(api_url, headers=self._headers)
            json_data = json.loads(response.text)
            if response.ok and 'response' in json_data:
                return json_data
            elif num_attempts == 5:
                return None
            else:
                print "Failed api response, waiting 60 seconds"
                num_attempts += 1
                time.sleep(60)

    def get_company_rating(self, company):
        results = self._get('employers', q=company)['response']
        if results['employers']:
            results_dict = {'glassdoor_url': results['attributionURL'],
                            'glassdoor_rating': results['employers'][0]['overallRating'],
                            'glassdoor_company_name': results['employers'][0]['name']
                            }
            if 'featuredReview' in results['employers'][0]:
                results_dict.update({'glassdoor_pros': results['employers'][0]['featuredReview']['pros'],
                                     'glassdoor_cons': results['employers'][0]['featuredReview']['cons']})
            return results_dict
        return

    def get_job_progression(self, jobtitle):
        return self._get('jobs-prog', countryId=1, jobTitle=jobtitle)

    def get_job_stats(self, city):
        return self._get('jobs-stats', returnCities='true', returnJobTitles='true', l=city)