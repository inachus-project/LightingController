import time
import falcon

# TODO
# Create rgb class
# Create millenium falcon library

"""

"""

if __name__ == "__main__":

    mf = falcon.MillenniumFalcon("COM4")

    # mf.canyouguess()
    # mf.lighttest()
    # mf.testalllighttypes()

    while True:
        mf.enginekill()
        time.sleep(2)

        mf.startupengines()
        time.sleep(2)
        mf.takingoff()

        mf.losingpower()
        time.sleep(3)

        mf.restartengines()
        time.sleep(4)

        mf.fireeverything()
        time.sleep(5)

        mf.landing()

        # mf.gotohyperspace()
        time.sleep(5)


    """
    sleep_time = 0.1

    main_count = 0
    while True:

        count = 0
        while count < 30:
            con.setpixelcolor(count, con.RED)
            con.updatepixels()
            time.sleep(sleep_time)
            count += 1



        count = 0
        while count < 30:
            con.setpixelcolor(count, con.BLUE)
            con.updatepixels()
            time.sleep(sleep_time)
            count += 1

        # main_count += 1
    """

    """
    ser.baudrate = 115200

    ready = ser.readline()
    print(ready)
    if ready != b"READY\n":
        exit(-1)

    ser.write(b"{INIT:1E,000000}\n")
    print(ser.readline())
    ser.write(b"{UPDATE}\n")
    print(ser.readline())
    ser.write(b"{ENTER_FAST}\n")
    print(ser.readline())

    initialize_colors()

    limit = 0
    while limit < 100:

        count = 29
        while count > 0:

            temp = get_pixel_color(count - 1)
            set_pixel_color(count, temp)

            count -= 1

        if get_pixel_color(0) == RED:

            set_pixel_color(0, GREEN)

        elif get_pixel_color(0) == GREEN:

            set_pixel_color(0, BLUE)

        else:

            set_pixel_color(0, RED)

        display_colors_fast()

        limit += 1

        # time.sleep(0.25)
    """

    """
    red = 0
    green = 0
    blue = 0
    up = True

    while True:

        new_color = hex(red).lstrip("0x").rstrip("L").zfill(2) + hex(green).lstrip("0x").rstrip("L").zfill(2) + hex(blue).lstrip("0x").rstrip("L").zfill(2)
        new_string = "{SET_MANY:0," + new_color + ",1E}\n"
        ser.write(bytes(new_string, encoding="utf8"))
        print(ser.readline())
        ser.write(b"{UPDATE}\n")
        print(ser.readline())

        if red == 255:
            up = False
        if red == 0:
            up = True

        if up:
            red += 1
            blue += 1
            green += 1

        else:
            red -= 1
            green -= 1
            blue -= 1
    """
