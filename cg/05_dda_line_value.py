import turtle
import time

# ---------------------------------------------------------
# Experiment 5: DDA Line Drawing Algorithm
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("DDA Line Drawing Algorithm")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

PIXEL_SIZE = 8

# Line endpoints
x1, y1 = -35, -20
x2, y2 = 35, 25


# ---------------------------------------------------------
# Draw X-Y Axis
# ---------------------------------------------------------
def draw_axes():

    axis = turtle.Turtle()
    axis.hideturtle()
    axis.speed(0)
    axis.pencolor("gray")

    # X-axis
    axis.penup()
    axis.goto(-400, 0)
    axis.pendown()
    axis.goto(400, 0)
    axis.write(" X", font=("Arial", 12, "bold"))

    # Y-axis
    axis.penup()
    axis.goto(0, -300)
    axis.pendown()
    axis.goto(0, 300)
    axis.write(" Y", font=("Arial", 12, "bold"))


# ---------------------------------------------------------
# Draw reference/original mathematical line
# ---------------------------------------------------------
def draw_reference_line(x1, y1, x2, y2):

    line = turtle.Turtle()
    line.hideturtle()
    line.speed(0)
    line.pencolor("lightgray")
    line.pensize(1)

    line.penup()
    line.goto(x1 * PIXEL_SIZE, y1 * PIXEL_SIZE)
    line.pendown()
    line.goto(x2 * PIXEL_SIZE, y2 * PIXEL_SIZE)


# ---------------------------------------------------------
# Plot one pixel
# ---------------------------------------------------------
def plot_pixel(x, y, color="red"):

    screen_x = x * PIXEL_SIZE
    screen_y = y * PIXEL_SIZE

    pen.penup()

    pen.goto(
        screen_x - PIXEL_SIZE / 2,
        screen_y - PIXEL_SIZE / 2
    )

    pen.setheading(0)

    pen.pencolor(color)
    pen.fillcolor(color)

    pen.pendown()

    pen.begin_fill()

    for _ in range(4):
        pen.forward(PIXEL_SIZE)
        pen.left(90)

    pen.end_fill()


# ---------------------------------------------------------
# Write point label
# ---------------------------------------------------------
def write_point(x, y, text):

    label = turtle.Turtle()
    label.hideturtle()
    label.penup()

    label.goto(
        x * PIXEL_SIZE + 10,
        y * PIXEL_SIZE + 10
    )

    label.write(
        text,
        font=("Arial", 10, "bold")
    )


# ---------------------------------------------------------
# DDA Algorithm
# ---------------------------------------------------------
def dda(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    # Same starting and ending point
    if steps == 0:
        plot_pixel(x1, y1)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    # Show calculation
    print("dx =", dx)
    print("dy =", dy)
    print("steps =", steps)
    print("x increment =", x_increment)
    print("y increment =", y_increment)

    x = x1
    y = y1

    for i in range(steps + 1):

        px = round(x)
        py = round(y)

        print(
            "Step", i,
            ": x =", round(x, 2),
            "y =", round(y, 2),
            "Pixel =", (px, py)
        )

        # First point = green
        if i == 0:
            plot_pixel(px, py, "green")

        # Last point = blue
        elif i == steps:
            plot_pixel(px, py, "blue")

        # Other pixels = red
        else:
            plot_pixel(px, py, "red")

        # Slow animation
        screen.update()
        time.sleep(0.03)

        x = x + x_increment
        y = y + y_increment


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

screen.tracer(0)

draw_axes()

draw_reference_line(x1, y1, x2, y2)

write_point(x1, y1, "P1")
write_point(x2, y2, "P2")

dda(x1, y1, x2, y2)

screen.update()

turtle.done()