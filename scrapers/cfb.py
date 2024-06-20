import csv
import pandas as pd
import random
import requests

from bs4 import BeautifulSoup


def generate_user_agent():
    user_agents_list = [
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    ]
    agent = random.choice(user_agents_list)

    return agent
    

def scrape_schools(base_url):
    agent = generate_user_agent()
    data = requests.get(base_url, headers={"User-Agent": agent})
    if data.status_code == 200:
        html_content = data.text
        soup = BeautifulSoup(html_content, "html.parser")
        table_data = []
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_data = [col.get_text(strip=True) for col in columns]
                table_data.append(row_data)
    columns = ["School", "From", "To", "Yrs", "G", "W", "L", "T", "Pct", 
           "G", "W", "L", "T", "Pct", "SRS", "SOS", "AP", "CC", "Notes"]
    df = pd.DataFrame(table_data, columns=columns)
    df.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
    df.dropna(how='all', inplace=True)
    df['School_URL'] = df['School'].str.replace(' ', '-').apply(lambda x: f"{base_url}{x.lower()}/")
    school_urls = df['School_URL'].tolist()

    return school_urls

        # with open('output.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup.prettify()))

def scrape_school_info(school_urls):
    agent = generate_user_agent()
    data = requests.get(school_urls, headers={"User-Agent": agent})
    if data.status_code == 200:
        html_content = data.text
        soup = BeautifulSoup(html_content, "html.parser")
        table_data = []
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                row_data = [col.get_text(strip=True) for col in columns]
                table_data.append(row_data)
    df = pd.DataFrame(table_data, columns=columns)
    df.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
    df.dropna(how='all', inplace=True)
    df.to_csv("../data/school_info.csv")
        # with open('output.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup.prettify()))

def scrape_coaches(school_url):
    agent = generate_user_agent()
    data = requests.get(school_url, headers={"User-Agent": agent})
    if data.status_code == 200:
        html_content = data.text
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"id": "akron"})
        rows = table.find("tbody").find_all("tr")
        coaches_data = []
        for row in rows:
            cols = row.find_all("td")
            coach_name = cols[0].get_text()
            from_year = cols[1].get_text()
            to_year = cols[2].get_text()
            total_years = cols[3].get_text()
            coaches_data.append((coach_name, from_year, to_year, total_years))
    print(coaches_data)


if __name__ == "__main__":
    #school_list = scrape_schools("https://www.sports-reference.com/cfb/schools/")
    scrape_school_info("https://www.sports-reference.com/cfb/schools/akron/")
    #scrape_coaches("https://www.sports-reference.com/cfb/schools/air-force/coaches.html")
