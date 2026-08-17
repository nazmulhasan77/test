import turtle

# ---------------------------------------------------------
# Experiment 5: DDA (Digital Differential Analyzer)
# Line Drawing Algorithm
# ---------------------------------------------------------
# Formula:
#   dx = x2 - x1
#   dy = y2 - y1
#   steps = max(abs(dx), abs(dy))
#   x_increment = dx / steps
#   y_increment = dy / steps
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("DDA Line Drawing Algorithm")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

PIXEL_SIZE = 8

# Input line endpoints
x1, y1 = -35, -20
x2, y2 = 35, 25


def draw_axes():
    axis = turtle.Turtle()
    axis.hideturtle()
    axis.speed(0)
    axis.pencolor("gray")

    axis.penup()
    axis.goto(-400, 0)
    axis.pendown()
    axis.goto(400, 0)

    axis.penup()
    axis.goto(0, -300)
    axis.pendown()
    axis.goto(0, 300)


def plot_pixel(x, y, color="red"):
    screen_x = x * PIXEL_SIZE
    screen_y = y * PIXEL_SIZE

    pen.penup()
    pen.goto(screen_x - PIXEL_SIZE / 2, screen_y - PIXEL_SIZE / 2)
    pen.setheading(0)
    pen.pencolor(color)
    pen.fillcolor(color)
    pen.pendown()

    pen.begin_fill()
    for _ in range(4):
        pen.forward(PIXEL_SIZE)
        pen.left(90)
    pen.end_fill()


def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    # If both points are the same
    if steps == 0:
        plot_pixel(x1, y1)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    # steps + 1 includes both start and end points
    for _ in range(steps + 1):
        plot_pixel(round(x), round(y))
        x = x + x_increment
        y = y + y_increment


draw_axes()
dda(x1, y1, x2, y2)

turtle.done()
