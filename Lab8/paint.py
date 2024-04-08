import pygame


class DrawingApplication:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 640))
        self.clock = pygame.time.Clock()
        self.radius_size = 20
        self.current_mode = 'red'
        self.color_map = {'r': (255, 0, 0), 'g': (0, 255, 0), 'b': (0, 0, 255), 'y': (255, 255, 0)}
        self.coordinates = []
        self.draw_triangle = False
        self.draw_circle = False
        self.draw_rectangle = True

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_keyboard_events(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.button)
                if event.type == pygame.MOUSEMOTION:
                    self.coordinates.append(event.pos)
                    self.coordinates = self.coordinates[-256:]

            self.draw_canvas()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_keyboard_events(self, key):
        if key == pygame.K_c:  # Clear points
            self.coordinates.clear()
        elif key == pygame.K_t:  # Set drawing mode to triangle
            self.draw_triangle = True
            self.draw_circle = False
            self.draw_rectangle = False
        elif key == pygame.K_o:  # Set drawing mode to circle
            self.draw_circle = True
            self.draw_triangle = False
            self.draw_rectangle = False
        elif key == pygame.K_p:  # Set drawing mode to rectangle
            self.draw_circle = False
            self.draw_triangle = False
            self.draw_rectangle = True
        elif key == pygame.K_r:  # Set drawing mode to red
            self.current_mode = 'red'
        elif key == pygame.K_g:  # Set drawing mode to green
            self.current_mode = 'green'
        elif key == pygame.K_b:  # Set drawing mode to blue
            self.current_mode = 'blue'
        elif key == pygame.K_y:  # Set drawing mode to yellow
            self.current_mode = 'yellow'

    def handle_mouse_click(self, button):
        key_unicode = pygame.key.name(button).lower()
        if key_unicode in self.color_map:
            self.current_color = self.color_map[key_unicode]
        if button == pygame.BUTTON_LEFT:
            self.radius_size = min(200, self.radius_size + 1)
        elif button == pygame.BUTTON_RIGHT:
            self.radius_size = max(1, self.radius_size - 1)

    def draw_canvas(self):
        self.window.fill((0, 0, 0))

        i = 0
        while i < len(self.coordinates) - 1:
            self.draw_line(i, self.coordinates[i], self.coordinates[i + 1])
            i += 1

    def draw_line(self, index, start, end):
        color = self.calculate_color(index)

        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))

        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0])
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            if self.draw_circle:
                pygame.draw.circle(self.window, color, (x, y), self.radius_size)
            elif self.draw_triangle:
                vertices = [(x, y), (x + self.radius_size, y + self.radius_size), (x - self.radius_size, y + self.radius_size)]
                pygame.draw.polygon(self.window, color, vertices)
            elif self.draw_rectangle:
                rect_width = 5
                rect_x, rect_y = x - 50, y - 37.5
                rect_size = (100, 75)
                pygame.draw.rect(self.window, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]))
                pygame.draw.rect(self.window, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]),
                                 rect_width)

    def calculate_color(self, index):

        if self.current_mode == 'blue':
            return self.color_map['b']
        elif self.current_mode == 'red':
            return self.color_map['r']
        elif self.current_mode == 'green':
            return self.color_map['g']
        elif self.current_mode == 'yellow':
            return self.color_map['y']


if __name__ == "__main__":
    app = DrawingApplication()
    app.start()

