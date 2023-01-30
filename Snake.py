import turtle as t
import time
import random
import pandas as pd
from csv import DictWriter

def RunSnake(name,snake_color,food_color,food_shape,highscore):
	t.TurtleScreen._RUNNING=True
	delay = 0.1
	score = 0
	high_score = int(highscore)

	wn = t.Screen()
	wn.title("Snake Game  "+" PlayerName: "+name)
	wn.bgcolor("black")

	wn.setup(width=600, height=600)
	wn.tracer(0)

	head = t.Turtle()
	head.shape("square")
	head.color("white")
	head.penup()
	head.goto(0, 0)
	head.direction = "Stop"

	food = t.Turtle()

	colors=food_color
	shapes=food_shape
	food.speed(0)
	food.shape(shapes)
	food.color(colors)
	food.penup()
	food.goto(0, 100)

	pen = t.Turtle()
	pen.speed(0)
	pen.shape("square")
	pen.color("white")
	pen.penup()
	pen.hideturtle()
	pen.goto(0, 250)
	pen.write("Score : 0 High Score : {} ".format(high_score), align="center",
			font=("candara", 24, "bold"))

	def goup():
		if head.direction != "down":
			head.direction = "up"

	def godown():
		if head.direction != "up":
			head.direction = "down"

	def goleft():
		if head.direction != "right":
			head.direction = "left"

	def goright():
		if head.direction != "left":
			head.direction = "right"

	def move():
		if head.direction == "up":
			y = head.ycor()
			head.sety(y+20)
		if head.direction == "down":
			y = head.ycor()
			head.sety(y-20)
		if head.direction == "left":
			x = head.xcor()
			head.setx(x-20)
		if head.direction == "right":
			x = head.xcor()
			head.setx(x+20)
	global running
	running=True

	def quit():
		global running
		running=False			

	wn.listen()
	wn.onkeypress(goup, "w")
	wn.onkeypress(godown, "s")
	wn.onkeypress(goleft, "a")
	wn.onkeypress(goright, "d")

	wn.listen()
	wn.onkeypress(goup, "W")
	wn.onkeypress(godown, "S")
	wn.onkeypress(goleft, "A")
	wn.onkeypress(goright, "D")
	wn.onkeypress(quit,"Escape")

	wn.listen()
	wn.onkeypress(goup, "Up")
	wn.onkeypress(godown, "Down")
	wn.onkeypress(goleft, "Left")
	wn.onkeypress(goright, "Right")
	wn.onkeypress(quit,"q")

	segments = []

	while running:
		wn.update()
		if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
			time.sleep(1)
			head.goto(0, 0)
			head.direction = "Stop"
			colors = food_color
			shapes = food_shape
			for segment in segments:
				segment.goto(1000, 1000)
			segments.clear()
			score = 0
			delay = 0.1
			pen.clear()
			pen.write("Score : {} High Score : {} ".format(
				score, high_score), align="center", font=("candara", 24, "bold"))
			df=pd.read_csv("Recognized_Faces.csv")
			df=df[df.Name!=name.lower()]
			df.to_csv("Recognized_Faces.csv",index=False)			
			fields = ['Name','Snake_Color','Food_Shape','Food_Color','Highscore']
			data_dict={'Name':name.lower() ,'Snake_Color':snake_color ,'Food_Shape':food_shape ,'Food_Color':food_color ,'Highscore':high_score }	
			
			with open("Recognized_Faces.csv", 'a') as f_object:
				
				dictwriter_object = DictWriter(f_object, fieldnames=fields)
			
				dictwriter_object.writerow(data_dict)
			
				f_object.close()
		if head.distance(food) < 20:
			x = random.randint(-270, 270)
			y = random.randint(-270, 270)
			food.goto(x, y)

			new_segment = t.Turtle()
			new_segment.speed(0)
			new_segment.shape("square")
			new_segment.color(snake_color) 
			new_segment.penup()
			segments.append(new_segment)
			delay -= 0.001
			score += 10
			if score > high_score:
				high_score = score
			pen.clear()
			pen.write("Score : {} High Score : {} ".format(
				score, high_score), align="center", font=("candara", 24, "bold"))

		for index in range(len(segments)-1, 0, -1):
			x = segments[index-1].xcor()
			y = segments[index-1].ycor()
			segments[index].goto(x, y)
		if len(segments) > 0:
			x = head.xcor()
			y = head.ycor()
			segments[0].goto(x, y)
		move()
		for segment in segments:
			if segment.distance(head) < 20:
				time.sleep(1)
				head.goto(0, 0)
				head.direction = "stop"
				colors = food_color
				shapes = food_shape
				for segment in segments:
					segment.goto(1000, 1000)
				segment.clear()
				score = 0
				delay = 0.1
				pen.clear()
				pen.write("Score : {} High Score : {} ".format(
					score, high_score), align="center", font=("candara", 24, "bold"))
				df=pd.read_csv("Recognized_Faces.csv")
				df=df[df.Name!=name.lower()]
				df.to_csv("Recognized_Faces.csv",index=False)			
				fields = ['Name','Snake_Color','Food_Shape','Food_Color','Highscore']
				data_dict={'Name':name.lower() ,'Snake_Color':snake_color ,'Food_Shape':food_shape ,'Food_Color':food_color ,'Highscore':high_score }	
				
				with open("Recognized_Faces.csv", 'a') as f_object:
					
					dictwriter_object = DictWriter(f_object, fieldnames=fields)
				
					dictwriter_object.writerow(data_dict)
				
					f_object.close()
		time.sleep(delay)
	wn.bye()
	#wn.mainloop()
	#t.done()
	
	
