import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
from graphics.puck import Puck
from data.server import data_server


class CalendarPlotter:
    def __init__(self, fiscal_week, output_image='calendar.png'):
        self.start_date = None
        self.fiscal_week = fiscal_week
        self.server = data_server
        self.output_image = output_image
        self.engagements = self.load_engagements()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

    def load_engagements(self):
        # Load engagement data from CSV
        df = self.server.engagements
        df['date'] = pd.to_datetime(df['date'])
        df['day'] = df['date'].dt.day_name()
        return df

    @staticmethod
    def adjust_weekends(day):
        # Adjust dates falling on weekends
        if day == 'Saturday':
            return 'Friday'
        elif day == 'Sunday':
            return 'Monday'
        return day

    def draw_frame(self):
        # Create a 50x40 grid
        self.ax.set_xticks(range(0, 51, 10))
        self.ax.set_xticks(range(0, 51), minor=True)
        self.ax.set_yticks(range(0, 41, 10))
        self.ax.set_yticks(range(0, 41), minor=True)
        self.ax.grid(which='major', color='black', linestyle='-', linewidth=1)

        # Label the days of the week at intervals of 10
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for i, day in enumerate(days):
            self.ax.text(i * 10 + 5, 41, day, ha='center', va='bottom', fontsize=10)

        # Label the weeks at intervals of 10
        for week in range(4):
            this_fiscal_week = week + self.fiscal_week
            self.ax.text(-2, week * 10 + 5, f'Week {this_fiscal_week + 1}', ha='right', va='center', fontsize=10)

        # Calculate the starting date of the calendar (Monday of the first week)
        min_date = self.engagements['date'].min()
        self.start_date = min_date - timedelta(days=min_date.weekday())  # Find the Monday of the starting week

        # Plot dates
        for week in range(4):
            for day in range(5):
                current_date = self.start_date + timedelta(days=week * 7 + day)
                date_str = current_date.strftime('%-m.%-d')
                x_pos = day * 10
                y_pos = (week * 10) - 9
                self.ax.text(x_pos + 0.5, y_pos + 9.5, date_str, ha='left', va='top', fontsize=10)

        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 40)
        self.ax.invert_yaxis()

    def plot_engagements(self):
        # Create a dictionary to store the engagements by date
        engagements_by_date = {}
        category_counters = {'Mil-Mil (US)': 1, 'Mil-Mil (ROK)': 1, 'Civ-Mil': 1}

        # Store each engagement
        for index, row in self.engagements.iterrows():
            week_index = (row['date'] - self.start_date).days // 7  # Convert date to week index
            day = self.adjust_weekends(row['day'])
            day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].index(day)  # Convert day to x-index

            if week_index < 4:
                # Store the engagement in the dictionary
                date_str = row['date'].strftime('%-m.%-d')
                if (week_index, day_index) not in engagements_by_date:
                    engagements_by_date[(week_index, day_index)] = {'date': date_str, 'engagements': []}
                engagements_by_date[(week_index, day_index)]['engagements'].append(row)

        # Function to wrap text
        def wrap_text(text, max_length):
            words = text.split()
            wrapped_text = ""
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= max_length:
                    if line:
                        line += " "
                    line += word
                else:
                    if wrapped_text:
                        wrapped_text += "\n"
                    wrapped_text += line
                    line = word
            if line:
                if wrapped_text:
                    wrapped_text += "\n"
                wrapped_text += line
            return wrapped_text

        # Plot engagements
        for (week_index, day_index), info in engagements_by_date.items():
            x_pos = day_index * 10
            y_pos = (week_index * 10) - 6

            for idx, engagement in enumerate(info['engagements']):
                y_offset = y_pos + 2 * idx  # Adjust y position by +2 for each additional event

                puck = Puck(x_pos + 1, y_offset + 9, engagement['category'], engagement['color'],
                            category_counters[engagement['category']], scale=6, font=8)
                puck.add_to_axes(self.ax)
                category_counters[engagement['category']] += 1

                # Wrap engagement text to fit within the day cell
                wrapped_engagement = wrap_text(engagement['engagement'],
                                               max_length=15)  # Adjust max_length as necessary
                self.ax.text(x_pos + 2, y_offset + 9, wrapped_engagement, ha='left', va='center', fontsize=8, wrap=True)

        return category_counters

    def save_calendar(self):
        plt.savefig(self.output_image, bbox_inches='tight')
        plt.show()

