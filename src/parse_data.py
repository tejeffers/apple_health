iport pandas as pd
import xmltodict

from workout import Workout
from common import * 


def parse_xml(path_to_file):
    with open(path_to_file) as fd:
        doc = xmltodict.parse(fd.read())
    return doc


def parse_metadata(row):
    if row.get('HKIndoorWorkout', None) is not None:
        return pd.Series([bool(row.get('HKIndoorWorkout')), 
                          row.get('HKAverageMETs', ' kcal/hr·kg').split(' kcal/hr·kg')[0],
                          row.get('HKWeatherTemperature', ' degF').split(' degF')[0],
                          row.get('HKWeatherHumidity', ' %').split(' %')[0], 
                          row.get('HKTimeZone'),
                          row.get('HKElevationAscended', ' cm').split(' cm')[0]])
    else:
        return pd.Series([None,None,None,None,None,None])
    
    
def add_metadata_unit(df):
    df['average_mets_unit'] = 'kcal/hr·kg'
    df['temperature_unit'] = 'degF'
    df['humidity_unit'] = '%'
    df['elevation_ascended_unit'] = 'cm'
    return df


def append_metadata(df):
    
    df[['was_indoor_workout','average_mets','temperature',
        'humidity', 'timezone','elevation_ascended']] = df.metadata_dict.apply(lambda x: parse_metadata(x))
    
    return add_metadata_unit(df)


def format_columns(df):
    df = df[FORMATTED_COLUMNS]
    df = df.replace(r'', None, regex=True)

    for dcol in DATETIMESTAMP_COLUMNS:
        df[dcol] = pd.to_datetime(df[dcol])

    for fcol in FLOAT_COLUMNS:
        df[fcol] = df[fcol].astype(float)
    return df



def create_workout_df():
    data = parse_xml('..data/export.xml')
    workouts = data['HealthData'].get('Workout')
    series_list = [Workout(i).return_pd_series() for i in workouts]
    workout_df = pd.DataFrame(series_list)
    workout_df.columns = COLUMNS
    workout_df = append_metadata(workout_df)
    workout_df = format_columns(workout_df)

    return workout_df

