import requests, pandas, sys
from datetime import datetime

url = "https://meowfacts.herokuapp.com/"


def get_facts(amount: int):
    facts = []
    timestamps = []
    for num in range(0, amount):
        response = requests.get(url)
        if response.status_code != 200:
            sys.exit(
                "problem with getting page. status code: " + str(response.status_code)
            )
        try:
            for value in response.json().values():
                facts.append(*value)
                timestamps.append(datetime.now().isoformat())
        except (requests.exceptions.JSONDecodeError, AttributeError):
            sys.exit(
                'payload not shaped as expected. needs to be either in json format or the json object needs to be equivalent to a python "dict" object.'
            )
    return pandas.DataFrame(
        {"facts": [*facts], "fetched_at": timestamps},
        index=[index for index in range(1, amount + 1)],
    )


def write_raw_data(dataframe: pandas.DataFrame, filename="facts"):
    filename = "data/raw/" + filename + str(datetime.now().isoformat()) + ".csv"
    csv = open(filename, "x")
    csv.write(str(dataframe))


def analyze_raw_data(dataframe: pandas.DataFrame):
    num_items = len(dataframe.values)
    sum_items = 0
    fact_with_longest_length = ""
    for value in dataframe["facts"]:
        sum_items += len(value)
        if len(value) > len(fact_with_longest_length):
            fact_with_longest_length = value

    print("\naverage fact character length: " + str(int(sum_items / num_items)))
    print("\nlongest fact: " + fact_with_longest_length[:120] + "...")


if __name__ == "__main__":
    amount = int(input("enter the number of facts you want to retrieve: "))
    dataframe = get_facts(amount)
    write_raw_data(dataframe)
    analyze_raw_data(dataframe)
