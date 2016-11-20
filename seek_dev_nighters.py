import requests
from datetime import datetime
from pytz import timezone,UTC

DEVMAN_API_URL = "http://devman.org/api/challenges/solution_attempts/"


def load_attempts(api_url=DEVMAN_API_URL):
    page_number = 1
    number_of_pages = 1
    while page_number <= number_of_pages:
        json_page = requests.get(api_url, params={'page': page_number}).json()
        number_of_pages = int(json_page['number_of_pages'])
        for record in json_page['records']:
            if record['timestamp']:
                yield record
        page_number += 1


def get_midnighters(load_attemps_info):
    midnighters = set()
    for load_attempt in load_attemps_info:
        if load_attempt["timestamp"] is None:
            continue
        timestamp = float(load_attempt["timestamp"])
        attempt_time = datetime.fromtimestamp(timestamp, tz=timezone(load_attempt["timezone"]))
        if 0 <= attempt_time.hour < 6:
            midnighters.add(load_attempt["username"])
    return midnighters


def print_midnighters(midnighters):
    print("Oh, damn! There are {} midnighters on Devman:".format(len(midnighters)))
    for number, midnighter in enumerate(midnighters, 1):
        print("{}) {}".format(number, midnighter))


if __name__ == '__main__':
    midnighters = get_midnighters(load_attempts())
    print_midnighters(midnighters)
