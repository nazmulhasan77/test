import turtle

# ---------------------------------------------------------
# Experiment 7: Deterministic Self-Similar Fractal
# Koch Curve
# ---------------------------------------------------------
# Rule:
# Each line is divided into 3 equal parts and replaced by
# 4 smaller line segments.
#
# The same fixed rule is repeated recursively, so the
# fractal is deterministic and self-similar.
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("Koch Curve Fractal")
screen.setup(1000, 700)

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)

# Number of recursive levels
depth = 4

# Total length of the first line
length = 700


def koch(length, depth):
    # Base case: draw a straight line
    if depth == 0:
        pen.forward(length)
        return

    # Recursive case
    length = length / 3

    koch(length, depth - 1)
    pen.left(60)

    koch(length, depth - 1)
    pen.right(120)

    koch(length, depth - 1)
    pen.left(60)

    koch(length, depth - 1)


# Start near the left side of the screen
pen.penup()
pen.goto(-350, -50)
pen.pendown()

koch(length, depth)

pen.hideturtle()
turtle.done()
