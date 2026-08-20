import turtle
screen = turtle.Screen()
screen.title("Koch Curve Fractal")
screen.setup(1000,700)

pen = turtle.Turtle()

pen.speed(0)
pen.pensize(2)

depth = 4
lengtn = 700

def koch(length, depth):
    if depth == 0:
        pen.forward(length)
        return
    
    length = length/3
    
    koch(length,depth-1)
    pen.left(60)
    
    koch(length,depth-1)
    pen.right(120)
    
    koch(length,depth-1)
    pen.left(60)
    
    koch(length,depth-1)
    
pen.penup()
pen.goto(-200,-25)
pen.pendown()

koch(lengtn,depth)

pen.hideturtle()
turtle.done()