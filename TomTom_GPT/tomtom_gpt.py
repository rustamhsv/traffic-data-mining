import pandas as pd 
import json
import scipy.io

df = pd.read_csv('gpt_data.csv')


# filter poi coordinates inside polygon
lat_filter = (df['lat'] < 47.4814930) & (df['lat'] > 47.4614077)
long_filter = (df['lon'] < 19.0553055) & (df['lon'] > 19.0231104)
df = df.loc[lat_filter & long_filter]

df.to_csv('out.csv', index=False)

weekly_data_pois = []
for poi in df['popular_times']:
	poi = poi.replace("'", '"')
	poi_json = json.loads(poi)
	weekly_data = []
	for day in range(5):
		daily_data = poi_json[day]['data']
		weekly_data += daily_data
	weekly_data_pois.append(weekly_data)

# print(weekly_data_pois)
print(weekly_data_pois)
print(type(weekly_data_pois[0][0]))

scipy.io.savemat('pois_weekly.mat', mdict={'pois_weekly':weekly_data_pois})


# a = list(df['popular_times'])[0]
# a = a.replace("'", '"')
# # print(a)
# a_js = json.loads(a)
# x = a_js
# print(x)


# Process TomTom data
df = pd.read_excel('tomtom_data.xlsx', skiprows=54)

df.to_csv('tomtom_out.csv', index=False)
df.columns = df.iloc[0]
df = df[1:]

travel_time_col = 'Average Travel Time [hh:mm:ss]'
half = len(df[travel_time_col])//2

tomtom_weekly = list(df[travel_time_col])[:half]
# print(tomtom_weekly)

# convert datetime strings to seconds
seconds_list = []
for time in tomtom_weekly:
	seconds_sum = sum(secs * int(t) for secs, t in zip([3600, 60, 1], time.split(':')))
	seconds_list.append(seconds_sum)

# print(len(tomtom_weekly))
scipy.io.savemat('tomtom_weekly.mat', mdict={'tomtom_weekly':seconds_list})


corr_result = '1,1,1,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,1,0,1,0,1,0,1,-0.9'
corr_result = corr_result.split(',')
# print(corr_result)
# print(len(corr_result))

df = pd.read_csv('out.csv')
df['corr_value'] = corr_result[:-1]
df.to_csv('corr_result_pois.csv', index=False)