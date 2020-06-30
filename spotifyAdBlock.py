import win32gui
import win32api
import win32process
import os
import time
import psutil
from dataclasses import dataclass

###Virtual-KeyCodes###
Media_Next = 0xB0
Media_Previous = 0xB1
Media_Pause = 0xB3 ##Play/Pause
Media_Mute = 0xAD

@dataclass
class SpotifyInfo:
	hwnd: int = 0
	path: str = ""
	song_info: str = ""
	
def getSpotifyInfo():
	def window_enumeration_handler(hwnd, top_windows):
		"""Add window title and ID to array."""
		top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

	top_windows = []
	win32gui.EnumWindows(window_enumeration_handler, top_windows)

	substring_list = ["spotify", "-", "advertisement"]

	for top_window in top_windows:
		window_text = top_window[1]
		hwnd = top_window[0]
		pid = win32process.GetWindowThreadProcessId(hwnd)
		path = psutil.Process(pid[1]).exe()

		if (any(substring in window_text.lower() for substring in substring_list)):
			if("Spotify" in path):
				spotifyInfo = SpotifyInfo()
				spotifyInfo.hwnd = hwnd
				spotifyInfo.song_info = window_text
				spotifyInfo.path = path
				#print(spotifyInfo.hwnd)
				#print(spotifyInfo.song_info)
				#print(spotifyInfo.path)
				return spotifyInfo

def getwindow():
	spotifyInfo = getSpotifyInfo()
	window_id = spotifyInfo.hwnd
	return window_id
	
def get_window_text():
	try:
		spotifyInfo = getSpotifyInfo()
		window_text = spotifyInfo.song_info
	except:
		return "window text not found"
	return window_text

def artist():
	try:
		temp = get_window_text()
		artist, song = temp.split(" - ",1)
		artist = artist.strip()
		return artist
	except:
		return "There is nothing playing at this moment"
	
def song():
	try:
		temp = get_window_text()
		artist, song = temp.split(" - ",1)
		song = song.strip()
		return song
	except:
		return "There is nothing playing at this moment"
	
###SpotifyBlock###
def createfolder(folder_path="C:\SpotiBlock"):
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	else:
		pass
	
def createfile(file_path="C:\SpotiBlock\Block.txt" ):
	if not os.path.exists(file_path):
		file = open(file_path, "a")
		file.write("ThisFirstLineWillBeIgnoredButIsNecessaryForUse")

def blocklist(file_path="C:\SpotiBlock\Block.txt"):
	block_list = []
	for line in open(file_path, "r"):
		if not line == "":
			block_list.append(line.strip())
	return block_list
	
def add_to_blocklist(file_path="C:\SpotiBlock\Block.txt"):
	with open(file_path, 'a') as text_file:
		text_file.write("\n" + get_window_text())
		
def reset_blocklist(file_path="C:\SpotiBlock\Block.txt"):
	with open(file_path, 'w') as text_file:
		text_file.write("ThisFirstLineWillBeIgnored")
		pass

def restart_spotify():
	spotifyInfo = getSpotifyInfo()
	os.system("TASKKILL /F /IM Spotify.exe")
	os.startfile(spotifyInfo.path)
	counter = 0
	while get_window_text() != "Spotify Free" and counter < 100:
		time.sleep(0.05)
		counter += 1
	next()


###Media Controls###
def hwcode(Media):
	hwcode = win32api.MapVirtualKey(Media, 0)
	return hwcode

def next():
	win32api.keybd_event(Media_Next, hwcode(Media_Next))
	
def previous():
	win32api.keybd_event(Media_Previous, hwcode(Media_Previous))
	
def pause():
	win32api.keybd_event(Media_Pause, hwcode(Media_Pause))
	
def play():
	win32api.keybd_event(Media_Pause, hwcode(Media_Pause))
	
def mute():
	win32api.keybd_event(Media_Mute, hwcode(Media_Mute))


while True:
	current_song_info = get_window_text()
	print(current_song_info)
	ad_list = ["spotify", "advertisement"]
	if(current_song_info.lower() in ad_list):
		print("restarting spotify")
		restart_spotify()
	time.sleep(0.5)