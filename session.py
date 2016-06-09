import operator
import os
import subprocess
import signal
from hue_api import HueBridge

# save the pid of the vlc parallel process that play music
PID = 0

# hue light id
LAMP_ID1 = 7
LAMP_ID2 = 8


# compute the mood
def compute_mood(joy, sadness, anger, fear):
    moods = {'joy': joy, 'sadness': sadness, 'anger': anger, 'fear': fear}

    # find the emotion with max value (in a magic way)
    mood1_n = max(moods.iteritems(), key=operator.itemgetter(1))[0]
    mood1_v = max(moods.iteritems(), key=operator.itemgetter(1))[1]

    moods.pop(mood1_n)

    mood2_n = max(moods.iteritems(), key=operator.itemgetter(1))[0]
    mood2_v = max(moods.iteritems(), key=operator.itemgetter(1))[1]

    if (mood1_v - mood2_v) >= 2:
        mood2_n = mood1_n

    final_moods = [mood1_n, mood2_n]

    return final_moods


def compute_img(img_set):
    values = [0, 0, 0, 0]

    # order like the compute_mood, so we don't get confused when we call this function
    # NB: negative index pick the n-th element starting from the end, no need to compute len()
    values[0] = int(img_set[-9])        # joy
    values[1] = int(img_set[-5])        # sadness
    values[2] = int(img_set[-11])       # anger
    values[3] = int(img_set[-7])        # fear

    return values


# play the audio file using vlc cli
def start_playlist(playlist_name):
    # This is for windows
    # win = 'C:\Program Files (x86)\VideoLAN\VLC\VLC.exe --random --loop'

    # This is for mac
    mac = '/Applications/VLC.app/Contents/MacOS/VLC -I rc --random --loop .'

    # This is for linux
    linux = 'cvlc --random --loop'

    # create the string to pass for play music
    command = mac + '/static/music/' + playlist_name + '/*.mp3'

    # create a new process to launch the command
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    global PID
    PID = p.pid


def stop_playlist():
    # stop music playing by kill vlc process using his pid
    # Send the signal to all the process groups (parent -> children)
    os.killpg(os.getpgid(PID), signal.SIGTERM)


def light_on(hue1, hue2):
    # the Hue bridge id
    bridge = HueBridge("http://192.168.0.201/api/newdeveloper")

    # turn on lights
    # light 1
    bridge.change_light_state(LAMP_ID1, 'on')
    # light 2
    bridge.change_light_state(LAMP_ID2, 'on')

    # change color
    # light 1
    bridge.set_hue(LAMP_ID1, hue1)
    # light 2
    bridge.set_hue(LAMP_ID2, hue2)


def light_off():
    # the Hue bridge id
    bridge = HueBridge("http://192.168.0.201/api/newdeveloper")

    # turn off lights
    # light 1
    bridge.change_light_state(LAMP_ID1, 'off')
    # light 2
    bridge.change_light_state(LAMP_ID1, 'off')


if __name__ == '__main__':
    # just some tests
    print 10
