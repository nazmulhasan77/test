import turtle

# ---------------------------------------------------------
# Experiment 1: Two Dimensional Geometric Translation
# ---------------------------------------------------------
# Translation moves an object from one position to another.
# Formula:
#   x' = x + tx
#   y' = y + ty
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("2D Translation")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(3)
pen.pensize(2)

# Original triangle points
triangle = [(-200, -100), (-100, -100), (-150, 0)]

# Translation values
tx = 250
ty = 150


def draw_shape(points, color, label):
    pen.pencolor(color)
    pen.penup()
    pen.goto(points[0])
    pen.pendown()

    for point in points[1:]:
        pen.goto(point)

    pen.goto(points[0])  # close the triangle

    pen.penup()
    pen.goto(points[0][0], points[0][1] - 30)
    pen.write(label, font=("Arial", 12, "normal"))


def translate(points, tx, ty):
    translated_points = []

    for x, y in points:
        new_x = x + tx
        new_y = y + ty
        translated_points.append((new_x, new_y))

    return translated_points


# Draw original object
draw_shape(triangle, "blue", "Original Triangle")

# Calculate translated object
new_triangle = translate(triangle, tx, ty)

# Draw translated object
draw_shape(new_triangle, "red", "Translated Triangle")

pen.hideturtle()
turtle.done()
