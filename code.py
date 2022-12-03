import time
from adafruit_magtag.magtag import MagTag
from adafruit_slideshow import PlayBackOrder, SlideShow, PlayBackDirection
# import board


class Subscriber_Magtag: #subs class for Magtag2.9

    def __init__(self, img_nn, max_lim=10000): #init of data pts

        self.reception_delay=180 #s

        self.magtag=None

        self.red = 0x880000
        self.green = 0x008800
        self.blue = 0x000088
        self.yellow = 0x884400
        self.cyan = 0x0088BB
        self.magenta = 0x9900BB
        self.white = 0x888888

        self.brightness_mgtg=0.2
        self.max_limit=max_lim #g
        self.image_name=img_nn

        self.time_quanta=0.006 #6


    def light_on(self, color): #light all 4 neopixels to color
        
        self.magtag.peripherals.neopixels.brightness = 0.1
        self.magtag.peripherals.neopixel_disable = False
        self.magtag.peripherals.neopixels.fill(color)

        pass


    def light_off(self):
        
        self.magtag.peripherals.neopixel_disable = True


    def light_condition(self, weight_data):

        if 0<=weight_data<self.max_limit/7:
            self.light_on(self.red)

        elif self.max_limit/7<=weight_data<(2*self.max_limit)/7:
            self.light_on(self.yellow)

        elif (2*self.max_limit)/7<=weight_data<(3*self.max_limit)/7:
            self.light_on(self.green)

        elif (3*self.max_limit)/7<=weight_data<(4*self.max_limit)/7:
            self.light_on(self.cyan)

        elif (4*self.max_limit)/7<=weight_data<(5*self.max_limit)/7:
            self.light_on(self.blue)

        elif (5*self.max_limit)/7<=weight_data<(6*self.max_limit)/7:
            self.light_on(self.magenta)

        elif (6*self.max_limit)/7<=weight_data<=(self.max_limit):
            self.light_on(self.white) #simple, all same color, level indicator 

        print("NeoPixels Activated.")

        pass


    # def try_refresh(self):
    #     try:
    #         board.DISPLAY.refresh()
    #     except RuntimeError as too_soon_error:
    #         # catch refresh too soon
    #         time.sleep(2)
    #         board.DISPLAY.refresh()

 
    def main(self): #main run

        self.magtag=MagTag()
        timestamp = time.monotonic()
        sound_toggle = False  # state of sound feedback
        autoplay_toggle = False  # state of autoplay
        auto_pause = 60  # time between slides in auto mode

        # Create the slideshow object that plays through alphabetically.
        slideshow = SlideShow(
            self.magtag.graphics.display,
            None,
            auto_advance=autoplay_toggle,
            folder="/slides",
            loop=True,
            order=PlayBackOrder.ALPHABETICAL,
            dwell=auto_pause,
        )

        weight_data = 3000

        while True:
            if self.magtag.peripherals.button_c_pressed:
                if self.magtag.peripherals.neopixel_disable:
                    self.light_condition(weight_data)
                else:
                    self.light_off()
            slideshow.update()
            if self.magtag.peripherals.button_a_pressed:
                slideshow.direction = PlayBackDirection.BACKWARD
                time.sleep(5)
                slideshow.advance()

            if self.magtag.peripherals.button_d_pressed:
                slideshow.direction = PlayBackDirection.FORWARD
                time.sleep(5)
                slideshow.advance()
            #time.sleep(1) #remove? 

        # while True:
        #     self.light_condition(weight_data)
        #     # self.try_refresh()
        #     weight_data += self.max_limit/7  #showcase: loop through each case ascendingly
        #     if weight_data >= self.max_limit*8/7:
        #         weight_data = 0
        #     time.sleep(2.0)
        #     pass

if __name__ == "__main__": #runs full class

    image_inst="barcode_prod1_test"
    subm=Subscriber_Magtag(image_inst)
    subm.main()

    #end





