import lightingController as lc
import RGB
import time
from datetime import datetime

# Constants
ENGINE_LOWER = 1
ENGINE_UPPER = 10
STRIP_LENGTH = 30

# Engine color constants
ENGINE_NORMAL = 0x202040
MID_DEATH = 0x202010
ROUGH_START = 0x404000
HYPERSPACE = 0xFFFF40

class Neopixel(RGB.Pixel):

    def __init__(self, index, color=RGB.BLACK):
        """
        Constructor
        :param index: The index of the neopixel
        """
        super(Neopixel, self).__init__(initial_color=color)

        self.index = index

    def setindex(self, index):
        """
        Set the index of the pixel
        :param index: index
        :return: None
        """

        if index < 0:
            return

        self.index = index

    def getindex(self):
        """
        Get the index of the pixel
        :return: index
        """

        return self.index

# Falcon class
class MillenniumFalcon:

    def __init__(self, port):
        """
        Constructor
        :param port: The serial port string
        """

        # Lighting controller
        self.con = lc.LightingController(port=port, length=STRIP_LENGTH, color=RGB.BLACK)
        self.con.begin()
        self.con.enablefastmode(fast_mode=True)

        # Create neopixels
        self.pixel_list = self.createlights()

        # Create engine indexes
        self.enginelist = self.createengineindexes()

    def lighttest(self):
        """
        Runs a test of all the lights
        :return: Does not return
        """

        while True:

            # Go full red
            main_count = 0
            sleep_time = 0.005
            while main_count <= 0xFF:

                self.setallcolor(main_count << 16)

                self.updatelights()
                time.sleep(sleep_time)
                main_count += 1

            # Taper off red
            main_count = 0xFF
            sleep_time = 0.005
            while main_count >= 0:
                self.setallcolor(main_count << 16)

                self.updatelights()
                time.sleep(sleep_time)
                main_count -= 1

            # Go full green
            main_count = 0
            sleep_time = 0.005
            while main_count <= 0xFF:
                self.setallcolor(main_count << 8)

                self.updatelights()
                time.sleep(sleep_time)
                main_count += 1

            # Taper off green
            main_count = 0xFF
            sleep_time = 0.005
            while main_count >= 0:
                self.setallcolor(main_count << 8)

                self.updatelights()
                time.sleep(sleep_time)
                main_count -= 1

            # Go full blue
            main_count = 0
            sleep_time = 0.005
            while main_count <= 0xFF:
                self.setallcolor(main_count)

                self.updatelights()
                time.sleep(sleep_time)
                main_count += 1

            # Taper off blue
            main_count = 0xFF
            sleep_time = 0.005
            while main_count >= 0:
                self.setallcolor(main_count)

                self.updatelights()
                time.sleep(sleep_time)
                main_count -= 1


    def startupengines(self):
        """
        Runs the startup engines simulation
        :return: None
        """

        main_count = 0
        sleep_time = 0.05
        while main_count < 0x40:

            self.setenginecolor(main_count)

            self.updatelights()
            time.sleep(sleep_time)
            main_count += 1

        main_count = 0
        while main_count < 0x2020:

            self.setenginecolor((main_count << 8) + 0x40)

            self.updatelights()
            time.sleep(sleep_time)
            main_count += 0x101

    def enginekill(self):
        """
        Runs the kill engines simulation
        :return: None
        """
        self.setenginecolor(RGB.BLACK)

        self.updatelights()

    def restartengines(self):
        """
        Run the restart engines simulation
        :return: None
        """

        time_off = 0.25
        while time_off > 0.0:
            self.engineflash(ROUGH_START, number_flashes=1, time_off=time_off, time_on=0.30 - time_off)
            time_off -= 0.05

        sleep_time = 0.05
        current_color = RGB.Pixel(initial_color=ROUGH_START)
        while current_color.getcolor() != ENGINE_NORMAL:

            current_color.modifyred(-1)
            current_color.modifygreen(-1)
            current_color.modifyblue(2)

            # Update the color
            self.setenginecolor(current_color.getcolor())

            self.updatelights()
            time.sleep(sleep_time)

        # Make sure engine is normal
        self.setenginecolor(ENGINE_NORMAL)

        self.updatelights()

    def gotohyperspace(self):
        """
        Run go to hyperspace simulation
        :return: None
        """

        # Go to hyperspace color
        main_count = 0x20
        current_color = RGB.Pixel(ENGINE_NORMAL)
        sleep_time = 0.005
        while main_count < 0xFF:

            current_color.modifyred(1)
            current_color.modifygreen(1)
            self.setenginecolor(current_color.getcolor())
            self.updatelights()
            time.sleep(sleep_time)
            main_count += 0x1

        time.sleep(1)

        # Vanish into the distance
        main_count = 0x40
        current_color = RGB.Pixel(HYPERSPACE)
        sleep_time = 0.01
        while main_count >= 0:

            self.setenginecolor(current_color.getcolor())

            self.updatelights()
            time.sleep(sleep_time)
            main_count -= 0x1

        self.setenginecolor(RGB.BLACK)

        self.updatelights()

    def losingpower(self):
        """
        Runs the losing power simulation
        :return: None
        """

        self.engineflash(ENGINE_NORMAL)
        count = 0.25
        while count < 0.40:
            self.engineflash(MID_DEATH, number_flashes=1, time_off=count, time_on=0.075)
            count += 0.05

        self.setenginecolor(RGB.BLACK)
        self.updatelights()

    def canyouguess(self):

        up = True
        current_light = ENGINE_LOWER
        while True:

            # Set the new light
            if up:

                current_light += 1

            else:

                current_light -= 1

            # Check bounds
            if up and current_light == ENGINE_UPPER:

                up = False

            elif not up and current_light == ENGINE_LOWER:

                up = True

            # Update colors
            count = ENGINE_LOWER
            while count <= ENGINE_UPPER:

                if count == current_light:
                    self.con.setpixelcolor(count, RGB.RED)

                else:
                    self.con.setpixelcolor(count, RGB.BLACK)

                count += 1

            self.con.updatepixels()

            time.sleep(0.1)

    def engineflash(self, on_color, number_flashes=2, time_off=0.1, time_on=0.1):
        """
        Flashes the engines
        :param number_flashes: Number of times the engines turn off and then back on
        :param time_off: Time the engine is off
        :param time_on: Time the ending is on between flashes
        :return: None
        """

        starting_color = on_color
        main_count = 0
        while main_count < number_flashes:

            # Turn engine off
            self.setenginecolor(RGB.BLACK)

            self.updatelights()
            time.sleep(time_off)

            # Turn engine on
            self.setenginecolor(starting_color)

            self.updatelights()
            time.sleep(time_on)
            main_count += 1

    def createlights(self):
        """
        Create the list of neopixels for the falcon
        :return: List of Neopixel objects
        """

        new_list = []
        count = 0
        while count < STRIP_LENGTH:

            new_list.append(Neopixel(count, color=RGB.BLACK))
            count += 1

        return new_list

    def createengineindexes(self):
        """
        Creates a list of indexes for engine pixels
        :return: The list of indexes
        """

        new_list = []
        count = ENGINE_LOWER
        while count <= ENGINE_UPPER:
            new_list.append(count)
            count += 1

        return new_list

    def setenginecolor(self, color):
        """
        Sets the color of the engines
        :param color: Engine color
        :return: None
        """

        for p in self.pixel_list:

            if p.getindex() in self.enginelist:

                p.setcolor(color)

    def setallcolor(self, color):
        """
        Sets the color of all the lights
        :param color: color
        :return: None
        """

        for p in self.pixel_list:

            p.setcolor(color)

    def updatelights(self):
        """
        Updates the lights to the new colors
        :return: None
        """

        for p in self.pixel_list:
            self.con.setpixelcolor(p.getindex(), p.getcolor())

        self.con.updatepixels()
