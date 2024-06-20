from bs4 import BeautifulSoup
import random
import requests


def scrape(url):
    user_agents_list = [
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    ]
    data = requests.get(url, headers={"User-Agent": random.choice(user_agents_list)})
    # //*[@id="coaches"]
    #
    #
    if data.status_code == 200:
        html_content = data.text
        # table = soup.find('table', {'id': 'coaches'})
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"id": "coaches"})
        # div_elements = soup.find_all(
        #     "div", class_="table_container-is_setup"
        # )
        rows = table.find("tbody").find_all("tr")

        # Initialize a list to hold the extracted data
        coaches_data = []

        # Loop through the rows and extract the desired data
        for row in rows:
            # Extract the columns for each row
            cols = row.find_all("td")
            coach_name = cols[0].get_text()
            from_year = cols[1].get_text()
            to_year = cols[2].get_text()
            total_years = cols[3].get_text()

            # Append the data to the list
            coaches_data.append((coach_name, from_year, to_year, total_years))
    print(coaches_data)


scrape("https://www.sports-reference.com/cfb/schools/air-force/coaches.html")
