import urllib.request
import json
from datetime import datetime, timezone
import tkinter as tk
import threading

#200 Bus 900110522
#M4 Bahn 900110521
STOP_ID = "900110521"
STOPS_AMOUNT = 3

def fetch_data():
    url = f"https://v6.bvg.transport.rest/stops/{STOP_ID}/departures?results={STOPS_AMOUNT}&duration=300"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        departures = data.get("departures", [])

        for i, (Linelabel, Directionlabel, Timelabel) in enumerate(label_rows):
            if i < len(departures):
                dep = departures[i]
                line = dep.get("line", {}).get("name", "?")
                direction = dep.get("direction", "?")
                actual = dep.get("when", dep.get("plannedWhen"))
                delay = dep.get("delay")

                try:
                    dt = datetime.fromisoformat(actual)
                    minutes = int((dt - datetime.now(timezone.utc)).total_seconds() / 60)
                except:
                    minutes = "?"

                root.after(0, lambda l=Linelabel, v=line: l.config(text=v))
                root.after(0, lambda l=Directionlabel, v=direction: l.config(text=v))
                root.after(0, lambda l=Timelabel, v=minutes: l.config(text="now" if v == 0 else f"{v} min"))

    except Exception as e:
        print(f"Error fetching data: {e}")

def update_data():
    threading.Thread(target=fetch_data, daemon=True).start()
    root.after(10000, update_data)


root = tk.Tk()
root.title("BVG Api Test")
root.geometry("1150x500")
root.minsize(1150, 500)
root.configure(background="gray20")

label_rows = []

for i in range(STOPS_AMOUNT):
    row = tk.Frame(master=root, bg="gray20")
    row.pack(side="top", fill="x", padx=5, pady=5)

    Box1 = tk.Frame(master=row, width=200, height=200)          #, bg="red"
    Box1.pack(side="left", padx=5, pady=5)
    Linelabel = tk.Label(master=Box1, text="...", bg="white", fg="black", font=("Helvetica", 40))
    Linelabel.pack(side="top", padx=5, pady=5)

    Box2 = tk.Frame(master=row, width=200, height=200)          #, bg="green"
    Box2.pack(side="left", padx=5, pady=5)
    Directionlabel = tk.Label(master=Box2, text="...", bg="white", fg="black", font=("Helvetica", 40))
    Directionlabel.pack(side="top", padx=5, pady=5)

    Box3 = tk.Frame(master=row, width=200, height=200)          #, bg="yellow"
    Box3.pack(side="left", padx=5, pady=5)
    Timelabel = tk.Label(master=Box3, text="...", bg="white", fg="black", font=("Helvetica", 40))
    Timelabel.pack(side="top", padx=5, pady=5)

    label_rows.append((Linelabel, Directionlabel, Timelabel))

update_data()
root.mainloop()