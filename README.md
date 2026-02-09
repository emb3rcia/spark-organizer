# spark-organizer
A productivity app originally written in C#, rewritten in Python as part of Hack Club’s Reboot program.

# Requirements
- Python 3.10+
- PyQt6
- Git ***(only for installations using `git clone`)***

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

<a id="dark-theme"></a>
<details>
<summary><strong>Dark theme</strong></summary>

<img width="787" height="272" alt="Screenshot_20260209_111100" src="https://github.com/user-attachments/assets/7ee8f22c-2bd3-43df-a93d-d792c3271790" />
<img width="787" height="272" alt="Screenshot_20260209_111117" src="https://github.com/user-attachments/assets/b8f5e89b-a653-4518-9699-3290422aed74" />
<img width="787" height="272" alt="Screenshot_20260209_111132" src="https://github.com/user-attachments/assets/09f13db0-c725-4c77-a0e0-e31a21ecfc7e" />
<img width="787" height="272" alt="Screenshot_20260209_111142" src="https://github.com/user-attachments/assets/a1256311-0f43-41fb-85bc-ef86e22cfb51" />
<img width="787" height="272" alt="Screenshot_20260209_111151" src="https://github.com/user-attachments/assets/ef3dfeaa-a7de-4037-99f5-13a901fe9538" />

</details>

<a id="amoled-theme"></a>
<details>
<summary><strong>AMOLED theme</strong></summary>
  
<img width="787" height="272" alt="Screenshot_20260209_111213" src="https://github.com/user-attachments/assets/9968e9cd-c7e5-4153-88ee-adb187b8229c" />
<img width="787" height="272" alt="Screenshot_20260209_111217" src="https://github.com/user-attachments/assets/5ff2088d-3e75-4708-8d34-19bf5b00eb67" />
<img width="787" height="272" alt="Screenshot_20260209_111222" src="https://github.com/user-attachments/assets/cac4ea88-7582-4cf7-9ffa-ee9a07ef4d08" />
<img width="787" height="272" alt="Screenshot_20260209_111227" src="https://github.com/user-attachments/assets/bfa88eaa-8228-46e8-acf6-7d2e977ff793" />
<img width="787" height="272" alt="Screenshot_20260209_111234" src="https://github.com/user-attachments/assets/fbf3a141-290d-4cfb-9388-2edeac20335c" />

</details>

<a id="light-theme"></a>
<details>
<summary><strong>Light theme</strong></summary>
  
<img width="787" height="272" alt="Screenshot_20260209_111247" src="https://github.com/user-attachments/assets/ac1aa750-630b-40bf-871a-718e57b4819a" />
<img width="787" height="272" alt="Screenshot_20260209_111254" src="https://github.com/user-attachments/assets/55564d91-e0a9-4c57-8131-84c57f37a2dd" />
<img width="787" height="272" alt="Screenshot_20260209_111258" src="https://github.com/user-attachments/assets/dfeffddc-12ab-478c-9f05-e6b19a462138" />
<img width="787" height="272" alt="Screenshot_20260209_111301" src="https://github.com/user-attachments/assets/94ff4057-8610-48b9-aa89-1c1e6ba70196" />
<img width="787" height="272" alt="Screenshot_20260209_111305" src="https://github.com/user-attachments/assets/792aa744-89f2-4db0-9909-04e146c0c045" />

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
- Set how many cycles should be between the long breaks `(default: 4)`
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
spark-organizer's `Settings` tab allows you to change theme and amount of how many minutes before an event, deadline, or reminder you should be notified! Simply change your settings and click `Save settings`

## Stats
spark-organizer tracks your stats such as work times started or cycles complete! Simply open the `Stats` tab!

## Background running in tray
When clicking X on spark-organizer's window, it doesn't fully close it, instead, it runs in background and is accessible using your system's tray. To exit the app fully, click `Quit app` on main screen and follow the pop-up message.

# Screenshots
<a id="pop-ups"></a>
<details>
<summary><strong>Pop-Ups</strong></summary>
  
<img width="299" height="133" alt="Screenshot_20260209_112929" src="https://github.com/user-attachments/assets/0d103165-92d1-4c31-ae7d-2d41342b341b" />
<img width="443" height="126" alt="Screenshot_20260209_112814" src="https://github.com/user-attachments/assets/8653684a-7e98-43ed-96e4-876e3da83bae" />
<img width="339" height="123" alt="Screenshot_20260209_112510" src="https://github.com/user-attachments/assets/ca2ef6ca-4a1c-4412-8fd6-758ee7fa8c86" />
<img width="261" height="123" alt="Screenshot_20260209_113230" src="https://github.com/user-attachments/assets/b858df59-ac86-4d0b-a732-63878a7e58e5" />

</details>

<a id="notifications"></a>
<details>
<summary><strong>Notifications (the appearance depends on the system and desktop enviornment used)</strong></summary>
  
<img width="359" height="106" alt="Screenshot_20260209_113225" src="https://github.com/user-attachments/assets/7fa3c192-092c-43b0-bea9-552ade77cccd" />
<img width="359" height="106" alt="Screenshot_20260209_113113" src="https://github.com/user-attachments/assets/b1979fcc-c83c-4e56-a21b-1b70ab1e19ca" />
<img width="359" height="106" alt="Screenshot_20260209_112946" src="https://github.com/user-attachments/assets/65d55971-a929-4e63-aa9d-437ba35a2eb5" />
<img width="354" height="105" alt="Screenshot_20260209_111318" src="https://github.com/user-attachments/assets/778e01b7-6da6-4d5d-a8cf-7f38868122ad" />

</details>

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
