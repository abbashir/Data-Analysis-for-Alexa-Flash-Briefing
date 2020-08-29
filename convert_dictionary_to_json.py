import json
import sql_queries as b

# Create Dictionary for business
business = {
    "id": "04",
    "target": b.YesterdayTarget,
    'Sales': b.YSales,
    'Achievements': b.Achievement
}
business1 = {
    "id": "05",
    "target": b.YesterdayTarget,
    'Sales': b.YSales,
    'Achievements': b.Achievement
}

# Convert Dictionary to json data
business_json_data = str(json.dumps(business, indent=5))
business_json_data1 = str(json.dumps(business1, indent=5))

all = '[' + business_json_data + ',\n' + business_json_data1 + ']'
print(all)