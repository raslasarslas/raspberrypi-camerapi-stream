
import numpy as np
import cv2
import pygame
from pygame.locals import *
import socket


class HandleStreamedImage(object):
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('your-computer-ip-address', 8000))
        self.server_socket.listen(0)
        # raspberry pi Ip Address
        self.raspberry_ip = 'raspberry-ip-adrdess'
        # port number, you can choose your own ip adress
        self.raspberry_socket_port = 15556

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        self.send_inst = True
        pygame.init()
        self.collect_image()

    def collect_image(self):

        width, height = 640, 640
        pygame.init()
        window = pygame.display.set_mode((width, height))

        socket_commande = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_commande.connect((self.raspberry_ip, self.raspberry_socket_port))
        e1 = cv2.getTickCount()
        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
                    image3 = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)

                    # show colored image in separed window

                    cv2.imshow('image', image3)
                    k = cv2.waitKey(1)


                    # get input from keyboard
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            print 'key down'
                            key_input = pygame.key.get_pressed()



                            # socket_commande.close()
                            if key_input[pygame.K_UP]:
                                # execute an action
                                print "key pressed"



                    # SHOW IMAGE IN A PYGAME WINDOW
                    # Find the frame's dimensions in (w, h) format.
                    frameSize = image.shape[1::-1]
                    # Convert the frame to RGB, which Pygame requires.
                    # if self.isGray(image2):
                    conversionType = cv2.COLOR_GRAY2RGB
                    rgbFrame = cv2.cvtColor(image, conversionType)
                    # Convert the frame to Pygame's Surface type.
                    pygameFrame = pygame.image.frombuffer(
                        rgbFrame.tostring(), frameSize, 'RGB')
                    # Resize the window to match the frame.
                    displaySurface = pygame.display.set_mode(frameSize)
                    # Blit and display the frame.
                    displaySurface.blit(pygameFrame, (0, 0))
                    pygame.display.flip()


            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()


        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    HandleStreamedImage()
