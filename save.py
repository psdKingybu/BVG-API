import urllib.request
import json
from datetime import datetime, timezone

import tkinter as tk
from tkinter import *

# station ID
STOP_ID = "900110521"

url = f"https://v6.bvg.transport.rest/stops/{STOP_ID}/departures?results=10"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

departures = data.get("departures", [])

print(f"Next departures from Hufelandstraße:\n")
for dep in departures[:10]:
    line = dep.get("line", {}).get("name", "?")
    LINE = dep.get("line", {}).get("name", "?")
    direction = dep.get("direction", "?")
    DIRECTION = dep.get("direction", "?")
    planned = dep.get("plannedWhen", "?")
    actual = dep.get("when", planned)

    time_str = actual[:16] if actual else "?"
    try:
        dt = datetime.fromisoformat(actual)
        time_str = dt.strftime("%H:%M")
        minutes = int((dt - datetime.now(timezone.utc)).total_seconds() / 60)
    except Exception as e:
        minutes = "?"

    print(f"  {line:6} → {direction:30} departs in {minutes} min")


root = tk.Tk()
root.title("BVG Api Test")
root.geometry("1150x500")
root.minsize(1150, 500)


Box1 = Frame(master=root, bg="red", width=200, height=200)
Box1.pack(side="left", padx="5", pady="5")

Linelabel = Label(master=Box1, text=LINE, bg="white", fg="black", font=("Helvetica", 40))
Linelabel.pack(side='top', padx='5', pady='5')

Box2 = Frame(master=root, bg="green", width=200, height=200)
Box2.pack(side="left", padx="5", pady="5")

Directionlabel = Label(master=Box2, text=DIRECTION, bg="white", fg="black", font=("Helvetica", 40))
Directionlabel.pack(side='top', padx='5', pady='5')

Box3 = Frame(master=root, bg="yellow", width=200, height=200)
Box3.pack(side="left", padx="5", pady="5")

Timelabel = Label(master=Box3, text=f"{minutes} min", bg="white", fg="black", font=("Helvetica", 40))
Timelabel.pack(side='top', padx='5', pady='5')

root.mainloop()