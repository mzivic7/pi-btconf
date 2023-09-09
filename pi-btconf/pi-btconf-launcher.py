from gpiozero import Button
from signal import pause
from datetime import datetime, timedelta
import subprocess

gpio_btn = 3   # launch button gpio pin
hold_s = 5   # seconds to hold button to shutdown device

Button.pressed_time = None   # when the button is pressed
Button.released_time = None   # when the button is released
Button.running = False   # is pi-btconf script running
Button.script = None   # scrpit subprocess object

subprocess.Popen("rfkill block bluetooth", shell=True)  # disable bluetooth at boot

def pressed(btn):
    btn.pressed_time = datetime.now()   # save button pressed time

def released(btn):
    if btn.pressed_time + timedelta(seconds=hold_s) > datetime.now():   # if button is released after less than n seconds
        if btn.released_time:   # if button is already pressed once
            if btn.released_time + timedelta(seconds=0.5) > datetime.now():   # if new time is 0.5s smaller than previous
                if btn.released_time + timedelta(seconds=0.05) < datetime.now():   # if button is not too fast pressed
                    btn.running = not btn.running   # invert script running state
                    if btn.running is True:   # if script is to be running:
                        btn.script = subprocess.Popen(['/usr/bin/python3', '/usr/local/sbin/pi-btconf.py'])   # run script
                    else:   # if script is to be terminated:
                        if btn.script.poll() is None:   # if script is still running:
                            btn.script.terminate()   # terminate script and disable bluetooth
                            subprocess.Popen("rfkill block bluetooth", shell=True)
                        else:   # if script has already been terminated
                            btn.script = subprocess.Popen(['/usr/bin/python3', '/usr/local/sbin/pi-btconf.py'])   # run script again
                            btn.running = True   # set script state to running
                    btn.released_time = None   # save button released time
                else:    # if button is too fast pushed:
                    btn.released_time = datetime.now()   # save button released time
            else:   # if to much time has passed: 
                btn.released_time = datetime.now()   # save button released time
        else:   # if button is not pressed before
            btn.released_time = datetime.now()   # save button released time
    else:   # if button is released after more than n seconds
        subprocess.Popen("shutdown now", shell=True)   # shutdown device


btn = Button(gpio_btn)   # define button object
btn.when_pressed = pressed   # when button is pressed activate function
btn.when_released = released   # when button is pressed activate function

pause()

