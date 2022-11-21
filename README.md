![screenshot](https://user-images.githubusercontent.com/89806788/203143460-577a32fb-e3dd-4e72-aa70-e549318db4ac.png)
# NextTrainDisplay
A local web page that displays live information about the next Regional Rail trains to depart a given SEPTA station. For this, a looping Python program is used to take data from [SEPTA's API](https://www3.septa.org/) and output a HTML file containing information about the next trains to depart a given station.
# Description
**NextTrainDisplay.py** - This gets data from SEPTA's API and outputs a HTML file. The code's loop frequency is determined by the minimum time until departure.\
**next-train-display.html** - This is the display for the data. This file is opened by a web browser and is intended to be displayed fullscreen on a 16:9 or wider aspect ratio display.\
**next-train-display.js** - This makes the clock on the display and refreshes the page every 10 seconds.\
**style.css** - This is the style sheet for next-train-display.html. This determines everything except for train-status-[1 - 5]'s border color, which is in next-train-display.html and determined by NextTrainDisplay.py.\
**settings.txt** - This determines what station (required) and what direction (optional) to get the train information for.
# Usage
To run this display, make sure that you have an internet connection, a web broswer, and anything that can run Python files.\
First, open settings.txt. Make the first line the station that you want the train information for. Please note that SEPTA's API sometimes uses different names internally than what is displayed publicly. Please check the table below to see if the name you are using has a different internal name. **If your display is not showing any trains, this may be the issue.** If you want to limit trains to a certain direction, add a second line and either 'N' or 'S'.\
**N** - Limit display to trains traveling "northbound" (Gray 30th Street Station → Suburban Station → Jefferson Station → Temple University)\
**S** - Limit display to trains traveling "southbound" (Temple University → Jefferson Station → Suburban Station → Gray 30th Street Station)\
Make sure to save settings.txt. Then, run NextTrainDisplay.py and open **next-train-display.html** with a web browser. If everything works, you should see something very similar to the screenshot above.
| Public name | Name you must use in settings.txt |
| --- | --- |
| North Philadelphia (Chestnut Hill West and Trenton Lines only) | North Philadelphia Amtrak |
| Gray 30th Street Station | 30th Street Station |
| Terminal A | Airport Terminal A |
| Terminal B | Airport Terminal B |
| Terminals C & D | Airport Terminal C D |
| Terminals E & F | Airport Terminal E F |
| Richard Allen Lane | Allen Lane |
| Delaware Valley University | Delaware Valley College |
| 9th Street | 9th Street Lansdale |
| Fern Rock Transportation Center | Fern Rock TC |
| Norristown (Elm Street) | Norristown Elm Street |
| Main Street Norristown | Main Street |
| Norristown Transportation Center | Norristown TC |
| Holmesburg Junction | Holmesburg Jct |
| Chester Transportation Center | Chester TC |
# Special Thanks
[GrapeJS](https://grapesjs.com/) for its HTML and CSS generating tool.\
[SEPTA](https://www3.septa.org/) for making the API that this project uses.
