import pandas as pd 
import json
import scipy.io
from collections import defaultdict
from os import listdir
# from scipy.stats.stats import pearsonr   
from scipy import stats
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import math
import random



def get_hour_from_interval(hour):
	end_idx = hour.find(':')
	hour = hour[:end_idx]
	return hour


def convert_time_to_sec(time):
	seconds_sum = sum(secs * int(t) for secs, t in zip([3600, 60, 1], time.split(':')))
	return seconds_sum


# place_id = 'ChIJhyxyHLXdQUcR6X3xu4va9kQ'

df = pd.read_csv('corr_result_pois.csv')
place_ids = df['place_id']


for place_id, node_type in zip(place_ids, df['node_type']):
	if node_type != 'bar':
		continue

	""" GET TomTom data for every hour - for every hour 20 data points (4 weeks) """
	df_tomtom = pd.read_excel('Moricz-Kelenfold_4_weeks.xlsx', skiprows=114)
	df_tomtom.columns = df_tomtom.iloc[0]
	df_tomtom = df_tomtom[1:]

	hours = list(df_tomtom['Time Set'])
	# travel_times = list(df_tomtom['Average Travel Time [hh:mm:ss]'])
	travel_times = list(df_tomtom['Average Travel Time ratios'])

	hours_dict_tomtom = defaultdict(list)
	for hour, travel_time in zip(hours, travel_times):
		# seconds_sum = convert_time_to_sec(travel_time)
		hour = get_hour_from_interval(hour)
		# hours_dict_tomtom[int(hour)].append(seconds_sum)
		hours_dict_tomtom[int(hour)].append(travel_time)



	""" GET TomTom data for every hour - for every hour 20 data points (4 weeks) """
	hours_dict_poi = defaultdict(list)

	for file in listdir():
		if 'Onlive' not in file:
			continue

		df_poi = pd.read_csv(file)
		poi_filter = df_poi['place_id'] == place_id
		df_poi = df_poi.loc[poi_filter]

		for poi in df_poi['popular_times']:
			poi = poi.replace("'", '"')
			poi_json = json.loads(poi)
			# print(poi_json)
			for day in range(5):
				daily_data = poi_json[day]['data']
				for hour, data in enumerate(daily_data):
					hours_dict_poi[hour].append(data)

	# hours_dict_tomtom[9] = [x for x in range(10, 1000, 100)][:20]
	# print(len(hours_dict_tomtom[0]), len(hours_dict_poi[0]))


	# print('TOMTOM:', len(hours_dict_tomtom[9]))
	# print('POI:', len(hours_dict_poi[9]))

	corr_matrix = []
	for hour in range(0, 24):
		try:
			corr_result = stats.pearsonr(hours_dict_tomtom[hour], hours_dict_poi[hour])
			corr_matrix.append(corr_result[0])
		except ValueError:
			continue
	corr_matrix = [0 if math.isnan(coef) else coef for coef in corr_matrix]
	sum_of_coefs = sum(map(abs, corr_matrix))
	print(place_id, sum_of_coefs)
	# print(len(hours_dict_poi.keys()), len(corr_matrix))

	if sum_of_coefs > 5 and len(corr_matrix)==24:
		plt.scatter(hours_dict_poi.keys(), corr_matrix)
		plt.axis([0, 25, -1, 1])
		plt.xlabel("HOURS")
		plt.ylabel(f"CORR VALUE {node_type}")
		plt.grid()
		plt.show()




# print(len(corr_matrix))
# plt.scatter(hours_dict_tomtom.keys(), corr_matrix)
# plt.axis([0, 25, -1, 1])
# plt.xlabel("HOURS")
# plt.ylabel("CORR VALUE")
# plt.grid()
# plt.show()

# df = pd.DataFrame(corr_matrix)
# print(df)
# corr = df.corr()
# print(corr)
# data = np.random.rand(24,2)
# df = pd.DataFrame(data) # Your data 
# print(df)
# corr = df.corr() # Calculates correlation matrix
# sb.heatmap(corr, cmap="Blues", annot=True)


# corr.style.background_gradient(cmap='coolwarm')


# a = stats.spearmanr(hours_dict_tomtom[10], hours_dict_poi[10])
# print(a)
		# 	print(daily_data)
		# 	weekly_data += daily_data
		# weekly_data_pois.append(weekly_data)

# for h in hours_dict_poi.values():
# 	print(len(h))

# hours_dict = {}
# for hour in hours:
# 	end_idx = hour.find(':')
# 	hour = hour[:end_idx]
# 	hours_dict[hour] = ''

# print(hours_dict)


# # filter poi coordinates inside polygon
# lat_filter = (df['lat'] < 47.4814930) & (df['lat'] > 47.4614077)
# long_filter = (df['lon'] < 19.0553055) & (df['lon'] > 19.0231104)
# df = df.loc[lat_filter & long_filter]

# df.to_csv('out.csv', index=False)

# weekly_data_pois = []
# for poi in df['popular_times']:
# 	poi = poi.replace("'", '"')
# 	poi_json = json.loads(poi)
# 	weekly_data = []
# 	for day in range(5):
# 		daily_data = poi_json[day]['data']
# 		weekly_data += daily_data
# 	weekly_data_pois.append(weekly_data)

# # print(weekly_data_pois)
# print(weekly_data_pois)
# print(type(weekly_data_pois[0][0]))

# scipy.io.savemat('pois_weekly.mat', mdict={'pois_weekly':weekly_data_pois})


# # a = list(df['popular_times'])[0]
# # a = a.replace("'", '"')
# # # print(a)
# # a_js = json.loads(a)
# # x = a_js
# # print(x)


# # Process TomTom data
# df = pd.read_excel('tomtom_data.xlsx', skiprows=54)

# df.to_csv('tomtom_out.csv', index=False)
# df.columns = df.iloc[0]
# df = df[1:]

# travel_time_col = 'Average Travel Time [hh:mm:ss]'
# half = len(df[travel_time_col])//2

# tomtom_weekly = list(df[travel_time_col])[:half]
# # print(tomtom_weekly)

# # convert datetime strings to seconds
# seconds_list = []
# for time in tomtom_weekly:
# 	seconds_sum = sum(secs * int(t) for secs, t in zip([3600, 60, 1], time.split(':')))
# 	seconds_list.append(seconds_sum)


# # print(len(tomtom_weekly))
# scipy.io.savemat('tomtom_weekly.mat', mdict={'tomtom_weekly':seconds_list})


# corr_result = '1,1,1,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,1,0,1,0,1,0,1,-0.9'
# corr_result = corr_result.split(',')
# # print(corr_result)
# # print(len(corr_result))

# df = pd.read_csv('out.csv')
# df['corr_value'] = corr_result[:-1]
# df.to_csv('corr_result_pois.csv', index=False)