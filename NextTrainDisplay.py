#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
import urllib.request
import time
import datetime
"""Make a visual display that contains live information about the next trains 
to depart a given SEPTA Regional Rail station using SEPTA's API.
"""


def main():
    """Make lists with the data, update the window with the data, then loop.
    """
    data = get_data_from_api()

    # Get the scheduled times and format the data
    depart_time = []
    depart_timestamps = []
    current_time = time.time()
    for index in range(len(data)):
        if (data[index:index+11] == "depart_time"):
            depart_time_output = data[index+14:index+30]
            depart_timestamp = time.mktime(datetime.datetime.strptime
                                           (depart_time_output,
                                            "%Y-%m-%d %H:%M").timetuple())
            depart_timestamps.append(depart_timestamp)

    # Format the data
    data = (data.replace(" ", "_").replace("\\", "").replace(",", " ")
            .replace("{", " ").replace("{", " ").replace("[", " ")
            .replace("}", " ").replace("]", " ").replace(":", " ").split())

    # Get the data into lists
    train_id = []
    destination = []
    line = []
    status = []
    service_type = []
    next_station = []
    min_until_depart_int = []
    min_until_depart = []
    for index, item in enumerate(data):
        if (item == "\"train_id\""):
            train_id.append(
                str(data[index + 1]).replace("\"", "").replace(".", ""))
        elif (item == "\"destination\""):
            destination.append(
                "To " + str(data[index + 1]).replace("\"", "")
                .replace("_", " "))
        elif (item == "\"line\""):
            line.append(
                str(data[index + 1]).replace("\"", "").replace("_", " ")
                + " Line")
        elif (item == "\"status\""):
            status.append(
                str(data[index + 1]).replace("\"", "").replace("_", " "))
        elif (item == "\"service_type\""):
            if ((str(data[index + 1])[1:4] == "EXP")):
                service_type.append("EXPRESS")
            else:
                service_type.append(str(data[index + 1]).replace("\"", ""))
        elif (item == "\"next_station\""):
            if (str(data[index + 1]) == "null"):
                next_station.append("")
            else:
                next_station.append(
                    "Next Stop: "
                    + str(data[index + 1]).replace("\"", "").replace("_", " ")
                    .replace("Penn Medical", "Penn Medicine")
                    .replace("Delaware Valley College",
                             "Delaware Valley University"))  # Fix API errors

    # Find the amount of minutes until the train departs
    for index in range(len(depart_timestamps)):
        # Create an int for the late time
        late = "0"
        if (status[index] == "On Time"):
            pass
        else:
            for second_index in range(0, 3):
                if (status[index][second_index] in ["0", "1", "2", "3", "4",
                                                    "5", "6", "7", "8", "9"]):
                    late = late + status[index][second_index]
            status[index] = status[index] + " late"
        late = int(late)
        if (str(next_station[index]) == ""):
            status[index] = "Not Tracked"

        # Make the minutes until the train departs message
        if (status[index] != "Suspended"):
            if (int((depart_timestamps[index] - current_time) / 60)
                    + late != 0):
                min_until_depart.append(
                    "Departs in "
                    + (str(int((depart_timestamps[index] - current_time) / 60)
                           + late)) + " min")
                min_until_depart_int.append(
                    int((depart_timestamps[index] - current_time) / 60)
                    + late)
            else:
                min_until_depart.append("Departing now")
                min_until_depart_int.append(0)
        else:
            min_until_depart.append("")
            min_until_depart_int.append(999)

    # Sort trains by time until departure.
    train_order = []
    departure_sorter = []
    for index in range(0, len(min_until_depart_int)):
        departure_sorter.append(min_until_depart_int[index])
    number_to_sort = len(train_id)
    if (number_to_sort > maximum_results):
        number_to_sort = maximum_results
    for index in range(0, number_to_sort):
        minimum = 2000
        min_index = -1
        for index, item in enumerate(departure_sorter):
            if (item < minimum):
                minimum = departure_sorter[index]
                min_index = index
        train_order.append(min_index)
        departure_sorter[min_index] = 2000

    # Update the display data
    for index in range(len(train_order)):
        display_train_id[index].config(text=train_id[train_order[index]])
        display_service_type[index].config(
            text=service_type[train_order[index]])
        display_status[index].config(text=status[train_order[index]],
                                     fg=status_color(
            status[train_order[index]]))
        display_min_until_depart[index].config(
            text=min_until_depart[train_order[index]])
        display_line[index].config(text=line[train_order[index]])
        display_destination[index].config(text=destination[train_order[index]])
        display_next_station[index].config(
            text=next_station[train_order[index]])

    # Remove data from rows that should be empty
    if (len(train_order) < maximum_results):
        for index in range(len(train_order), maximum_results):
            display_train_id[index].config(text="")
            display_service_type[index].config(text="")
            display_status[index].config(text="")
            display_min_until_depart[index].config(text="")
            display_line[index].config(text="")
            display_destination[index].config(text="")
            display_next_station[index].config(text="")

    update_frequency = time_until_next_update(min_until_depart_int)
    root.after(update_frequency, main)


def get_data_from_api():
    """Get data from SEPTA's API and format the data
    Return the API data
    """
    url = ("https://www3.septa.org/api/Arrivals/index.php?station=" + station
           + "&direction=" + direction)
    url = url.replace(" ", "%20")
    site = urllib.request.urlopen(url)
    raw_data = site.read()
    site.close()
    return str(raw_data)


def status_color(status):
    """Determine the text color of the status message
    Return the hexadecimal value for the color
    """
    if (status == "On Time"):
        return "#00FF00"  # Lime
    elif (status == "Suspended"):
        return "#FF6347"  # Tomato
    elif (status == "Not Tracked"):
        return "#00FFFF"  # Cyan
    elif (int(status.replace(" min late", "")) < 3):
        return "#00FF00"  # Lime
    elif (int(status.replace(" min late", "")) < 6):
        return "#FFFF00"  # Yellow
    elif (int(status.replace(" min late", "")) < 9):
        return "#FFA500"  # Orange
    else:
        return "#FF6347"  # Tomato


def time_until_next_update(min_until_depart_int):
    """Determine amount of time until the data gets updated,
    which is lower when a train is close to depart the station
    Return the time until the data gets updated in milliseconds
    """
    if (len(min_until_depart_int) > 0):
        next_departure_time = min(min_until_depart_int)
        if (next_departure_time > 20):
            return 60000
        elif (next_departure_time > 10):
            return 45000
        elif (next_departure_time > 5):
            return 30000
        elif (next_departure_time > 2):
            return 15000
        else:
            return 10000


if __name__ == "__main__":
    """Get the settings and create the display
    """
    # Get the settings
    settings = open("settings.txt", "r")
    fullscreen = settings.readline().strip("\n")
    maximum_results = int(settings.readline().strip("\n"))
    station = settings.readline().strip("\n")
    direction = settings.readline().strip("\n")
    settings.close()

    # Create the display
    root = Tk()
    BG_COLOR = "#000000"  # Black
    FG_COLOR = "#FFFFFF"  # White
    root.configure(bg=BG_COLOR)
    if (fullscreen[0].upper() == "T"):
        fullscreen = True
    else:
        fullscreen = False
    root.attributes('-fullscreen', fullscreen)
    root.title("Next Train Display")
    FONT = ("Arial", int(root.winfo_screenwidth() / 50))

    display_train_id = []
    display_service_type = []
    display_status = []
    display_min_until_depart = []
    display_line = []
    display_destination = []
    display_next_station = []

    copyright = []

    for index in range(maximum_results):
        # Make labels
        display_train_id.append(Label(root))
        display_service_type.append(Label(root))
        display_status.append(Label(root))
        display_min_until_depart.append(Label(root))
        display_line.append(Label(root))
        display_destination.append(Label(root))
        display_next_station.append(Label(root))

        # Set the labels' font and background
        display_train_id[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_service_type[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_status[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_min_until_depart[index].config(
            bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_line[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_destination[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)
        display_next_station[index].config(bg=BG_COLOR, fg=FG_COLOR, font=FONT)

        # Make the grid
        display_train_id[index].grid(row=index * 3, column=0)
        display_service_type[index].grid(row=index * 3, column=1)
        display_status[index].grid(row=index * 3, column=2)
        display_min_until_depart[index].grid(row=index * 3, column=3)
        display_line[index].grid(row=index * 3 + 1, column=0, columnspan=2)
        display_destination[index].grid(row=index * 3 + 1, column=2)
        display_next_station[index].grid(row=index * 3 + 1, column=3)
        root.grid_rowconfigure(index * 3, weight=4)
        root.grid_rowconfigure(index * 3 + 1, weight=4)
        ttk.Separator(root, orient=HORIZONTAL).grid(
            row=index * 3 + 2, column=0, columnspan=4, sticky="ew")

    # Make copyright disclaimer
    copyright.append(Label(root))
    copyright[0].config(bg=BG_COLOR, fg=FG_COLOR, font=("Arial", int(root.winfo_screenwidth() / 130)),
                        text="This is an unofficial real-time information display that uses SEPTA's API. Visit septa.org for more information. The displayed data is Copyright Southeastern Pennsylvania Transportation Authority. All Rights Reserved.")
    copyright[0].grid(row=(maximum_results - 1) *
                      3 + 3, column=0, columnspan=4)
    root.grid_rowconfigure((maximum_results - 1) * 3 + 3, weight=1)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=2)
    root.grid_columnconfigure(3, weight=2)

    main()
    root.mainloop()
