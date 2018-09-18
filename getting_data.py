import json
import psycopg2
import pandas as pd
env = json.load(open('env.json'))
conn = psycopg2.connect(
        host=env["host"],
        port=env["port"],
        user=env["user"],
        password=env["pass"],
        database=env["database"],
    )

example_query = """ SELECT campaign_id , user_id , type , device_type , country 
                  FROM analytics where  campaign_id in (1472,1473,1479,1482,1487,1515)"""

cursor = conn.cursor()
cursor.execute(example_query)
results = cursor.fetchall() 

campaign_id =[]
user_id =[]
campaing_type = []
device_type   =[]
country =[]
print "query finished"
for i in results:
	campaign_id.append(i[0])
	user_id.append(i[1])
	campaing_type.append(i[2])
	device_type.append(i[3])
	country.append(i[4])

dataframe = pd.DataFrame({"campaign_id":campaign_id,
	                       "user_id":user_id,
	                       "campaing_type":campaing_type,
	                        "device_type":device_type,
	                        "country":country})
print "dim",dataframe.shape
dataframe.to_csv('campaign_666.csv',index=False,header=True)
print "Done"






