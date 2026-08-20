import turtle

# ---------------------------------------------------------
# 2D Translation - All Common Variations
# ---------------------------------------------------------

screen = turtle.Screen()
screen.setup(1000, 700)
screen.title("2D Translation - All Variations")

t = turtle.Turtle()
t.speed(0)
t.pensize(2)

scale = 1


# ---------------------------------------------------------
# Draw X and Y axes
# ---------------------------------------------------------
def draw_axes():

    t.color("black")

    # X-axis
    t.penup()
    t.goto(-450, 0)
    t.pendown()
    t.goto(450, 0)
    t.write(" X")

    # Y-axis
    t.penup()
    t.goto(0, -320)
    t.pendown()
    t.goto(0, 320)
    t.write(" Y")


# ---------------------------------------------------------
# Draw polygon / shape
# ---------------------------------------------------------
def draw_shape(points, color, label):

    t.color(color)

    t.penup()
    t.goto(points[0])
    t.pendown()

    for point in points[1:]:
        t.goto(point)

    # close the shape
    t.goto(points[0])

    # label
    t.penup()
    t.goto(points[0][0], points[0][1] - 25)
    t.write(label, font=("Arial", 11, "bold"))


# ---------------------------------------------------------
# Translation function
# Formula:
# x' = x + tx
# y' = y + ty
# ---------------------------------------------------------
def translate(points, tx, ty):

    new_points = []

    for x, y in points:

        x_new = x + tx
        y_new = y + ty

        new_points.append((x_new, y_new))

    return new_points


# ---------------------------------------------------------
# Original Triangle
# ---------------------------------------------------------
points = [
    (-200, -100),
    (-100, -100),
    (-150, 0)
]


draw_axes()
draw_shape(points, "blue", "Original")


# =========================================================
# CHOOSE ANY ONE VARIATION
# =========================================================


# ---------------------------------------------------------
# 1. Basic Translation
# moves in both X and Y direction
# ---------------------------------------------------------

tx = 250
ty = 150

new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 2. X-axis Translation Only
# Uncomment these lines to use
# ---------------------------------------------------------

# tx = 250
# ty = 0
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 3. Y-axis Translation Only
# Uncomment these lines to use
# ---------------------------------------------------------

# tx = 0
# ty = 200
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 4. Negative X Translation
# moves left
# ---------------------------------------------------------

# tx = -150
# ty = 100
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 5. Negative Y Translation
# moves downward
# ---------------------------------------------------------

# tx = 150
# ty = -100
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 6. Both Negative Translation
# moves left and downward
# ---------------------------------------------------------

# tx = -150
# ty = -100
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# 7. Successive Translation
#
# First translation  = (tx1, ty1)
# Second translation = (tx2, ty2)
#
# Final:
# tx = tx1 + tx2
# ty = ty1 + ty2
# ---------------------------------------------------------

# tx1 = 100
# ty1 = 50
#
# tx2 = 150
# ty2 = 100
#
# tx = tx1 + tx2
# ty = ty1 + ty2
#
# new_points = translate(points, tx, ty)


# ---------------------------------------------------------
# Draw translated shape
# ---------------------------------------------------------

draw_shape(new_points, "red", "Translated")


t.hideturtle()
turtle.done()
