import turtle
import math

screen = turtle.Screen()
screen.setup(1000, 700)
screen.title("Scaling About Fixed / Pivot Point")

t = turtle.Turtle()
t.speed(0)
t.pensize(2)

def draw_axes():
    t.color("black")
    t.penup()
    t.goto(-450, 0)
    t.pendown()
    t.goto(450, 0)
    t.write(" X")

    t.penup()
    t.goto(0, -320)
    t.pendown()
    t.goto(0, 320)
    t.write(" Y")

def draw_shape(points, color, label):
    t.color(color)
    t.penup()
    t.goto(points[0])
    t.pendown()

    for p in points[1:]:
        t.goto(p)

    t.goto(points[0])

    t.penup()
    t.goto(points[0][0], points[0][1] - 25)
    t.write(label, font=("Arial", 11, "bold"))

points = [(100, 50), (220, 50), (220, 150), (100, 150)]

sx = 1.5
sy = 1.5

xf = 100
yf = 50

scaled = []

for x, y in points:
    x_new = xf + (x - xf) * sx
    y_new = yf + (y - yf) * sy
    scaled.append((x_new, y_new))

draw_axes()

t.penup()
t.goto(xf, yf)
t.dot(10, "green")
t.write(" Fixed Point")

draw_shape(points, "blue", "Original")
draw_shape(scaled, "red", "Fixed Point Scaling")

t.hideturtle()
turtle.done()
