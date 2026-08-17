import turtle

# ---------------------------------------------------------
# Experiment 6: Cohen-Sutherland Line Clipping Algorithm
# ---------------------------------------------------------
# Region codes:
#   INSIDE = 0000
#   LEFT   = 0001
#   RIGHT  = 0010
#   BOTTOM = 0100
#   TOP    = 1000
# ---------------------------------------------------------

screen = turtle.Screen()
screen.title("Cohen-Sutherland Line Clipping")
screen.setup(900, 700)

pen = turtle.Turtle()
pen.speed(3)
pen.pensize(3)
pen.hideturtle()

# Clipping window boundaries
X_MIN = -200
Y_MIN = -120
X_MAX = 200
Y_MAX = 120

# Line endpoints
x1, y1 = -330, -200
x2, y2 = 330, 220

# Region code constants
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def draw_window():
    box = turtle.Turtle()
    box.hideturtle()
    box.speed(0)
    box.pensize(2)
    box.pencolor("black")

    box.penup()
    box.goto(X_MIN, Y_MIN)
    box.pendown()

    box.goto(X_MAX, Y_MIN)
    box.goto(X_MAX, Y_MAX)
    box.goto(X_MIN, Y_MAX)
    box.goto(X_MIN, Y_MIN)


def draw_line(x1, y1, x2, y2, color):
    pen.pencolor(color)
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y2)


def compute_code(x, y):
    code = INSIDE

    if x < X_MIN:
        code = code | LEFT
    elif x > X_MAX:
        code = code | RIGHT

    if y < Y_MIN:
        code = code | BOTTOM
    elif y > Y_MAX:
        code = code | TOP

    return code


def cohen_sutherland(x1, y1, x2, y2):
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    accept = False

    while True:
        # Case 1: both endpoints are inside
        if code1 == 0 and code2 == 0:
            accept = True
            break

        # Case 2: both endpoints share an outside region
        elif code1 & code2:
            break

        # Case 3: line is partially inside
        else:
            # Choose one outside point
            code_out = code1 if code1 != 0 else code2

            # Find intersection with a boundary
            if code_out & TOP:
                x = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1)
                y = Y_MAX

            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)
                y = Y_MIN

            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)
                x = X_MAX

            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)
                x = X_MIN

            # Replace the outside endpoint
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)

    if accept:
        return x1, y1, x2, y2
    else:
        return None


draw_window()

# Draw original complete line first
draw_line(x1, y1, x2, y2, "lightgray")

# Find clipped line
result = cohen_sutherland(x1, y1, x2, y2)

if result:
    cx1, cy1, cx2, cy2 = result
    draw_line(cx1, cy1, cx2, cy2, "red")

    pen.penup()
    pen.goto(-100, -250)
    pen.pencolor("black")
    pen.write("Gray = Original Line   Red = Visible/Clipped Line",
              font=("Arial", 12, "normal"))
else:
    pen.penup()
    pen.goto(-100, -250)
    pen.pencolor("black")
    pen.write("Line is completely outside the clipping window.",
              font=("Arial", 12, "normal"))

turtle.done()
