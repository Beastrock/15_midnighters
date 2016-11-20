import requests
from datetime import datetime
import pytz


def load_attempts():
    load_attempts_info = []
    api_url = "http://devman.org/api/challenges/solution_attempts/?page = 1"
    last_page_number = requests.get(api_url).json()["number_of_pages"] + 1
    for page in range(1, last_page_number):
        one_page_json = requests.get(api_url, params={"page": page}).json()
        load_attempts_info.extend(one_page_json["records"])
    return (load_attempts_info)


def get_midnighters(load_attemps_info):
    midnighters = set()
    for load_attempt in load_attemps_info:
        if not load_attempt["timestamp"] is None:
            utc_now = datetime.fromtimestamp(int(load_attempt["timestamp"])).replace(tzinfo=pytz.UTC)
            time_for = utc_now.astimezone(pytz.timezone(load_attempt["timezone"]))
            if 0 <= time_for.hour < 6:
                midnighters.add(load_attempt["username"])
    return midnighters


def print_midnighters(midnighters):
    print("Oh, damn! There are {} midnighters on Devman:".format(len(midnighters)))
    for number,midnighter in enumerate(midnighters,1):
        print("{}) {}".format(number, midnighter))


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    print_midnighters(midnighters)
