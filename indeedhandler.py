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
        response = br.open(br.geturl() + '&limit=50') # 50 items per page, consider looping through pages
        print br.geturl()
        response = response.read()

        soup = BeautifulSoup(response)

        titles = soup.findAll("a", attrs={"data-tn-element": "jobTitle"})
        titles = [item.text for item in titles]
        companies = self._find_field_in_soup(soup, "company")
        locations = self._find_field_in_soup(soup, "location")
        summaries = self._find_field_in_soup(soup, "summary")
        dates = self._find_field_in_soup(soup, "date")

        return self._create_jobs_dict(title=titles, company=companies, location=locations, summary=summaries, date=dates)

    def _find_field_in_soup(self, soup, class_name):
        results = soup.findAll("span", attrs={"class": class_name})
        return [item.text for item in results]

    def _create_jobs_dict(self, **kwargs):
        for lst in kwargs.values():
            print len(lst) # may want to assert they are all equals here

        jobs_list = []
        for field, value in kwargs.items():
            for i in range(len(value)):
                try:
                    jobs_list[i][field] = value[i]
                except IndexError:
                    jobs_list.append({field: value[i]})
        return jobs_list


