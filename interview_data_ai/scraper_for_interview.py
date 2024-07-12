import aiohttp
from aiohttp import ClientSession
import asyncio
import async_timeout
from bs4 import BeautifulSoup
import json
import random


class ParsePageData:
    @staticmethod
    def parse_title_information(soup):
        result = {}

        tag_sections = soup.find_all("div", class_="sc-13223bcc-0")
        for tag in tag_sections:
            tag_key = tag.find('div', class_="sc-13223bcc-1")
            tag_value = tag.find('div', class_="sc-13223bcc-2")
            if tag_key and tag_key.text.strip():
                _key = tag_key.text.strip()
                result[_key] = tag_value.text.strip() if tag_value else ""

        return result

    @classmethod
    def parse_overview(cls, soup):
        # print("began to parse overview")
        overview = cls.parse_title_information(soup)

        tag_description = soup.find("p", attrs={"data-testid": "more-about-text"})
        overview["Description"] = tag_description.text.strip() if tag_description else ""

        tag_institution = soup.find(id="csp-custom-description-id-text")
        overview["From the Institution"] = tag_institution.text.strip() if tag_institution else ""

        # print("end to parse overview")

        return overview

    @classmethod
    def parse_admissions(cls, soup):
        # print("began to parse admissions")
        admissions = cls.parse_title_information(soup)

        tag_by_the_numbers = soup.find("p", class_="sc-32c54a86-6 JrLSP cb-paragraph1-st cb-margin-bottom-32")
        admissions["By the Numbers"] = tag_by_the_numbers.text.strip() if tag_by_the_numbers else ""

        tag_sections = soup.find_all("section", class_="sc-9c7840b9-2 jggIiR cb-margin-bottom-32")
        for tag in tag_sections:
            tag_key = tag.find('h4')
            tag_value = tag.find('p')
            if tag_key and tag_key.text.strip():
                _key = tag_key.text.strip()
                _key = _key[:-1] if _key.endswith("*") else _key
                if _key in ["SAT Range"]:
                    # ignore it because it was saved in the above section
                    continue

                if _key.startswith("Acceptance Rate"):
                    applicants_data = {}
                    tag_applicants = tag.select("ul > li")
                    for tag_applicant in tag_applicants:
                        applicant_key = tag_applicant.find("div",
                                                           class_="HorizontalFunnelChartLabelListstyles__LabelItemName-bf-ui-components__sc-2f4def-2")
                        applicant_value = tag_applicant.find("div",
                                                           class_="HorizontalFunnelChartLabelListstyles__LabelItemValue-bf-ui-components__sc-2f4def-3")
                        if applicant_key and applicant_key.text.strip():
                            applicants_data[applicant_key.text.strip()] = int(applicant_value.text.strip().replace(",", "")) if applicant_value else applicant_value
                    else:
                        admissions["Applicants_Data"] = applicants_data
                else:
                    admissions[_key] = tag_value.text.strip() if tag_value else ""

        # For application Requirements
        application_requirements = {}
        tag_sections = soup.find("ul", id="application-requirements-information").find_all("li")
        for tag in tag_sections:
            tag_key = tag.find("span", class_="cs-label-value-pair-label")
            tag_value = tag.find("span", class_="cs-label-value-pair-value")
            if tag_key and tag_key.text.strip():
                _key = tag_key.text.strip()
                application_requirements[_key] = tag_value.text.strip() if tag_value else ""
        else:
            admissions["Application Requirements"] = application_requirements

        tag_application_deadline = soup.find("div", attrs={"data-testid": "csp-important-dates-date-early-action-application-due"})
        admissions["Application Deadline"] = tag_application_deadline.text.strip() if tag_application_deadline else ""

        tag_application_fee = soup.find("span", attrs={"class": "cs-label-value-pair-value cs-application-process-application-fee"})
        admissions["Application Fee"] = tag_application_fee.text.strip() if tag_application_fee else ""

        application_types_accepted = []
        tag_application_types_accepted = soup.find("ul", attrs={"class": "cb-text-list cb-padding-left-24"}).find_all("li")
        for tag in tag_application_types_accepted:
            application_types_accepted.append(tag.text.strip())
        admissions["Application Types Accepted"] = application_types_accepted

        # print("end to parse admissions")

        return admissions

    @classmethod
    def parse_academics(cls, soup):
        # print("began to parse academics")
        academics = cls.parse_title_information(soup)

        tag_ap_credit_policy = soup.find("p", attrs={"class": "sc-32c54a86-6 JrLSP cb-paragraph1-st cb-margin-bottom-32"})
        academics["AP Credit Policy"] = tag_ap_credit_policy.text.strip() if tag_ap_credit_policy else ""

        ap_credits_list = {}
        tag_ap_credits_list = soup.find("ul", id="ap_credits_list").find_all("li")
        for tag in tag_ap_credits_list:
            tag_credit = tag.find_all("p")
            _key = tag_credit[0]
            _value = tag_credit[1]
            if _key and _key.text.strip():
                _key = _key.text.strip()
                ap_credits_list[_key] = _value.text.strip() if _value else ""
        else:
            academics["AP Credits List"] = ap_credits_list

        # ap_courses_list = []
        # ap_courses_header = []
        # tag_ap_courses_header = soup.find("thead", attrs={"data-testid": "csp-ap-credit-policy-table-header"}).find("tr").find_all("th")
        # for tag in tag_ap_courses_header:
        #     ap_courses_header.append(tag.text.strip())
        # else:
        #     ap_courses_data = {}
        #     tag_ap_courses_body = soup.find("tbody", attrs={"data-testid": "csp-ap-credit-policy-table-body"}).find_all("tr")
        #     for index, tag_row in tag_ap_courses_body:
        #         tag_cells = tag_row.select(".cell")
        #         ap_courses_data[ap_courses_header[index]] = tag_cells.text.strip()
        #     else:
        #         ap_courses_list.append(ap_courses_data)
        # academics["AP Courses List"] = ap_courses_list


        # majors_list = []
        # tag_majors_list = soup.find("ul", id="csp-majors-typeahead-unordered-list").find_all("li")
        # for tag in tag_majors_list:
        #     majors_list = tag.select("ul > li")
        #     for major in majors_list:
        #         majors_list.append(major.text.strip())
        # else:
        #     academics["Majors List"] = majors_list

        json_data = json.loads(soup.find("script", id="__NEXT_DATA__").text)
        college_data = json_data["props"]["pageProps"]["collegeData"]

        course_list, course_list_dict = [], college_data.get("apExamTypes")
        course_list_dict = sorted(course_list_dict, key=lambda x: x["examType"])
        for course in course_list_dict:
            course_list.append({
                course["examType"]: {
                    "Min Score Required": course["values"][0]['apcpMinScoreRequired'],
                    "Number of Credits": course["values"][0]['apcpCreditsAwarded'],
                    "Course Equivalent": course["values"][0]['apcpCourseEquivalent']
                }
            })
        else:
            academics["Course List"] = course_list

        tag_majors_and_degrees = soup.find("p", id="csp-academics-majors-header-description")
        academics["Majors and Degrees"] = tag_majors_and_degrees.text.strip() if tag_majors_and_degrees else ""

        majors_list, majors_list_dict = [], college_data.get("collegeMajors")
        for major in majors_list_dict:
            majors_list.append(major["name"])
        else:
            majors_list.sort()
            academics["Major List"] = majors_list

        special_academics_program = []
        tag_sections = soup.find("ul", id="special_academics_program").find_all("li")
        for tag in tag_sections:
            special_academics_program.append(tag.text.strip())
        else:
            academics["Special Academics Program"] = special_academics_program

        # print("end to parse academics")

        return academics

    @classmethod
    def parse_costs(cls, soup):
        # print("began to parse costs")

        costs = cls.parse_title_information(soup)

        Tuition = {}
        tag_average_net_price = soup.find('span', class_='sc-ffa908c4-3 ctZrfL cb-paragraph1-st cb-margin-bottom-16')
        tag_tuition_description = soup.find('span', class_='sc-ffa908c4-4 hYKeHS cb-paragraph1-st cb-margin-bottom-16')
        Tuition["Average Net Price"] = tag_average_net_price.text.strip() if tag_average_net_price else ""
        Tuition["Description"] = tag_tuition_description.text.strip() if tag_tuition_description else ""
        costs["Tuition"] = Tuition

        tag_section = soup.find_all('h5', class_='cb-h5 cb-margin-bottom-16 cb-margin-top-32')
        for tag in tag_section:
            cost_key = tag.parent.find('h5').text.strip()
            cost = {}
            tag_cost = tag.parent.find_all('div', class_='sc-c7482855-0 dUwnCJ')
            for _tag in tag_cost:
                _key = _tag.find_all("p")[0]
                _value = _tag.find_all("p")[-1]
                if _key and _key.text.strip():
                    cost[_key.text.strip()] = _value.text.strip() if _value else ""
            else:
                costs[cost_key] = cost

        financial_aid = {}
        financial_aid["Description"] = soup.find(id="college-financial-aid-section").parent.parent.find("p").text.strip()
        tag_section = soup.find("div",attrs={"data-testid": "csp-financial-aid-title-section"}).find('div', class_='sc-32c54a86-1 bmKUUN cb-margin-bottom-16').find_all("ul")
        for tag in tag_section:
            aid_key = tag.parent.find("h5").text.strip()
            aid_section = {}
            tag_aid = tag.find_all("li")
            for _tag in tag_aid:
                _key = _tag.find_all("p")[0]
                _value = _tag.find_all("p")[-1]
                if _key and _key.text.strip():
                    aid_section[_key.text.strip()] = _value.text.strip() if _value else ""
            else:
                financial_aid[aid_key] = aid_section
        else:
            financial_aid["Tuition Guarantee Plans"] = soup.find("p", attrs={
                "data-testid": "csp-financial-aid-section-description"}).text.strip()
            costs["Financial Aid"] = financial_aid


        financial_aid_dates = {}
        tag_aid_dates = soup.find("div", attrs={"class": "csp-financial-aid-dates-section-container"})
        financial_aid_dates["Description"] = tag_aid_dates.find("div", attrs={"data-testid": "csp-financial-aid-dates-section-description"}).text.strip()
        tag_section = tag_aid_dates.find_all('div', class_='csp-financial-aid-dates-item-container')
        for tag in tag_section:
            tag_date = tag.find_all("span")
            _key = tag_date[0]
            _value = tag_date[-1]
            if _key and _key.text.strip():
                financial_aid_dates[_key.text.strip()] = _value.text.strip() if _value else ""
        else:
            costs["Financial Aid Dates"] = financial_aid_dates

        # print("end to parse costs")

        return costs

    @classmethod
    def parse_campus_life(cls, soup):
        # print("began to parse campus life")
        campus_life = cls.parse_title_information(soup)

        housing = {}
        house_cost_section = soup.find("div", class_="csp-housing-options-section-header-container").parent.parent.find_all("div", class_="sc-c7482855-0 dUwnCJ")
        for tag in house_cost_section:
            tag_house_cost =  tag.find_all("p")
            _key = tag_house_cost[0]
            _value = tag_house_cost[-1]
            if _key and _key.text.strip():
                housing[_key.text.strip()] = _value.text.strip() if _value else ""
        else:
            campus_life["Housing"] = housing

        housing_options = []
        tag_housing_options = soup.find(id="housing-options-list-items").find_all("li")
        for tag in tag_housing_options:
            housing_options.append(tag.text.strip())
        else:
            campus_life["Housing Options"] = housing_options

        json_data = json.loads(soup.find("script", id="__NEXT_DATA__").text)
        college_data = json_data["props"]["pageProps"]["collegeData"]
        sport_list, sport_list_dict = {}, college_data.get("studentSports")
        sport_list_dict = sorted(sport_list_dict, key=lambda x: (x['sportDescription'], x['sportTypeDescription']))
        for sport in sport_list_dict:
            new_sport_name = sport["sportDescription"]
            sport_gender = sport["genderDescription"]
            if not new_sport_name in sport_list.keys():
                sport_list[new_sport_name] = {}
            if not sport_gender in sport_list[new_sport_name].keys():
                sport_list[new_sport_name][sport_gender] = []
            sport_list[new_sport_name][sport_gender].append(sport["sportTypeDescription"])
        else:
            campus_life["Course Sports"] = sport_list

        activities = []
        tag_activities = soup.find(id="activities-options-list-items").find_all("li")
        for tag in tag_activities:
            activities.append(tag.text.strip())
        else:
            campus_life["Activities"] = activities


        tag_sections = soup.find(id="college-student-body-section").parent.parent.find_all("div", class_="cb-margin-bottom-32")
        student_body = {}
        tag_student_body = tag_sections[0]
        for tag in tag_student_body.find_all("li"):
            tag_body = tag.find_all("p")
            _key = tag_body[0]
            _value = tag_body[-1]
            if _key and _key.text.strip():
                student_body[_key.text.strip()] = _value.text.strip() if _value else ""
        else:
            campus_life["Student Body"] = student_body

        tag_other_sections = tag_sections[1:]
        for tag in tag_other_sections:
            tag_key, section_result = tag.find("h5").text.strip(), {}
            tag_li_sections = tag.find_all("li")
            for tag_li in tag_li_sections:
                tag_body = tag_li.find_all("p")
                _key = tag_body[0]
                _value = tag_body[-1]
                if _key and _key.text.strip():
                    section_result[_key.text.strip()] = _value.text.strip() if _value else ""
            else:
                campus_life[tag_key] = section_result

        # print("end to parse campus life")

        return campus_life


async def fetch_url(session, url):
    result = ""
    if not session or not url:
        return result

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:62.0) Gecko/20100101 Firefox/62.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"
    ]
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    print(f"began to download {url}")
    for attempt in range(10):
        try:
            async with async_timeout.timeout(3):
                async with session.get(url, headers=headers) as response:
                    # if the status code not in 200-399，then will raise an exception
                    response.raise_for_status()
                    result = await response.text()
                    print(f"completed to download {url}")
                    break
        except (aiohttp.ClientError, aiohttp.http.HttpProcessingError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            # wait for 0.1 second and retry it again
            await asyncio.sleep(0.1)
    else:
        print(f"Failed to download data from web page : {url}, Please try it latter again.")

    return result


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


async def fetch_pages(session, url, tag=None):
    result = {}
    url = '/'.join([url, tag]) if tag else url

    download_text = await fetch_url(session, url)
    if download_text:
        soup = BeautifulSoup(download_text, 'html.parser')
        if tag == "admissions":
            result = ParsePageData.parse_admissions(soup)
        elif tag == "academics":
            result = ParsePageData.parse_academics(soup)
        elif tag == "tuition-and-costs":
            result = ParsePageData.parse_costs(soup)
        elif tag == "campus-life":
            result = ParsePageData.parse_campus_life(soup)
        else:
            result = ParsePageData.parse_overview(soup)

    return result


async def scrape_college_list(url):
    # response = requests.get(url)
    result = []

    async with ClientSession() as session:
        download_text = await fetch_url(session, url)
        if download_text:
            soup = BeautifulSoup(download_text, 'html.parser')
            college_links = soup.select('a[class="cb-link-blue"]')
            for link in college_links:
                college = {
                    "name": link.get_text(strip=True),
                    "url": (url + link['href']).replace("/colleges/colleges", "/colleges")
                }
                result.append(college)

    if result:
        save_to_json(result, 'college_list.json')

    return result


async def scrape_college_data(url):
    result = {}

    tags = ['overview', 'admissions', 'academics', 'tuition-and-costs', 'campus-life']
    async with ClientSession() as session:
        tasks = []
        for tag in tags:
            if tag == 'overview':
                task = asyncio.create_task(fetch_pages(session, url))
            else:
                task = asyncio.create_task(fetch_pages(session, url, tag))
            tasks.append(task)
        else:
            results = await asyncio.gather(*tasks)
            result = dict(zip(tags, results))

    college_file_name = url.split("/")[-1].replace("-", "_")
    if result:
        save_to_json(result, f'{college_file_name}.json')

    return result


async def main(_url, _download_college_list):
    college_list = await scrape_college_list(url)
    if college_list:
        with open("college_list.json", 'r') as file:
            college_list = json.load(file)
            tasks = []
            for college in college_list:
                if college["name"] in download_college_list:
                    task = asyncio.create_task(scrape_college_data(college["url"]))
                    tasks.append(task)
            else:
                _ = await asyncio.gather(*tasks)

if __name__ == "__main__":
    url = 'https://bigfuture.collegeboard.org/colleges'
    download_college_list = ["Massachusetts Institute of Technology", "Harvard College"]
    asyncio.run(main(url, download_college_list))
