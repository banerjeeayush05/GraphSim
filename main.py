import pygame
import math
from module.edge import Edge
from module.vertex import Vertex



WIDTH = 600
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

CIRCLE_OFFSET = 10
DELAY = 300
RADIUS = 5

clear_screen_rect = pygame.Rect(0, HEIGHT - 30, 160, 30)
add_lines_rect = pygame.Rect(WIDTH/2-30, 0, 100, 30)

vertices = []
edges = []

def check_in_vertex(vertices, x_coord, y_coord):
    vertex_label = -1
    for i in range(len(vertices)):
        if(math.hypot(vertices[i].x - x_coord, vertices[i].y - y_coord) <= RADIUS):
            vertex_label = vertices[i].label
            break
    return vertex_label

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAPH THEORY SIMULATOR")

pygame.font.init()
text_font = pygame.font.SysFont('Comic Sans', 20)
label_font = pygame.font.SysFont('Comic Sans', 10)

add_line_text = text_font.render('ADD LINE', False, WHITE)
add_line_remove_text = text_font.render('ADD LINE', False, BLACK)
clear_screen_text = text_font.render('CLEAR SCREEN', False, WHITE)

def main():
    running = True
    is_long_clicked = False
    two_points = True
    clear_button_check = False

    first_mouse_x = 0
    first_mouse_y = 0
    last_mouse_x = 0
    last_mouse_y = 0

    label = 1

    pygame.draw.rect(screen, GRAY, clear_screen_rect)
    screen.blit(clear_screen_text, (5, HEIGHT-30))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                first_mouse_x = pygame.mouse.get_pos()[0]
                first_mouse_y = pygame.mouse.get_pos()[1]
                if(is_long_clicked and not two_points and any(math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS for vertex in vertices)):
                    for vertex in vertices:
                        if (math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS):
                            end_label = vertex.label
                        if (math.hypot(last_mouse_x - vertex.x, last_mouse_y - vertex.y) <= RADIUS):
                            start_label = vertex.label
                    pygame.draw.line(screen, WHITE, (last_mouse_x, last_mouse_y), (first_mouse_x, first_mouse_y), 3)
                    edges.append(Edge(first_mouse_x, first_mouse_y, last_mouse_x, last_mouse_y, start_label, end_label))

                    screen.blit(add_line_remove_text, (WIDTH/2-30, 0))
                    pygame.draw.rect(screen, BLACK, add_lines_rect)

                    two_points = True
                elif(0 <= pygame.mouse.get_pos()[0] <= 130 and HEIGHT - 30 <= pygame.mouse.get_pos()[1] <= HEIGHT):
                    screen.fill(BLACK)
                    clear_button_check = True
                else:
                    time1 = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONUP:
                if(clear_button_check):
                    pygame.draw.rect(screen, GRAY, clear_screen_rect)
                    screen.blit(clear_screen_text, (5, HEIGHT-30))
                    clear_button_check = False

                    vertices.clear()
                    edges.clear() 

                    is_long_clicked = False
                    two_points = True
                    clear_button_check = False
                    label = 1

                    first_mouse_x = 0
                    first_mouse_y = 0
                    last_mouse_x = 0
                    last_mouse_y = 0
                elif(is_long_clicked and two_points):
                    is_long_clicked = False
                elif (pygame.time.get_ticks() - time1  >= DELAY and not is_long_clicked and any(math.hypot(first_mouse_x - vertex.x, first_mouse_y - vertex.y) <= RADIUS for vertex in vertices)):
                    last_mouse_x = pygame.mouse.get_pos()[0]
                    last_mouse_y = pygame.mouse.get_pos()[1]

                    pygame.draw.rect(screen, GRAY, add_lines_rect)
                    screen.blit(add_line_text, (WIDTH/2 - 30, 0))

                    is_long_clicked = True
                    two_points = False
                else:
                    if(two_points):
                        last_mouse_x = pygame.mouse.get_pos()[0]
                        last_mouse_y = pygame.mouse.get_pos()[1]
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
                        if(ind and not is_long_clicked and last_mouse_x + RADIUS < WIDTH and last_mouse_x - RADIUS > 0 and last_mouse_y + RADIUS < HEIGHT and last_mouse_y - RADIUS > 0 and not pygame.Rect.collidepoint(clear_screen_rect, (last_mouse_x, last_mouse_y)) and not pygame.Rect.collidepoint(add_lines_rect, (last_mouse_x, last_mouse_y))):
                            pygame.draw.circle(screen, WHITE, (last_mouse_x, last_mouse_y), RADIUS)
                            vertices.append(Vertex(last_mouse_x, last_mouse_y, label))
                            label_text = label_font.render(str(label), False, WHITE)
                            screen.blit(label_text, (last_mouse_x - 15, last_mouse_y - 7.5))
                            label += 1
            pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()