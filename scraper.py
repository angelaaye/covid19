import json
import requests
from bs4 import BeautifulSoup


def get_weekly_state_data(state, abbrev, url, result):
    post_params = { 'level': 'state',
                    'final_yr': '2021',
                    'strtdate': '2020',
                    'enddate': '2021',
                    'filetype': 'html',
                    'states[]': abbrev,
                    'submit': 'Submit'}
    response = requests.post(url, data=post_params)
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup.prettify())

    result[state] = []

    rows = soup.select("tr")
    for row in rows[2:]: # first row is [<td axis="No Information available" colspan="10" id="noinfo"></td>], second row is empty
        columns = row.select("td")
        result[state].append({
            "Filed Week Ended": columns[0].attrs['headers'][1],
            "Initial Claims": columns[0].text.title(),
            "Reflecting Week Ended": columns[1].text.title(),
            "Continued Claims": columns[2].text.title(),
            "Covered Employment": columns[3].text.title(),
            "Insured Unemployment Rate": columns[4].text.title(),
        })

if __name__ == "__main__":
    with open("states.txt", "r") as f:
        states = f.read().splitlines()

    url = 'https://oui.doleta.gov/unemploy/wkclaims/report.asp'

    result = {}

    for state in states:
        state = state.split(',')
        get_weekly_state_data(state[0], state[1], url, result)

    with open("UI.json", "w") as f:
        json.dump(result, f)






# Method 1: Can't redirect to the corrent URL
# import scrapy

# class UnemploymentInsurance(scrapy.Spider):
#     name = "UI"

#     start_urls = ['https://oui.doleta.gov/unemploy/claims.asp']
    
#     def parse(self, response):
#         return scrapy.FormRequest.from_response(
#             response,
#             meta = {
#                 'dont_redirect': True,
#                 'handle_httpstatus_list': [302]
#             },
#             formid='wkclaim',
#             # dont_click=True,
#             formdata = {"level": "state",
#                         "final_yr": "2021",
#                         "strtdate": "2020",
#                         "enddate": "2021",
#                         "filetype": "html",
#                         "states[]": "AL",
#                         "submit": "Submit"},
#             callback = self.download_file
#             )

#     def download_file(self, response):
#         filename = 'alaska.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)
#         # self.log(response.url)




# Method 2: Can't seem to install webdriver on Mac...

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from bs4 import BeautifulSoup

# driver = webdriver.Chrome()

# driver.get('https://oui.doleta.gov/unemploy/wkclaims/report.asp')

# search_button = driver.find_element_by_id("submit")
# search_button.click()

# doc = BeautifulSoup(driver.page_source, "html.parser")
# print(doc.prettify())