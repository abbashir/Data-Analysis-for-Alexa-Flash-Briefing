import json
import sql_queries as b

business = {
    "id": "04",
    "target": b.YesterdayTarget,
    'Sales': b.YSales,
    'Achievements': b.Achievement
}

# Serializing json
business_json_data = json.dumps(business, indent=5)
print(business_json_data)