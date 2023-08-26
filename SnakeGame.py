import pygame
import random

# Caption Name
NAME = "Snake_Game"
# Initialize game window size
SCREEN = {"width": 640, "Height": 480}
# Snake Size
SNAKE_SIZE = 20
# Snake Speed
LEVEL = 15
# RGB color
BACKGROUND = (0, 0, 0)
SNAKE_BODY_IN = (100, 100, 255)
SNAKE_BODY_OUT = (0, 0, 255)
FOOD_COLOR_OUT = (255, 0, 0)
FOOD_COLOR_IN = (255, 100, 100)
SCORE_COLOR = (255, 255, 255)


# Snake Object
class Snake:
    def __init__(self, window):
        self.window = window
        self.head = {"x": int(SCREEN["width"] / 2), "y": int(SCREEN["Height"] / 2)}
        self.snake_position = [self.head]
        self.tail = self.snake_position[-1]
        self.current_direction = "RIGHT"
        self.game_status = True  # False means GameOver
        self.score = 0
        window.fill(BACKGROUND)

    def Update_Position(self):
        if self.current_direction == "RIGHT":
            self.head = {"x": self.head["x"] + SNAKE_SIZE, "y": self.head["y"]}
        elif self.current_direction == "LEFT":
            self.head = {"x": self.head["x"] - SNAKE_SIZE, "y": self.head["y"]}
        elif self.current_direction == "UP":
            self.head = {"x": self.head["x"], "y": self.head["y"] - SNAKE_SIZE}
        elif self.current_direction == "DOWN":
            self.head = {"x": self.head["x"], "y": self.head["y"] + SNAKE_SIZE}
        if not self.Snake_Collusion():
            self.tail = self.snake_position.pop()
            self.snake_position.insert(0, self.head)
            self.Snake_Draw()

    def Snake_Draw(self):
        pygame.draw.rect(
            self.window,
            BACKGROUND,
            pygame.Rect(self.tail["x"], self.tail["y"], SNAKE_SIZE, SNAKE_SIZE),
        )
        for pos in self.snake_position:
            pygame.draw.rect(
                self.window,
                SNAKE_BODY_OUT,
                pygame.Rect(pos["x"], pos["y"], SNAKE_SIZE, SNAKE_SIZE),
            )
            pygame.draw.rect(
                self.window,
                SNAKE_BODY_IN,
                pygame.Rect(
                    pos["x"] + SNAKE_SIZE / 10,
                    pos["y"] + SNAKE_SIZE / 10,
                    SNAKE_SIZE - SNAKE_SIZE / 5,
                    SNAKE_SIZE - SNAKE_SIZE / 5,
                ),
            )
            pygame.display.flip()

    def Snake_Collusion(self):
        if (
            self.head["x"] in range(0, SCREEN["width"])
            and self.head["y"] in range(0, SCREEN["Height"])
            and not self.head in self.snake_position
        ):
            return False
        else:
            self.game_status = False
            return True


# Food Object
class Food:
    def __init__(self, window):
        self.window = window
        self.position = {
            "x": SCREEN["width"] / 2,
            "y": SCREEN["Height"] / 2 + SNAKE_SIZE,
        }
        pygame.draw.rect(
            self.window,
            FOOD_COLOR_OUT,
            pygame.Rect(self.position["x"], self.position["y"], SNAKE_SIZE, SNAKE_SIZE),
        )
        pygame.draw.rect(
            self.window,
            FOOD_COLOR_IN,
            pygame.Rect(
                self.position["x"] + SNAKE_SIZE / 10,
                self.position["y"] + SNAKE_SIZE / 10,
                SNAKE_SIZE - SNAKE_SIZE / 5,
                SNAKE_SIZE - SNAKE_SIZE / 5,
            ),
        )

    def Food_Spawn(self):
        self.position = {
            "x": random.choice(range(0, SCREEN["width"] - SNAKE_SIZE, SNAKE_SIZE)),
            "y": random.choice(range(0, SCREEN["Height"] - SNAKE_SIZE, SNAKE_SIZE)),
        }

    def draw(self):
        pygame.draw.rect(
            self.window,
            FOOD_COLOR_OUT,
            pygame.Rect(self.position["x"], self.position["y"], SNAKE_SIZE, SNAKE_SIZE),
        )
        pygame.draw.rect(
            self.window,
            FOOD_COLOR_IN,
            pygame.Rect(
                self.position["x"] + SNAKE_SIZE / 10,
                self.position["y"] + SNAKE_SIZE / 10,
                SNAKE_SIZE - SNAKE_SIZE / 5,
                SNAKE_SIZE - SNAKE_SIZE / 5,
            ),
        )


def Key_Board_Event(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.game_status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not snake.current_direction == "LEFT":
                snake.current_direction = "RIGHT"
            elif event.key == pygame.K_LEFT and not snake.current_direction == "RIGHT":
                snake.current_direction = "LEFT"
            elif event.key == pygame.K_UP and not snake.current_direction == "DOWN":
                snake.current_direction = "UP"
            elif event.key == pygame.K_DOWN and not snake.current_direction == "UP":
                snake.current_direction = "DOWN"


def Snake_Eat(window, snake, food):
    if snake.head == food.position:
        snake.snake_position.insert(-1, snake.head)
        snake.score += 1
        window.fill(BACKGROUND)  # clear screen
        # To avoid food spawn inside snake body
        while food.position in snake.snake_position:
            food.Food_Spawn()
        food.draw()


def Score_Display(window, snake, font):
    text = font.render("Score: " + str(snake.score), True, SCORE_COLOR)
    window.blit(text, [0, 0])
    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(NAME)
    font = pygame.font.SysFont("arial", 25)
    window = pygame.display.set_mode((SCREEN["width"], SCREEN["Height"]))
    clock = pygame.time.Clock()
    # Initialize snake object
    snake = Snake(window)
    # Initialize food
    food = Food(window)
    while snake.game_status:
        Snake_Eat(window, snake, food)
        Key_Board_Event(snake)
        snake.Update_Position()
        Score_Display(window, snake, font)
        clock.tick(LEVEL)
    print("Score -", snake.score)
    pygame.quit()