import collections
import pandas as pd


def read_from_original_file(file):
    """ for reading from original excel file """
    # sheet to read
    sheet = 'filtered'

    # read loop detector excel file
    data = pd.read_excel(file, sheet_name=sheet)

    data['Time'] = pd.to_datetime(data['Time'], errors='coerce').dt.strftime('%Y-%m-%d')

    # filter dates - keep only 1 day
    one_day_data = data['Time'] == '2019-02-04'
    data = data.loc[one_day_data]

    # keep only required cols
    cols_to_keep = ['Name', 'Time.1', 'processed_all_vol']
    data = data[cols_to_keep]

    return data


if __name__ == '__main__':
    excel_file = 'FULL_Detector-Measurement Point-Traffic Data - Processed-190401_190407.xlsx'

    # filter sheet
    filter_sheet = 'detectors'
    df_filter = pd.read_excel(excel_file, sheet_name=filter_sheet)

    # get working loop detectors
    loop_detectors = []
    for idx in range(len(df_filter.index)):
        status_col = str(df_filter.iloc[idx, -2])  # get status of the detector
        if status_col == 'OK' or status_col == 'OK*':
            detector_name = df_filter.iloc[idx, 0]  # store detector name
            loop_detectors.append(detector_name)

    """ hard-coded version of loop detectors """
    # loop_detectors = ['es31FD0_D1123_MD4', 'es31FD0_D1133_MD14', 'es31FD0_D1134_MD15', 'es31FD770_D3_D770.3', 'es31FD770_D4_D770.4', 'es31FD909_D1_D909.1', 'es31FD909_D2_D909.2', 'es31FD909_D3_D909.3', 'es31FD909_D4_D909.4', 'es31FD909_D5_D909.5', 'es31FD909_D6_D909.6', 'es31FD909_D7_D909.7', 'es31FD910_D1_D910.1', 'es31FD910_D2_D910.2', 'es31FD916_D3_D916.3', 'es31FD918_D10_Det 10', 'es31FD918_D6_Det 6', 'es31FD918_D7_Det 7', 'es31FD918_D8_Det 8', 'es31FD918_D9_Det 9', 'ig13FD776_D1_Det 1', 'ig13FD776_D2_Det 2', 'ig13FD926_D1_D926.1', 'ig13FD926_D2_D926.2', 'ig13FD926_D7_D926.7', 'ig13FD926_D8_D926.8']

    """ for reading from original excel file """
    # df = read_from_original_file(excel_file)
    # df.to_csv('cache-output.csv', index=False)

    """ for faster reading """
    csv_file = 'cache-output.csv'
    df = pd.read_csv(csv_file)

    # keep only working loop detectors
    status_OK_detectors = df.iloc[:, 0].isin(loop_detectors)
    df = df.loc[status_OK_detectors]

    # replace noise values with moving average
    last_value = 0
    for idx in range(len(df.index)):
        if ',' in str(df.iloc[idx, 2]):  # noise in date format
            for i in range(idx + 1, idx + 5):
                try:
                    # get moving average - if failed go to next value
                    df.iloc[idx, 2] = (last_value + float(df.iloc[i, 2]))/2
                    break
                except (TypeError, ValueError):
                    continue
        else:
            last_value = float(df.iloc[idx, 2])  # store last normal value

    # calculate hourly occupancy
    detector_data = collections.defaultdict(dict)  # store df in dict
    for idx in range(len(df.index)):

        # get name of detector
        name = df.iloc[idx, 0]
        if name not in detector_data:
            detector_data[name] = collections.defaultdict(dict)

        # get hour and volume parameters from excel
        time = str(df.iloc[idx, 1])
        hour = time[:2]
        volume = float(df.iloc[idx, -1])/12

        # store volume for every hour for every detector
        if hour not in detector_data[name]:
            detector_data[name][hour] = volume
        else:
            detector_data[name][hour] += volume

    # create dataframe from dict
    df = pd.DataFrame(detector_data)

    # write to csv output
    df.to_csv('hourly-occupancy-output.csv', index=True)



