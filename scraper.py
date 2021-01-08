from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import serialization
import time

class Scraper:
    def __init__(self):
        self.url = "https://atcoder.jp/ranking/all"
        self.parser = "lxml"

    def get_page_num(self):
        page_list_label = "ul"
        page_list_class_name = "pagination pagination-sm mt-0 mb-1"

        with request.urlopen(self.url) as response:
            soup = BeautifulSoup(response, features = self.parser)

        page_list = soup.find(page_list_label, {"class": page_list_class_name})
        page_num = int(page_list.find_all("a")[-1].text)

        return page_num

    def get_user_list(self):
        page_query_suffix = "?page="
        user_table_label = "table"
        user_table_class_name = "table table-bordered table-striped th-center"
        user_country_index = 1
        user_birthyear_index = 2
        user_rating_index = 3
        user_participation_index = 5
        user_country_name_offset = 23
        df_header = ["Country", "Birthyear", "Participation", "Rating"]
        result = []

        for i in range(1, self.get_page_num() + 1):
            with request.urlopen(self.url + page_query_suffix + str(i)) as response:
                soup = BeautifulSoup(response, features = self.parser)
            user_table = soup.find(user_table_label, {"class": user_table_class_name})
            for row in user_table.find("tbody").find_all("tr"):
                columns = row.find_all("td")
                country = columns[user_country_index].contents[0].attrs["href"][user_country_name_offset:]
                birthyear = columns[user_birthyear_index].text if columns[user_birthyear_index].text else None
                participation = int(columns[user_participation_index].text)
                rating = int(columns[user_rating_index].text)
                user = [country, birthyear, participation, rating]
                result.append(user)
            print(i)
        
        df = pd.DataFrame(result, columns = df_header)
        return df

def main():
    start = time.time()
    scraper = Scraper()
    user_list = scraper.get_user_list()
    serialization.save_data(user_list)
    print(serialization.load_data())
    print(time.time() - start)

if __name__ == "__main__":
    main()