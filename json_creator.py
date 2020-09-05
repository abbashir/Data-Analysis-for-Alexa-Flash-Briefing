import json
import sql_queries as s
import datetime
import random
import string


# # ----- Random number generator --------
def generate_random(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


current_time = str(datetime.datetime.now())
data = {}


# data['Yesterday_Summary'] = {
#     "uid": generate_random(8, "1234ABCD"),
#     "updateDate": current_time,
#     "titleText": "Yesterday Sales Summary",
#     "mainText": "Welcome to Transcom Limited. Our, last day target was : " + s.YesterdayTarget +
#                 " Taka" +
#                 " and total sales was : " + s.YSales + " Taka" +
#                 " Overall sales achievements are : " + s.Achievement + "%" +
#                 " End of the day sales will be " + s.trend + ' Taka',
#     "redirectionUrl": ""
# }

# # ---- Doctor call status ----------
# def d_call_status(ld_call, avg_call):
#     if (ld_call >= avg_call):
#         status = 'It is ' + str(round(ld_call / avg_call, 2)) + ' times higher than average call.'
#     else:
#         status = 'But, it is less than average call.'
#     return status


# data['DoctorCall'] = {
#     "uid": generate_random(8, "1234ABCD"),
#     "updateDate": current_time,
#     "titleText": "Yesterday Doctor Count",
#     "mainText": "This months total : " + str(s.thismonth_d_count) + " doctors are visited " +
#                 " Where last day visited doctors are : " + str(s.lastday_d_count) +
#                 " " + str(d_call_status(s.lastday_d_count, s.averaged_call)) + " ",
#     "redirectionUrl": ""
# }


# print(list(data.values()))

def chemist_status(percentage):
    if percentage >= 10:
        status = "  which was covered " + str(percentage) + " percent of total chemist."
    else:
        status = " which was covered only " + str(percentage) + " percent of our total chemist. " \
                                                               "Please take necessary steps to make it higher."
        return status


data['ChemistCoverage'] = {
    "uid": generate_random(8, "1234ABCD"),
    "updateDate": current_time,
    "titleText": "Chemist Status",
    "mainText": "We have total " + str(s.total_chemist) + " active chemist " +
                " Where last day our sales force visited " + str(s.covered_chemist) + " chemist" +
                str(chemist_status(s.chemist_cov_per))
    ,
    "redirectionUrl": ""
}
with open("data.json", "w") as f:
    json.dump(list(data.values()), f)
    print('JSON Data created.')
