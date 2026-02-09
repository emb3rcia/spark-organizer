# spark-organizer
A productivity app originally written in C#, rewritten in Python as part of Hack Club’s Reboot program.

# Requirements
- Python 3.10+
- PyQt6

# Features
- [Custom themes](#custom-themes)
- [Custom sounds](#custom-sounds)
- [Pomodoro timer](#pomodoro-timer)
- [Deadline and event reminders](#deadline-and-event-reminders)
- [Normal reminders](#normal-reminders)
- [File corruption check](#file-corruption-check)
- [Settings](#settings)
- [Stats](#stats)
- [Background running in tray](#background-running-in-tray)

## Custom themes
spark-organizer includes 3 default themes (that are used in case of corruption): [dark](#dark-theme), [AMOLED](#amoled-theme) and [light](#light-theme). They aren't very pretty (I made them lol), but they are decent looking (at least for my UI design skills). But - if you don't like them, you can make your own! It's simple! Just do this:
- Open `config/themes.json`
- Copy one of the default themes
- Paste it (preferably at the end)
- Change its name
- In `Settings` tab select your theme and click Change settings

Done! Your new theme is ready to use!

### Dark theme

<details>
<summary>Screenshots</summary>

TODO: add screenshots through GitHub

</details>

### AMOLED theme

<details>
<summary>Screenshots</summary>

TODO: add screenshots through GitHub

</details>

### Light theme

<details>
<summary>Screenshots</summary>

TODO: add screenshots through GitHub

</details>

## Custom sounds
You can also replace default sounds with custom ones! Just do this:
- Prepare your sound: It must be `.wav`
- Open `assets/sounds/`
- Change the default sound's name to some other one (eg `ding1.wav`)
- Move your sound to the folder and set its name to `ding.wav` or `error.wav` depending on which sound you are changing

Done! App uses your sounds!

## Pomodoro timer
spark-organizer's feature number 1 is [Pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer. It's easy to use:
- Open `Pomodoro Timer` tab
- Set how many minutes the work time should be `(default: 25)`
- Set how many minutes the break time should be `(default: 5)`
- Set how many minutes the longer break time should be `(default: 15)`
- Set how many cycles should be between the long breaks`(default: 4)`
- Click `Start timer`
- To pause timer, click `Pause timer`
- To resume timer, click `Resume timer`
- To reset timer and/or change settings, click `Reset timer`

## Deadline and event reminders
spark-organizer's feature number 2 is deadline and event reminders, simply:
- Open `Events` tab
- On the left you will see added events and deadlines
- On the right you will see menu where you can add new event/deadline
- Select your event's/deadline's title
- Select its type
- *(in case of events)* Select its start date *(if you can't select it, select `Event type: event` first)*
- Select its end date
- Click `Add event`
- To delete event/deadline scroll to the last column in table on the left and click `Delete event`

Done, event/deadline added, you will be reminded the amount of minutes you set

## Normal reminders
spark-organizer's feature number 3 are normal reminders, usage? Here:
- Open `Reminders` tab
- On the left you will see added reminders
- On the right you will see menu where you can add new reminder
- Select your reminder's title
- Select its date and time
- Click `Add reminder`
- To delete reminder scroll to the last column in table on the left and click `Delete reminder`

## File corruption check
spark-organizer checks for corruption of files in `config` directory. If any of them is corrupted, it will display a pop-up asking you if you want to overwrite the corrupted file with default values, or allow you to debug it manually. If overwrite won't work the first time, please report this on `GitHub Issues`

## Settings
spark-organizer's `Settings` tab allows you to change theme and amount of how many minutes before event/deadline/reminder you should be notified! Simply change your settings and click `Save settings`

## Stats
spark-organizer tracks your stats such as work times started or cycles complete! Simply open the `Stats` tab!

## Background running in tray
When clicking X on spark-organizer's window, it doesn't fully close it, instead, it runs in background and is accessible using your system's tray. To exit the app fully, click `Quit app` on main screen and follow the pop-up message.

# Installation
There are 2 main ways to install spark-organizer:
- [GitHub Releases](#github-releases)
- [Git clone](#git-clone)

## GitHub releases
- Install `spark-organizer.zip` from [GitHub Releases](https://github.com/emb3rcia/spark-organizer/releases/)
- Extract files to desired destination folder
- Open terminal/command line window in desired destination folder
- Run `pip install -r requirements.txt`
- Run `python spark-organizer.py`

## Git clone
- Run `git clone https://github.com/emb3rcia/spark-organizer`
- Run `cd spark-organizer`
- Run `pip install -r requirements.txt`
- Run `python spark-organizer.py`

# Known errors
## Function-impacting errors
None function-impacting errors known
## Other errors
| Error                      | Description                                                                                                                                                                                                                             |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Naming style continuity    | Currently, I mix this_style with thisStyle. I know I shouldn't, I know there are python conventions (according to PyCharm) that regulate that, before next project I will read them, and then I will name variables accordingly to them |
| First theme change per run | Currently, first time you change your theme in settings it won't update. But! You just need to change it again to another theme and return to your desired one.                                                                         |

# Credits
Sounds used:
- "ding.wav" and "error.wav" by [https://orangefreesounds.com](https://orangefreesounds.com), licensed under CC BY-NC 4.0, transformed to WAV from MP3
- "icon.svg" by [iconscout.com](https://iconscout.com)
