import time                              # import so we can sleep
# import board                             # get the info of the board we're using
# import busio							 # serial protocols
# import digitalio                         # we are using digital inputs 
import argparse                          # for osc messages
import random                            # for testing
from pythonosc import udp_client         # for osc messages
from pythonosc import osc_message_builder

# define the number of toggles
numToggles = 25

itsTime = 10 # change the numbers after 10 seconds
lastTime = 0 # last time we changed the numbers

# function so we don't have to run 4 lines of code for each input setup
# def toggle_register(pin):
# 	tog = digitalio.DigitalInOut(pin)
# 	tog.direction = digitalio.Direction.INPUT
# 	tog.pull = digitalio.Pull.UP
# 	return tog

# create a list of toggles and a list of pins
toggles = []
pins = []

# name the lists, ie toggle2, toggle3 and board.D2, board.D3, etc
def newNums():
    for i in range(numToggles):
	    #toggles.append("toggle" + str(i + 2)) # add 2 to the index so toggle num matches pin num
	    toggles.append(random.random())
	    #pins.append("board.D" + str(i + 2))   # add 2 to the index because we aren't using pins 0 or 1
    
    print(toggles)

newNums()

#print(toggles) 	# print our list of toggle names
#print(pins)     # print our list of pin names

# for each toggle, run our toggle_register function and set the pins to inputs with pullups activated
# for i in range(numToggles):
# 	toggles[i] = toggle_register(eval(pins[i]))

# illustration of part of what we avoided with the above function and loops
# set pins 0 to 24 as inputs with pullup resistor enabled
# toggle0 = toggle_register(board.D0)
# toggle1 = toggle_register(board.D1)
# toggle2 = toggle_register(board.D2)
# toggle3 = toggle_register(board.D3)
# toggle4 = toggle_register(board.D4)
# toggle5 = toggle_register(board.D5)
# toggle6 = toggle_register(board.D6)
# toggle7 = toggle_register(board.D7)
# toggle8 = toggle_register(board.D8)
# toggle9 = toggle_register(board.D9)
# toggle10 = toggle_register(board.D10)
# toggle11 = toggle_register(board.D11)
# toggle12 = toggle_register(board.D12)
# toggle13 = toggle_register(board.D13)
# toggle14 = toggle_register(board.D14)
# toggle15 = toggle_register(board.D15)
# toggle16 = toggle_register(board.D16)
# toggle17 = toggle_register(board.D17)
# toggle18 = toggle_register(board.D18)
# toggle19 = toggle_register(board.D19)
# toggle20 = toggle_register(board.D20)
# toggle21 = toggle_register(board.D21)
# toggle22 = toggle_register(board.D22)
# toggle23 = toggle_register(board.D23)
# toggle24 = toggle_register(board.D24)

# setup for OSC library
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="the ip of the osc server") # ip is localhost (this computer)
parser.add_argument("--port", type=int, default = 5005, help="the port the osc server is listening on") # port is 5005, must match in pd
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)



while True:
    now = time.monotonic()

	# loop through the number of toggles
    for i in range(numToggles):
        client.send_message("/toggle", i+2) # send a message for each toggle
        # if toggles[i].value == False:       # if the reading is 0 (ie, the toggle is ON, because we have pullUPs)
        if toggles[i] < 0.25:
            client.send_message("/on", 1)   # send a 1
        else:							    # otherwise
            client.send_message("/on", 0)   # send a 0
    if now > itsTime + lastTime:
        toggles.clear()
        newNums()
        lastTime = now
    time.sleep(0.05)