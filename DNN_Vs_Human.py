# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:00:22 2018

@author: jkell

RESULT:
    Game: 1000 Avg score: 10.136
"""
import DNN
import random
import numpy as np
import matplotlib.pyplot as plt
import graphics as gfx
import pong_model as png

def _ReLu(z):
    outp = np.zeros(z.shape)
    if len(z.shape) == 2:
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                if (z[i,j] > 0):
                    outp[i,j] = z[i,j]
    else:
        for i in range(z.shape[0]):
            if (z[i] > 0):
                outp[i] = z[i]
    return outp


ReLu = lambda inp: _ReLu(inp)   # rectified linear

def load_data(fname):
    f = open(fname, 'r')
    data = []
    y=[]
    for line in f:
        linedata = line.split(" ")
        
        state = [float(linedata[0]), float(linedata[1]), float(linedata[2]),
                 float(linedata[3]), float(linedata[4])]
        y.append(float(linedata[5]))
        data.append(state)
        
    return data, y


def UpKey(Game): # move player 2
    Game.move_up(2)
    
def DownKey(Game):
    Game.move_down(2)
    
if __name__ == '__main__':
    
    BATCH_SIZE = 100
    
    Network = DNN.NeuralNetwork(5,3)   # 5 inputs, 3 outputs
    Network.add_hidden_layer(256, activation=ReLu, bias=True)
    Network.add_hidden_layer(256, activation=ReLu, bias=True)
    Network.add_hidden_layer(256, activation=ReLu, bias=True)
    Network.add_hidden_layer(256, activation=ReLu, bias=True)
    Network.generate_weights(0.01)
    X=[]
    Y=[]
    # construct training set
    # load data
    X, Y = load_data("./data/test_policy_easy.txt")
    
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    for i in range(np.size(X, axis=0)):
        X[i] = np.divide(X[i]-means, stds).tolist()
        
    print("Training Neural Network...")
    loss=[]
    error=[]
    for i in range(200):
        
        # generate a new batch
        batch = []
        batch_y = []
        for _ in range(BATCH_SIZE):
            selection = random.randint(0,len(X)-1)
            while (X[selection] in batch):
                selection = random.randint(0,len(X)-1)
            batch.append(X[selection])
            batch_y.append(Y[selection])
            
        
        # train
        a = Network.forward(batch)
        Network.backward(batch_y)
        dW = Network.dW
        W=Network.weights
    #    print(W[-1][0:5])
        aa = Network.a
    #    print("dW", Network.dW)
        loss.append( Network.update_weights(5*0.95**i))
        print(loss[-1])
        YY = np.argmax(a,axis=1)
        error.append(BATCH_SIZE-sum(np.equal(batch_y,YY)))
        if (i%20 == 0):
            print(i, "epochs. Error:", error[-1])
    
    print("Training Done. Loss =",loss[-1])
    
    window = gfx.GFX(players=2)
    window.fps = 30  # you can modify this for debugging purposes, default=30
    Game = png.PongModel(0.5, 0.5, 0.03, 0.01, 0.4)   # initialize state
    Game.init2(0.4, 0)
    window.win.bind('<Up>',lambda eff: UpKey(Game))
    window.win.bind('<Down>',lambda eff: DownKey(Game))
    
    games = 0
    totalscore = 0
    while 1:
        # main loop
        if (window._open == False):
            break
        
        state = Game.get_state()  # get the values of relevant variables
        state = np.divide(state-means, stds).tolist()   # normalize data
        actionlist = Network.forward(state)   # forward propagation of the DNN
        maxidx = 0
        for i in range(1,len(actionlist)):
            if (actionlist[i] > actionlist[maxidx]):
                maxidx = i
        if (maxidx == 0):    # make the decision
            Game.move_up()
        elif (maxidx == 2):
            Game.move_down()
            
            
        Game.update(window)   # update the environment (graphics, "physics")
        
        if (Game.lost == True):
            if (Game.won == 1):
                print("Player 1 wins!")
            else:
                print("Player 2 wins!")
            Game.reset()
            games+=1
    
    print("Game ended.")