import turtle
import math

# ---------------------------------------------------------
# Experiment 2: Two Dimensional Geometric Rotation
# ---------------------------------------------------------
# Rotation changes the orientation of an object.
# Rotation about origin:
#   x' = x*cos(theta) - y*sin(theta)
#   y' = x*sin(theta) + y*cos(theta)
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("2D Rotation")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(3)
pen.pensize(2)

# Original triangle points
triangle = [(100, 50), (250, 50), (175, 180)]

# Rotation angle in degrees
angle = 45


def draw_axes():
    pen.pencolor("gray")

    # X-axis
    pen.penup()
    pen.goto(-400, 0)
    pen.pendown()
    pen.goto(400, 0)

    # Y-axis
    pen.penup()
    pen.goto(0, -300)
    pen.pendown()
    pen.goto(0, 300)


def draw_shape(points, color, label):
    pen.pencolor(color)
    pen.penup()
    pen.goto(points[0])
    pen.pendown()

    for point in points[1:]:
        pen.goto(point)

    pen.goto(points[0])

    pen.penup()
    pen.goto(points[0][0], points[0][1] - 25)
    pen.write(label, font=("Arial", 12, "normal"))


def rotate(points, angle):
    rotated_points = []

    # math functions use radians
    theta = math.radians(angle)

    for x, y in points:
        new_x = x * math.cos(theta) - y * math.sin(theta)
        new_y = x * math.sin(theta) + y * math.cos(theta)

        rotated_points.append((new_x, new_y))

    return rotated_points


draw_axes()

# Original object
draw_shape(triangle, "blue", "Original")

# Rotated object
new_triangle = rotate(triangle, angle)
draw_shape(new_triangle, "red", f"Rotated {angle} degrees")

pen.hideturtle()
turtle.done()
