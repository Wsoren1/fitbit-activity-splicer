import tkinter as tk
from tkcalendar import Calendar, DateEntry
import pandas as pd
from datetime import datetime as dt
import os
from dotenv import load_dotenv
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt 

load_dotenv()
tz_region = os.environ.get("timezone")

root = tk.Tk()

cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
cal.pack(pady=20)

selected_date = None

def get_date():
    global selected_date 
    selected_date = cal.get_date()
    root.destroy()

btn = tk.Button(root, text='Get Date', command=get_date)
btn.pack(pady=10)

date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=10)

root.mainloop()

if not selected_date:
    raise ValueError('Must select a date')

df = pd.read_csv('data/imports/processed_HR.csv')
df = df.loc[df['date'] == selected_date]
df['timestamp'] = df['timestamp'].apply(lambda x : dt.strptime(x, '%Y-%m-%d %H:%M:%S'))

print(f'{selected_date} selected.  Found {len(df)} entries.')

start_time_unfmt = input('select a start time of the activity.\nTime: ')

t1 = dt.strptime(f'{selected_date} {start_time_unfmt}', '%Y-%m-%d %I:%M %p')

end_time_unfmt = input('select a end time of the activity.\nTime: ')

t2 = dt.strptime(f'{selected_date} {end_time_unfmt}', '%Y-%m-%d %I:%M %p')


time_range_filter = (df['timestamp'] >= t1) & (df['timestamp'] <= t2)

activity_data = df[time_range_filter]
print(f'Found {len(activity_data)} entries between {t1} and {t2}.')

X = activity_data['beats per minute']
print(X.describe())

plt.plot(X)
plt.show()
