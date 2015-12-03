import requests

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
        response = requests.get(api_url, headers=self._headers)
        return response.text

    def get_company_rating(self, company):
        return self._get('employers', q=company)

    def get_job_progression(self, jobtitle):
        return self._get('jobs-prog', countryId=1, jobTitle=jobtitle)

    def get_job_stats(self, city):
        return self._get('jobs-stats', returnCities='true', returnJobTitles='true', l=city)