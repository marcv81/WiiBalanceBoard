import array
import struct
import fcntl
import select

class Generic:

    JS_EVENT_BUTTON = 0x01
    JS_EVENT_AXIS = 0x02

    JSIOCGBUTTONS = 0x80016a12
    JSIOCGAXES = 0x80016a11

    def __init__(self, device):
        self.device = open(device, 'rb', 0)
        self.buttons = [0] * self.get_buttons_count()
        self.axes = [0] * self.get_axes_count()

    def get_buttons_count(self):
        buffer = array.array('B', [0])
        fcntl.ioctl(self.device, self.JSIOCGBUTTONS, buffer)
        return buffer[0]

    def get_axes_count(self):
        buffer = array.array('B', [0])
        fcntl.ioctl(self.device, self.JSIOCGAXES, buffer)
        return buffer[0]

    def update(self):
        while self.device in select.select([self.device], [], [], 0)[0]:
            event = self.device.read(8)
            e_time, e_value, e_type, e_number = struct.unpack('IhBB', event)
            if e_type & self.JS_EVENT_BUTTON:
                self.buttons[e_number] = e_value
            if e_type & self.JS_EVENT_AXIS:
                self.axes[e_number] = e_value

class BalanceBoard:

    THRESHOLD = 2500 # 25kg

    def __init__(self, device):
        self.joystick = Generic(device)
        self.buttons = []
        self.axes = [0, 0, 0]

    def update(self):
        self.joystick.update()

        # Raw axes
        up_right = self.joystick.axes[0] + 32767
        down_right = self.joystick.axes[1] + 32767
        up_left = self.joystick.axes[2] + 32767
        down_left = self.joystick.axes[3] + 32767

        # Mixed axes
        horizontal = (up_right + down_right) - (up_left + down_left)
        vertical = (down_right + down_left) - (up_right + up_left)
        total = up_right + down_right + up_left + down_left

        # Scaled axes when loaded
        if total > self.THRESHOLD:
            self.axes[0] = 32767 * horizontal // total
            self.axes[1] = 32767 * vertical // total

        # Zeroed axes otherwise
        else:
            self.axes[0] = 0
            self.axes[1] = 0

        self.axes[2] = total
