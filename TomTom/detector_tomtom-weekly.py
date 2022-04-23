import collections

import matplotlib.pyplot as plt
import pandas as pd

url = '/home/rustam/Desktop/University/Master-Thesis/Loop-Detector/FULL.xlsx'
df = pd.read_excel(url, sheet_name='full')

# calculate hourly occupancy
detector_data = collections.defaultdict(dict)  # store df in dict
for idx in range(len(df.index)):

    # get name of detector
    name = df.iloc[idx, 0]
    if name not in detector_data:
        detector_data[name] = collections.defaultdict(dict)

    # get hour and volume parameters from excel
    time = str(df.iloc[idx, 3])
    hour = time[:2]
    volume = float(df.iloc[idx, 7]) / 12
    hour = str(df.iloc[idx, 1])[:5] + hour

    # store volume for every hour for every detector
    if hour not in detector_data[name]:
        detector_data[name][hour] = volume
    else:
        detector_data[name][hour] += volume

# create dataframe from dict
df = pd.DataFrame(detector_data)

loop_detector = []
for idx in range(len(df)):
    sum_detectors = float(df.iloc[idx, 0]) + float(df.iloc[idx, 0])
    loop_detector.append(sum_detectors)

# # write to csv output
# df.to_csv('hourly-occupancy-output.csv', index=True)
#
#
# loop_detector = [35.6666666666666, 24.0, 25.0, 40.6666666666667, 60.0, 186.00000000000028, 1040.333333333333, 1440.0,
#                  1242.666666666666, 1208.0, 993.666666666667, 935.0, 872.333333333333, 897.3333333333339,
#                  889.6666666666661, 1066.333333333334, 1165.666666666666, 1123.333333333333, 919.6666666666661,
#                  653.666666666667, 457.0, 259.66666666666697, 141.33333333333331, 76.0]

# a = '105.55	4	8	2	7	5	20	85	157	165	113	96	94	81	94	81	84	123	119	73	73	40	20	12	16	6	3	4	7	9	16	74	151	127	137	130	94	75	118	91	103	130	144	134	68	52	19	16	13	9	4	3	4	5	16	74	187	151	141	134	116	112	128	99	125	110	164	169	108	66	24	26	19	12	4	1	4	7	14	88	179	148	148	113	111	132	120	116	140	137	153	165	139	59	36	35	10	5	3	5	10	9	13	87	174	128	119	113	133	103	121	115	134	101	128	119	95	51	38	20	24	18	10	5	11	7	3	10	55	83	127	107	120	99	99	114	104	89	125	105	85	65	45	30	29	12	16	4	8	5	9	3	24	46	78	88	80	82	84	109	153	176	197	169	124	69	48	21	12'
# tomtom = a.split('	')
# tomtom = [float(a) for a in tomtom]
# print(tomtom)
tomtom = [105.55, 4.0, 8.0, 2.0, 7.0, 5.0, 20.0, 85.0, 157.0, 165.0, 113.0, 96.0, 94.0, 81.0, 94.0, 81.0, 84.0, 123.0, 119.0, 73.0, 73.0, 40.0, 20.0, 12.0, 16.0, 6.0, 3.0, 4.0, 7.0, 9.0, 16.0, 74.0, 151.0, 127.0, 137.0, 130.0, 94.0, 75.0, 118.0, 91.0, 103.0, 130.0, 144.0, 134.0, 68.0, 52.0, 19.0, 16.0, 13.0, 9.0, 4.0, 3.0, 4.0, 5.0, 16.0, 74.0, 187.0, 151.0, 141.0, 134.0, 116.0, 112.0, 128.0, 99.0, 125.0, 110.0, 164.0, 169.0, 108.0, 66.0, 24.0, 26.0, 19.0, 12.0, 4.0, 1.0, 4.0, 7.0, 14.0, 88.0, 179.0, 148.0, 148.0, 113.0, 111.0, 132.0, 120.0, 116.0, 140.0, 137.0, 153.0, 165.0, 139.0, 59.0, 36.0, 35.0, 10.0, 5.0, 3.0, 5.0, 10.0, 9.0, 13.0, 87.0, 174.0, 128.0, 119.0, 113.0, 133.0, 103.0, 121.0, 115.0, 134.0, 101.0, 128.0, 119.0, 95.0, 51.0, 38.0, 20.0, 24.0, 18.0, 10.0, 5.0, 11.0, 7.0, 3.0, 10.0, 55.0, 83.0, 127.0, 107.0, 120.0, 99.0, 99.0, 114.0, 104.0, 89.0, 125.0, 105.0, 85.0, 65.0, 45.0, 30.0, 29.0, 12.0, 16.0, 4.0, 8.0, 5.0, 9.0, 3.0, 24.0, 46.0, 78.0, 88.0, 80.0, 82.0, 84.0, 109.0, 153.0, 176.0, 197.0, 169.0, 124.0, 69.0, 48.0, 21.0, 12.0]

# plt.plot(loop_detector, 'g', tomtom, 'r')

plt.plot(loop_detector, "g", label="Loop Detector [flow]")
plt.plot(tomtom, "r", label="TomTom [probe size]")
plt.legend(loc="upper right")
plt.xlabel("hour")
plt.show()


# for a, b in zip(aa.splitlines(), bb.splitlines()):
#     flow = float(a) + float(b)
#     loop_detector.append(flow)
#
# print(loop_detector)

# tt = '105.55	6	3	4	7	9	16	74	151	127	137	130	94	75	118	91	103	130	144	134	68	52	19	16	13	50'
# tt = tt.split('	')
# tt = [float(t) for t in tt]
# print(tt)


