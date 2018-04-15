#Internal representation of game state and actions.
#Different from actual game view
#This is the model component following an MVC design pattern

import random
import numpy as np

def intersect_line(x1,y1,x2,y2,linex):
    """
    Determine where the line drawn through (x1,y1) and (x2,y2)
    will intersect the line x=linex
    """
    
    return ((y2-y1)/(x2-x1))*(linex-x1)+y1
    


class PongModel:
    def __init__(self, ballX, ballY, bvelocityX, bvelocityY, paddleY):
        self.ball_x = ballX
        self.ball_y = ballY
        self.ball_velocity_x = bvelocityX
        self.ball_velocity_y = bvelocityY
        self.paddle_x = 1.0 #this is a constant
        self.paddle_y = paddleY
        
        self.ball_lastx = ballX
        self.ball_lasty = ballY
        
        self.lost = False



    def move(self, proposed_move = 0):
        """
           Move the paddle
           Args:
              proposed_move(float): the distance to move the paddle, in the y direction. 
        """
        self.paddle_y += proposed_move

        if self.paddle_y+0.2 > 1:
            self.paddle_y = 0.8
        elif self.paddle_y < 0:
            self.paddle_y = 0
                
      
    def move_up(self):
        self.move(-0.04)
        
    def move_down(self):
        self.move(0.04)
        
    def update(self, gfx):
        """
        Update the window based on the internal state
        """
        
        if gfx.thread.done == True:
            """
            we want to make sure we are only calculating the new position
            when the frame is refreshed
            """
            self.ball_lastx = self.ball_x
            self.ball_lasty = self.ball_y
            
            # update ball position
            self.ball_x += self.ball_velocity_x
            self.ball_y += self.ball_velocity_y
            
            
            # check bouncing
            if (self.ball_y > 1 and self.ball_velocity_y > 0):
                self.ball_velocity_y *= -1
            elif (self.ball_y < 0 and self.ball_velocity_y < 0):
                self.ball_velocity_y *= -1
            elif (self.ball_x < 0 and self.ball_velocity_x < 0):
                self.ball_velocity_x *= -1
            elif (self.ball_x > 1 and self.ball_velocity_x > 0):
                intersect_y = intersect_line(self.ball_lastx, self.ball_lasty, self.ball_x, self.ball_y, 1)
                if (intersect_y >= self.paddle_y and intersect_y <= self.paddle_y + 0.2 and self.ball_lastx <= 1):
                    # we hit the paddle!
                    self.ball_x = 2*self.paddle_x - self.ball_x
                    
                    # randomize velocities
                    U = random.uniform(-0.015, 0.015)
                    V = random.uniform(-0.03,  0.03 )
                    temp_vx = -1*self.ball_velocity_x + U
                    temp_vy = -1*self.ball_velocity_y + V
                    while (np.sqrt(temp_vx**2 + temp_vy**2) < 0.03):
                        # better way to do this? maybe
                        U = random.uniform(-0.015, 0.015)
                        V = random.uniform(-0.03,  0.03 )
                        temp_vx = -1*self.ball_velocity_x + U
                        temp_vy = -1*self.ball_velocity_y + V
                        
                    self.ball_velocity_x = temp_vx
                    self.ball_velocity_y = temp_vy
                    
                else:
                    # missed the paddle. lost!
                    self.lost = True
        
        
            gfx.player.y = self.paddle_y * gfx.height + gfx.player.height/2  # to be consistent with spec, y represents top of player
            gfx.ball.x = self.ball_x * gfx.width
            gfx.ball.y = self.ball_y * gfx.height
            
            
            gfx.update() # this happens on a different thread
    
    


    
    