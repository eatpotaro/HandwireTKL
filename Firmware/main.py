#show starting of device
print("Hello World!")

#import libraries
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.keys import Key

from kmk.modules.layers import Layers

from kmk.extensions.international import International
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

import board
import busio

import random

from kmk.extensions.display import Display, TextEntry, ImageEntry

from boid import Ball, Boid

#for display from example
# For SSD1306
from kmk.extensions.display.ssd1306 import SSD1306

# Replace SCL and SDA according to your hardware configuration.
i2c_bus = busio.I2C(board.GP1, board.GP0)

driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,
)

# setup a new keyboard object with an updateloop
class UpdateKeyboard(KMKKeyboard):
    def __init__(self) -> None:
        super().__init__()
        
    def _main_loop(self) -> None:
        super()._main_loop()
        updateDisplay()
        
keyboard = UpdateKeyboard()

#add extras
keyboard.extensions.append(International())
keyboard.extensions.append(MediaKeys())
layers = Layers()
keyboard.modules.append(layers)

#setup encoder
encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP27, board.GP28, None, False, 4),)
encoder_handler.map = [ ((KC.VOLD, KC.VOLU, KC.NO),), ]
keyboard.modules.append(encoder_handler)

#setup keymap
keyboard.col_pins = (board.GP8,board.GP9,board.GP10,board.GP11,board.GP12,board.GP13,board.GP14,board.GP15,board.GP16,board.GP17,board.GP18,board.GP19,board.GP20,board.GP21,board.GP22,board.GP26,)
keyboard.row_pins = (board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP7,)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

#setup readers so can call change states based on keypressed e.g. capslock
isCaps = False
    
class CapsReader(Key):
    def on_press(self, key: Key, is_pressed: bool):
        global isCaps
        isCaps = not isCaps

KC.CAPS = CapsReader()

keyboard.keymap = [[
KC.LCTL, KC.LGUI, KC.LALT, KC.NO, KC.NO, KC.NO,KC.SPC, KC.NO, KC.NO, KC.NO, KC.RALT, KC.MO(2),KC.MO(2), KC.RCTL, KC.LEFT, KC.DOWN,
KC.LSFT, KC.NONUS_BSLASH, KC.Z, KC.X, KC.C, KC.V,KC.B, KC.N, KC.M, KC.COMM, KC.DOT, KC.SLSH,KC.RSFT, KC.NO, KC.UP, KC.RIGHT,
KC.CAPS, KC.A, KC.S, KC.D, KC.F, KC.G,KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT,KC.NONUS_HASH, KC.ENT, KC.END, KC.NO,
KC.TAB, KC.Q, KC.W, KC.E, KC.R, KC.T,KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRC,KC.RBRC, KC.NO, KC.DEL, KC.PGDN,
KC.GRV, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.MINS,KC.EQL, KC.BSPC, KC.HOME, KC.PGUP,
KC.ESC, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5,KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.F11,KC.F12, KC.NO, KC.INS, KC.PGUP, 
]]

#setup display       
# For all display types
display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    brightness=0.8, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    dim_time=200, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=600, # time in seconds to turn off screen
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)

#create list of boids
boids = [Boid(64, 16, 1.2, i/2, True) for i in range(0, 12)]
#boids = [Boid(50, 10, 0.1, 0), Boid(50, 20, 0.1, 0)]

def updateDisplay():
    global display, boids
    
    for boid in boids:
        boid.updatePos(boids)
    
    if(isCaps):                                                                                                                                                                                                                    
        display.entries = [TextEntry(text="CAPS ON!", x=0, y=0),]
    else:
        if(len(display.entries) != len(boids)):
            display.entries = []
            for boid in boids:
                display.entries.append(ImageEntry(image="ball.bmp", x=boid.getXPosInt(), y=boid.getYPosInt()),)
                
        for i in range(len(boids)):
            display.entries[i].x = int(boids[i].getXPosInt())
            display.entries[i].y = int(boids[i].getYPosInt())
            
    display.render(keyboard.active_layers[-1])

keyboard.extensions.append(display)

if __name__ == '__main__':
    keyboard.go()