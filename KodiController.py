# Running in python 3.5.2


# Controller for kodi

import xbmcaddon
import xbmcgui
import xbmc
import os

class KodiController:
  def __init__(self, input_song):
    self.player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
    self.paused = False
    self.nas_location = "/mnt/nas_music"
    self.song_name    = input_song
    self.volume       = str(0)

  # Play the audio
  def play(self):
    if self.paused is True:
      self.player.pause()
      self.paused = False
    else:
      self.player.play(os.path.join(self.nas_location, self.song_name))

  # Pause the audio
  def pause(self):
    if self.paused is False:
      self.player.pause()
      self.paused = True

  # Get song position
  def get_position(self):
    return self.player.getTime()

  def set_position(self, input_position):
    self.player.seekTime(float(input_position))

  # Set the volume of the player
  def set_volume(self, input_volume):
    self.volume = str(input_volume)
    xbmc.executebuiltin("XBMC.SetVolume(%s)" % str(input_volume))

  def is_playing(self):
    return self.player.isPlaying()

  def close_kodi(self):
    xbmc.executebuiltin("XBMC.Quit()")  

# Methods to add
  # get_song_queue
  # get_current_song
  # get_song_info
  # full controlls (play, pause, skip, rewind, etc...)
