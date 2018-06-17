#!/usr/bin/env python
import skywriter
import signal
import json
import sys
import requests
import subprocess

some_value = 0

def to_node(type, message):
    if type == "tap":
        print("play/pause")
        requests.get("http://localhost:5005/Living%20Room/playpause")
    elif type == "gesture" and message == "left":
        print("next")
        requests.get("http://localhost:5005/Living%20Room/next")
    elif type == "gesture" and message == "right":
        print("previous")
        requests.get("http://localhost:5005/Living%20Room/previous")
    elif type == "rotate" and (message == "clockwise" or message == "anticlockwise"):
        volume = str(round(some_value / 100))
        print("volume: " + volume)
        requests.get("http://localhost:5005/Living%20Room/volume/" + volume)

state = requests.get("http://localhost:5005/Living%20Room/state").json()
new_volume = state["volume"]
some_value = new_volume * 100

print("Volume " + str(new_volume) + " fetched from sonos")
print("Ready for input...")

@skywriter.flick()
def flick(start, finish):
    if start == "east" and finish == "west":
        to_node("gesture", "left")
    if start == "west" and finish == "east":
        to_node("gesture", "right")
    if start == "north" and finish == "south":
        to_node("gesture", "down")
    if start == "south" and finish == "north":
        to_node("gesture", "up")

@skywriter.airwheel()
def spinny(delta):
    global some_value
    some_value += delta * 2

    if some_value < 0:
        some_value = 0
    elif some_value > 10000:
        some_value = 10000

    if delta > 0:
        to_node("rotate", "clockwise")
    elif delta < 0:
        to_node("rotate", "anticlockwise")

@skywriter.tap()
def tap(position):
  subprocess.call("xset s activate -display :0", shell = True)
  to_node("tap", position)

signal.pause()
