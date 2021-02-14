import serial


# controller class to manage the neopixels
class LightingController:

    # Constants
    # Serial constants
    BAUDRATE = 115200
    MAXLEDS = 255
    BITS24 = 0xFFFFFF

    # Color constants
    BLACK = 0
    RED = 0x200000
    GREEN = 0x002000
    BLUE = 0x000020
    WHITE = 0x202020

    # Constant commands
    COM_UPDATE = b"{UPDATE}\n"
    COM_UPDATE_FAST = b'U\n'
    COM_RECEIVED = b'COMMAND_RECEIVED\n'
    COM_INVALID = b'COMMAND_INVALID\n'
    COM_ENTER_FAST = b'{ENTER_FAST}\n'
    COM_EXIT_FAST = b'EXIT\n'
    COM_SET_ONE = "SET_ONE"

    def __init__(self, port=None, length=None, color=None):

        # Create pixel buffer
        self.pixel_buffer = self.createpixelbuffer()
        self.record_buffer = self.createpixelbuffer()

        # Create serial port
        self.ser = serial.Serial(baudrate=self.BAUDRATE)

        # Set port value
        self.port = None
        if port is not None:
            self.setport(port)

        # Set length value
        self.length = None
        if length is not None:
            self.setlength(length)

        # Set color value
        self.color = None
        if color is not None:
            self.setcolor(color)

        # Set initial mode
        self.fast_mode = False

    def copytorecordbuffer(self):

        count = 0
        while count < len(self.pixel_buffer):
            self.record_buffer[count] = self.pixel_buffer[count]
            count += 1

    # Creates the list to store pixels colors
    def createpixelbuffer(self):

        new_list = []
        count = 0
        while count < self.MAXLEDS:

            new_list.append(self.BLACK)
            count += 1

        return new_list

    # Sets a pixel to a new color
    def setpixelcolor(self, pixel, color):

        if pixel >= self.length:
            return

        color = color & self.BITS24
        self.pixel_buffer[pixel] = color

    # Sends updated buffer and shows all pixels
    def updatepixels(self):

        if self.fast_mode:

            self.updatepixelsfast()

        else:

            self.updatepixelsslow()

    # Update the pixels in fast mode
    def updatepixelsfast(self):

        count = 0
        while count < self.length:

            # Create and send command if pixel changed
            if self.pixel_buffer[count] != self.record_buffer[count]:
                pixel_command = self.create_command_fast(count, self.pixel_buffer[count])
                self.ser.write(pixel_command)

            count += 1

        self.showneopixels()
        self.copytorecordbuffer()

    # Updates the pixels in slow mode
    def updatepixelsslow(self):

        count = 0
        while count < self.length:

            # Create and send command if pixel changed
            if self.pixel_buffer[count] != self.record_buffer[count]:
                pixel_command = self.create_command(self.COM_SET_ONE, [count, self.pixel_buffer[count]])
                self.sendslowcommand(pixel_command)

            count += 1

        self.showneopixels()
        self.copytorecordbuffer()

    # Sends command to update neopixels
    def showneopixels(self):

        if self.fast_mode:

            self.showneopixelsfast()

        else:

            self.showneopixelsslow()

    # Sends update command in slow mode
    def showneopixelsslow(self):

        new_command = self.COM_UPDATE
        self.sendslowcommand(new_command)

    # Sends update command in fast mode
    def showneopixelsfast(self):

        self.ser.write(self.COM_UPDATE_FAST)

    # Sends a command in slow mode
    def sendslowcommand(self, command):

        self.ser.write(command)
        result = self.ser.readline()
        if result == self.COM_RECEIVED:
            return True
        else:
            return False

    def enablefastmode(self, fast_mode=False):

        # Check if already in mode
        if fast_mode and self.fast_mode:

            return

        elif not fast_mode and not self.fast_mode:

            return

        # Change mode
        if fast_mode:
            self.sendslowcommand(self.COM_ENTER_FAST)

        else:
            self.sendslowcommand(self.COM_EXIT_FAST)

        # Update mode
        self.fast_mode = fast_mode

    # Creates a pixel color change command for fast mode
    def create_command_fast(self, command, param):

        new_command = ""
        new_command += self.createhexvalue(command, 2) + ":"
        new_command += self.createhexvalue(param, 6) + "\n"
        return bytes(new_command, encoding="utf8")

    # Creates and formats a new command to send
    def create_command(self, command, param_list=None):

        # Start with command
        new_command = "{"
        new_command += command

        if len(param_list) > 0:
            new_command += ":"

        # Handle parameters
        for p in param_list:

            new_command += self.createhexvalue(p, 6) + ","

        new_command.rstrip(",")
        new_command += "}\n"

        # Return command
        return bytes(new_command, encoding="utf8")


    # Sets the serial port
    def setport(self, port):

        self.port = port

    # Sets the number of neopixels
    def setlength(self, length):

        if length > self.MAXLEDS:
            length = self.MAXLEDS

        self.length = length

    # Sets initial color
    def setcolor(self, color):

        self.color = (self.BITS24 & color)

    # Closes the serial port
    def end(self):

        self.ser.close()

    # Starts communication and shows the initial color
    def begin(self, autodetect=False):

        # Validate user settings
        if self.length is None:
            return False

        # Autodetect if necessary
        if autodetect:

            if not self.autodetectport():

                return False

        # Open with user specified settings
        else:

            # Validate user settings
            if self.port is None:

                return False

            # Open port
            self.ser.port = self.port
            self.ser.open()

            # Check port
            result = self.ser.readline()
            if result == "READY\n":

                self.ser.close()
                return False

        # Set color if necessary
        if self.color is None:
            self.color = self.BLACK

        # Send length
        init_command = "{INIT:"
        init_command += self.createhexvalue(self.length, 2)
        init_command += ","
        init_command += self.createhexvalue(self.color, 6)
        init_command += "}\n"

        self.ser.write(bytes(init_command, encoding="utf8"))
        result = self.ser.readline()
        if result != self.COM_RECEIVED:
            self.ser.close()
            return False

        # Update the pixels
        self.ser.write(self.COM_UPDATE)
        result = self.ser.readline()
        if result != self.COM_RECEIVED:
            self.ser.close()
            return False

        # Success
        return True

    # Converts a hex value to strength
    def createhexvalue(self, number, characters):

        return hex(number).lstrip("0x").rstrip("L").zfill(characters).upper()

    # Tries to autodetect the port
    def autodetectport(self):

        # Loop through all serial ports to find the correct one
        count = 1
        detected = False
        while count < 256:

            # Set attempt variables
            self.ser.setPort("COM" + str(count))
            self.ser.timeout = 3

            # Try to open the port
            try:
                self.ser.open()

            except serial.SerialException:
                self.ser.close()
                continue

            # Port found, check if correct
            result = self.ser.readline()

            if result == "READY\n":
                detected = True
                self.ser.close()
                break

            count += 1

        # Didn't find the port
        if not detected:
            return False

        # Success
        return True

