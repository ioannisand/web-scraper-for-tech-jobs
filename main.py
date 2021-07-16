from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime


# initializing lists of jobs
all_jobs_jobfind = []
all_jobs_kariera = []
today = datetime.datetime.now().date()



# ====================== JOBFIND.GR ==========================#

def scan_page_jobfind(number):
    url = f"https://www.jobfind.gr/JobAds/Pliroforiki_Tilepikoinonies/Athens/GR/Theseis_Ergasias?pageid={number}"
    # acquiring html content
    response = requests.get(url)

    # making soup
    soup = BeautifulSoup(response.text, "html.parser")

    # getting dates
    date_elements = soup.select(".date")
    dates = []
    for date_element in date_elements:
        dates.append(date_element.text)

    # getting job titles
    job_title_elements = soup.select(".title a")
    job_titles = []
    for job_title_element in job_title_elements:
        job_titles.append(job_title_element.text)

    # getting hrefs
    job_hrefs = soup.select(".title a", href=True)
    job_links = []
    for link in job_hrefs:
        whole_link = "https://www.jobfind.gr"
        new_link = whole_link + link['href']
        job_links.append(new_link)

    # getting city
    city_elements = soup.select(".city .darkblue")
    cities = []
    for city in city_elements:
        cities.append(city.text)

    # creating jobs as lists
    for i in range(len(job_titles)):
        job = [dates[i], job_titles[i], job_links[i], cities[i]]
        all_jobs_jobfind.append(job)
        print("jobfind", job)





#============================KARIERA.GR===========================#

def scan_page_kariera(number):
    url =  f"https://www.kariera.gr/%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82?filter_category=jn008&pg={number}"

    # acquiring html content
    response = requests.get(url)

    # making soup
    soup = BeautifulSoup(response.text, "html.parser")

    # getting time passed
    hours_ago_tags = soup.select(".date a")
    hours_ago_list = []
    for element in hours_ago_tags:
        hours_ago_list.append(element.text)

    # getting job titles
    job_title_elements = soup.select(".job-title")
    job_titles = []
    for job_title_element in job_title_elements:
        job_titles.append(job_title_element.text)

    # getting hrefs
    job_hrefs = []
    for job_title_element in job_title_elements:
        whole_link = 'https://www.kariera.gr/'
        new_link = whole_link + job_title_element["href"]
        job_hrefs.append(new_link)

    # getting location
    location_elements = soup.select("a.snapshot-item")
    locations = []
    for element in location_elements:
        locations.append(element.text)

    # creating jobs as lists
    for i in range(len(job_titles)):
        job = [hours_ago_list[i], job_titles[i], job_hrefs[i], locations[i]]
        all_jobs_kariera.append(job)
        print("Kariera", job)








page_number = int(input("Insert how many pages you want to save"))

for page in range(1, page_number + 1):
    scan_page_jobfind(page)
    scan_page_kariera(page)

print(all_jobs_jobfind)
print(all_jobs_kariera)
df_jobfind = pd.DataFrame(all_jobs_jobfind, columns=["Date", "Job Title", "Job Link", "Location"])
csv_jobfind_name = f"jobfind_tech_in_Athens{today}.csv"
df_jobfind.to_csv(csv_jobfind_name)

df_kariera = pd.DataFrame(all_jobs_kariera, columns=["Daate", "Job Title", "Job Link", "Location"])
csv_kariera_name = f"kariera_tech_in_Athens{today}.csv"
df_kariera.to_csv(csv_kariera_name)
