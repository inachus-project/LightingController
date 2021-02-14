# Colors
BLACK = 0x000000
RED = 0x200000
GREEN = 0x002000
BLUE = 0x000020
WHITE = 0x202020

# Brightness
BRIGHT_OFF = 0
BRIGHT_LOW = 0x20
BRIGHT_MED = 0x40
BRIGHT_HIGH = 0x80
BRIGHT_MAX = 0xFF

# Limits
COMPONENT_MIN = 0
COMPONENT_MAX = 0xFF

# Masks
BIT24 = 0xFFFFFF
RED_MASK = 0xFF0000
RED_SHIFT = 16
GREEN_MASK = 0x00FF00
GREEN_SHIFT = 8
BLUE_MASK = 0x0000FF
BLUE_SHIFT = 0
COMPONENT_MAX = 0xFF


class Pixel:

    def __init__(self, initial_color=BLACK):
        """
        Constructor
        :param initial_color: Sets the initial 24 bit color
        """

        self.RGB = initial_color & BIT24

    def getcolor(self):
        """
        Gets the full 24 bit color value
        :return: Color
        """

        return self.RGB

    def setcolor(self, color):
        """
        Sets the full 24 bit color value
        :param color: The 24 bit RGB value
        :return: None
        """

        self.RGB = color & BIT24

    def getred(self):
        """
        Gets the red component of the color
        :return: Red value
        """

        return (self.RGB & RED_MASK) >> RED_SHIFT

    def getgreen(self):
        """
        Gets the green component of the color
        :return: Green value
        """

        return (self.RGB & GREEN_MASK) >> GREEN_SHIFT

    def getblue(self):
        """
        Gets the blue component of the color
        :return: Blue value
        """

        return (self.RGB & BLUE_MASK) >> BLUE_SHIFT

    def setred(self, red_value):
        """
        Sets the red component of the color
        :param red_value: The red component value
        :return: None
        """

        red = COMPONENT_MAX & red_value
        self.RGB &= (RED_MASK ^ BIT24)
        self.RGB |= (red << RED_SHIFT)

    def setgreen(self, green_value):
        """
        Sets the green component of the color
        :param green_value: The green component value
        :return: None
        """

        green = COMPONENT_MAX & green_value
        self.RGB &= (GREEN_MASK ^ BIT24)
        self.RGB |= (green << GREEN_SHIFT)

    def setblue(self, blue_value):
        """
        Sets the green component of the color
        :param blue_value: The green component value
        :return: None
        """

        blue = COMPONENT_MAX & blue_value
        self.RGB &= (BLUE_MASK ^ BIT24)
        self.RGB |= (blue << BLUE_SHIFT)

    def modifyred(self, change):
        """
        Modifies red component by change delta
        :param change: value of change, can be positive or negative
        :return: None
        """

        red = self.getred()
        new_red = red + change

        if new_red < COMPONENT_MIN or new_red > COMPONENT_MAX:

            return

        self.setred(new_red)

    def modifygreen(self, change):
        """
        Modifies green component by change delta
        :param change: value of change, can be positive or negative
        :return: None
        """

        green = self.getgreen()
        new_green = green + change

        if new_green < COMPONENT_MIN or new_green > COMPONENT_MAX:
            return

        self.setgreen(new_green)

    def modifyblue(self, change):
        """
        Modifies blue component by change delta
        :param change: value of change, can be positive or negative
        :return: None
        """

        blue = self.getblue()
        new_blue = blue + change

        if new_blue < COMPONENT_MIN or new_blue > COMPONENT_MAX:
            return

        self.setblue(new_blue)
