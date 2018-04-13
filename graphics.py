# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:39:40 2018

@author: jkell
"""

import tkinter as tk
import time

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.color = color
        self.x = 0
        self.y = 0
        self.width=20
        self.height=20
    def draw(self):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2,fill=self.color)


class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 10, 50, fill="black")
        self.x = 0
        self.y = 0
        self.width=10
        self.height=50
        
    def draw(self):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2, fill="black")


class GFX:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title = "Pong"
        self.win.resizable(0,0)
        self.win.wm_attributes("-topmost", 1)
        
        self.canvas = tk.Canvas(self.win, width=500, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
    
        self.ball = Ball(self.canvas, "red")
        self.ball.width = 10
        self.ball.height= 10
        self.ball.x = 50
        self.ball.y = 50
        
        self.player = Player(self.canvas)
        self.player.x = 400
        self.player.y = 200

    
    def update(self):
        # put this in the main loop
        self.ball.draw()
        self.player.draw()
        
        self.win.update_idletasks()
        self.win.update()
        time.sleep(0.033)
        