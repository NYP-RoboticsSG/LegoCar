#!/usr/bin/env python3
from time import sleep
import cwiid
from PIL.Image import open as imgopen
from PIL.ImageChops import invert

from ev3dev2.motor import Motor, OUTPUT_D ,OUTPUT_B, OUTPUT_C, OUTPUT_A
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.display import Display

def clamp(value, lower, upper):
    return min(upper, max(value, lower))

def damp(value, prevval):
    if value <= prevval - 5 or value >= prevval + 5:
        return value
    else:
        return prevval

sounder = Sound()

nyp_logo = invert(imgopen('nyp.bmp'))

screen = Display()
screen.image.paste(nyp_logo, (4, 23))
screen.update()

w = cwiid.Wiimote()
w.led = 6
w.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN

leds = Leds()
leds.set_color("LEFT", "RED")
leds.set_color("RIGHT", "RED")

colour = ColorSensor(INPUT_4)
colour.mode = 'COL-REFLECT'

left_motor = Motor(OUTPUT_B)
left_motor.reset()
left_motor.run_direct(speed_sp = 1050, ramp_down_sp = 2000, stop_action = 'coast')

right_motor = Motor(OUTPUT_C)
right_motor.reset()
right_motor.run_direct(speed_sp = 1050, ramp_down_sp = 2000, stop_action = 'coast')

mid_motor = Motor(OUTPUT_A)
mid_motor.reset()
mid_motor.run_direct(speed_sp = 1050, ramp_down_sp = 2000, stop_action = 'coast')

arm = Motor(OUTPUT_D)
arm.reset()
arm.run_to_rel_pos(position_sp = 120, speed_sp = 1500, stop_action = 'brake')
sleep(0.5)
arm.reset()
arm.run_to_rel_pos(position_sp = -44, speed_sp = 1500, stop_action = 'brake')
sleep(0.5)
arm.reset()
arm.run_to_abs_pos(position_sp = 0, speed_sp = 1500, stop_action = 'hold')

top_speed = 100
last_btn_state = 0
move = 0
adjust = 0
turn = 0

leds.all_off()
flashing = False

try:
    while True:

        state = w.state
        
        buttons = state['buttons']
        if buttons != last_btn_state:
            if buttons & cwiid.BTN_MINUS:
                top_speed -= 10
                top_speed = clamp(top_speed, 50, 100)
            if buttons & cwiid.BTN_PLUS:
                top_speed += 10
                top_speed = clamp(top_speed, 50, 100)
            if buttons & cwiid.BTN_A and not (buttons & cwiid.BTN_1) and not (buttons & cwiid.BTN_2):
                arm.reset()
                arm.run_to_rel_pos(position_sp = 120, speed_sp = 1500, stop_action = 'brake')
                sleep(0.5)
                arm.reset()
                arm.run_to_rel_pos(position_sp = -44, speed_sp = 1500, stop_action = 'brake')
                sleep(0.5)
                arm.reset()
                arm.run_to_abs_pos(position_sp = 0, speed_sp = 1500, stop_action = 'hold')
            if buttons & cwiid.BTN_HOME:
                sounder.beep(play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            
            if buttons & cwiid.BTN_2:
                move = -1
                colour.mode = 'COL-COLOR'
            elif buttons & cwiid.BTN_1:
                move = 1
                colour.mode = 'COL-AMBIENT'
            else:
                move = 0
                colour.mode = 'COL-REFLECT'
            
            last_btn_state = buttons
        
        if move:
            left_motor.duty_cycle_sp = top_speed * move
            mid_motor.duty_cycle_sp = top_speed * -move
            right_motor.duty_cycle_sp = top_speed * move
        else:
            left_motor.duty_cycle_sp = 0
            mid_motor.duty_cycle_sp = 0
            right_motor.duty_cycle_sp = 0

        acc = state['acc']
        tilt = (clamp(acc[1], 100, 150) - 125 + adjust) / 25.0  # roughly between -1 and 1
        newturn = int(50 * tilt)
        newturn = clamp(newturn, -abs(50), abs(50))
        if damp(newturn,turn) != turn:
            arm.run_to_abs_pos(position_sp = damp(newturn,turn), speed_sp = 600, stop_action = 'hold')
            turn = damp(newturn,turn)
            if turn >= 20 and flashing == False:
                leds.animate_cycle(('ORANGE','BLACK'), groups=['RIGHT'], sleeptime=0.2, duration=None, block=False)
                flashing = True
                #leds.animate_rainbow(group1='RIGHT', group2='RIGHT', increment_by=0.1, sleeptime=0.1, duration=None, block=False)
            elif turn <= -20 and flashing == False:
                leds.animate_cycle(('ORANGE','BLACK'), groups=['LEFT'], sleeptime=0.2, duration=None, block=False)
                flashing = True
                #leds.animate_rainbow(group1='LEFT', group2='LEFT', increment_by=0.1, sleeptime=0.1, duration=None, block=False)
            elif turn < 20 and turn > -20 and flashing == True:
                flashing = False
                leds.animate_stop()
                leds.all_off()

finally:
    left_motor.stop()
    right_motor.stop()
    mid_motor.stop()