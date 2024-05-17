import pandas as pd
import geopandas as gpd
import os


class Server:
    def __init__(self, include_maps=False):
        self.files = []
        self.engagements = pd.read_csv(self.get_relative_path('engagements.csv'))
        if include_maps:
            self.locations = pd.read_csv(self.get_relative_path('locations.csv'))
            self.bases = pd.read_csv(self.get_relative_path('bases.csv'))
            self.countries = gpd.read_file(self.get_relative_path('10m_cultural/ne_10m_admin_0_countries_usa.shp'))

    @staticmethod
    def get_relative_path(filename):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the data file
        return os.path.join(script_dir, filename)


data_server = Server()
map_server = Server(include_maps=True)
