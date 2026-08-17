import turtle

# ---------------------------------------------------------
# Experiment 4: Bresenham Line Drawing Algorithm
# ---------------------------------------------------------
# This program draws a line pixel by pixel using only
# integer calculations.
#
# The code below works for ALL line directions.
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("Bresenham Line Drawing Algorithm")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

PIXEL_SIZE = 8

# Input line endpoints (small logical coordinates)
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


def plot_pixel(x, y, color="blue"):
    """Draw one square pixel centered at logical point (x, y)."""
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


def bresenham(x1, y1, x2, y2):
    # Distance in x and y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Direction of movement
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # Error value
    error = dx - dy

    while True:
        plot_pixel(x1, y1)

        # Stop when destination is reached
        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * error

        if e2 > -dy:
            error = error - dy
            x1 = x1 + sx

        if e2 < dx:
            error = error + dx
            y1 = y1 + sy


draw_axes()
bresenham(x1, y1, x2, y2)

turtle.done()
