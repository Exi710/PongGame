from tkinter import *
import random
import time

class   Ball:
    
    def __init__(self, canvas, paddle, color, pongGame):
        self.pongGame = pongGame
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 235, 185)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.addSpeed = 1
        self.speedX = 3
        self.speedY = 3
        self.y = -self.speedY
        self.hitTop = False
        self.ballColors = ['red', 'orange', 'green', 'purple', 'yellow']
        self.color = 'red'

        
    def getRandomColor(self):
        random.shuffle(self.ballColors)
        if self.color == self.ballColors[0]:
            self.color = self.ballColors[1]
            return self.ballColors[1]

        self.color = self.ballColors[0]

        return self.ballColors[0]
        

        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
    
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        if pos[1] >= self.canvas_height:
            self.hit_bottom = True 
        elif self.hit_paddle(pos) == True and self.hitTop == True:
            self.y = -self.speedY
            self.pongGame.addScore()
            self.hitTop = False
        else:
            if pos[1] <= 0:
                if self.speedY < 5:
                    self.speedY = self.speedY + self.addSpeed
                    self.paddle.addSpeed()

                self.canvas.itemconfig(self.id, fill=self.getRandomColor())
                
                self.hitTop = True

                self.y = self.speedY
            elif pos[0] <= 0:
                if self.speedX < 5:
                    self.speedX = self.speedX + self.addSpeed
                    self.paddle.addSpeed()

                self.canvas.itemconfig(self.id, fill=self.getRandomColor())

                self.x = self.speedX
                
            elif pos[2] >= self.canvas_width:
                if self.speedX < 5:
                    self.speedX = self.speedX + self.addSpeed
                    self.paddle.addSpeed()

                self.canvas.itemconfig(self.id, fill=self.getRandomColor())

                self.x = -self.speedX

    def destroy(self):
        self.canvas.move(self.id, -1000, 0)
            
class Paddle:

    def addSpeed(self):
        self.moveX = self.moveX + 2.5

    
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 370)
        self.moveX = 4
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.end_game_state = False
        
    def end_game(self):
        self.canvas.move(self.id, -1000, 370)
        self.end_game_state = True
        
    def turn_left(self, evt):
        if self.end_game_state == False:
            pos = self.canvas.coords(self.id)  
            leftX = pos[0]
        
            if leftX >= self.moveX:
                self.canvas.move(self.id, -self.moveX, 0)
            else:
                self.canvas.move(self.id, -leftX, 0)
                
    def turn_right(self, evt):
        if self.end_game_state == False:
            pos = self.canvas.coords(self.id)  
            rightX = pos[2]
            diff = (self.canvas_width - rightX)

        
            if diff >= self.moveX:
                self.canvas.move(self.id, self.moveX, 0)
            else:
                self.canvas.move(self.id, diff, 0)
                
class PongGame:
    
    def addScore(self):
        self.score = self.score + 1
        self.canvas.delete(self.scoreId)
        self.scoreId = self.canvas.create_text(self.canvas_width / 2, 15, text='Score: %d' % self.score, fill='green', font=('Times', 15))
        if self.score == self.winScore:
            self.winState = True
            
    def __init__(self):
        self.winState = False
        self.winScore = 25
        self.score = 0
        self.tk = Tk()
        self.tk.title("Pong")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas_width = 500
        self.canvas_height = 400
        self.canvas = Canvas(self.tk, width=self.canvas_width, height=self.canvas_height, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.deleteMessage = False

    def drawScoreMessages(self):
        if self.score == 5 and self.deleteMessage == False:
            self.deleteMessage = True
            self.scoreMessageId = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 4, text='Неплохо...', fill='blue', font=('Times', 20, 'bold'))
        if self.score == 6 and self.deleteMessage == True:
            self.canvas.delete(self.scoreMessageId)
            self.deleteMessage = False
            
        if self.score == 10 and self.deleteMessage == False:
            self.deleteMessage = True
            self.scoreMessageId = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 4, text='Давай давай!', fill='orange', font=('Times', 20, 'bold'))
        if self.score == 11 and self.deleteMessage == True:
            self.canvas.delete(self.scoreMessageId)
            self.deleteMessage = False


        if self.score == 15 and self.deleteMessage == False:
            self.deleteMessage = True
            self.scoreMessageId = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 4, text='Вот это ты можешь!', fill='green', font=('Times', 20, 'bold'))
        if self.score == 16 and self.deleteMessage == True:
            self.canvas.delete(self.scoreMessageId)
            self.deleteMessage = False


        if self.score == 20 and self.deleteMessage == False:
            self.deleteMessage = True
            self.scoreMessageId = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 4, text='Ещё чуть-чуть!', fill='purple', font=('Times', 20, 'bold'))
        if self.score == 21 and self.deleteMessage == True:
            self.canvas.delete(self.scoreMessageId)
            self.deleteMessage = False

            


        
    def startGame(self):
        self.scoreId = self.canvas.create_text(self.canvas_width / 2, 15, text='Score: %d' % self.score, fill='green', font=('Times', 15))
        paddle = Paddle(self.canvas, 'blue')
        ball = Ball(self.canvas, paddle, 'red', self)

        while 1:
            if ball.hit_bottom == False and self.winState == False:
                ball.draw()
                self.tk.update_idletasks()
                self.tk.update()
                self.drawScoreMessages()
                time.sleep(0.01)
                    
            elif ball.hit_bottom == True:
                self.textId = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 3, text='YOU DIED', fill='red', font=('Times', 20, 'bold'))
                self.btn = Button(self.tk, text='Начать заново?', bg='red', fg='yellow', height = 3, width = 20, command = self.buttonPressed)
                self.btn.pack()
                self.btn.place(x = 177,y = 200)
                paddle.end_game()
                
                del paddle
                del ball

                self.canvas.delete(self.scoreId)
                self.score = 0
                if self.deleteMessage == True:
                    self.canvas.delete(self.scoreMessageId)
                    self.deleteMessege = False
                break
            else:
                self.textId = self.canvas.create_text(self.canvas_width / 2 + 5, self.canvas_height / 3, text='YOU WON! :)', fill='green', font=('Times', 20, 'bold'))
                self.btn = Button(self.tk, text='Начать заново?', bg='green', fg='black', height = 3, width = 20, command = self.buttonPressed)
                self.btn.pack()
                self.btn.place(x = 177,y = 200)
                paddle.end_game()
                ball.destroy()

                
                del paddle
                del ball

                
                self.canvas.delete(self.scoreId)
                self.score = 0
                self.winState = False
                break
            
    def buttonPressed(self):
        self.canvas.delete(self.textId)
        self.btn.destroy()
        self.startGame()

pongGame =  PongGame()
pongGame.startGame()



