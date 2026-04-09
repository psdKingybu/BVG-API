import urllib.request
import json
from datetime import datetime, timezone
import tkinter as tk
import threading

STOP_ID = "900100003"

def fetch_data():
    url = f"https://v6.bvg.transport.rest/stops/{STOP_ID}/departures?results=2"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        departures = data.get("departures", [])

        if departures:
            dep = departures[0]
            line = dep.get("line", {}).get("name", "?")
            direction = dep.get("direction", "?")
            actual = dep.get("when", dep.get("plannedWhen"))

            try:
                dt = datetime.fromisoformat(actual)
                minutes = int((dt - datetime.now(timezone.utc)).total_seconds() / 60)
            except:
                minutes = "?"

            # update UI from main thread
            root.after(0, lambda: Linelabel.config(text=line))
            root.after(0, lambda: Directionlabel.config(text=direction))
            root.after(0, lambda: Timelabel.config(text="now" if minutes == 0 else f"{minutes} min"))

    except Exception as e:
        print(f"Error fetching data: {e}")

def update_data():
    threading.Thread(target=fetch_data, daemon=True).start()
    root.after(10000, update_data)  # schedule next update


root = tk.Tk()
root.title("BVG Api Test")
root.geometry("1150x500")
root.minsize(1150, 500)

Box1 = tk.Frame(master=root, bg="red", width=200, height=200)
Box1.pack(side="left", padx=5, pady=5)
Linelabel = tk.Label(master=Box1, text="...", bg="white", fg="black", font=("Helvetica", 40))
Linelabel.pack(side="top", padx=5, pady=5)

Box2 = tk.Frame(master=root, bg="green", width=200, height=200)
Box2.pack(side="left", padx=5, pady=5)
Directionlabel = tk.Label(master=Box2, text="...", bg="white", fg="black", font=("Helvetica", 40))
Directionlabel.pack(side="top", padx=5, pady=5)

Box3 = tk.Frame(master=root, bg="yellow", width=200, height=200)
Box3.pack(side="left", padx=5, pady=5)
Timelabel = tk.Label(master=Box3, text="...", bg="white", fg="black", font=("Helvetica", 40))
Timelabel.pack(side="top", padx=5, pady=5)

update_data()
root.mainloop()