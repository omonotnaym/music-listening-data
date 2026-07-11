import requests, pandas, random, sys
from datetime import datetime

url = "https://meowfacts.herokuapp.com/"
facts = []
timestamps = []


def get_facts(amount):
    for iteration in range(0, amount):
        response = requests.get(url)
        timestamps.append(datetime.now().isoformat())
        if response.status_code != 200:
            sys.exit(
                "problem with getting page. status code: " + str(response.status_code)
            )
        try:
            facts.append(list(*response.json().values())[0])
        except (requests.exceptions.JSONDecodeError, AttributeError):
            sys.exit(
                "payload not shaped as expected (either not in json format or not a dict)"
            )
    return pandas.DataFrame(facts)


get_facts(random.randint(2, 10))

series_of_cat_facts = pandas.Series(
    facts, index=["fact " + str(index) + ":" for index in range(0, len(facts))]
)
series_of_timestamps = pandas.Series(timestamps, name="fetched_at")

print("all cat facts obtained:\n")
print(series_of_cat_facts)

print("\naccessing one random element:\n")
print(series_of_cat_facts.iloc[random.randint(0, len(series_of_cat_facts.index) - 1)])

print("\nslicing cat facts randomly:\n")
start = random.randint(0, len(series_of_cat_facts.index) - 2)
print(
    series_of_cat_facts.iloc[
        start : random.randint(start + 1, len(series_of_cat_facts.index) - 1)
    ]
)

print("\nadding a new fact\n")
# new_fact = {'fact ' + str(len(series_of_cat_facts.index)) + ':' : list(*requests.get(url).json().values())[0]}
# for key in new_fact.keys():
#     print('new fact to be added: ' + new_fact[key])
# series_of_cat_facts = pandas.concat([series_of_cat_facts, pandas.Series(new_fact)])
series_of_cat_facts["fact " + str(len(series_of_cat_facts.index)) + ":"] = list(
    *requests.get(url).json().values()
)[0]
series_of_timestamps[len(series_of_timestamps.index)] = datetime.now().isoformat()
print("updated series:\n" + str(series_of_cat_facts) + "\n")

print("conversion to data frame:")
series_of_cat_facts.index = [
    index for index in range(1, len(series_of_cat_facts.values) + 1)
]
series_of_timestamps.index = [
    index for index in range(1, len(series_of_timestamps.values) + 1)
]
frame_of_cat_facts = series_of_cat_facts.to_frame(name="facts")
frame_of_cat_facts[series_of_timestamps.name] = series_of_timestamps.values
print(frame_of_cat_facts)

facts = []
try:
    cap = int(input("\nenter an integer: "))
    get_facts(cap)
except ValueError:
    print("did not enter an integer. getting 10 cat facts instead.")
    get_facts(10)

print(facts)

filename = "data/raw/cat_facts_" + str(datetime.now().isoformat()) + ".csv"
csv = open(filename, "x")
csv.write(str(frame_of_cat_facts) + "\n")

print("\nreading from the file that was created and written to: ")
csv = open(filename, "r")
print(csv.read())

print("total facts: " + str(len(frame_of_cat_facts["facts"] + "\n")))

total = 0
longest_fact = ""
for fact in frame_of_cat_facts["facts"]:
    total += len(fact)
    if len(fact) > len(longest_fact):
        longest_fact = fact

average_length = int(total / len(frame_of_cat_facts))
print("average fact length: ")
print(str(average_length) + " characters")

longest_fact = longest_fact[:120] + "..."
print(longest_fact)
