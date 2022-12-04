#Importing python libraries
import pygame
import math
from module.edge import Edge
from module.vertex import Vertex

#Defining Algorithms

#Eulerian
def is_eulerian(vertices, edges):
    if(not is_connected(vertices, edges)):
        return False
    for vertex in vertices:
        label = vertex.label
        count = 0
        for edge in edges:
            if(edge.start_label == label or edge.end_label == label):
                count += 1
        if(count % 2 == 1):
            return False
    return True

#Connected
def is_connected(vertices, edges):
    if(len(vertices) == 0): 
        return False

    for vertex in vertices:
        if(all(edge.start_label != vertex.label and edge.end_label != vertex.label for edge in edges)):
            return False
    return True

#Dirac's Hamiltonian Theorem
def dirac_is_hamiltonian(vertices, edges):
    if(not is_connected(vertices, edges)):
        return -1

    for vertex in vertices:
        n = len(vertices)
        label = vertex.label
        count = 0
        for edge in edges:
            if(edge.start_label == vertex.label and edge.end_label == vertex.label):
                count += 1
        if(count < math.floor(n/2)):
            return 0
    return 1

#Ore's Hamiltonian Theorem
def ore_is_hamiltonian(vertices, edges):
    if(not is_connected(vertices, edges)):
        return -1
    
    n = len(vertices)
    for i in range(n):
        for j in range(i, n):
            label1 = vertices[i].label
            label2 = vertices[j].label
            if(not any((edge.start_label == label1 and edge.end_label == label2) or (edge.start_label == label2 and edge.end_label == label1) for edge in edges)):
                count1 = 0
                count2 = 0
                for edge in edges:
                    if(label1 == edge.start_label or label1 == edge.end_label):
                        count1 += 1
                    if(label2 == edge.start_label or label2 == edge.end_label):
                        count2 += 1
                if(count1 + count2 >= n):
                    return 1
    return 0

#Clear screen
def clear_screen():
    pygame.draw.rect(window_surface, BLACK, graph_rect)

    vertices = []
    edges = []

    label = 1
    first_mouse_x = 0
    first_mouse_y = 0
    last_mouse_x = 0
    last_mouse_y = 0
    return vertices, edges, label, first_mouse_x, first_mouse_y, last_mouse_x, last_mouse_y

#Save Graph
def save_graph_image():
    graph_surface = window_surface.subsurface(graph_rect)
    pygame.image.save(graph_surface, file)

#Pygame window dimensions
WIDTH = 900
HEIGHT = 600

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#Other constants
CIRCLE_OFFSET = 10
DELAY = 300
RADIUS = 5

file = "/Users/ayushbanerjee/Documents/graph_image.jpg" #Change the path to save the image file

#Options arrays
options_text = ["CONNECTED", "EULERIAN", "HAMILTONIAN", "SAVE GRAPH", "CLEAR SCREEN"]
options_functions = [is_connected, is_eulerian, dirac_is_hamiltonian]
options_colors = [RED, BLUE, GREEN, YELLOW, WHITE]

#Initializing pygame window
pygame.init()
pygame.display.set_caption("GRAPH THEORY SIMULATOR")
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

#Creating fonts and texts
pygame.font.init()
text_font = pygame.font.SysFont('Comic Sans', 20)
label_font = pygame.font.SysFont('Comic Sans', 10)
add_line_add_text = text_font.render('ADD LINE', False, WHITE)
add_line_remove_text = text_font.render('ADD LINE', False, BLACK)

yes_add_text = text_font.render("YES", False, WHITE)
yes_remove_text = text_font.render("YES", False, BLACK)
no_add_text = text_font.render("NO", False, WHITE)
no_remove_text = text_font.render("NO", False, BLACK)
no_determine_add_text = text_font.render("CANNOT BE DETERMINED", False, WHITE)
no_determine_remove_text = text_font.render("CANNOT BE DETERMINED", False, BLACK)

saved_image_add_text = text_font.render("Saved Image", False, WHITE)
saved_image_remove_text = text_font.render("Saved Image", False, BLACK)

#Defining rectangles
add_lines_rect = pygame.Rect(WIDTH/2 - 30, 0, 100, 30)
button_rect = pygame.Rect(WIDTH - 160, 0, 160, HEIGHT)
graph_rect = pygame.Rect(0, 0, WIDTH - 160, HEIGHT)

#Drawing rectangles
for i in range(len(options_text)):
    pygame.draw.rect(window_surface, options_colors[i], (WIDTH - 160, 120 * i, 160, 120))
    text = text_font.render(options_text[i], False, BLACK)
    window_surface.blit(text, (WIDTH - 160, 120 * i + 60))

#Main function
def main():
    #Setting up game variables
    vertices = []
    edges = []

    is_long_clicked = False
    two_points = True
    running = True
    two_points = True
    is_long_clicked = False

    label = 1
    clicked_button = -1  

    first_mouse_x = 0
    first_mouse_y = 0
    last_mouse_x = 0
    last_mouse_y = 0

    #Game loop
    while running:
        for event in pygame.event.get():
            #Detecting if the quit is button pressed
            if event.type == pygame.QUIT:
                running = False
            #Getting all the mouse down clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                first_mouse_x = pygame.mouse.get_pos()[0]
                first_mouse_y = pygame.mouse.get_pos()[1]
                #Extracting the labels the edges connect
                if(is_long_clicked and not two_points and any(math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS for vertex in vertices)):
                    for vertex in vertices:
                        if (math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS):
                            end_label = vertex.label
                        if (math.hypot(last_mouse_x - vertex.x, last_mouse_y - vertex.y) <= RADIUS):
                            start_label = vertex.label
                    #Drawing the edge and storing it the edges array
                    pygame.draw.line(window_surface, WHITE, (last_mouse_x, last_mouse_y), (first_mouse_x, first_mouse_y), 3)
                    edges.append(Edge(first_mouse_x, first_mouse_y, last_mouse_x, last_mouse_y, start_label, end_label))

                    #Removing the "ADD LINE" text at the top of the window
                    window_surface.blit(add_line_remove_text, (WIDTH/2-30, 0))
                    pygame.draw.rect(window_surface, BLACK, add_lines_rect)

                    two_points = True
                    #Detecting if the algorithm buttons are pressed
                elif(button_rect.collidepoint(pygame.mouse.get_pos())):
                    clicked_button = math.trunc(pygame.mouse.get_pos()[1]/120)
                else:
                    #Getting the time of the down click
                    time1 = pygame.time.get_ticks()
            #Getting all the mouse up clicks
            elif event.type == pygame.MOUSEBUTTONUP:
                #Clear screen
                if(clicked_button == 4):
                    vertices, edges, label, first_mouse_x, first_mouse_y, last_mouse_x, last_mouse_y = clear_screen()
                    clicked_button = -1
                #Save graph image
                elif(clicked_button == 3):
                    save_graph_image()
                    window_surface.blit(saved_image_add_text, (WIDTH/2, 0))
                    pygame.display.update()

                    pygame.time.delay(1000)

                    window_surface.blit(saved_image_remove_text, (WIDTH/2, 0))
                    pygame.display.update()
                elif(clicked_button != -1):
                    #Executing the algorithms
                    if(clicked_button == 2):
                        #Hamiltonian algorithm
                        if(options_functions[clicked_button](vertices, edges) == 1 or ore_is_hamiltonian(vertices, edges) == 1):
                            window_surface.blit(yes_add_text, (WIDTH/2, 0))
                            pygame.display.update()

                            pygame.time.delay(1000)

                            window_surface.blit(yes_remove_text, (WIDTH/2, 0))
                            pygame.display.update()
                        elif(options_functions[clicked_button](vertices, edges) == 0 or ore_is_hamiltonian(vertices, edges) == 0):
                            window_surface.blit(no_determine_add_text, (WIDTH/2, 0))
                            pygame.display.update()

                            pygame.time.delay(1000)

                            window_surface.blit(no_determine_remove_text, (WIDTH/2, 0))
                            pygame.display.update()
                        else:
                            window_surface.blit(no_add_text, (WIDTH/2, 0))
                            pygame.display.update()

                            pygame.time.delay(1000)

                            window_surface.blit(no_remove_text, (WIDTH/2, 0))
                            pygame.display.update()

                    elif(options_functions[clicked_button](vertices, edges)):
                        window_surface.blit(yes_add_text, (WIDTH/2, 0))
                        pygame.display.update()

                        pygame.time.delay(1000)

                        window_surface.blit(yes_remove_text, (WIDTH/2, 0))
                        pygame.display.update()
                    else:
                        window_surface.blit(no_add_text, (WIDTH/2, 0))
                        pygame.display.update()

                        pygame.time.delay(1000)

                        window_surface.blit(no_remove_text, (WIDTH/2, 0))
                        pygame.display.update()
                    clicked_button = -1
                elif(is_long_clicked and two_points):
                    is_long_clicked = False
                    #Detecting a long click meaning an edge will be drawn
                elif (clicked_button == -1 and pygame.time.get_ticks() - time1  >= DELAY and not is_long_clicked and any(math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS for vertex in vertices)):
                    last_mouse_x = pygame.mouse.get_pos()[0]
                    last_mouse_y = pygame.mouse.get_pos()[1]

                    pygame.draw.rect(window_surface, GRAY, add_lines_rect)
                    window_surface.blit(add_line_add_text, (WIDTH/2 - 30, 0))

                    is_long_clicked = True
                    two_points = False
                else:
                    if(two_points):
                        last_mouse_x = pygame.mouse.get_pos()[0]
                        last_mouse_y = pygame.mouse.get_pos()[1]
                        #Making sure the edges do not overlap with the points
                    if(all(math.hypot(vertex.x - last_mouse_x, vertex.y - last_mouse_y) > 2 * RADIUS + CIRCLE_OFFSET for vertex in vertices)):
                        ind = True
                        for line in edges:
                            slope = float((line.end_y - line.start_y) / (line.end_x - line.start_x))
                            y_intercept = line.start_y - slope * line.start_x

                            a = -slope
                            b = 1
                            c = -y_intercept

                            dist = (abs(a * last_mouse_x + b * last_mouse_y + c))/(math.sqrt(a ** 2 + b ** 2))
                            if(dist <= RADIUS + CIRCLE_OFFSET): 
                                ind = False
                                break
                            #Making sure the points do not overlap with each other
                        if(ind and not is_long_clicked and last_mouse_x + RADIUS < WIDTH and last_mouse_x - RADIUS > 0 and last_mouse_y + RADIUS < HEIGHT and last_mouse_y - RADIUS > 0 and not pygame.Rect.collidepoint(add_lines_rect, (last_mouse_x, last_mouse_y)) and not pygame.Rect.collidepoint(button_rect, (last_mouse_x, last_mouse_y))):
                            pygame.draw.circle(window_surface, WHITE, (last_mouse_x, last_mouse_y), RADIUS)
                            vertices.append(Vertex(last_mouse_x, last_mouse_y, label))
                            label_text = label_font.render(str(label), False, WHITE)
                            window_surface.blit(label_text, (last_mouse_x - 12, last_mouse_y - 7.5))
                            label += 1
            pygame.display.update()
    pygame.quit()

#Running the main() function
if __name__ == "__main__":
    main()