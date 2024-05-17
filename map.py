import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from puck import Puck


class MapPlotter:
    def __init__(self, engagements_file='data/engagements.csv', bases_file='data/bases.csv', output_image='map.png'):
        self.engagements_file = engagements_file
        self.bases_file = bases_file
        self.output_image = output_image
        self.gdf = self.load_data()
        self.category_counters = {'Mil-Mil (US)': 0, 'Mil-Mil (ROK)': 0, 'Civ-Mil': 0}

    def load_data(self):
        # Load base location data from CSV
        bases_df = pd.read_csv(self.bases_file)
        engagements_df = pd.read_csv(self.engagements_file)

        # Merge engagements with base locations on the base name
        merged_df = engagements_df.merge(bases_df, left_on='location', right_on='name', how='left')

        if 'longitude' not in merged_df.columns or 'latitude' not in merged_df.columns:
            raise KeyError("The merged DataFrame must contain 'longitude' and 'latitude' columns.")

        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df['longitude'], merged_df['latitude']))
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf

    def plot_legend(self, ax, scale=1):
        # Add legend at the top of the map
        legend_x_start = 124.5
        legend_y = 38.8  # Adjust y position for the legend
        categories = ['Mil-Mil (US)', 'Mil-Mil (ROK)', 'Civ-Mil']
        colors = ['grey', 'grey', 'grey']

        # Draw white rectangle with a black outline around the legend
        rect = mpatches.Rectangle((legend_x_start - 0.5, legend_y - 0.3), 8.5, 0.6 * scale, facecolor='white',
                                  edgecolor='black', lw=1, zorder=1)
        shadow = mpatches.Rectangle((legend_x_start - 0.52, legend_y - 0.32), 8.5, 0.6 * scale,
                                    facecolor=(0, 0, 0, 0.3), zorder=0)
        ax.add_patch(shadow)
        ax.add_patch(rect)

        for i, category in enumerate(categories):
            count = self.category_counters.get(category, 0)
            x = legend_x_start + i * 2.5
            y = legend_y

            puck = Puck(x, y, category, colors[i], count, scale=scale)
            puck.add_to_axes(ax)
            ax.text(x + 0.4 * scale, y, category, ha='left', va='center', fontsize=12 * scale, zorder=3)

    def plot_map(self):
        # Create the plot with cartopy
        fig, ax = plt.subplots(figsize=(10, 12), subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_extent([124, 131, 33, 39], crs=ccrs.PlateCarree())

        # Add detailed coastlines
        ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=1)
        ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')

        # Color the map regions
        ax.add_feature(cfeature.OCEAN, facecolor='lightgrey')
        ax.add_feature(cfeature.LAND, facecolor='lightblue')
        ax.add_feature(cfeature.LAKES, facecolor='white')
        ax.add_feature(cfeature.RIVERS, edgecolor='blue')

        # Color South Korea and North Korea
        countries = gpd.read_file('data/10m_cultural/ne_10m_admin_0_countries_usa.shp')
        #countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        rok = countries[countries['ADM0_A3_US'] == 'KOR']
        # rok = gpd.read_file('data/10m_cultural/ne_10m_admin_0_countries_kor.shp')
        dprk = countries[countries['ADM0_A3_US'] == 'PRK']
        # dprk = gpd.read_file('data/10m_cultural/')
        jpn = countries[countries['ADM0_A3_US'] == 'JPN']
        rok.plot(ax=ax, facecolor='lightblue')
        dprk.plot(ax=ax, facecolor='red')
        jpn.plot(ax=ax, facecolor='white')

        # Plot the GeoDataFrame
        offset_dict = {}

        for idx, row in self.gdf.iterrows():
            location = (row.geometry.x, row.geometry.y)
            category = row['category']
            self.category_counters[category] += 1
            if location not in offset_dict:
                offset_dict[location] = []
            offset_dict[location].append((idx, self.category_counters[category], row))

        for location, items in offset_dict.items():
            base_x, base_y = location
            for i, (idx, num, row) in enumerate(items):
                x_offset = (i % 3) * 0.2  # Adjust offset as necessary
                y_offset = (i // 3) * 0.2  # Adjust offset as necessary
                x = base_x + x_offset
                y = base_y + y_offset

                puck = Puck(x, y, row['category'], row['color'], num, scale=1)
                puck.add_to_axes(ax)

        # Add legend
        self.plot_legend(ax, scale=1)

        # Save the plot as an image
        plt.savefig(self.output_image, bbox_inches='tight')
        plt.show()
