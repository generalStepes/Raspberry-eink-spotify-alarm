
# Raspberry E ink clock & Spotify alarm
Disclaimer: The documentation was intended mainly for my personal use, but as I didn’t find any other similar project, I decided to publish it.

## Prerequisites <br />
*	Raspberry Pi (RPI Zero in my case) <br />
*	Network capabilities <br /> <br />
*	E-ink display (Waveshare 4.3inch in my case) <br />
*	microSD card to put weather icons on, any size will work <br />

*	Weather icons (originally taken from: https://www.webpagefx.com/blog/web-design/free-icon-set-weather/) <br />
*	Free OpenWeatherMap Account <br />
*	All python libraries specified in the main file (note that epd library has to be configured separately) <br />
*	Mopidy and Mopidy Alarm Clock plugin configured and working, make sure your Spotify account and audio work <br />

## How does it work <br />
The whole thing is divided into two parts: the day version and night version. The “Day” version displays clock, current date, day of week and weather information. The “night” version displays information about Spotify alarm. <br />
<br />
*	Stuff is displayed on E-ink display via epd library. I use an E-ink display from Waveshare. <br />
  *	The display is updated once per minute, this is ensured by a cron job, after it gets updated, it’s put sleep and waken again during the next update <br /> 
  *	The display is cleared when the current time (minute specifically) divided by 5 is 0, i.e. every 5th minute. <br />
*	Weather information – are fetched via pyowm library from OpenWeatherMap, thus it’s necessary to create an OWM account.  <br />
*	Spotify is provided by Mopidy, alarm clock capabilities by Mopidy Alarm Clock plugin. <br />
*	The tricky part was how to know if there’s an alarm set up. I just fetch the webpage (e.g. http://192.168.2.110:6690/alarmclock/) and check if content is more than 3000 bytes. I’m able to tell if there’s an alarm set up or not as the page size differs significantly. Nothing to be proud about, but if it looks stupid and it works, it ain’t stupid, right? :-D <br />
*	If there’s an alarm set up, I parse the downloaded webpage and find strings for the time and playlist, which then get displayed. <br />
*	In case RPI is rebooted, alarm is restored from the "alarmLog" file

## How to make it work <br />
After fulfilling the prerequisites, there’re basically just few things that need to be modified in the python script. <br />
*	Change GPIO pin number, url where Mopidy runs, OWM api key and the location where alarmLog should be saved if necessary <br />
*	It order to get the icons work, copy them on FAT 32 formatted memory card, insert the card into the display and uncomment the epd_set_memory_sd(), epd_import_pic() and edp_set_memory_nand() parts in the script, wait for a minute or run the script manually. After that the icons should work and you can remove these parts. <br />

I’ve attached icons that I already processed myself, they’re cropped, converted and are verified to be working. <br />

## Known, expected issues and to-dos <br />
*	I’m sure that there’re some issues with getting the playlist name correctly displayed, especially when foreign accents are used. I implemented a function to remove the ones used in Czech language as I didn’t want to waste time trying to import any fonts to the E-ink display. <br />
*	I would like to add a button capability to stop the alarm when the button is pressed. <br />

## Changelog <br />
30th July - added support for alarm restoration if RPI is rebooted, clearer code, other fixes

![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/weather.jpg?raw=true)
![alt text](https://github.com/generalStepes/Waveshare-eink-raspberry/blob/master/img/spotify.jpg?raw=true)

