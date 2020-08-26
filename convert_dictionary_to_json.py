import json
import sql_queries as b

# Create Dictionary for business
business = {
    "id": "04",
    "target": b.YesterdayTarget,
    'Sales': b.YSales,
    'Achievements': b.Achievement
}

# Convert Dictionary to json data
business_json_data = '['+ str(json.dumps(business, indent=5)) +']'
print(business_json_data)