"""
SEEsod
Kuba Calik
ICS-4U1
Submitted to Mr.Ferreira
"""
#Initialize libraries and pygame screen
import pygame
import random
import math

pygame.init()
pygame.mixer.init()

#Introduce all scripts

from Contents.Scripts import player, barriers, bullet, background, sodlings, menus

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
display_screen = pygame.Surface((300, 300))

pygame.display.set_caption("SEEsod")
pygame.display.set_icon(pygame.image.load("Contents/Sprites/Menu/icon.png").convert_alpha())

font = pygame.font.Font("Contents/Typeface/soddy.otf", 15)
font_mini = pygame.font.Font("Contents/Typeface/soddy.otf", 10)
font_sized = pygame.font.Font("Contents/Typeface/soddy.otf", 12)
font_side = pygame.font.Font("Contents/Typeface/soddy.otf", 20)
font_big = pygame.font.Font("Contents/Typeface/soddy.otf", 22)
font_biggest = pygame.font.Font("Contents/Typeface/soddy.otf", 30)
font_fredoka = pygame.font.Font("Contents/Typeface/fredoka.ttf", 10)

clock = pygame.time.Clock()
tick = 0


#Define all game functions and methods
bullets_group = pygame.sprite.Group()
bullet_indicators = []
bullet_spawn_delay = 50
sodling_group = pygame.sprite.Group()
sodling_count = 0

top_barrier = barriers.GameBarriers(0, 70, screen_width/2, 5, (255, 255, 255))
bottom_barrier = barriers.GameBarriers(0, 230, screen_width/2, 5, (255, 255, 255))

top_barrier.movement(top_barrier, 2.5, tick, "set-position", 0, 145)
bottom_barrier.movement(bottom_barrier, 2.5, tick, "set-position", 0, 155)

key_cooldown = 0
screen_shake = 0

player = player.Player(145, 115, 0.45)

level = 1
score = 0
level_score = 0
clear_score = 1000
score_increase = 1
best_score = 0

bullets_spawned = 0
games_played = 0

game_state = "intro"
running = True

#Define Spawn Events
BULLETEVENT = pygame.USEREVENT + 0
pygame.time.set_timer(BULLETEVENT, 1250)

SODLINGEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SODLINGEVENT, 4000)

background = background.BackgroundManager(None, display_screen)
background.new_palette()
#Define all UI Functions and Variables
menu_selections = ["start", "options", "statistics", "credits", "exit"]
mode_selections = ["tutorial", "classic", "no sodling", "hardcore"]
flavor_texts = [
    ["Choose a mode and start the game!", "Configure the settings!", "Look at your stats!", "See the wonderful creator", "Leave it all"], #Main Menu
    ["Learn the Basics!", "The Standard Experience", "Play without those little sods", "One Life, One Chance"]
]
tutorial_texts = [
    ["Welcome to SeeSOD!", "(SurvivE Every Shape Or Die)", 3000, 20, 15],
    ["Let's learn the basics", "Simple and Sweet", 5000, 20, 15],
    ["Use WASD to move!", "or the arrow keys!", 3000, 20, 15],
    ["Above you is the score", "The longer you survive, the more you get", 7000, 20, 12],
    ["Bullets will spawn", "Dodge them! You have three lives!", 8000, 20, 12],
    ["Collect sodlings to survive", "Any more than two will kill you", 6000, 18, 12],
    ["I think you are ready", "Top those leaderboards", 4000, 20, 15]
]
start_hint_x, start_key_x, intro_fade, intro_slide = 105, 90, 255, False
current_selection = 0
current_mode_selection = 0
key_direction, key_direction_target = 0.0, 0.0
leaderboard_width = 5
current_name = ["A", "A", "A", "A"]
current_letter = 0
tutorial_count, tutorial_time = 0, 0


def Intro():
    global top_barrier, bottom_barrier, start_hint_x, start_key_x, intro_fade
    
    start_hint = font_biggest.render("Press", False, (255, 255, 255))
    start_key = font_big.render("E to Start", False, (255, 255, 255))

    if intro_slide and game_state == "intro":
        start_hint_x += 5
        start_key_x -= 5

        if top_barrier.y >= 80:
            top_barrier.y -= 1
        if bottom_barrier.y <= 220:
            bottom_barrier.y += 1
        if intro_fade > 0:
            intro_fade -= 5

    top_barrier.movement(top_barrier, 0.2, tick, "sine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "sine")

    alpha_surface = pygame.Surface(display_screen.get_size(), pygame.SRCALPHA)
    alpha_surface.fill((0, 0, 0, intro_fade))

    display_screen.blit(alpha_surface, (0, 0))
    display_screen.blit(start_hint, (start_hint_x, top_barrier.y-40))
    display_screen.blit(start_key, (start_key_x, bottom_barrier.y+15))


def Menu_Screen():
    global top_barrier, bottom_barrier, current_selection, key_direction, key_direction_target

    top_barrier.movement(top_barrier, 0.2, tick, "sine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "sine")

    up_arrow = pygame.image.load("Contents/Sprites/Menu/up_arrow.png")
    down_arrow = pygame.image.load("Contents/Sprites/Menu/down_arrow.png")

    key_direction += (key_direction_target - key_direction) * 0.4
    if abs(key_direction_target - key_direction) < 0.5:
        key_direction_target = 0

    current_menu_selection = font_big.render(menu_selections[current_selection], False, (255, 255, 255))
    menu_choice = font_sized.render("Main Menu", False, (255, 255, 255))
    flavor_text = font_sized.render(flavor_texts[0][current_selection], False, (255, 255, 255))

    display_screen.blit(menu_choice, ((display_screen.get_width() // 2) - (menu_choice.get_width() // 2), top_barrier.y+15))
    display_screen.blit(current_menu_selection, ((display_screen.get_width() // 2) - (current_menu_selection.get_width() // 2) + math.sin(tick) * 3, 140+key_direction))
    display_screen.blit(flavor_text, ((display_screen.get_width() // 2) - (flavor_text.get_width() // 2), bottom_barrier.y-20))
    display_screen.blit(up_arrow, ((display_screen.get_width() // 2) - (up_arrow.get_width() // 2), top_barrier.y+40))
    display_screen.blit(down_arrow, ((display_screen.get_width() // 2) - (up_arrow.get_width() // 2), bottom_barrier.y-50))


def Options_Screen():
    top_barrier.movement(top_barrier, 0.2, tick, "cosine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "cosine")

    version_number = font_sized.render("Current Version: V.1.0.1", False, (255, 255, 255))
    controls = font_fredoka.render("Game Controls: WASD or Arrow Keys", False, (255, 255, 255))
    menu_controls = font_fredoka.render("Menu Controls: Enter to Select, Escape to Exit", False, (255, 255, 255))

    current_menu_selection = font.render(menu_selections[current_selection], False, (255, 255, 255))
    display_screen.blit(version_number, ((display_screen.get_width() // 2) - (version_number.get_width() // 2), bottom_barrier.y-25))
    display_screen.blit(controls, ((display_screen.get_width() // 2) - (controls.get_width() // 2), top_barrier.y+45))
    display_screen.blit(menu_controls, ((display_screen.get_width() // 2) - (menu_controls.get_width() // 2), top_barrier.y+55))
    pygame.draw.rect(display_screen, (255, 255, 255), [(display_screen.get_width() // 2) - (80 // 2), top_barrier.y+35, 80, 2])
    display_screen.blit(current_menu_selection, ((display_screen.get_width() // 2) - (current_menu_selection.get_width() // 2), top_barrier.y+15))


def Statistics_Screen():
    top_barrier.movement(top_barrier, 0.2, tick, "cosine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "cosine")


    stat_bullets_spawned = font_fredoka.render("Bullets Spawned: " + str(bullets_spawned), False, (255, 255, 255))
    stat_games_played = font_fredoka.render("Games Played (All Modes): " + str(games_played), False, (255, 255, 255))

    display_screen.blit(stat_bullets_spawned, ((display_screen.get_width() // 2) - (stat_bullets_spawned.get_width() // 2), top_barrier.y+45))
    display_screen.blit(stat_games_played, ((display_screen.get_width() // 2) - (stat_games_played.get_width() // 2), top_barrier.y+55))


    current_menu_selection = font.render(menu_selections[current_selection], False, (255, 255, 255))
    pygame.draw.rect(display_screen, (255, 255, 255), [(display_screen.get_width() // 2) - (80 // 2), top_barrier.y+35, 80, 2])
    display_screen.blit(current_menu_selection, ((display_screen.get_width() // 2) - (current_menu_selection.get_width() // 2), top_barrier.y+15))


def Credits_Screen():
    top_barrier.movement(top_barrier, 0.2, tick, "cosine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "cosine")

    current_menu_selection = font.render(menu_selections[current_selection], False, (255, 255, 255))
    creator = font_sized.render("This game was created by: ", False, (255, 255, 255))
    logo = pygame.image.load("Contents/Sprites/Menu/logo-bright.png")

    pygame.draw.rect(display_screen, (255, 255, 255), [(display_screen.get_width() // 2) - (80 // 2), top_barrier.y+35, 80, 2])
    display_screen.blit(current_menu_selection, ((display_screen.get_width() // 2) - (current_menu_selection.get_width() // 2), top_barrier.y+15))
    display_screen.blit(creator, ((display_screen.get_width() // 2) - (creator.get_width() // 2), top_barrier.y+40))
    display_screen.blit(logo, ((display_screen.get_width() // 2) - (logo.get_width() // 2), top_barrier.y+60))


def Mode_Select():
    global top_barrier, bottom_barrier, current_mode_selection, key_direction, key_direction_target
    background.mode = "sine"

    top_barrier.movement(top_barrier, 0.2, tick, "sine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "sine")

    up_arrow = pygame.image.load("Contents/Sprites/Menu/up_arrow.png")
    down_arrow = pygame.image.load("Contents/Sprites/Menu/down_arrow.png")

    key_direction += (key_direction_target - key_direction) * 0.4
    if abs(key_direction_target - key_direction) < 0.5:
        key_direction_target = 0

    current_menu_selection = font_big.render(mode_selections[current_mode_selection], False, (255, 255, 255))
    menu_choice = font_sized.render("Game Mode", False, (255, 255, 255))
    flavor_text = font_sized.render(flavor_texts[1][current_mode_selection], False, (255, 255, 255))

    display_screen.blit(menu_choice, ((display_screen.get_width() // 2) - (menu_choice.get_width() // 2), top_barrier.y+15))
    display_screen.blit(current_menu_selection, ((display_screen.get_width() // 2) - (current_menu_selection.get_width() // 2) + math.sin(tick) * 3, 140+key_direction))
    display_screen.blit(flavor_text, ((display_screen.get_width() // 2) - (flavor_text.get_width() // 2), bottom_barrier.y-20))
    display_screen.blit(up_arrow, ((display_screen.get_width() // 2) - (up_arrow.get_width() // 2), top_barrier.y+40))
    display_screen.blit(down_arrow, ((display_screen.get_width() // 2) - (up_arrow.get_width() // 2), bottom_barrier.y-50))


def Game_Over():
    global leaderboard_width, tick, score, current_letter, key_cooldown, current_mode_selection
    #Read the current leaderboard
    current_top = []
    current_leaderboard = open("Contents/Data/Leaderboards/"+mode_selections[current_mode_selection]+".txt", "r")
    for line in current_leaderboard:
        line = line.strip()
        if "," in line:
            name, leaderboard_score = line.split(",", 1)
            name.strip()
            leaderboard_score.strip()
            current_top.append((int(leaderboard_score), name))
    current_top = sorted(current_top, key=lambda x: int(x[0]), reverse=True)[:10]
    display_screen.fill((255, 255, 255))

    #Move player to correct resting position
    end_area = (35, 150)
    unit_x = player.x - end_area[0]
    unit_y = player.y - end_area[1]
    magnitude = math.sqrt(unit_x ** 2 + unit_y ** 2)

    if player.x != 35 and player.y != 150:
        player.x -= ((unit_x) / magnitude) * 2
        player.y -= ((unit_y) / magnitude) * 2
        player.rect.x -= ((unit_x) / magnitude) * 2
        player.rect.y -= ((unit_y) / magnitude) * 2
    player.update([0, 0], top_barrier, bottom_barrier, bullets_group)
    player.display(display_screen)

    #Game Over Screen
    gameover_text = font_big.render("Game Over", False, (0, 0, 0))
    leaderboard_text = font.render("Leaderboard", False, (255, 255, 255))
    score_notifier = font_sized.render("Your Score", False, (0, 0, 0))
    leaderboard_next = font_sized.render("Press Enter to continue", False, (0, 0, 0))
    score_text = font.render(str(score), False, (0, 0, 0))
    tutorial_done = font.render("Tutorial Complete", False, (0, 0, 0))
    score_updater = font_sized.render("New Top Score!", False, (0, 0, 0))

    if player.x <= 40 and 150 <= player.y <= 180:
        if mode_selections[current_mode_selection] != "tutorial":
            player.state = "alive"
            if leaderboard_width <= 85:
                leaderboard_width += 1
            display_screen.blit(score_notifier, (15, player.y-60))
            pygame.draw.rect(display_screen, (0, 0, 0), [15, player.y-45, 80, 2])
            display_screen.blit(score_text, (player.x-15, player.y-30+math.sin(tick)*2))
            pygame.draw.rect(display_screen, (0, 0, 0), [195, 45+math.sin(tick)*3, leaderboard_width, 220])
            pygame.draw.rect(display_screen, (0, 0, 0), [195-leaderboard_width, 45+math.sin(tick)*3, leaderboard_width, 220])
            display_screen.blit(leaderboard_text, (140, 50+math.sin(tick)*3))
            pygame.draw.rect(display_screen, (255, 255, 255), [130, 67+math.sin(tick)*3, 130, 2])
            
            for i in range(10):
                rank_text = font.render(str(i+1) + ". " + current_top[i][1] + " - " + str(current_top[i][0]), False, (255, 255, 255))
                rank_offset = 70 + i * 18
                display_screen.blit(rank_text, (115, rank_offset + math.sin(tick) * 3))

            if score > current_top[9][0]:   
                for i in range(4):
                    name_up_arrow = pygame.image.load("Contents/Sprites/Menu/up_arrow-black.png").convert_alpha()
                    name_down_arrow = pygame.image.load("Contents/Sprites/Menu/down_arrow-black.png").convert_alpha()
                    color = "#72cbcf" if i == current_letter else (0, 0, 0)
                    letters = font.render(current_name[i], False, color)
                    letter_offset = 15 + i * 18
                    display_screen.blit(name_up_arrow, (letter_offset-2, 165+math.sin(tick)))
                    display_screen.blit(name_down_arrow, (letter_offset-2, 200-math.sin(tick)))
                    display_screen.blit(letters, (letter_offset, 180))
                    display_screen.blit(score_updater, (0, 220+math.sin(tick)))
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and key_cooldown == 0:
                    pygame.mixer.Sound.play(sound_effects[0])
                    current_letter = max(0, current_letter - 1)
                    key_cooldown = 15
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and key_cooldown == 0:
                    pygame.mixer.Sound.play(sound_effects[0])
                    current_letter = min(3, current_letter + 1)
                    key_cooldown = 15
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and key_cooldown == 0:
                    pygame.mixer.Sound.play(sound_effects[0])
                    key_cooldown = 5
                    current = ord(current_name[current_letter])
                    current = current + 1 if current < ord('Z') else ord('A')
                    current_name[current_letter] = chr(current)
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and key_cooldown == 0:
                    pygame.mixer.Sound.play(sound_effects[0])
                    key_cooldown = 5
                    current = ord(current_name[current_letter])
                    current = current - 1 if current > ord('A') else ord('Z')
                    current_name[current_letter] = chr(current)

                if keys[pygame.K_RETURN] and key_cooldown == 0 and player.x <= 40:
                    key_cooldown = 15
                    name_str = "".join(current_name)
                    
                    # Add current score and name to leaderboard list
                    current_top.append((int(score), name_str))
                    
                    # Sort the leaderboard, keeping only the top 10
                    current_top = sorted(current_top)[::-1][:10]
                    
                    # Save back to file
                    with open("Contents/Data/Leaderboards/" + mode_selections[current_mode_selection] + ".txt", "w") as leaderboard_file:
                        for entry in current_top:
                            leaderboard_file.write(f"{entry[1]},{entry[0]}\n")
                    current_mode_selection = 0
            else:
                score_updater = font_sized.render("Cannot qualify!", False, (0, 0, 0))
                display_screen.blit(score_updater, (0, 220+math.sin(tick)))
        else:
            display_screen.blit(tutorial_done, ((display_screen.get_width() // 2) - (gameover_text.get_width() // 2), 150+math.cos(tick)*2))

    display_screen.blit(gameover_text, ((display_screen.get_width() // 2) - (gameover_text.get_width() // 2), 10+math.sin(tick)*2))
    display_screen.blit(leaderboard_next, ((display_screen.get_width() // 2) - (leaderboard_next.get_width() // 2), 280+math.sin(tick)*2))
    
    

def Cleanup():
    global sodling_count, player, game_state, bullet_patterns
    sodling_count = 0
    player.lives = 3
    for i in [bullets_group, sodling_group]:
        for v in i:
            v.kill()
    bullet_patterns = [bullet.t_pattern]
    bullet_indicators.clear()
    sodling_group.empty()
    bullets_group.empty()
    


def Tutorial():
    global tutorial_count, game_state, tutorial_time
    
    current_time = pygame.time.get_ticks()

    if tutorial_time == 0:
        tutorial_time = current_time

    # Get current step
    current_line = tutorial_texts[tutorial_count]
    main_tip = pygame.font.Font("Contents/Typeface/soddy.otf", current_line[3]).render(current_line[0], False, (255, 255, 255))
    side_tip = pygame.font.Font("Contents/Typeface/soddy.otf", current_line[4]).render(current_line[1], False, (255, 255, 255))
    display_screen.blit(main_tip, ((display_screen.get_width() // 2) - (main_tip.get_width() // 2), 125))
    display_screen.blit(side_tip, ((display_screen.get_width() // 2) - (side_tip.get_width() // 2), 145))

    # Check if time has passed
    if current_time - tutorial_time >= current_line[2]:
        if tutorial_count+1 >= len(tutorial_texts):
            game_state = "gameover"
            Cleanup()
        else:
            tutorial_count += 1
            tutorial_time = 0 
        if tutorial_count == 4:
            bullet_indicators.append([80, 180, "a", bullet_spawn_delay])
            bullet_indicators.append([220, 180, "a", bullet_spawn_delay])
        if tutorial_count == 5:
            sodling_group.add(sodlings.Sodling(80, 180))
            sodling_group.add(sodlings.Sodling(220, 180))


def Jukebox(track):
    pygame.mixer.music.load(music[track])
    pygame.mixer.music.play(-1, fade_ms=4000)

music = {
    0:"Contents/Audio/Music/menu.mp3", #Title Screen
    1:"Contents/Audio/Music/game.mp3",
    2:"Contents/Audio/Music/over.mp3"
}

sound_effects = [
    pygame.mixer.Sound("Contents/Audio/Sounds/scroll.mp3"),
    pygame.mixer.Sound("Contents/Audio/Sounds/back.mp3"),
    pygame.mixer.Sound("Contents/Audio/Sounds/spawn.mp3"),
    pygame.mixer.Sound("Contents/Audio/Sounds/high_score.mp3")
]


bullet_patterns = []
Jukebox(0)
while running:
    movement = [0, 0]
    render_offset = [0, 0]

    keys = pygame.key.get_pressed()

    #Update and Draw Graphics
    background.update()

    clear_score = 1000 + level * 100

    if level_score >= clear_score:
        level += 1
        background.new_palette()
        background.objects_shape.clear()
        background.mode = random.choice(["color_bars", "spiral", "sine", "shapes", "smear", "flag", "static", "sine16"])
        bullet_spawn = max(425, 1250 - (level * 25))
        sodling_spawn = max(2, 4000 - (level * 25))
        pygame.time.set_timer(BULLETEVENT, bullet_spawn)
        level_score = level_score - clear_score

    #Update game based off events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == BULLETEVENT and game_state == "game" and mode_selections[current_mode_selection] != "tutorial":
            bullets_spawned += 4
            random_x, random_y = bullet.random_bullet_spawn(top_barrier, bottom_barrier)
            bullet_indicators.append([random_x, random_y, "a", bullet_spawn_delay])
        
        if event.type == SODLINGEVENT and game_state == "game" and mode_selections[current_mode_selection] != "no sodling" and mode_selections[current_mode_selection] != "tutorial":
            sodling_group.add(sodlings.Sodling(random.randint(20, 280), random.uniform(top_barrier.y + 40, bottom_barrier.y - 40)))
            sodling_count += 1

    #Gather keys and relay movement
    if game_state == "game":
        if movement[0] != 0 and movement[1] != 0:
            movement[0] *= 0.7071
            movement[1] *= 0.7071
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement[1] = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement[1] = 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement[0] = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement[0] = -1
    
    screen_shake = max(0, screen_shake - 1)
    key_cooldown = max(0, key_cooldown - 1)
    
    if screen_shake:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4 
    
    #Game State Manager
    if game_state == "intro":
        background.mode = "sine"
        Intro()
        if keys[pygame.K_e] and key_cooldown == 0:
            key_cooldown = 15
            intro_slide = True
        if top_barrier.y <= 80 and bottom_barrier.y >= 220 and intro_fade <= 0:
            game_state = "menu"

    #Update game area bounds
    game_area = barriers.GameBarriers(0, top_barrier.y+5, screen_width/2, bottom_barrier.y-(top_barrier.y+4), (0, 0, 0))
    top_barrier.display(display_screen)
    bottom_barrier.display(display_screen)
    game_area.display(display_screen)
    
    if game_state == "menu":
        Menu_Screen()
        background.mode = "sine"
        if keys[pygame.K_RETURN] and key_cooldown == 0:
            pygame.mixer.Sound.play(sound_effects[1])
            screen_shake = 15
            game_state = menu_selections[current_selection]
            key_cooldown = 15
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and key_cooldown == 0:
            pygame.mixer.Sound.play(sound_effects[0])
            key_direction_target = -10
            current_selection = (current_selection - 1) % len(menu_selections)
            key_cooldown = 15
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and key_cooldown == 0:
            pygame.mixer.Sound.play(sound_effects[0])
            key_direction_target = 10
            current_selection = (current_selection + 1) % len(menu_selections)
            key_cooldown = 15
    
    #Update screen depending on selection
    if game_state in menu_selections:
        if keys[pygame.K_ESCAPE] or keys[pygame.K_BACKSPACE]:
            pygame.mixer.Sound.play(sound_effects[1])
            current_selection = 0
            screen_shake = 15
            top_barrier.movement(top_barrier, 2.5, tick, "set-position", 0, 80)
            bottom_barrier.movement(bottom_barrier, 2.5, tick, "set-position", 0, 220)
            game_state = "menu"
    
    if game_state == "start":
        Mode_Select()
        if keys[pygame.K_RETURN] and key_cooldown == 0:
            pygame.time.set_timer(BULLETEVENT, 1250)
            pygame.mixer.Sound.play(sound_effects[1])
            screen_shake = 15
            Jukebox(1)
            game_state = mode_selections[current_mode_selection] #Chnage to correct mode
            player.rect.x = 145
            player.rect.y = 180
            player.x = player.rect.x
            player.y = player.rect.y
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and key_cooldown == 0:
            pygame.mixer.Sound.play(sound_effects[0])
            key_direction_target = -10
            current_mode_selection = (current_mode_selection - 1) % len(mode_selections)
            key_cooldown = 15
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and key_cooldown == 0:
            pygame.mixer.Sound.play(sound_effects[0])
            key_direction_target = 10
            current_mode_selection = (current_mode_selection + 1) % len(mode_selections)
            key_cooldown = 15
    if game_state == "options":
        Options_Screen()
    if game_state == "statistics":
        Statistics_Screen()
    if game_state == "credits":
        Credits_Screen()
    if game_state == "exit":
        pygame.quit()
    
    if game_state in mode_selections:
        if mode_selections[current_mode_selection] == "hardcore":
            player.lives = 1
        if mode_selections[current_mode_selection] == "tutorial":
            tutorial_count = 0
        games_played += 1
        game_state = "game"
    
    if mode_selections[current_mode_selection] == "tutorial" and game_state == "game":
        Tutorial()

    if game_state == "gameover":
        Game_Over()
        if keys[pygame.K_RETURN]:
            Jukebox(0)
            key_cooldown = 15
            game_state = "menu"
            score = 0
            level_score = 0
            clear_score = 1000
            level = 1
            score_increase = 1

    #Game conditionals for ending the game
    if sodling_count == 3:
        player.lives = 0

    if pygame.sprite.spritecollide(player, bullets_group, True) and game_state == "game" and player.state != "invincible":
        screen_shake = 35
        player.state = "invincible"
        top_barrier.movement(top_barrier, 2.5, "sine", tick)
        bottom_barrier.movement(bottom_barrier, 2.5, "sine", tick)
        
    if player.lives <= 0:
        player.state = "dead"
        game_state = "gameover"
        pygame.time.set_timer(BULLETEVENT, 0)
        score_increase = 0
        player.state = "end"
        Cleanup()
        Jukebox(2)
    
    #Draw and Update all game mechanics
    if game_state == "game":
        if level == 1 and not bullet.t_pattern in bullet_patterns:
            bullet_patterns.append(bullet.t_pattern)

        if level == 4 and not bullet.x_pattern in bullet_patterns:
            bullet_patterns.append(bullet.x_pattern)
        
        if level == 12 and not bullet.closer_right in bullet_patterns and not bullet.closer_left in bullet_patterns:
            bullet_patterns.append(bullet.closer_right)
            bullet_patterns.append(bullet.closer_left)
        
        if level == 18 and not bullet.line_pattern in bullet_patterns:
            bullet_patterns.append(bullet.line_pattern)
        
        if level == 22 and not bullet.sine_pattern in bullet_patterns and not bullet.cosine_pattern in bullet_patterns and mode_selections[current_mode_selection] == "hardcore":
            bullet_patterns.append(bullet.sine_pattern)
            bullet_patterns.append(bullet.cosine_pattern)

    
        bullets_group.update(display_screen, top_barrier, bottom_barrier, tick)
        bullets_group.draw(display_screen)

        sodling_group.draw(display_screen)

        #Spawn bullets with respective indicators
        for indicator in bullet_indicators:
            indicator_x, indicator_y, indicator_type, delay = indicator

            pygame.draw.circle(display_screen, (255, 0, 0), (indicator_x, indicator_y), 5)

            indicator[3] -= 1
            if indicator[3] <= 0:
                random.choice(bullet_patterns)(indicator_x, indicator_y, bullets_group)
                bullet_indicators.remove(indicator)
        
        player.update(movement, top_barrier, bottom_barrier, bullets_group)
        player.display(display_screen)

        scoretext = font.render(str("{:06d}".format(math.floor(score))), False, (255, 255, 255))
        score_transparency = scoretext.set_alpha(int(math.sqrt((((display_screen.get_width() // 2) - player.x) ** 2 + (((top_barrier.y + 10) - player.y) ** 2)))) * 3 + 10)
        display_screen.blit(scoretext, ((display_screen.get_width()//2)-25, top_barrier.y + 10))

        lives_display = pygame.image.load("Contents/Sprites/Game/heart-white.png").convert_alpha()
        lives_display.set_alpha(int(math.sqrt((((display_screen.get_width() // 2)+100 - player.x) ** 2 + (((top_barrier.y + 10) - player.y) ** 2)))) * 3 + 50)
        for i in range(player.lives):
            display_screen.blit(lives_display, ((display_screen.get_width()//2)+80+ 20*i, top_barrier.y + 10))
        
        
        for sodling in sodling_group:
            if player.rect.colliderect(sodling):
                sodling_count -= 1
                score += 400
                level_score += 400
                sodling.kill()
        
        score += score_increase * level
        level_score += score_increase * level

    screen.blit(pygame.transform.scale(display_screen, screen.get_size()), render_offset)    
    pygame.display.update()
    clock.tick(60)
    tick += 0.1
