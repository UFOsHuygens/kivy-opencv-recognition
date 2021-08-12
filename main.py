from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
import cv2

kv = '''
GameLayout:
    canvas:
        # cor branca para o fundo
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
    Image
        # imagem que recebera update de 30x por segundo
        id: img1
        size_hint: 1, 1
    Image:
        # bola
        source: "ball.png"
        size_hint: 0.15, 0.15
        x: ball.width/2
        y: 0
        id: ball
'''

class GameLayout(FloatLayout):
    velocidade_y = 25
    interval = 0.001
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)
        self.cap = cv2.VideoCapture(0) # solicitação para captura de video com opencv
        ret, img = self.cap.read() # leitura da captura de video
        Clock.schedule_interval(self.update, 1.0/30.0) # chamada da função update 30x por segundo
        
    def update(self, dt):
        cascade = cv2.CascadeClassifier("palm.xml") # chamando o arquivo xml
        ret, img = self.cap.read() # leitura da captura de video chamada 30 vezes por segundo
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        objects = cascade.detectMultiScale(imgGray, 1.1, 4)
        for (x, y, w, h) in objects: # para todas entradas de detecções corretas, um evento pode receber --->
            cv2.rectangle(img,(x, y), (x+w, y+h), (255, 0, 0), 2)
            self.velocidade_y = 15
            Clock.schedule_interval(self.jump, self.interval)
            # <---
         
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
         
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
         
        self.ids.img1.texture = texture1



    def on_touch_down(self, touch): # ao tocar no display a função jump é chamada
        self.velocidade_y = 15
        Clock.schedule_interval(self.jump, self.interval)

    def jump(self, dt):  # função que movimenta objeto
        ball = self.ids.ball
        ball.y += self.velocidade_y # posição y é acrescentada várias vezes
        self.interval = 5

        self.velocidade_y -= 1

        if ball.y <= 0: # se a posição y da bola for menor ou igual a 0, a velocidade é nula
            self.velocidade_y = 0

            

class Kivy(App):
    def build(self):
        return Builder.load_string(kv)


Kivy().run()
