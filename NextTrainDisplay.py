#!/usr/bin/python3
import urllib.request
import time
import datetime


def main():
    """Generate a HTML file containing information from SEPTA's API about the 
    next trains to depart a given SEPTA station.
    """
    # Open settings to make and open the URL
    settings = open("settings.txt", "r")
    station = settings.readline().strip("\n")
    NUMBER_OF_RESULTS = 5
    direction = settings.readline().strip("\n")
    settings.close()
    url = ("https://www3.septa.org/api/Arrivals/index.php?station=" + station
           + "&results=" + str(NUMBER_OF_RESULTS) + "&direction=" + direction)
    url = url.replace(" ", "%20")
    site = urllib.request.urlopen(url)
    raw_data = site.read()
    site.close()

    # Get the scheduled times and format the data
    data = str(raw_data)
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
            depart_time_output = data[index+24:index+29]
            # Convert from 24 hour clock to 12 hour clock
            if (int(depart_time_output[0:2]) > 12):
                depart_time_output = (str(int(depart_time_output[0:2]) - 12) +
                                     depart_time_output[2:5] + " pm")
            elif (int(depart_time_output[0:2]) < 12 and
                  int(depart_time_output[0:2]) > 0):
                depart_time_output = depart_time_output + " am"
            elif (int(depart_time_output[0:2]) == 12):
                depart_time_output = depart_time_output + " pm"
            else:
                depart_time_output = str(
                    "12" + depart_time_output[2:5] + " am")
            depart_time.append(depart_time_output)

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
    min_until_depart = []
    for index, item in enumerate(data):
        if (item == "\"train_id\""):
            train_id.append(
                str(data[index + 1]).replace("\"", "").replace(".", ""))
        elif (item == "\"destination\""):
            destination.append(
                str(data[index + 1]).replace("\"", "").replace("_", " "))
        elif (item == "\"line\""):
            line.append(
                str(data[index + 1]).replace("\"", "").replace("_", " "))
        elif (item == "\"status\""):
            status.append(
                str(data[index + 1]).replace("\"", "").replace("_", " "))
        elif (item == "\"service_type\""):
            if ((str(data[index + 1])[1:4] == "EXP")):
                service_type.append("EXPRESS")
            else:
                service_type.append(str(data[index + 1]).replace("\"", ""))
        elif (item == "\"next_station\""):
            next_station.append(
                str(data[index + 1]).replace("\"", "").replace("_", " ")
                .replace("Penn Medical", "Penn Medicine")
                .replace("Delaware Valley College",
                         "Delaware Valley University")) # Fix API name errors

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
        min_until_depart.append(
            int((depart_timestamps[index] - current_time) / 60) + late)

    # Sort trains by time until departure.
    train_order = []
    departure_sorter = []
    for x in range(0, len(min_until_depart)):
        departure_sorter.append(min_until_depart[x])
    number_to_sort = len(train_id)
    if (number_to_sort > 5):
        number_to_sort = 5
    for x in range(0, number_to_sort):
        minimum = 1000
        min_index = -1
        for index, item in enumerate(departure_sorter):
            if (item < minimum):
                minimum = departure_sorter[index]
                min_index = index
        train_order.append(min_index)
        departure_sorter[min_index] = 1000

    # Output the data to next-train-display.html
    output = open("next-train-display.html", "w")
    output.write('<!doctype html> <html lang="en">  <head> ' +
                 '<meta charset="utf-8"> <link rel="stylesheet" ' +
                 'href="./style.css"> <title>Next Train Display</title>' +
                 '<script type="text/javascript" ' +
                 'src="next-train-display.js" defer></script></head><body>' +
                 '<body> <div id="top"></div> <div id="title-row" ' +
                 'class="gjs-row"> <div id="time" class="gjs-cell"> ' +
                 '<div id="time-text"></div> </div> <div id="about" ' +
                 'class="gjs-cell"> <div id="about-text">This is an ' +
                 'unofficial real-time information display that uses ' +
                 'SEPTA&#039;s API. Visit septa.org for official real-time ' +
                 'information, schedules, maps, alerts, advisories, ' +
                 'elevator outages, and more. The data displayed here is ' +
                 'Copyright Southeastern Pennsylvania Transportation ' +
                 'Authority. All Rights Reserved.</div> </div> </div>')
    for index, position in enumerate(train_order):
        # Set train_status
        train_status = ""
        if (status[position] != "999 min late"):
            if (next_station[position] == "null"):
                train_status = "Not Tracked"
            else:
                train_status = status[position]
        else:
            train_status = "Suspended"
        # Set border_color
        if (train_status == "On Time"):
            border_color = "green"
        elif (train_status == "Suspended"):
            border_color = "red"
        elif (train_status == "Not Tracked"):
            border_color = "blue"
        else:
            LEN_MIN_LATE = 9
            train_status_int = int(
                train_status[0:len(train_status) - LEN_MIN_LATE])
            if (train_status_int < 3):
                border_color = "green"
            elif (train_status_int < 6):
                border_color = "yellow"
            elif (train_status_int < 9):
                border_color = "orange"
            else:
                border_color = "red"
        # Set train_min_until_depart
        train_min_until_depart = ""
        if (train_status != "Suspended"):
            train_min_until_depart = "Departs in " + \
                str(min_until_depart[position]) + " min"
            if (min_until_depart[position] == 0):
                train_min_until_depart = "Departing now"
        else:
            train_min_until_depart = ""
        # Set next_stop
        if (train_status != "Suspended" and next_station[position] != "null"):
            next_stop = "Next Stop: " + next_station[position]
        else:
            next_stop = ""

        output.write('<div id="horizontal-line-' + str(index + 1) +
                     '" class="gjs-row"></div> <div id="train-' +
                     str(index + 1) +
                     '-row-1" class="gjs-row"> <div id="train-id-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-id-' +
                     str(index + 1) + '-text">' + train_id[position] +
                     '<br /></div> </div> <div id="train-service-type-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-service-type-' +
                     str(index + 1) + '-text">' + service_type[position] +
                     '</div> </div> <div id="train-status-' + str(index + 1) +
                     '" style="border: 0.5vh solid ' + border_color +
                     ';" class="gjs-cell"> <div id="train-status-' +
                     str(index + 1) + '-text">' + train_status +
                     '<br /></div> </div> <div id="train-min-until-depart-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-min-until-depart-' +
                     str(index + 1) + '-text">' + train_min_until_depart +
                     '<br /></div> </div> </div> <div id="train-' +
                     str(index + 1) +
                     '-row-2" class="gjs-row"> <div id="train-line-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-line-' +
                     str(index + 1) + '-text">' + line[position] +
                     ' Line<br /></div> </div> <div id="train-destination-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-destination-' +
                     str(index + 1) + '-text">To ' + destination[position] +
                     '<br /></div> </div> <div id="train-next-station-' +
                     str(index + 1) +
                     '" class="gjs-cell"> <div id="train-next-station-' +
                     str(index + 1) + '-text">' + next_stop +
                     '<br /></div> </div> </div>')

    output.write('</body> </body> </html>')
    output.close()

    # Determined by the minimum next_departure_time,
    # set the time until the next update
    if (len(min_until_depart) > 0):
        next_departure_time = min(min_until_depart)
        if (next_departure_time > 20):
            update_frequency = 60
        elif (next_departure_time > 10):
            update_frequency = 45
        elif (next_departure_time > 5):
            update_frequency = 30
        elif (next_departure_time > 2):
            update_frequency = 15
        else:
            update_frequency = 10
    else:
        update_frequency = 60
    time.sleep(update_frequency)
    main()


if __name__ == "__main__":
    main()
