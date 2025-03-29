import tkinter as tk
from tkcalendar import Calendar, DateEntry
import pandas as pd

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
print(df.loc[df['date'] == selected_date])