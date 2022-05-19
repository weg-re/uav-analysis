import pandas as pd
import numpy as np


def read_imet_data(filename):
    records = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = lines[1:]
        n = len(lines)
        tail = n % 5
        if tail != 0:
            lines = lines[:-tail]

        n_samples = n // 5
        for i in range(n_samples):
            sample = lines[i * 5:(i + 1) * 5]
            # some stuff we dont need, and with some we need to remove the \n
            sample = [e.split(',') for e in sample]
            sample = np.array([s for e in sample for s in e])
            # according to manual "iMet-XQ UserGuide and Manual with Application Notes"
            # 'The iMet-XQ outputs data via the serial port once a second in the following format:
            # XQ, Pressure, Temperature, Humidity, Date, Time, Latitude x 1000000, Longitude x 1000000, Altitude x 1000,
            # Sat Count'
            # problem: in out date we have one entry more before the date....
            try:
                sample_dic = {
                    # 'xq': int(sample[0]),
                    'p': int(sample[1]),
                    't': int(sample[2]),
                    'h': int(sample[3]),
                    'UNKNOWN???': int(sample[4]),
                    # we combine date and time into one entry
                    'datetime': pd.to_datetime(sample[6] + '-' + sample[7]),
                    'lat': int(sample[8]) / 1000000,
                    'lon': int(sample[9]) / 1000000,
                    'alt': int(sample[10]) / 1000
                }
            except Exception as e:
                print(f'parsing sample {sample} failed with error {e}, skipping')
                continue

            records.append(sample_dic)

    df = pd.DataFrame(records, index=np.arange(len(records)))
    return df


def read_deltaquad_position_data(filename, round_time=False):
    """read the position data from the deltaquad drone from the vehicle_gps_position_0.csv file obtained with
    ulog2csv"""
    # ifile = f'data/{flightnumber}/{flightnumber}_vehicle_gps_position_0.csv'
    df = pd.read_csv(filename, sep=',')
    df['datetime'] = df['time_utc_usec'].apply(pd.Timestamp, unit='us')

    if round_time:
        # round time, and select the first occurence (since we now might have rows with the same time)
        df['datetime'] = df['datetime'].dt.round(round_time)
        df = df.groupby('datetime').head(1).reset_index()

    return df
