import turtle
import time

# ---------------------------------
# Screen setup
# ---------------------------------
screen = turtle.Screen()
screen.title("Koch Snowflake Iteration")
screen.setup(1000, 700)

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)


# ---------------------------------
# Koch Curve
# ---------------------------------
def koch(length, depth):

    # Base case
    if depth == 0:
        pen.forward(length)
        return

    length = length / 3

    koch(length, depth - 1)

    pen.left(60)

    koch(length, depth - 1)

    pen.right(120)

    koch(length, depth - 1)

    pen.left(60)

    koch(length, depth - 1)


# ---------------------------------
# Koch Triangle / Snowflake
# ---------------------------------
def draw_snowflake(length, depth):

    for i in range(3):

        koch(length, depth)

        pen.right(120)


# ---------------------------------
# Show iteration one by one
# ---------------------------------

length = 400

for depth in range(5):

    pen.clear()

    # Starting position
    pen.penup()
    pen.goto(-200, 120)
    pen.setheading(0)
    pen.pendown()

    # Write iteration number
    pen.penup()
    pen.goto(-80, 280)
    pen.write(
        "Iteration = " + str(depth),
        font=("Arial", 20, "bold")
    )

    pen.goto(-200, 120)
    pen.setheading(0)
    pen.pendown()

    # Draw snowflake
    draw_snowflake(length, depth)

    # Wait before next iteration
    time.sleep(2)


turtle.done()