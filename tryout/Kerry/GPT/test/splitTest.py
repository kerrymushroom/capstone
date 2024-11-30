import re

data = {
    "196": {
        "vis_query": {
            "vis_part": "Visualize BAR",
            "data_part": {
                "sql_part": "SELECT date_address_from , COUNT(date_address_from) FROM Student_Addresses GROUP BY other_details",
                "binning": "BIN date_address_from BY YEAR"
            },
            "VQL": "Visualize BAR SELECT date_address_from , COUNT(date_address_from) FROM Student_Addresses GROUP BY other_details BIN date_address_from BY YEAR"
        }
    }
}


table_name = ''
for key, value in data.items():
    sql = value['vis_query']['data_part']['sql_part']
    table_name = re.search(r' from\s+(\w+)', sql, re.IGNORECASE).group(1)
print(table_name)
