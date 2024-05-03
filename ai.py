import math
import random
import turtle
from queue import PriorityQueue

mn = turtle.Screen()
mn.bgcolor("black")
mn.title("Daino-Maze")
mn.setup(width=800, height=400)  # Set the size of the screen

images = ["dinasour.gif", "meat.gif", "bombleft.gif", "bombright.gif"]

for image in images:
    turtle.register_shape(image)

# Creating Pen
class SquarePen(turtle.Turtle):
    def __init__(self):
        # Initialization of class
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        # Animation Speed

class Win(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("dinasour.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.hint_arrow = turtle.Turtle()  # Create a turtle for hint arrow
        self.hint_arrow.hideturtle()  # Hide the hint arrow initially
        self.hint_arrow.color("yellow")
        self.hint_arrow.penup()
        self.hint_arrow.speed(0)

    def go_up(self):
        # Calculating spot to move
        move1_to_x = self.xcor()
        move1_to_y = self.ycor() + 23

        # Checking if next position is a wall
        if (move1_to_x, move1_to_y) not in walls:
            self.goto(move1_to_x, move1_to_y)

    def go_down(self):
        # Calculating spot to move
        movee_to_x = self.xcor()
        movee_to_y = self.ycor() - 23

        # Checking if next position is a wall
        if (movee_to_x, movee_to_y) not in walls:
            self.goto(movee_to_x, movee_to_y)

    def go_left(self):
        # Calculating spot to move
        move2_to_x = self.xcor() - 23
        move2_to_y = self.ycor()

        # Checking if next position is a wall
        if (move2_to_x, move2_to_y) not in walls:
            self.goto(move2_to_x, move2_to_y)

    def go_right(self):
        # Calculating spot to move
        move_to_x = self.xcor() + 23
        move_to_y = self.ycor()

        # Checking if next position is a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

    def get_nearest_enemy(self):
        nearest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            distance = math.sqrt((self.xcor() - enemy.xcor()) ** 2 + (self.ycor() - enemy.ycor()) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        return nearest_enemy

    def get_direction_to_enemy(self):
        enemy = self.get_nearest_enemy()
        if enemy:
            dx = enemy.xcor() - self.xcor()
            dy = enemy.ycor() - self.ycor()

            # Calculate the angle between player and enemy
            angle = math.atan2(dy, dx) * (180 / math.pi)
            if angle < 0:
                angle += 360

            # Determine direction based on angle
            if 45 <= angle < 135:
                return "up"
            elif 135 <= angle < 225:
                return "left"
            elif 225 <= angle < 315:
                return "down"
            else:
                return "right"
        else:
            return None

    def move_hint(self):
        direction_to_enemy = self.get_direction_to_enemy()
        if direction_to_enemy:
            print("Hint: Move", direction_to_enemy, "to avoid the enemy")
            # Draw arrow based on the direction to move
            self.draw_arrow(direction_to_enemy)
        else:
            self.hint_arrow.clear()  # Clear the arrow if no enemy nearby

    def draw_arrow(self, direction):
        self.hint_arrow.clear()  # Clear previous arrow
        if direction == "up":
            self.hint_arrow.setheading(90)  # Set arrow direction
            self.hint_arrow.goto(self.xcor(), self.ycor() + 30)  # Move to player position + offset
            self.hint_arrow.showturtle()  # Show arrow
            self.hint_arrow.stamp()  # Draw arrow
        elif direction == "down":
            self.hint_arrow.setheading(270)
            self.hint_arrow.goto(self.xcor(), self.ycor() - 30)
            self.hint_arrow.showturtle()
            self.hint_arrow.stamp()
        elif direction == "left":
            self.hint_arrow.setheading(180)
            self.hint_arrow.goto(self.xcor() - 30, self.ycor())
            self.hint_arrow.showturtle()
            self.hint_arrow.stamp()
        elif direction == "right":
            self.hint_arrow.setheading(0)
            self.hint_arrow.goto(self.xcor() + 30, self.ycor())
            self.hint_arrow.showturtle()
            self.hint_arrow.stamp()

def get_neighbors(pos):
    x, y = pos
    return [(x + 23, y), (x - 23, y), (x, y + 23), (x, y - 23)]

def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("bombleft.gif")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
        self.move()  # Start enemy movement using A* search

    # A* search algorithm to find the shortest path to the player
    def a_star_search(self, player_x, player_y):
        frontier = PriorityQueue()
        frontier.put((0, (self.xcor(), self.ycor())))  # Priority queue with (priority, position)
        came_from = {}
        cost_so_far = {}
        came_from[(self.xcor(), self.ycor())] = None
        cost_so_far[(self.xcor(), self.ycor())] = 0

        while not frontier.empty():
            current_cost, current_pos = frontier.get()

            if current_pos == (player_x, player_y):
                break

            for next_pos in get_neighbors(current_pos):
                new_cost = cost_so_far[current_pos] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + distance((next_pos[0], next_pos[1]), (player_x, player_y))
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current_pos

        path = []
        current_pos = (player_x, player_y)
        while current_pos != (self.xcor(), self.ycor()):
            path.append(current_pos)
            current_pos = came_from[current_pos]
        path.reverse()
        return path

    def move(self):
        dx, dy = 0, 0
        # Get the player's current position
        player_pos = (player.xcor(), player.ycor())

        # Use A* search to find the shortest path to the player
        path_to_player = self.a_star_search(player_pos[0], player_pos[1])

        if path_to_player:
            # Get the next position in the path
            next_pos = path_to_player[0]

            # Calculate the direction to move
            if next_pos[0] > self.xcor():
                self.direction = "right"
            elif next_pos[0] < self.xcor():
                self.direction = "left"
            elif next_pos[1] > self.ycor():
                self.direction = "up"
            elif next_pos[1] < self.ycor():
                self.direction = "down"

            # Change shape based on direction
            if self.direction == "right":
                self.shape("bombright.gif")
            elif self.direction == "left":
                self.shape("bombleft.gif")

        if self.direction == "up":
            dy = 23
        elif self.direction == "down":
            dy = -23
        elif self.direction == "left":
            dx = -23
        elif self.direction == "right":
            dx = 23

        # Calculate new position
        new_x = self.xcor() + dx
        new_y = self.ycor() + dy

        # Check if new position is not a wall
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

        # Schedule next move
        turtle.ontimer(self.move, t=random.randint(1000, 3000))

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("meat.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

# Creating List of Levels
levels = [""]

level_1 = [
    "XXXXXXXXXXXXX PXXXXXXXXXXXXXXXXX",
    "X           X                  X",
    "X   XXX  X  X                  X",
    "X     X  X  X  XXXX  X  XXXX   X",
    "X     X  X     X     X     X   X",
    "XXXX  XXXXXXXXXXXXXXXXT XXXXE  X",
    "X   E    XE   T   X     XT     X",
    "XE       X  X     X     X      X",
    "X  XXXXXXX  XXXX  XXXXXXX  X   X",
    "X        X     X  X     X  X   X",
    "X        X     X  X     X  X   X",
    "X   X  XXXXXX  X  X  XXXX  XXXXX",
    "X   X       X  X     ET XE     X",
    "X   XTE     X  X        X T    X",
    "X   XXXXXX  X  XXXXXXX  XXXX E X",
    "X   X       X  X        X  X   X",
    "X   X       X  X        X  X   X",
    "X   XXXXXXXXX  X  XXXX  X  X   X",
    "X    TE  XE    X  X  X   E XE  X",
    "X        X     X  X  XE    XT  X",
    "XXXXXXXT X  XXXXT X  XXXX  X   X",
    "X           XE    XE    X  X  EX",
    "X           X     X     X  X   X",
    "X  X  XXXXXXX  XXXX     X  X   X",
    "X  XE    X  X  X     X     X   X",
    "X  X     X  X  X     XE    X   X",
    "XXXX     X  X  XXXX  X  XXXXE  X",
    "X E   X     X     X  X     T   X",
    "X     X     X     X  X         X",
    "XXXXXXXXXXXXXXXX--XXXXXXXXXXXXXX"]


level_2= [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X           X                  X",
    "X   XXX  X  X      X           X",
    "X     X  X  X  XXXX  X  XXXX   X",
    "X     X  X     X     X     X   X",
    "XXXX  XXXXXXXXXX PXXXXXXXXXXXXXX",
    "X   E    XE   T   X     X      X",
    "XE       X  X     X     X      X",
    "X  XXXXXXX  XXXX  XXXXXXX  X   X",
    "X        X     X  X     X  X   X",
    "X        X     X  X     X  X   X",
    "X   X  XXXXXX  X  X  XXXX  XXXXX",
    "X   X       X  X     ET XE     X",
    "X   XTE     X  X        X      X",
    "X   XXXXXX  X  XXXXXXX  XXXX E X",
    "X   X       X  X        X  X   X",
    "X   X       X  X        X  X   X",
    "X   XXXXXXXXX  X  XXXX  X  X   X",
    "X    TE  XE    X  X  X   E XE  X",
    "X        X     X  X  XE    X   X",
    "XXXXXXXT X  XXXXT X  XXXX  X   X",
    "X           XE    XE    X  X  EX",
    "X           X     X     X  X   X",
    "X  X  XXXXXXX  XXXX     X  X   X",
    "X  XE    X  X  X     X     X   X",
    "X  X     X  X  X     XE    X   X",
    "XXXX     X  X  XXXX  X  XXXXE  X",
    "X E   X     X     X  X         X",
    "X     X     X     X  X         X",
    "XXXXXXXXXXXXXXXX--XXXXXXXXXXXXXX"]

# Treasure List
treasures = []

# Enemy list
enemies = []

wins = []

levels.extend([level_1, level_2])

def set_maze(levels):
    for y in range(len(levels)):
        for x in range(len(levels[y])):
            char = levels[y][x]
            screen_x = -370 + (x * 23)
            screen_y = 325 - (y * 23)

            if char == 'X':
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            elif char == '-':
                wins.append(Win(screen_x, screen_y))
            elif char == 'P':
                player.goto(screen_x, screen_y)
            elif char == 'T':
                treasures.append(Treasure(screen_x, screen_y))
            elif char == 'E':
                enemies.append(Enemy(screen_x, screen_y))

pen = SquarePen()
player = Player()

# Walls Coordinate list
walls = []

set_maze(levels[1])

# Keyboard Binding
turtle.listen()
turtle.onkey(player.go_left, "a")
turtle.onkey(player.go_right, "d")
turtle.onkey(player.go_down, "s")
turtle.onkey(player.go_up, "w")
mn.tracer(0)

# Main Game loop
while True:
    # Check for player collision with treasure
    for treasure in treasures:
        if player.collision(treasure):
            player.gold += treasure.gold
            print("**Player gold:", int(format(player.gold)))
            # Destroy the treasure
            treasure.destroy()
            # Remove the Treasure from list
            treasures.remove(treasure)

    for enemy in enemies:
        if player.collision(enemy):
            turtle.color("red")  # Set color to white
            turtle.write("You Lost!", align="center", font=("Arial", 24, "bold"))
            turtle.done()
        else:
            player.move_hint()  # Display hint if enemy is nearby

    for win in wins:
        if player.collision(win):
            turtle.color("blue")  # Set color to white
            turtle.write("Level Completed!", align="center", font=("Arial", 24, "bold"))
            turtle.done()

    mn.update()
