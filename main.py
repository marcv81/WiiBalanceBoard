import joystick_in
import uinput
import sys
import vpython

# VPython scene

vpython.scene.range = 1.5
vpython.scene.userspin = False
vpython.scene.userzoom = False

center = vpython.sphere(
    pos=vpython.vector(0, 0, 0),
    radius=0.05,
    color=vpython.color.green)
sphere = vpython.sphere(
    pos=vpython.vector(0, 0, 0),
    radius=0.1)
label = vpython.label(height=36, box=False, yoffset=25)

# Virtual joystick

device = '/dev/input/js0'
if len(sys.argv) > 1:
    device = sys.argv[1]

balance_board = joystick_in.BalanceBoard(device)

virtual_joystick = uinput.Device((
    uinput.ABS_X + (0, 0, 0, 0),
    uinput.ABS_Y + (0, 0, 0, 0),
))

while True:
    vpython.rate(60)
    balance_board.update()

    # Update VPython scene

    x = balance_board.axes[0] / 32767.0
    y = balance_board.axes[1] / -32767.0
    w = balance_board.axes[2] / 100.0
    sphere.pos = vpython.vector(x, y, 0)
    label.pos = sphere.pos
    label.text = text='%.2f, %.2f, %.1f kg' % (x, y, w)

    # Update virtual joystick

    virtual_joystick.emit(uinput.ABS_X, balance_board.axes[0])
    virtual_joystick.emit(uinput.ABS_Y, balance_board.axes[1])
