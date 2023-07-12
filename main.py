import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, InvalidSchema, ConnectionError
import json
import sys

url = "https://www.empireonline.com/tv/features/best-tv-shows-ever-2/"

try:
    response = requests.get(url=url)
    response.raise_for_status()
except (HTTPError, InvalidSchema, ConnectionError) as e:
    print(f"Invalid request: {e.args}")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

try:
    data = soup.select_one(selector="#__NEXT_DATA__").text
except AttributeError as e:
    print(f"No element found")

data_json = json.loads(data)

try:
    json_data_path = data_json["props"]["pageProps"]["data"]["getArticleByFurl"][
        "_layout"
    ][2]["content"]["images"]
except KeyError as e:
    print(f"No key found: {e.args}")
    sys.exit(1)


data_list = []

try:
    for x in range(0, len(json_data_path)):
        if not str(json_data_path[x]["titleText"])[0].isdigit():
            json_data_path[x][
                "titleText"
            ] = f"{100 -x}) {json_data_path[x]['titleText']}"
            data_list.append(json_data_path[x]["titleText"])
        else:
            data_list.append(json_data_path[x]["titleText"])
except KeyError as e:
    print(f"No key found: {e.args}")
except IndexError as e:
    print(f"Index out of range: {e.args}")


try:
    with open("file.txt", "w+") as f:
        f.write("\n".join(data_list[::-1]))
except (FileExistsError, FileNotFoundError) as e:
    print(f"File not found: {e.args}")
