#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import unicodedata
from datetime import datetime as date
from pprint import pprint
import httplib2
import requests
import RPi.GPIO as GPIO  
from epd import *
from time import sleep
import sys
import datetime
import pyowm
import os, sys 
import ctypes
import struct



#alarmLog file location, change if necessary
alarmLogLocation = "/home/pi/alarmLog"

#alarmLog file location, change if necessary
alarmLogPlaylistLocation = "/home/pi/alarmLogPlaylist"


#for which city should the forecast be fetched
forecastLocation = "Brno,cz"

#apikey for OWM
apiKey = 'APIKEY'

#gpio pin number where wakeup wire is connected
GPIOPin = 12

#mopidy port
mopidyPort = "6690"



#get system uptime
#https://stackoverflow.com/questions/42471475/fastest-way-to-get-system-uptime-in-python-in-linux
def uptime3():
    libc = ctypes.CDLL('libc.so.6')
    buf = ctypes.create_string_buffer(4096) # generous buffer to hold
                                            # struct sysinfo
    if libc.sysinfo(buf) != 0:
        print('failed')
        return -1

    uptime = struct.unpack_from('@l', buf.raw)[0]
    return uptime



def getAlarmTime():
   h = httplib2.Http(".cache")
   resp, content = h.request("http://127.0.0.1:" + mopidyPort + "/alarmclock", "GET")
   headers={'cache-control':'no-cache'}

   if int(resp.values()[1]) < 3000:

      alarmTime=content[1495:1500]
      playlistEnd = content.find("with <strong>")
      playlist=content[1536:playlistEnd-10]

      return[alarmTime,playlist]
   else:
       #fetch playlist code for playlist name  
      global globalContent
      globalContent = content
      return(0)



def displayWeather():
   try:
      os.remove(alarmLogLocation)
   except:
      pass
   owm = pyowm.OWM(apiKey) 



   #weather
   observation = owm.three_hours_forecast(forecastLocation)
   w = observation.get_forecast().get_weathers()
   #second item is plus 3 hours
   w = w[1]
   if "01d" in w.get_weather_icon_name(): todayIcon = "01D.BMP"
   if "01n" in w.get_weather_icon_name(): todayIcon = "01N.BMP"
   if "02d" in w.get_weather_icon_name(): todayIcon = "02D.BMP"
   if "02n" in w.get_weather_icon_name(): todayIcon = "02N.BMP"
   if "03d" in w.get_weather_icon_name(): todayIcon = "03D.BMP"
   if "03n" in w.get_weather_icon_name(): todayIcon = "03D.BMP"
   if "04d" in w.get_weather_icon_name(): todayIcon = "04D.BMP"
   if "04n" in w.get_weather_icon_name(): todayIcon = "04D.BMP"
   if "09d" in w.get_weather_icon_name(): todayIcon = "09D.BMP"
   if "09n" in w.get_weather_icon_name(): todayIcon = "09D.BMP"
   if "10d" in w.get_weather_icon_name(): todayIcon = "10D.BMP"
   if "10n" in w.get_weather_icon_name(): todayIcon = "10D.BMP"
   if "11d" in w.get_weather_icon_name(): todayIcon = "11D.BMP"
   if "11n" in w.get_weather_icon_name(): todayIcon = "11D.BMP"
   if "13d" in w.get_weather_icon_name(): todayIcon = "13D.BMP"
   if "13n" in w.get_weather_icon_name(): todayIcon = "13D.BMP"
   if "50d" in w.get_weather_icon_name(): todayIcon = "50D.BMP"
   if "50n" in w.get_weather_icon_name(): todayIcon = "05D.BMP"
 


   forecast = owm.daily_forecast(forecastLocation , limit=2)
   f = forecast.get_forecast()
   lst = f.get_weathers()
   #for weather in f:
      #print (weather.get_reference_time('iso'),weather.get_status(),weather.get_temperature('celsius'))

   if "01d" in lst[0].get_weather_icon_name(): tomorrowIcon = "01D.BMP"
   if "01n" in lst[0].get_weather_icon_name(): tomorrowIcon = "01N.BMP"
   if "02d" in lst[0].get_weather_icon_name(): tomorrowIcon = "02D.BMP"
   if "02n" in lst[0].get_weather_icon_name(): tomorrowIcon = "02N.BMP"
   if "03d" in lst[0].get_weather_icon_name(): tomorrowIcon = "03D.BMP"
   if "03n" in lst[0].get_weather_icon_name(): tomorrowIcon = "03D.BMP"
   if "04d" in lst[0].get_weather_icon_name(): tomorrowIcon = "04D.BMP"
   if "04n" in lst[0].get_weather_icon_name(): tomorrowIcon = "04D.BMP"
   if "09d" in lst[0].get_weather_icon_name(): tomorrowIcon = "09D.BMP"
   if "09n" in lst[0].get_weather_icon_name(): tomorrowIcon = "09D.BMP"
   if "10d" in lst[0].get_weather_icon_name(): tomorrowIcon = "10D.BMP"
   if "10n" in lst[0].get_weather_icon_name(): tomorrowIcon = "10D.BMP"
   if "11d" in lst[0].get_weather_icon_name(): tomorrowIcon = "11D.BMP"
   if "11n" in lst[0].get_weather_icon_name(): tomorrowIcon = "11D.BMP"
   if "13d" in lst[0].get_weather_icon_name(): tomorrowIcon = "13D.BMP"
   if "13n" in lst[0].get_weather_icon_name(): tomorrowIcon = "13D.BMP"
   if "50d" in lst[0].get_weather_icon_name(): tomorrowIcon = "50D.BMP"
   if "50n" in lst[0].get_weather_icon_name(): tomorrowIcon = "05D.BMP"
 

   if "01d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "01D.BMP"
   if "01n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "01N.BMP"
   if "02d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "02D.BMP"
   if "02n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "02N.BMP"
   if "03d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "03D.BMP"
   if "03n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "03D.BMP"
   if "04d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "04D.BMP"
   if "04n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "04D.BMP"
   if "09d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "09D.BMP"
   if "09n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "09D.BMP"
   if "10d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "10D.BMP"
   if "10n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "10D.BMP"
   if "11d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "11D.BMP"
   if "11n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "11D.BMP"
   if "13d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "13D.BMP"
   if "13n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "13D.BMP"
   if "50d" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "50D.BMP"
   if "50n" in lst[1].get_weather_icon_name(): dayAfterTomorrowIcon = "05D.BMP"

   return [todayIcon,tomorrowIcon,dayAfterTomorrowIcon,w,lst[0],lst[1]]


def readAlarmLog():
   try:
      F = open(alarmLogLocation,"r")
      playlistHour = F.readline().rstrip()
      playlistName =  F.readline().rstrip()
      buttonPressedCheck = F.readline().rstrip()
      F.close()
      #find encoded playlist name
      playlistEndLocation = globalContent.find(playlistName)
      playlistStartLocation = globalContent[0:playlistEndLocation].rfind("spotify")
      playlistEncoded = globalContent[playlistStartLocation:playlistEndLocation-2]
      #re-set the alarm if low uptime indicates that rpi has been rebooted recently, i.e. in 300 seconds
      if (uptime3() < 300) or (buttonPressedCheck == "true"):
         r = requests.post("http://127.0.0.1:" + mopidyPort + "/alarmclock/set/", data={'time': playlistHour, 'playlist': playlistEncoded})
         alarmTime = removeChars(playlistHour, playlistName)
         return (alarmTime)
      else:
         return (0)
   except:
      return (0)


def removeChars(alarmTime):
   if alarmTime[0]:
      F = open(alarmLogPlaylistLocation,"w")
      F.write(alarmTime[1])
      F = open(alarmLogLocation,"w")
      F.write(alarmTime[0])
      F.write("\n")
      F.write(alarmTime[1])
      F.close()
   alarmTime[1] = string.replace(alarmTime[1], "&amp;", "&")
   #crashes with that type of dash
   alarmTime[1] = string.replace(alarmTime[1], "–", "-")
  #http://www.py.cz/Cestina2X
   #remove czech accents
   alarmTime[1] = unicode(alarmTime[1], 'utf-8')
   alarmTime[1] = unicodedata.normalize('NFKD', alarmTime[1])

   output = ''
   for c in alarmTime[1]:
      if not unicodedata.combining(c):
         output += c

   alarmTime[1] = output
   return alarmTime

   
#wait a bit so that mopidy initialises properly
if uptime3()<120: quit()
#readAlarmLog()
alarmTime = getAlarmTime()
#alarmTime returns zero if alarmtime doesnt exist, firstly try to fetch from website, ifnot load file, ifnot display weather
if alarmTime == 0:
   alarmTime = readAlarmLog()
if alarmTime == 0: 
      weatherStuff = displayWeather()
else:
   alarmTime = removeChars(alarmTime)

 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(GPIOPin, GPIO.OUT) # set a port/pin as an output   
GPIO.output(GPIOPin, 1)       # set port/pin value to 1/GPIO.HIGH/True


now = datetime.datetime.now()


def english():
    for x in [x for x in range(25,790,100)]:
        epd_ascii(x-1, 30, 'ABC')
    epd_update()


# display LCD digits 
def lcd_digits():
    epd_lcd_digits(30,10,str(now.hour)+":"+ str(now.minute).zfill(2),scale=LCD_MD)

if __name__=="__main__":
    try:
        epd_connect()
    except:
        sys.exit()

    if now.minute % 5 ==0: epd_clear()

    #epd_set_memory_sd()                   # use internal memory (default)
    #epd_import_pic()                        # copy images from SD card to internal memory
    #epd_set_memory_nand()          
    
    epd_set_en_font(ASCII64)    
    epd_ascii(500,10,str(now.day)+".   "+str(now.month)+".   "+str(now.year))
    epd_ascii(500,90,date.today().strftime("%A"))    
    if alarmTime == 0:
       epd_set_en_font(ASCII48)   
       epd_ascii(30,200,"+3 Hours :")
       epd_bitmap(30,400,weatherStuff[0])    
       epd_ascii(30,260,str(round(weatherStuff[3].get_temperature('celsius')['temp'],1))+ " C")
       epd_ascii(30,310,str(weatherStuff[3].get_status()))
       epd_ascii(305,200,"+1 Day :")
       epd_bitmap(305,400,weatherStuff[1])
       epd_ascii(305,260,str(round(weatherStuff[4].get_temperature('celsius').values()[5],1))+ " C")
       epd_ascii(305,310,str(weatherStuff[4].get_status()))    
       epd_ascii(580,200,"+2 Days :")
       epd_bitmap(580,400,weatherStuff[2])
       epd_ascii(580,260,str(round(weatherStuff[5].get_temperature('celsius').values()[5],1))+ " C")
       epd_ascii(580,310,str(weatherStuff[5].get_status()))
    else:
       epd_set_en_font(ASCII64)
       epd_ascii(30,200,"Spotify  alarm  is  set  up !")
       epd_set_en_font(ASCII48)
       epd_ascii(30,300,alarmTime[0])
       epd_ascii(30,400,alarmTime[1])    
   
    lcd_digits()       
    epd_halt()                              # put EPD to sleep. to wake up pin by physical pin only
    epd_disconnect()

GPIO.output(GPIOPin, 0)       # set port/pin value to 1/GPIO.LOW
   
