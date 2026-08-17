import turtle

# ---------------------------------------------------------
# Experiment 3: Two Dimensional Geometric Scaling
# ---------------------------------------------------------
# Scaling changes the size of an object.
# Formula:
#   x' = x * sx
#   y' = y * sy
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("2D Scaling")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(3)
pen.pensize(2)

# Original rectangle points
rectangle = [(50, 50), (180, 50), (180, 130), (50, 130)]

# Scaling factors
sx = 1.8
sy = 1.8


def draw_axes():
    pen.pencolor("gray")

    pen.penup()
    pen.goto(-400, 0)
    pen.pendown()
    pen.goto(400, 0)

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


def scale(points, sx, sy):
    scaled_points = []

    for x, y in points:
        new_x = x * sx
        new_y = y * sy
        scaled_points.append((new_x, new_y))

    return scaled_points


draw_axes()

# Draw original object
draw_shape(rectangle, "blue", "Original Rectangle")

# Scale and draw new object
new_rectangle = scale(rectangle, sx, sy)
draw_shape(new_rectangle, "red", "Scaled Rectangle")

pen.hideturtle()
turtle.done()
