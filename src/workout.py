class Workout(object):
    
    def __init__(self, item):
        self.activity_type = item.get('@workoutActivityType')
        self.duration = item.get('@duration', None)
        self.duration_unit = item.get('@durationUnit', None)
        self.total_distance = item.get('@totalDistance', None)
        self.total_distance_unit = item.get('@totalDistanceUnit', None)
        self.total_energy_burned = item.get('@totalEnergyBurned', None)
        self.total_energy_burned_unit = item.get('@totalEnergyBurnedUnit', None)
        self.device = item.get('@device', None)  # TODO: parse out details '<<HKDevice: 0x281da5590>, name:Apple Watch, manufacturer:Apple, model:Watch,
        self.creation_date = item.get('@creationDate', None)
        self.start_date = item.get('@startDate', None)  #TODO: parse to datetime '2018-12-08 16:03:34 -0400'
        self.end_date = item.get('@endDate', None) 
        self.route = item.get('WorkoutRoute', 
                              {'FileReference': {'@path': None}}).get('FileReference').get('@path')
        self.metadata = item.get('MetadataEntry', None)

        
    def parse_metadata(self, metadata):
        metadata_dict = {}
        if type(metadata) is not list:
            metadata = list(metadata)
        for i in metadata:
            metadata_dict[i.get('@key')] = i.get('@value')
        return metadata_dict
    
    
    def return_pd_series(self):
        
        self.metadata_dict = self.parse_metadata(self.metadata)
        
        return pd.Series([self.activity_type,
                         self.duration,
                         self.duration_unit,
                         self.total_distance,
                         self.total_distance_unit,
                         self.total_energy_burned,
                         self.total_energy_burned_unit,
                         self.device,
                         self.creation_date,
                         self.start_date,
                         self.end_date,
                         self.route,
                         self.metadata_dict])
                                    
        
    
