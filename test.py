import urllib.request
import json
from datetime import datetime, timezone
import tkinter as tk
import threading

#200 Bus 900110522
#M4 Bahn 900110521
#Am Friedrichhain 900110019
STOP_ID = "900110019"
STOPS_AMOUNT = 5

request_count = 0

def get_line_color(line):
    if line == "200":
        return "#a5027d"
    elif line == "M4":
        return "#ff0000"
    elif line.startswith("S"):
        return "#17db52"
    elif line.startswith("X") or line.startswith("Y"):
        return "#00cc00"
    else:
        return "white"

def delay_config(l, d):
    if d == 0:
        text, color = "", "black"
    elif d < 0:
        text, color = f"{abs(d)} min early", "green"
    else:
        text, color = f"{d} min late", "red"
    l.config(text=text, fg=color)

def fetch_data():
    #API REQUEST COUNTER --- REMOVE LATER
    global request_count
    request_count += 1
    print(f"Request #{request_count}")
    ...

    url = f"https://v6.bvg.transport.rest/stops/{STOP_ID}/departures?results={STOPS_AMOUNT}&duration=300"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        departures = data.get("departures", [])

        for i, (Linelabel, Directionlabel, Timelabel, Delaylabel, Departurelabel) in enumerate(label_rows):
            if i < len(departures):
                dep = departures[i]
                line = dep.get("line", {}).get("name", "?")
                direction = dep.get("direction", "?")
                actual = dep.get("when") #, dep.get("plannedWhen") PLACEHOLDER
                delay = dep.get("delay") or 0

                try:
                    dt = datetime.fromisoformat(actual)
                    minutes = max(0, int((dt - datetime.now(timezone.utc)).total_seconds() / 60))
                except:
                    minutes = "?"

                d = int(delay / 60)

                root.after(0, lambda l=Linelabel, v=line: l.config(text=v, fg=get_line_color(v)))
                root.after(0, lambda l=Directionlabel, v=direction: l.config(text=v))
                root.after(0, lambda l=Timelabel, v=minutes, dd=d: l.config(text="now" if v + dd <= 0 else f"{v + dd} min"))
                root.after(0, lambda l=Delaylabel, dd=d: delay_config(l, dd))
                root.after(0, lambda l=Departurelabel, t=actual: l.config(text=datetime.fromisoformat(t).strftime("%H:%M")))
                #print(f"{i} {line} {direction} {minutes} + {d} and {actual}")
                #print(datetime.fromisoformat(actual).strftime("%H:%M"))
                #print("---")

    except Exception as e:
        print(f"Error fetching data: {e}")

def update_data():
    threading.Thread(target=fetch_data, daemon=True).start()
    root.after(10000, update_data)


root = tk.Tk()
root.title("BVG Api Test")
root.geometry("1550x480")
root.minsize(1550, 480)
root.configure(background="gray10")

label_rows = []

for i in range(STOPS_AMOUNT):
    row = tk.Frame(master=root, bg="gray10")
    row.pack(side="top", fill="x", padx=5, pady=5)

    Box1 = tk.Frame(master=row, width=200, height=200)
    Box1.pack(side="left", padx=5, pady=5)
    Linelabel = tk.Label(master=Box1, text="...", bg="gray10", fg="#a5027d", font=("Helvetica", 40))
    Linelabel.pack(side="top", padx=5, pady=5)

    Box2 = tk.Frame(master=row, width=200, height=200)
    Box2.pack(side="left", padx=5, pady=5)
    Directionlabel = tk.Label(master=Box2, text="...", bg="gray10", fg="white", font=("Helvetica", 40))
    Directionlabel.pack(side="top", padx=5, pady=5)

    Box5 = tk.Frame(master=row, width=200, height=200)
    Box5.pack(side="right", padx=5, pady=5)
    Departurelabel = tk.Label(master=Box5, text="", bg="gray10", fg="white", font=("Helvetica", 40))
    Departurelabel.pack(side="top", padx=5, pady=5)

    Box4 = tk.Frame(master=row, width=200, height=200)
    Box4.pack(side="right", padx=5, pady=5)
    Delaylabel = tk.Label(master=Box4, text="", bg="gray10", fg="white", font=("Helvetica", 40))
    Delaylabel.pack(side="top", padx=5, pady=5)

    Box3 = tk.Frame(master=row, width=200, height=200)
    Box3.pack(side="right", padx=5, pady=5)
    Timelabel = tk.Label(master=Box3, text="...", bg="gray10", fg="white", font=("Helvetica", 40))
    Timelabel.pack(side="top", padx=5, pady=5)


    label_rows.append((Linelabel, Directionlabel, Timelabel, Delaylabel, Departurelabel))

update_data()
root.mainloop()