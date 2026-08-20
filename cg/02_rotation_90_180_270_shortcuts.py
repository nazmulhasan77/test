import turtle

screen = turtle.Screen()
screen.setup(1000, 700)
screen.title("90, 180, 270 Degree Rotation")

t = turtle.Turtle()
t.speed(0)
t.pensize(2)

points = [(80, 50), (180, 50), (130, 140)]

angle = 90      # change to 180 or 270

rotated = []

for x, y in points:

    if angle == 90:
        x_new = -y
        y_new = x

    elif angle == 180:
        x_new = -x
        y_new = -y

    elif angle == 270:
        x_new = y
        y_new = -x

    rotated.append((x_new, y_new))


def draw_axes():
    t.penup()
    t.goto(-450, 0)
    t.pendown()
    t.goto(450, 0)

    t.penup()
    t.goto(0, -320)
    t.pendown()
    t.goto(0, 320)


def draw(points, color):
    t.color(color)
    t.penup()
    t.goto(points[0])
    t.pendown()

    for p in points[1:]:
        t.goto(p)

    t.goto(points[0])


draw_axes()
draw(points, "blue")
draw(rotated, "red")

t.hideturtle()
turtle.done()
