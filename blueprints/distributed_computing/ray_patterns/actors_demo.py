import argparse
from collections import namedtuple
import csv
import tarfile
import time

import ray


@ray.remote
class GSODActor():
    
    def __init__(self, year, high_temp):
        self.high_temp = float(high_temp)
        self.high_temp_count = None
        self.rows = []
        self.stations = None
        self.year = year

    async def get_row_count(self):
        return len(self.rows)

    async def get_high_temp_count(self):
        if self.high_temp_count is None:
            filtered = [l for l in self.rows if float(l.TEMP) >= self.high_temp]
            self.high_temp_count = len(filtered)
        return self.high_temp_count

    async def get_station_count(self):
        return len(self.stations)

    async def get_stations(self):
        return self.stations

    async def get_high_temp_count_for_stations(self, stations):
        filtered_rows = [l for l in self.rows if float(l.TEMP) >= self.high_temp and l.STATION in stations]
        return len(filtered_rows)

    async def load_data(self):
        file_name = self.year + '.tar.gz'
        Row = namedtuple('Row', ('STATION', 'DATE', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME', 'TEMP', 'TEMP_ATTRIBUTES', 'DEWP',
                                'DEWP_ATTRIBUTES', 'SLP', 'SLP_ATTRIBUTES', 'STP', 'STP_ATTRIBUTES', 'VISIB', 'VISIB_ATTRIBUTES',
                                'WDSP', 'WDSP_ATTRIBUTES', 'MXSPD', 'GUST', 'MAX', 'MAX_ATTRIBUTES', 'MIN', 'MIN_ATTRIBUTES', 'PRCP',
                                'PRCP_ATTRIBUTES', 'SNDP', 'FRSHTT'))

        tar = tarfile.open(file_name, 'r:gz')
        for member in tar.getmembers():
            member_handle = tar.extractfile(member)
            byte_data = member_handle.read()
            decoded_string = byte_data.decode()
            lines = decoded_string.splitlines()
            reader = csv.reader(lines, delimiter=',')

            # Get all the rows in the member. Skip the header.
            _ = next(reader)
            file_rows = [Row(*l) for l in reader]
            self.rows += file_rows

            #if self.high_temperature:
            #    filtered = [l for l in file_rows if float(l.TEMP) >= self.high_temperature]
            #    if len(filtered) > 0:
            #        self.rows += filtered
            #else:
            #    self.rows += file_rows

        self.stations = {l.STATION for l in self.rows}


def compare_years(year1, year2, high_temp):
    ray.init(num_cpus=2)

    gsod_y1 = GSODActor.remote(year1, high_temp)
    gsod_y2 = GSODActor.remote(year2, high_temp)

    ray.get([gsod_y1.load_data.remote(), gsod_y2.load_data.remote()])

    y1_stations, y2_stations = ray.get([gsod_y1.get_stations.remote(),
                                        gsod_y2.get_stations.remote()])

    intersection = set.intersection(y1_stations, y2_stations)

    y1_count, y2_count = ray.get([gsod_y1.get_high_temp_count_for_stations.remote(intersection),
                                  gsod_y2.get_high_temp_count_for_stations.remote(intersection)])

    print('Number of stations in common: {}'.format(len(intersection)))
    print('{} - High temp count for common stations: {}'.format(year1, y1_count))
    print('{} - High temp count for common stations: {}'.format(year2, y2_count))


async def compare_years_parallel(year1, year2, high_temp):
    ray.init(num_cpus=2)

    start_time = time.time()
    gsod_y1 = GSODActor.remote(year1, high_temp)
    gsod_y2 = GSODActor.remote(year2, high_temp)
    ray.get([gsod_y1.load_data.remote(), gsod_y2.load_data.remote()])
    duration = time.time() - start_time
    print('Load time: ', duration)

    start_time = time.time()
    y1_high_temp_count, y2_high_temp_count = ray.get([gsod_y1.get_high_temp_count.remote(),
                                                                 gsod_y2.get_high_temp_count.remote()])
    print('{} - Number of readings at {} degrees and above: {}'.format(year1, high_temp, y1_high_temp_count))
    print('{} - Number of readings at {} degress and above: {}'.format(year2, high_temp, y2_high_temp_count))
    duration = time.time() - start_time
    print('Get high temp time: ', duration)

    start_time = time.time()
    y1_station_count, y2_station_count = ray.get([gsod_y1.get_station_count.remote(),
                                                  gsod_y2.get_station_count.remote()])
    print('{} - Number of stations: {}'.format(year1, y1_station_count))
    print('{} - Number of stations: {}'.format(year2, y2_station_count))
    duration = time.time() - start_time
    print('Get station count time: ', duration)

    start_time = time.time()
    y1_stations, y2_stations = ray.get([gsod_y1.get_stations.remote(),
                                        gsod_y2.get_stations.remote()])
    intersection = set.intersection(y1_stations, y2_stations)
    print('Number of stations in common: {}'.format(len(intersection)))
    duration = time.time() - start_time
    print('Get stations time: ', duration)

    start_time = time.time()
    y1_common_high_temp_count, y2_common_high_temp_count = ray.get([gsod_y1.get_high_temp_count_for_stations.remote(intersection),
                                                                    gsod_y2.get_high_temp_count_for_stations.remote(intersection)])
    print('{} - High temp count for common stations: {}'.format(year1, y1_common_high_temp_count))
    print('{} - High temp count for common stations: {}'.format(year2, y2_common_high_temp_count))
    duration = time.time() - start_time
    print('Get common high temp time: ', duration)


def compare_years_sequential(year1, year2, high_temp):
    ray.init(num_cpus=2)

    start_time = time.time()
    gsod_y1 = GSODActor.remote(year1, high_temp)
    gsod_y2 = GSODActor.remote(year2, high_temp)
    ray.get(gsod_y1.load_data.remote())
    ray.get(gsod_y2.load_data.remote())
    duration = time.time() - start_time
    print('Load time: ', duration)

    start_time = time.time()
    y1_high_temp_count = ray.get(gsod_y1.get_high_temp_count.remote())
    y2_high_temp_count = ray.get(gsod_y2.get_high_temp_count.remote())
    print('{} - Number of readings at {} degrees and above: {}'.format(year1, high_temp, y1_high_temp_count))
    print('{} - Number of readings at {} degress and above: {}'.format(year2, high_temp, y2_high_temp_count))
    duration = time.time() - start_time
    print('Get high temp time: ', duration)

    start_time = time.time()
    y1_station_count = ray.get(gsod_y1.get_station_count.remote())
    y2_station_count = ray.get(gsod_y2.get_station_count.remote())
    print('{} - Number of stations: {}'.format(year1, y1_station_count))
    print('{} - Number of stations: {}'.format(year2, y2_station_count))
    duration = time.time() - start_time
    print('Get station count time: ', duration)

    start_time = time.time()
    y1_stations = ray.get(gsod_y1.get_stations.remote())
    y2_stations = ray.get(gsod_y2.get_stations.remote())
    intersection = set.intersection(y1_stations, y2_stations)
    print('Number of stations in common: {}'.format(len(intersection)))
    duration = time.time() - start_time
    print('Get stations time: ', duration)

    start_time = time.time()
    y1_common_high_temp_count = ray.get(gsod_y1.get_high_temp_count_for_stations.remote(intersection))
    y2_common_high_temp_count = ray.get(gsod_y2.get_high_temp_count_for_stations.remote(intersection))
    print('{} - High temp count for common stations: {}'.format(year1, y1_common_high_temp_count))
    print('{} - High temp count for common stations: {}'.format(year2, y2_common_high_temp_count))
    duration = time.time() - start_time
    print('Get common high temp time: ', duration)


if __name__ == '__main__':

    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-ht', '--high_temp',
                        help='High temperature for load filter.')
    parser.add_argument('-y1', '--year1',
                        help='Year to load data.')
    parser.add_argument('-y2', '--year2',
                        help='Year to load data.')


    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message if something is wrong.
    args = parser.parse_args()


    #START_TIME = time.time()

    #compare_years_sequential(args.year1, args.year2, args.high_temp)
    #asyncio.run(compare_years_parallel(args.year1, args.year2, args.high_temp))
    compare_years(args.year1, args.year2, args.high_temp)

    #DELTA = time.time() - START_TIME
    #print('Total elapsed time: ', DELTA)
