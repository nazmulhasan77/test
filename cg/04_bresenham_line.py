import turtle

# =========================
# Screen Setup
# =========================
screen = turtle.Screen()

t = turtle.Turtle()
t.speed(1)
t.pensize(1)


# =========================
# Draw X-Y Axis
# =========================

# X-axis
t.penup()
t.goto(-300, 0)
t.pendown()
t.goto(300, 0)
t.write(" X")

# Y-axis
t.penup()
t.goto(0, -250)
t.pendown()
t.goto(0, 250)
t.write(" Y")


# Manual screen update
screen.tracer(0)


# =========================
# Traditional Bresenham
# =========================

def bresenham(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    p = 2 * dy - dx

    x = x1
    y = y1

    count = 0

    # First point
    t.penup()
    t.goto(x, y)
    t.dot(2, "red")

    count += 1

    while x < x2:

        x = x + 1

        if p < 0:
            p = p + 2 * dy

        else:
            y = y + 1
            p = p + 2 * dy - 2 * dx

        # Draw point
        t.penup()
        t.goto(x, y)
        t.dot(2, "red")

        count += 1

        # Update after every 5 points
        if count % 3 == 0:
            screen.update()
        
        
        # Name first point
        t.penup()
        t.goto(x1 + 5, y1 + 5)
        t.write("A", font=("Arial", 12, "bold"))

        # Name last point
        t.penup()
        t.goto(x2 + 5, y2 + 5)
        t.write("B", font=("Arial", 12, "bold"))

    screen.update()


# =========================
# Manual Input
# =========================

# x1 = int(input("Enter x1: "))
# y1 = int(input("Enter y1: "))
# x2 = int(input("Enter x2: "))
# y2 = int(input("Enter y2: "))


# # =========================
# # Draw Line
# # =========================

# bresenham(x1, y1, x2, y2)
bresenham(-200,-200,200,120)


# Click window to close
screen.exitonclick()