from gpiozero import Button
from signal import pause
from datetime import datetime, timedelta
import subprocess

gpio_btn = 3   # launch button

Button.pressed_time = None   # when the button is pressed
Button.running = False   # is pi-btconf script running
Button.script = None   # scrpit subprocess object

def pressed(btn):
    if btn.pressed_time:   # if button is already pressed once
        if btn.pressed_time + timedelta(seconds=0.5) > datetime.now():   # if new time is 0.5s greater than previous
            if btn.pressed_time + timedelta(seconds=0.05) < datetime.now():   # if button is not too fast pushed
                btn.running = not btn.running   # invert script running state
                if btn.running is True:   # if script is to be running:
                    btn.script = subprocess.Popen(['python3', 'pi-btconf.py'])   # run script
                else:   # if script is to be terminated:
                    if btn.script.poll() is None:   # if script is still running:
                        btn.script.terminate()   # terminate script and disable bluetooth
                        subprocess.Popen(["rfkill", "block", "bluetooth"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:   # if script has already been terminated
                        btn.script = subprocess.Popen(['python3', 'pi-btconf.py'])   # run script again
                        btn.running = True   # set script state to running
                btn.pressed_time = None   # save button pressed time
            else:    # if button is too fast pushed:
                btn.pressed_time = datetime.now()   # save button pressed time
        else:   # if to much time has passed: 
            btn.pressed_time = datetime.now()   # save button pressed time
    else:   # if button is not pressed
        btn.pressed_time = datetime.now()   # save button pressed time


btn = Button(gpio_btn)   # define button object
btn.when_pressed = pressed   # when button is pressed activate function

pause()
