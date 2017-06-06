# Running in python 3.5
#
# Recources
# xbmc.player functions
#   http://mirrors.kodi.tv/docs/python-docs/13.0-gotham/xbmc.html#Player
# 
# XBMC functions
#  http://kodi.wiki/view/list_of_built-in_functions
#
# xbmcgui functions
#   http://mirrors.xbmc.org/docs/python-docs/stable/xbmcgui.html

import xbmcaddon
import xbmcgui
import xbmc
import time
import sys
import os
import subprocess as sub

from datetime       import datetime
from KodiSQL        import KodiSQL
from KodiController import KodiController

# Print to a file
def printf(input_value):
  sub.call("echo \"%s\" >> $HOME/.kodi/temp/my_log.txt" % (input_value), shell=True)

# Print to a pop up window
def printd(input_string):
  xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo("name"), str(input_string))

# Sync up time to the given increment
def sleep(input_time=1):
  # Create default variables
  addon_time = int(0)
  sleep_time = float(0)
  input_time = float(input_time)

  # Get the current decimal time
  date       = float(datetime.now().strftime(".%f"))
  
  # If the sleep time is longer then a second compensate for it
  if input_time > 1:
    # Get the seconds by turning the time into a int
    # Then subtract that number from the input time to get the decimal version of the sleep time
    addon_time = int(input_time)
    input_time = input_time - float(addon_time)

  # If the input time is greater then the current date
  if input_time > date:
    # Subtract the decimal time from the current input time
    sleep_time = input_time - date
  else:
    # Else the the remainder of the input time out of the date and subtract it from the input time
    sleep_time = input_time - (date % input_time)

  # Finally sleep that ammount of time + and extra seconds that may have been added
  time.sleep(sleep_time + addon_time)

# Use sql and kodi to sync up the current player to the lead device
def sync_audio(player, kodisql):
  synced     = False
  sleep_time = 1
  while synced is False:
    # Sleep to the standard time
    sleep(sleep_time)
    # Uplad current time and place in the song to the database
    kodisql.set_sync(datetime.now().strftime("%S.%f"), player.get_position())
    # Get the difference in the time stamps between you and the lead device
    difference = kodisql.get_difference()
    # Check if you are synced up
    synced = is_synced(kodisql, difference)
    if not synced:
      # get the difrance between you and the lead device
      sleep(sleep_time)
      player.set_position(float(player.get_position()) + float(difference) - float(0.4))

def is_synced(kodisql, difference):
  result = False
  tolerance = 0.08
  # difference = kodisql.get_difference()
  if difference < tolerance and difference > tolerance * -1:
    result = True
  return result

# Main Function
if __name__ == "__main__":
  # printd(sys.version)
  # Set initial needed information
  song_name = "PHIL_GOOD_-_Sleeping_In.mp3"
  player  = KodiController(song_name)
  kodisql = KodiSQL()
  
  # Set volume to zero untill music is ready to be played
  # xbmc.executebuiltin("XBMC.SetVolume(0)")
  player.set_volume(0)
  volume = 45

  # Sync to the zero and start playing music
  sleep()
  player.play()

  # If you are not lead sync up with the music
  if int(kodisql.get_rank()) > int(0):
    sync_time = kodisql.get_sync(int(datetime.now().strftime("%S")))
    player.set_position(sync_time)
    sync_audio(player, kodisql)

  # Set volume
  player.set_volume(volume)

  # Repoty Player | Correct errors
  while player.is_playing():
    kodisql.set_sync(datetime.now().strftime("%S.%f"), player.get_position())
    sleep()

  player.close_kodi()
