import requests
import datetime
import pytz


def load_attempts():
    all_page_list = []
    url = "http://devman.org/api/challenges/solution_attempts/?page = 1"
    last_page = requests.get(url).json()["number_of_pages"] + 1
    for page in range(1, last_page):
        params = {"page": page}
        one_page_json = requests.get("http://devman.org/api/challenges/solution_attempts/", params=params)
        print("loading page number {}".format(one_page_json.json()["page"]))
        all_page_list.extend(one_page_json.json()["records"])
        print(all_page_list)
    print(all_page_list)
    return (all_page_list)



def get_midnighters(all_page_list):
    midnighters = []
    for all_page in all_page_list:
        if all_page["timestamp"]:
            time = datetime.datetime.fromtimestamp(float(all_page["timestamp"]),tz=pytz.UTC)
            print(time.time())
            time_for = time.astimezone(pytz.timezone(all_page["timezone"]))
            print(time_for.time())
            if (0 <= time_for.hour < 6) and (not all_page["username"] in midnighters):
                midnighters.append(all_page["username"])
                print("этот хуев программист {} решал задачу в {}".
                      format(all_page["username"], datetime.datetime.fromtimestamp(int(all_page["timestamp"])).time()))
    return midnighters

def print_midnighters(midnighters):
    print("Oh, damn! There are {} midnighters on devman! Let us output them:".format(len(midnighters)))
    for midnighter in midnighters:
        print("{:^30s}".format(midnighter))


if __name__ == '__main__':
    print_midnighters(get_midnighters(load_attempts()))
