"""
    Turtle Graphics - Shooting Game
"""

import turtle
import pygame

"""
    Constants and variables
"""
pygame.init()
pygame.mixer.init(buffer=16)
shoot_sound = pygame.mixer.Sound('dumpling_shoot.wav')
explode_sound = pygame.mixer.Sound('shot.wav')
win_sound= pygame.mixer.Sound('win.wav')
lose_sound=pygame.mixer.Sound('lose.wav')
# General parameters
score=0
cheat_counter=0
window_height = 675
window_width = 800
window_margin = 75
update_interval = 20    # The screen update interval in ms, which is the
                        # interval of running the updatescreen function

# Player's parameters
player_size = 150        # The size of the player image plus margin
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       # The speed the player moves left or right

# Enemy's parameters
enemy_number=26
enemy_size = 70         # The size of the enemy image plus margin
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin
enemy_min_x = enemy_init_x
enemy_max_x = (window_width / 2) - (enemy_size*7)
    # The maximum x coordinate of the first enemy, which will be used
    # to restrict the x coordinates of all other enemies
enemy_hit_player_distance =75
    # The player will lose the game if the vertical
    # distance between the enemy and the player is smaller
    # than this value

# Enemy movement parameters
enemy_speed = 2
enemy_speed_increment =1 
    # The increase in speed every time the enemies move
    # across the window and back
enemy_direction = 1
    #     1 means from left to right and
    #     -1 means from right to left

# The list of enemies
enemies = []

# Laser parameter
laser_speed = 20
laser_hit_enemy_distance = 45
laser_hit_bonus_distance = 50
    # The laser will destory an enemy if the distance
    # between the laser and the enemy is smaller than
    # this value

#bonus parameters
bonus_init_x=window_width / 2 - window_margin
bonus_init_y=window_height / 2 - window_margin

#bonus init
def bonusenemy(): 
    if cheat_counter%2==0:
        bonus.showturtle()
        bonus.goto(bonus_init_x,bonus_init_y)
    turtle.ontimer(bonusenemy, 7000)
    


def cheatcode():
    global cheat_counter
    cheat_counter+=1
"""
    Handle the player movement
"""

# This function is run when the "Left" key is pressed. The function moves the
# player to the left when the player is within the window area
def playermoveleft():

    # Get current player position
    x, y = player.position()

    # Player should only be moved only if it is within the window range
    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)

# This function is run when the "Right" key is pressed. The function moves the
# player to the right when the player is within the window area
def playermoveright():

    # Get current player position
    x, y = player.position()

    # Player should only be moved only if it is within the window range
    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)

"""
    Handle the screen update and enemy movement
"""

# This function is run in a fixed interval. It updates the position of all
# elements on the screen, including the player and the enemies. It also checks
# for the end of game conditions.
def updatescreen():
    # Use the global variables here because we will change them inside this
    # function
    global enemy_direction, enemy_speed, score

    # x and y displacements for all enemies
    dx = enemy_speed*enemy_direction
    dy = 0

    # Perform several actions if the enemies hit the window border
    
    x0 = enemies[0].xcor()
    if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
        # Switch the moving direction
        enemy_direction = -enemy_direction
        dy=-enemy_size/2
        dx = enemy_speed*enemy_direction
        if enemy_direction==1:
            enemy_speed=enemy_speed + enemy_speed_increment

    # Move the enemies according to the dx and dy values determined above

    if(cheat_counter%2==0):
        for enemy in enemies:
            x, y = enemy.position()
            enemy.goto(x + dx, y + dy)
        
    #Change enemy icons every 20 pixels travelled horizontally

            if(x//20)%2==0:
                enemy.shape("patrick.gif") 
            else:
                enemy.shape("patrick1.gif")

    # Perfrom several actions if the laser is visible

    if laser.isvisible():
        # Move the laser
        x, y = laser.position()
        laser.goto(x,y+laser_speed)
        # Hide the laser if it goes beyong the window
        if laser.ycor()>window_height/2:
            laser.hideturtle()
        # Check the laser against every enemy using a for loop
        for enemy in enemies:
            # If the laser hits a visible enemy, hide both of them
            if enemy.isvisible() and laser.distance(enemy)<laser_hit_enemy_distance:
                enemy.hideturtle()
                laser.hideturtle()
                explode_sound.play()

                #update scores  
                score=score+20
                score_string=str(score)
                score_turtle.clear()
                score_turtle.write("SCORE: "+score_string,font=("System", 12, "bold"), align="center")
                break

        #check if bonus killed
        if bonus.isvisible() and laser.distance(bonus)<laser_hit_bonus_distance:
            bonus.hideturtle()
            laser.hideturtle()
            explode_sound.play()

            #update scores  
            score=score+100
            score_string=str(score)
            score_turtle.clear()
            score_turtle.write("SCORE: "+score_string,font=("System", 12, "bold"), align="center")

    #bonus movement       
    if (cheat_counter%2==0):
        if bonus.isvisible():
            x, y = bonus.position()
            bonus.goto(x-5,y)      

    # If one of the enemies is very close to the player, the game will be over
    for enemy in enemies:
        if enemy.ycor()-player.ycor() < enemy_hit_player_distance and enemy.isvisible():
            # Show a message
            gameover("You lose!")
            lose_sound.play()
            # Return and do not run updatescreen() again
            return

    count=0
    for enemy in enemies:
        if enemy.isvisible():
            count+=1
    if count==0:
        gameover("You Win!")
        win_sound.play()
        return
    
    turtle.update()
    turtle.ontimer(updatescreen, update_interval)

"""
    Shoot the laser
"""

def shoot():

    # Shoot the laser only if it is not visible
    if not laser.isvisible():
        laser.showturtle()
        laser.goto(player.position())
        shoot_sound.play()
"""
    Game start
"""
def gamestart(x,y):
    turtle.bgpic("game_background.gif")
    start_button.clear()
    start_button.hideturtle()
    labels.clear()
    opening_turtle.clear()
    rightarrow.hideturtle()
    leftarrow.hideturtle()
    enemy_number_text.clear()
    enemy_number_text.hideturtle()
    # Use the global variables here because we will change them inside this
    # function
    global player, laser, bonus, score_turtle

    #score turtle
    score_turtle=turtle.Turtle()
    score_turtle.up()
    score_turtle.pencolor("white")
    score_turtle.goto(-window_width/2+45,window_height/2-25)
    score_turtle.hideturtle()
    score_turtle.write("SCORE: 0",font=("System", 15, "bold"), align="center")

    ### Player turtle ###

    # Add the spaceship picture
    turtle.addshape("panda.gif")
    #laser picture
    turtle.addshape("dumpling.gif")
    #bonus picture
    turtle.addshape("doge.gif")
    
    # Create the player turtle and move it to the initial position
    player = turtle.Turtle()
    player.shape("panda.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    # Map player movement handlers to key press events
    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")
    turtle.onkeypress(cheatcode,"x")
    turtle.listen()

    ### Enemy turtles ###

    # Add the enemy picture
    turtle.addshape("patrick.gif")
    turtle.addshape("patrick1.gif")

    for i in range(enemy_number):
        # Create the turtle for the enemy
        enemy = turtle.Turtle()
        enemy.shape("patrick.gif")
        enemy.up()

        # Move to a proper position counting from the top left corner
        enemy.goto(enemy_init_x + enemy_size *(i%7), enemy_init_y-enemy_size*(i//7))

        # Add the enemy to the end of the enemies list
        enemies.append(enemy)

    ### Laser turtle ###

    # Create the laser turtle using the square turtle shape
    laser = turtle.Turtle()
    laser.shape("dumpling.gif")
    laser.up()

    # Hide the laser turtle
    laser.hideturtle()

    #bonus turtle
    turtle.addshape("doge.gif")
    bonus=turtle.Turtle()
    bonus.shape("doge.gif")
    bonus.up()
    bonus.hideturtle()
    
    # Part 4.2 - Mapping the shooting function to key press event

    turtle.onkeypress(shoot, "space")
        
    # Part 3.1 - Controlling animation using the timer event
    turtle.ontimer(bonusenemy, 7000)
    turtle.ontimer(updatescreen, update_interval)
    
def decrease_enemy_number(x,y):
    global enemy_number
    if enemy_number>1:
        enemy_number-=1
        enemy_number_text.clear()
        enemy_number_text.write(enemy_number, font=("System", 12, "bold"), align="center")

def increase_enemy_number(x,y):
    global enemy_number
    if enemy_number<49:
        enemy_number+=1
        enemy_number_text.clear()
        enemy_number_text.write(enemy_number, font=("System", 12, "bold"), align="center")
"""
    Game over
"""

# This function shows the game over message.
def gameover(message):

    endmessage=turtle.Turtle()
    endmessage.pencolor("Yellow")
    endmessage.write(message, align="center", font=("System", 30, "bold") )
    endmessage.hideturtle()
    turtle.update()

"""
    Set up main Turtle parameters
"""

# Set up the turtle window
turtle.setup(window_width, window_height)
turtle.tracer(False)
turtle.bgpic("opening_wallpaper.gif")
opening_turtle=turtle.Turtle()
opening_turtle.hideturtle()
opening_turtle.color("yellow","black")
opening_turtle.up()
opening_turtle.goto(0,60)
opening_turtle.write("Killer Dumplings", align="center", font=("System", 30, "bold"))
opening_turtle.goto(-380,-200)
opening_turtle.down()
opening_turtle.begin_fill()

for _ in range(2):
    opening_turtle.forward(760)
    opening_turtle.right(90)
    opening_turtle.forward(110)
    opening_turtle.right(90)
    
opening_turtle.end_fill()
opening_turtle.pencolor("yellow")
opening_turtle.up()
opening_turtle.goto(0,-250)
opening_turtle.write("Use left and right arrow keys to move the awesome panda", align="center", font=("System", 17, "bold"))
opening_turtle.goto(0,-300)
opening_turtle.write("Press space bar to shoot dumplings at the evil starfish", align="center", font=("System", 17, "bold"))

# Start the game
start_button = turtle.Turtle()
start_button.up()
start_button.goto(-40, -165)
start_button.color("White", "DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()
start_button.color("yellow")
start_button.goto(0, -158)
start_button.write("Start", font=("System", 12, "bold"), align="center")
start_button.goto(0,-151)
start_button.shape("square")
start_button.shapesize(1.25,4)
start_button.color("")
start_button.onclick(gamestart)

#enemy spinner
labels=turtle.Turtle()
labels.hideturtle()
labels.up()
labels.goto(-140, -120) # Put the text next to the spinner control
labels.pencolor("black")
labels.write("Number of evil starfishes:", font=("System", 14, "bold"))
enemy_number_text=turtle.Turtle()
enemy_number_text.hideturtle()
enemy_number_text.pencolor("yellow")
enemy_number_text.up()
enemy_number_text.goto(80,-120)
enemy_number_text.write(enemy_number, font=("System", 14, "bold"), align="center")

#left arrow
leftarrow=turtle.Turtle()
leftarrow.up()
leftarrow.shape("arrow")
leftarrow.color("yellow")
leftarrow.shapesize(0.5,1)
leftarrow.left(180)
leftarrow.goto(60,-112)
leftarrow.down()
leftarrow.onclick(decrease_enemy_number)

#rightarrow
rightarrow=turtle.Turtle()
rightarrow.up()
rightarrow.shape("arrow")
rightarrow.color("yellow")
rightarrow.shapesize(0.5,1)
rightarrow.goto(100,-112)
rightarrow.down()
rightarrow.onclick(increase_enemy_number)
turtle.update()

# Switch focus to turtle graphics window
turtle.done()

