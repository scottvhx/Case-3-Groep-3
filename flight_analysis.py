import pandas as pd
from datetime import datetime

import data_cleaning
import flight_analysis

flight_schedule_df = data_cleaning.scheduleclean[['STA_STD_ltc', 'ATA_ATD_ltc', 'Org/Des']].copy()

flight_schedule_df['STA_STD_ltc'] = pd.to_datetime(flight_schedule_df['STA_STD_ltc'], format='mixed')
flight_schedule_df['ATA_ATD_ltc'] = pd.to_datetime(flight_schedule_df['ATA_ATD_ltc'], format='mixed')

flight_schedule_df.loc[:, 'Delay'] = (flight_schedule_df['ATA_ATD_ltc'] - flight_schedule_df['STA_STD_ltc']).dt.total_seconds().div(60).astype(float)

flight_schedule_df.sort_values(by=['Delay'], ascending=False, inplace=True)

print(flight_schedule_df.head(10))


# Convert 'Delay' column to numeric format (hours)
flight_analysis.scheduleclean['Delay_hours'] = pd.to_timedelta(flight_analysis.scheduleclean['Delay']).dt.total_seconds() / 3600

# Grouping by Aircraft Type (FLT) and calculating the average Delay
avg_delay_per_aircraft_type = flight_analysis.scheduleclean.groupby('ACT')['Delay_hours'].mean().reset_index()

