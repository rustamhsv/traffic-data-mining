import matplotlib.pyplot as plt

loop_detector = [35.6666666666666, 24.0, 25.0, 40.6666666666667, 60.0, 186.00000000000028, 1040.333333333333, 1440.0,
                 1242.666666666666, 1208.0, 993.666666666667, 935.0, 872.333333333333, 897.3333333333339,
                 889.6666666666661, 1066.333333333334, 1165.666666666666, 1123.333333333333, 919.6666666666661,
                 653.666666666667, 457.0, 259.66666666666697, 141.33333333333331, 76.0]

tomtom = [6.0, 3.0, 4.0, 7.0, 9.0, 16.0, 74.0, 151.0, 127.0, 137.0, 130.0, 94.0, 75.0, 118.0, 91.0, 103.0,
          130.0, 144.0, 134.0, 68.0, 52.0, 19.0, 16.0, 13.0]

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


