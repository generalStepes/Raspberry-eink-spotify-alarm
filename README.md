
# Raspberry E ink clock & Spotify alarm

## Prerequisites <br />

* Files description: <br />
  * pialarm.py - core file handling eink display and alarm
  * autoamp - script for switching the amp relay on and off
  * snooze_mpd - snooze script - "red button"
  * mopidy_mpd - turn off script - "green button"  
  * cron - copy of my cron file scheduling jobs for display, buttons and wifi dongle (to keep it alive)
  * box.svg - Inkscape file with the box design
  * weather_icons.tar - weather icons


Core stuff <br />
*	Raspberry Pi (RPI Zero in my case) <br />
*	Network capabilities <br /> <br />
*	E-ink display (Waveshare 4.3inch in my case) <br />
*	microSD card to put weather icons on, any size will work <br />

*	Weather icons (originally taken from: https://www.webpagefx.com/blog/web-design/free-icon-set-weather/) <br />
*	Free OpenWeatherMap Account <br />
*	All python libraries specified in the main file (note that epd library has to be configured separately) <br />
*	Mopidy and Mopidy Alarm Clock plugin configured and working, make sure your Spotify account and audio work <br />

Sound system <br />
* Apart from the Raspberry itself, it is necessary to get some other things in order to get the sound working.<br />
In my case that meant: <br />
*	USB hub + Wifi dongle as Raspberry Pi Zero doesn’t have wifi <br />
*	DAC <br />
*	Amplifier – I’m using a cheap 2x3 W stereo amp based on pam8403 chip, powered on 3,3 V <br />
*	Speakers – two 9 x 5 cm speakers <br />

* Ground loop isolator – after putting all the stuff together I encountered some serious issues with noise – I could hear the power supply, wifi dongle and CPU in speakers. Thus I bought a ground loop isolator (specifically Audac TR-2070), which solved most of the noise issues. The rest got solved by powering the amp on 3,3 V instead of 5 V (powered directly from RPI GPIO pins). <br />


## How to make it work <br />
After fulfilling the prerequisites, there’re basically just few things that need to be modified in the python script. <br />
*	Change GPIO pin number, url where Mopidy runs, OWM api key and the location where alarmLog should be saved if necessary <br />
*	It order to get the icons work, copy them on FAT 32 formatted memory card, insert the card into the display and uncomment the epd_set_memory_sd(), epd_import_pic() and edp_set_memory_nand() parts in the script, wait for a minute or run the script manually. After that the icons should work and you can remove these parts. <br />

I’ve attached icons that I already processed myself, they’re cropped, converted and are verified to be working. <br />

## Box & Design <br />
I'm attaching an SVG file created in Inscape with the box design I use. Laser cutter Trotec Speedy 300 was used for the creation together with a 4 mm poplar plywood.<br />

## Optional stuff <br />
* Amp Relay - I've added an amp relay, which turns on amp when music is played and turns it off after 30 seconds of inacitivity. The script can be found in the **autoamp** file (not that you'll likely have to modify the GPIO pin). Original source is: http://www.runeaudio.com/forum/auto-amplifier-on-off-t928.html - you can also find there a guide how to set it up as a service.
* Spotify Connect - I reccomend to install a Spotify connect client (e.g. https://github.com/dtcooper/raspotify), so that you can use this bedside clock as a wireless Spotify speaker.
* Buttons - I'm using two buttons - red one for snoozing and a green one to turn the alarm off. Also pressing the red one whilst there's no alarm set up, will set up an alarm in 15 minutes. Note that the display has to be refreshed twice to react to button press. Also don't forger to change GPIO pin number if necessary.
.

## Known, expected issues and to-dos <br />
*	I’m sure that there’re some issues with getting the playlist name correctly displayed, especially when foreign accents are used. I implemented a function to remove the ones used in Czech language as I didn’t want to waste time trying to import any fonts to the E-ink display. <br />
* I'd like to add an equalizer to tune up the sound a bit. However this has turned out to be a bit of a hassle so far.

## How does it work <br />
The whole thing is divided into two parts: the day version and night version. The “Day” version displays clock, current date, day of week and weather information. The “night” version displays information about Spotify alarm. <br />
<br />
*	Stuff is displayed on E-ink display via epd library. I use an E-ink display from Waveshare. <br />
  *	The display is updated once per minute, this is ensured by a cron job, after it gets updated, it’s put sleep and waken again during the next update <br /> 
  *	The display is cleared when the current time (minute specifically) divided by 5 is 0, i.e. every 5th minute. <br />
*	Weather information – are fetched via pyowm library from OpenWeatherMap, thus it’s necessary to create an OWM account.  <br />
*	Spotify is provided by Mopidy, alarm clock capabilities by Mopidy Alarm Clock plugin: https://github.com/DavisNT/mopidy-alarmclock. <br />
*	The tricky part was how to know if there’s an alarm set up. I just fetch the webpage (e.g. http://192.168.2.110:6690/alarmclock/) and check if content is more than 3000 bytes. I’m able to tell if there’s an alarm set up or not as the page size differs significantly. Nothing to be proud about, but if it looks stupid and it works, it ain’t stupid, right? :-D <br />
*	If there’s an alarm set up, I parse the downloaded webpage and find strings for the time and playlist, which then get displayed. <br />
*	In case RPI is rebooted, alarm is restored from the "alarmLog" file. <br />

## Changelog <br />
30th July - added support for alarm restoration if RPI is rebooted, clearer code, other fixes <br />
19th August - added sound system info <br />
6th September - added box info and new photos <br />
12th September - added GPIOs layout

![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/front.jpg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/gpios.svg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/side.jpg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/up.jpg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/inside.jpg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/spotify.jpg?raw=true)

