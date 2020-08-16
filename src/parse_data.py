import pandas as pd
import xmltodict

from workout import Workout

COLUMNS = ['activity_type',
           'duration',
           'duration_unit',
           'total_distance',
           'total_distance_unit',
           'total_energy_burned',
           'total_energy_burned_unit',
           'device',
           'creation_date',
           'start_date',
           'end_date',
           'route',
           'metadata_dict']


def parse_xml(path_to_file):
    with open(path_to_file) as fd:
        doc = xmltodict.parse(fd.read())
    return doc


def create_workout_df():
    data = parse_xml('..data/export.xml')
    workouts = data['HealthData'].get('Workout')
    series_list = [Workout(i).return_pd_series() for i in workouts]
    workout_df = pd.DataFrame(series_list)
    workout_df.columns = COLUMNS
    return workout_df

