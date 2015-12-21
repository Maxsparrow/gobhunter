import mechanize
from BeautifulSoup import BeautifulSoup

class IndeedHandler:
    def check_indeed(self, title, city):
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_handle_robots(False)

        indeed_url = 'http://www.indeed.com'

        br.open(indeed_url)

        br.form = list(br.forms())[0]

        br["q"] = title # The What id
        br["l"] = city # The Where id
        response = br.submit()
        print br.geturl()
        response = br.open(br.geturl() + '&limit=20') # 20 items per page, this is good to keep only relevant items
        print br.geturl()
        response = response.read()

        soup = BeautifulSoup(response)

        titles_soup = soup.findAll("a", attrs={"data-tn-element": "jobTitle"})
        titles = [item.text for item in titles_soup]
        urls = ['http://www.indeed.com' + item.get('href') for item in titles_soup]
        companies = self._find_field_in_soup(soup, "company")
        locations = self._find_field_in_soup(soup, "location")
        summaries = self._find_field_in_soup(soup, "summary")
        dates = self._find_field_in_soup(soup, "date")

        return self._create_jobs_dict(title=titles, company=companies, location=locations,
                                      summary=summaries, date_posted=dates, job_url=urls)

    def _find_field_in_soup(self, soup, class_name):
        results = soup.findAll("span", attrs={"class": class_name})
        return [item.text.encode('ascii', 'ignore') for item in results]

    def _create_jobs_dict(self, **kwargs):
        # assert they are all equal length here
        first_len = len(kwargs.values()[0])
        for lst in kwargs.values():
            if len(lst) != first_len:
                raise IndexError("Object is not correct length. Please find the bad value: %s" % kwargs)

        jobs_list = []
        for field, value in kwargs.items():
            for i in range(len(value)):
                try:
                    jobs_list[i][field] = value[i]
                except IndexError:
                    jobs_list.append({field: value[i]})
        return jobs_list


