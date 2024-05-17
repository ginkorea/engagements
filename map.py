import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches
from matplotlib.patheffects import withStroke

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

    def plot_legend(self, ax):
        # Add legend at the top of the map
        legend_x_start = 124.5
        legend_y = 38.8  # Adjust y position for the legend
        categories = ['Mil-Mil (US)', 'Mil-Mil (ROK)', 'Civ-Mil']
        colors = ['grey', 'grey', 'grey']
        shapes = ['triangle', 'circle', 'square']

        # Draw white rectangle with a black outline around the legend
        rect = mpatches.Rectangle((legend_x_start - 0.45, legend_y - 0.2), 8.35, 0.4, facecolor='white',
                                  edgecolor='black', lw=2, zorder=30, path_effects=[withStroke(linewidth=2, foreground='black')])
        shadow = mpatches.Shadow(rect, -0.02, -0.02, alpha=0.25, zorder=29)
        ax.add_patch(shadow)
        ax.add_patch(rect)

        for i, category in enumerate(categories):
            count = self.category_counters.get(category, 0)
            x = legend_x_start + i * 2.5
            y = legend_y

            if shapes[i] == 'triangle':
                marker = mpatches.RegularPolygon((x, y), numVertices=3, radius=0.12, orientation=-3.14 / 2,
                                                 color=colors[i], zorder=32)
            elif shapes[i] == 'circle':
                marker = mpatches.Circle((x, y), 0.12, color=colors[i], zorder=32)
            else:  # 'square'
                marker = mpatches.Rectangle((x - 0.12, y - 0.12), 0.24, 0.24, color=colors[i],
                                            zorder=32)

            ax.add_patch(marker)
            ax.text(x, y, str(count), ha='center', va='center', color='white', fontweight='bold', zorder=33)
            ax.text(x + 0.4, y, category, ha='left', va='center', fontsize=12, zorder=33)

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
        countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        rok = countries[countries['name'] == 'South Korea']
        dprk = countries[countries['name'] == 'North Korea']
        rok.plot(ax=ax, facecolor='lightblue')
        dprk.plot(ax=ax, facecolor='red')

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

                if row['category'] == 'Mil-Mil (US)':
                    marker = mpatches.RegularPolygon((x, y), numVertices=3, radius=0.12, orientation=-3.14 / 2,
                                                     color=row['color'], ec='black', lw=1, zorder=11)
                elif row['category'] == 'Mil-Mil (ROK)':
                    marker = mpatches.Circle((x, y), 0.08, color=row['color'], ec='black', lw=1, zorder=11)
                else:
                    marker = mpatches.Rectangle((x - 0.06, y - 0.06), 0.12, 0.12, color=row['color'], ec='black', lw=1,
                                                zorder=11)

                shadow = mpatches.Shadow(marker, -0.01, -0.01, alpha=0.3, zorder=10)

                ax.add_patch(shadow)
                ax.add_patch(marker)
                ax.text(x, y, str(num), fontsize=10, ha='center', va='center', color='white', fontweight='bold',
                        zorder=12, transform=ccrs.PlateCarree())

        # Add legend
        self.plot_legend(ax)

        # Save the plot as an image
        plt.savefig(self.output_image, bbox_inches='tight')
        plt.show()
