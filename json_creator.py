import json
import sql_queries as s
import datetime
import random
import string


# Random number generator
def generate_random(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


current_time = str(datetime.datetime.now())

data = {}

data['Yesterday_Summary'] = {
    "uid": generate_random(4, "122f"),
    "updateDate": current_time,
    "titleText": "Yesterday Sales Summary",
    "mainText": "Welcome to Transcom Limited. Our, last day target was : " + s.YesterdayTarget +
                " Taka" +
                " and total sales was : " + s.YSales + " Taka" +
                " Overall sales achievements are : " + s.Achievement + "%" +
                " Todays Sales Trends will be" +s.trend + 'Taka',
    "redirectionUrl": ""
}

# print(list(data.values()))
with open("data.json", "w") as f:
    json.dump(list(data.values()), f)
    print('JSON Data created.')
