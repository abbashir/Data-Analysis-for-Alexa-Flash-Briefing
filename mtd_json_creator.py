import json
import datetime
import random
import string

import mtd_queries as d
current_time = str(datetime.datetime.now())
def generate_random(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def currency_converter(num):
    num_size = len(str(num))
    if num_size >= 8:
        number = str(round((num / 10000000), 2)) +' Crore'
    elif num_size >= 6:
        number = str(round(num / 100000, 2))+' million'
    elif num_size >= 4:
        number = str(round(num / 1000, 2)) +' Thousand'
    else:
        number = num
    return str(number)

data = {}

data['mtd_Summary'] = {
    "uid": generate_random(8, "1234ABCD"),
    "updateDate": current_time,
    "titleText": "Month to Date Sales Summary",
    "mainText": " Welcome to Transcom Limited. Our, month to date target is : " + str(currency_converter(d.mtd_target)) +
                ". Till now we have made sales near : " + str(currency_converter(d.mtd_sales)) +
                " which gives us an achievements of " + str(d.mtd_achiv) + " % ." +
                " By the way, this month our total target is " + str(currency_converter(d.todays_target)) +
                " and after analyzing sales behaviour at the end of the month our sales will be "
                + str(currency_converter(d.mtd_trend_val)),
    "redirectionUrl": ""
}

data['yesterday_Summary'] = {
    "uid": generate_random(8, "1234ABCD"),
    "updateDate": current_time,
    "titleText": "Yesterday Sales Summary",
    "mainText": " Yesterday the target amount was : " + str(currency_converter(d.yesterday_target)) +
                ". and we made sales of about : " + str(currency_converter(d.yesterday_sales)) +
                " Therefore our achievements was " + str(d.yesterday_achiv) + "% ." ,
    "redirectionUrl": ""
}

data['todays_Summary'] = {
    "uid": generate_random(8, "1234ABCD"),
    "updateDate": current_time,
    "titleText": "Todays Sales Summary",
    "mainText": " For today, our estimated target is : " + str(currency_converter(d.todays_target)) +
                ". Till now we have made sales of about : " + str(currency_converter(d.todays_sales)) +
                " which covers only " + str(d.todays_achiv) +
                "% of our target. If our sales goes like this, we may get an achievements of "+str(
        d.willbe_todays_achiv)+
    "% which indicates a sale value of " + str(currency_converter(d.todays_trend_val)),
    "redirectionUrl": ""
}

with open("summary_data.json", "w") as f:
    json.dump(list(data.values()), f)
    print('JSON Data created.')
