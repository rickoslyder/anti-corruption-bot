import requests
import json, datetime
from bs4 import BeautifulSoup

date = datetime.datetime.now()
formatted_date = f"{date.day}-{date.month}-{date.year}"

# TheyWorkForYou's API has an endpoint called getMPs that returns a list of all active MPs
# however to get an API key, you need to pay a monthly fee based on usage
# The TWFY docs page allows you to get an up-to-date example response (rendered on page as HTML, although still json formatted)
# for now, we'll use BS4 and requests to extract & save the output in a JSON file, then convert this to a Python dictionary
list_of_mps_url = "https://www.theyworkforyou.com/api/docs/getMPs?party=&date=&search=&output=json#output"

list_r = requests.get(list_of_mps_url)
list_soup = BeautifulSoup(list_r.content, "html.parser")

mps_json = list_soup.find_all("pre")[1].string

with open(f"listOfMPs {formatted_date}.json", "w") as outfile:
    outfile.write(mps_json)

mp_list = json.loads(mps_json)

# the function below scrapes an MPs voting data by parsing through the policy groups & positions
# for each policy group, it will create a dict of all voting directions (for/against) & list out all policies that match that direction
# e.g. ["business"]["mostly voted against"]: ["corporation tax increase", "employer NI contributions"]


def scrape_mp_votes(personId):
    mp_url = f"https://www.theyworkforyou.com/mp/{personId}/votes"
    r = requests.get(mp_url)

    soup = BeautifulSoup(r.content, "html.parser")

    voting_positions = {}

    positions = soup.select("div.panel > ul.vote-descriptions > li")

    for i in positions:
        if i["data-policy-group"] not in voting_positions:
            voting_positions[i["data-policy-group"]] = {}
            voting_positions[i["data-policy-group"]][i["data-policy-direction"]] = [
                i["data-policy-desc"]
            ]

        elif i["data-policy-direction"] not in voting_positions[i["data-policy-group"]]:
            voting_positions[i["data-policy-group"]][i["data-policy-direction"]] = []
            voting_positions[i["data-policy-group"]][i["data-policy-direction"]].append(
                i["data-policy-desc"]
            )

        else:
            voting_positions[i["data-policy-group"]][i["data-policy-direction"]].append(
                i["data-policy-desc"]
            )

    return voting_positions


# this function save MP voting positions to a labelled & prettified JSON


def save_mp_scraped_votes(mp_name, personId, party=""):
    json_string = json.dumps(scrape_mp_votes(personId), ensure_ascii=False, indent=4)
    if json_string != "{}":
        with open(
            f"Voting Data by MP/MP Voting Positions - {mp_name}.json", "w"
        ) as outfile:
            outfile.write(json_string)
    else:
        print(f"No data found - please check if person ID for {mp_name} is correct")


# from here, we scrape the data of all MPs returned by the TheyWorkForYou API
# currently one-by-one, need to look into a more efficient way of scraping multiple MPs votes concurrently (multithreading?)


def scrape_all_mps(mp_list):
    print(f"Total MPs to be processed: {len(mp_list)}")
    for mp in mp_list:
        mp_name = mp["name"]
        person_id = mp["person_id"]
        party = mp["party"]
        print(f"Scraping data for: {mp_name} (ID: {person_id})")
        save_mp_scraped_votes(mp_name, person_id, party=party)
        print(f"Data saved!")
    print(f"All done!")


# and finally, the scraping begins ;)

# scrape_all_mps(mp_list[:10])
