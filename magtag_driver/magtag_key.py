from time import sleep
from PIL import Image 

import displayio #only rpi4 downloads
from adafruit_magtag.magtag import MagTag
import board

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

        self.brightness_mgtg=0.5
        self.max_limit=max_lim #g
        self.image_name=img_nn

        self.time_quanta=0.006 #6

    def light_up(self, color): #light all 4 neopixels to color

        self.magtag.peripherals.neopixel_disable = False
        self.magtag.peripherals.neopixels.fill(color)

        pass

    def jpg_to_bmp(self, filename): #jpg or jpg or jpeg to bitmap conversion

        file_in="barcode_imgs/"+filename+".jpg"
        img=Image.open(file_in)

        file_out="{}.bmp".format(filename)
        img.save("barcode_bitmaps/{}".format(file_out))

        print("Image converted to Bitmap.")

        pass

    def load_image(self, img_name): #loadimage to magtag

        board.DISPLAY.brightness = 0
        splash = displayio.Group()
        board.DISPLAY.show(splash)

        odb = displayio.OnDiskBitmap('barcode_bitmaps/{}.bmp'.format(img_name))
        face = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        splash.append(face)

        board.DISPLAY.refresh(target_frames_per_second=60)

        board.DISPLAY.brightness = self.brightness_mgtg
        sleep(self.time_quanta)

        print("Image loaded to Matgag 2.9.")

        pass

    def light_condition(self, weight_data):

        if 0<=weight_data<self.max_limit/7:
            self.light_up(self.red)

        elif self.max_limit/7<=weight_data<(2*self.max_limit)/7:
            self.light_up(self.yellow)

        elif (2*self.max_limit)/7<=weight_data<(3*self.max_limit)/7:
            self.light_up(self.green)

        elif (3*self.max_limit)/7<=weight_data<(4*self.max_limit)/7:
            self.light_up(self.cyan)

        elif (4*self.max_limit)/7<=weight_data<(5*self.max_limit)/7:
            self.light_up(self.blue)

        elif (5*self.max_limit)/7<=weight_data<(6*self.max_limit)/7:
            self.light_up(self.magenta)

        elif (6*self.max_limit)/7<=weight_data<=(self.max_limit):
            self.light_up(self.white) #simple, all same color, level indicator 

        print("NeoPixels Activated.")

        pass

    def main(self): #main run

        self.magtag=MagTag()
        self.jpg_to_bmp(self.image_name)
        self.load_image(self.image_name)

        pass

if __name__ == "__main__": #runs full class

    image_inst="barcode_prod1_test"
    subm=Subscriber_Magtag(image_inst)
    subm.main()

    #end 