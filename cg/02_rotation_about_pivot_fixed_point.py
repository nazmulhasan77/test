import turtle
import math

screen = turtle.Screen()
screen.setup(1000, 700)
screen.title("Rotation About Pivot / Fixed Point")

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

points = [(100, 50), (250, 50), (175, 180)]

angle = 80
xr = 100
yr = 50

theta = math.radians(angle)

rotated = []

for x, y in points:
    x_new = xr + (x - xr) * math.cos(theta) - (y - yr) * math.sin(theta)
    y_new = yr + (x - xr) * math.sin(theta) + (y - yr) * math.cos(theta)

    rotated.append((x_new, y_new))

draw_axes()

# Pivot point
t.penup()
t.goto(xr, yr)
t.dot(10, "green")
t.write(" Pivot")

draw_shape(points, "blue", "Original")
draw_shape(rotated, "red", "Pivot Rotation")

t.hideturtle()
turtle.done()
