import joystick_in
import uinput
import sys

device = '/dev/input/js0'
if len(sys.argv) > 1:
    device = sys.argv[1]

balance_board = joystick_in.BalanceBoard(device)

virtual_joystick = uinput.Device((
    uinput.ABS_X + (0, 0, 0, 0),
    uinput.ABS_Y + (0, 0, 0, 0),
))

while True:
    balance_board.update()
    virtual_joystick.emit(uinput.ABS_X, balance_board.axes[0])
    virtual_joystick.emit(uinput.ABS_Y, balance_board.axes[1])
