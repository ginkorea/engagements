import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from graphics.puck import IEPuck
from data.server import data_server


class InformationEnvironmentGenerator:
    def __init__(self, output_image='90-day-information-env.png'):
        self.engagements = None
        self.today = datetime.today()
        self.output_image = output_image
        self.load_engagements()

    def load_engagements(self):
        # Load engagement data using data_server
        self.engagements = data_server.engagements90
        self.engagements['date'] = pd.to_datetime(self.engagements['date'])  # Ensure date is in datetime format

    def plot_engagement_chart(self):
        # Calculate the current date and the end date (three months from now)
        start_date = self.today.replace(day=1)
        if self.today.day > (datetime(self.today.year, self.today.month + 1, 1) - timedelta(days=1)).day - 7:
            start_date = (start_date + timedelta(days=31)).replace(day=1)
        end_date = start_date + timedelta(days=90)

        # Filter engagements within the date range
        df_filtered = self.engagements[
            (self.engagements['date'] >= start_date) & (self.engagements['date'] <= end_date)]

        # Define the rows for the y-axis
        y_labels = ['Civilian', 'Military', 'DIV', '8A', 'Higher', 'Holidays']
        y_bounds = {'Civilian': 16, 'Military': 42, 'DIV': 50, '8A': 58, 'Higher': 66, 'Holidays': 74}
        y_mapping = {label: y_bounds[label] - (y_bounds[label] - (0 if i == 0 else list(y_bounds.values())[i - 1])) / 2
                     for i, label in enumerate(y_labels)}

        # Create the plot
        fig, ax = plt.subplots(figsize=(15, 8))

        # Set major and minor ticks for grid lines
        ax.set_xticks(pd.date_range(start=start_date, end=end_date, freq='W-MON'), minor=False)
        ax.set_yticks(list(y_bounds.values()), minor=False)
        ax.grid(which='major', linestyle='--', linewidth=0.5)

        # Label the y-axis with vertical text
        for label, y in y_mapping.items():
            ax.text(start_date - timedelta(days=5), y, label, va='center', ha='center', rotation=45, fontsize=10, color='black')

        # Adjust plotting area to avoid plotting directly on the lines
        ax.set_ylim(0, max(y_bounds.values()) + 5)

        # Create dictionaries to store the counts for each category and status
        counts = {label: 0 for label in y_labels}
        total_counts = {'in planning': 0, 'for approval': 0, 'approved': 0}
        status_counts = {'in planning': 0, 'for approval': 0, 'approved': 0}

        status_mapping = {0: 'in planning', 1: 'for approval', 2: 'approved'}
        color_mapping = {'in planning': 'brown', 'for approval': 'darkorange', 'approved': 'green'}

        # Plot each engagement
        for idx, row in df_filtered.iterrows():
            date = mdates.date2num(row['date'])  # Convert date to numerical value
            category = row['category']
            engagement_type = row['type']
            engagement = row['engagement']
            status = status_mapping[row['status']]

            y_base = y_bounds[category]  # Base y position for the category
            i = counts[category]

            # Determine the vertical position for the engagement
            y = y_base - 1.5 - (i * 3)
            if y <= (0 if list(y_bounds.values())[0] == y_base else y_bounds[
                list(y_bounds.keys())[list(y_bounds.values()).index(y_base) - 1]]):
                counts[category] = 0
                y = y_base - 1.5 - (counts[category] * 3)

            # Update count
            counts[category] += 1
            total_counts[status] += 1
            status_counts[status] += 1

            x = date
            puck = IEPuck(x, y, engagement_type, status_counts[status], approved=row['status'], scale=14)
            puck.add_to_axes(ax)
            ax.text(x + 2, y, engagement, fontsize=8, ha='left', va='center', color='black', wrap=True)

        # Set x and y axis labels and limits
        ax.set_xlim(start_date, end_date)
        ax.set_ylim(0, max(y_bounds.values()) + 5)

        # Add gridlines and format the x-axis for dates
        ax.grid(True, which='major', linestyle='--', linewidth=0.5)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()

        # Add title to the graph
        ax.set_title(f'90 Day Information Environment ({start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")})', fontsize=14)

        # Add legend at the bottom with total counts
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label=f'In Planning ({total_counts["in planning"]})',
                       markerfacecolor='brown', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label=f'For Approval ({total_counts["for approval"]})',
                       markerfacecolor='darkorange', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label=f'Approved ({total_counts["approved"]})',
                       markerfacecolor='green', markersize=10)
        ]
        ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=10)

        # Save the plot as an image
        plt.savefig(self.output_image, bbox_inches='tight')
        plt.show()


# Example usage
generator = InformationEnvironmentGenerator()
generator.plot_engagement_chart()
