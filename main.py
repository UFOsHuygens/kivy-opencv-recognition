from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
import cv2

kv = '''
GameLayout:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
    Image
        id: img1
        size_hint: 1, 1
'''

class GameLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cap = cv2.VideoCapture(0) # solicitação para captura de video com opencv
        ret, img = self.cap.read() # leitura da captura de video
        Clock.schedule_interval(self.update, 1.0/30.0) # chamada da função update 30x por segundo
        
    def update(self, dt):
        cascade = cv2.CascadeClassifier("xml/face.xml") # face ou xml
        ret, img = self.cap.read() # leitura da captura de video chamada 30 vezes por segundo
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        objects = cascade.detectMultiScale(imgGray, 1.1, 4)
        for (x, y, w, h) in objects: # para todas entradas de detecções corretas, um evento pode receber --->
            cv2.rectangle(img,(x, y), (x+w, y+h), (255, 0, 0), 2) # aqui é desenhado um retangulo
            # <---
         
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
         
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
         
        self.ids.img1.texture = texture1

class Kivy(App):
    def build(self):
        return Builder.load_string(kv)


Kivy().run()
