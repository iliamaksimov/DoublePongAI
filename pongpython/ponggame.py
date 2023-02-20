import pygame

from .pongpaddle import PongPaddle
from .pongball import PongBall

pygame.init()


class PongInfo:
    """
    Implements game statistics returned at each game main loop iteration.
    """
    def __init__(self, hits_l: int, hits_r: int, score_l: int, score_r: int):
        self.hits_l =hits_l
        self.hits_r = hits_r
        self.score_l = score_l
        self.score_r = score_r


class PongGame:
    """
    Implements actual game functionalities like drawing and moving game objects, restarting the game.
    """

    def __init__(self, window, width, height):
        self.window_width = width
        self.window_height = height

        self.color = (155, 255, 255)
        self.color_back = (0, 0, 0)
        self.color_sp = (255, 0, 0)
        self.font = pygame.font.SysFont("Arial", 40)
        
        self.paddle_vel = 4
        self.paddle_width = 20
        self.paddle_height = 100

        self.ball_radius = 6
        self.ball_vel = 4

        self.paddle_l = PongPaddle(
            5, (self.window_height - self.paddle_height) // 2, self.color, self.paddle_vel, self.paddle_width, self.paddle_height)
        self.paddle_r = PongPaddle(
            self.window_width - self.paddle_width - 5, (self.window_height - self.paddle_height) // 2, self.color, self.paddle_vel, self.paddle_width, self.paddle_height)
        self.ball1 = PongBall(self.window_width // 2, self.window_height // 2, True, self.color, self.ball_radius, self.ball_vel)
        self.ball2 = PongBall(self.window_width // 2, self.window_height // 2, False, self.color, self.ball_radius, self.ball_vel)

        self.score_l = 0
        self.score_r = 0
        self.hits_l = 0
        self.hits_r = 0
        self.window = window

    def _draw_score(self):
        score_l_text = self.font.render(
            f"{self.score_l}", True, self.color)
        score_r_text = self.font.render(
            f"{self.score_r}", True, self.color)
        self.window.blit(score_l_text, (self.window_width // 4 - score_l_text.get_width()//2, 20))
        self.window.blit(score_r_text, (3 * self.window_width // 4 - score_r_text.get_width()//2, 20))

    def _draw_hits(self):
        hits_text = self.font.render(
            f"{self.hits_l + self.hits_r}", True, self.color_sp)
        self.window.blit(hits_text, ((self.window_width - hits_text.get_width())//2, 10))

    def _draw_net(self):
        for i in range(20):
            if i % 2 == 0:
                continue
            pygame.draw.rect(
                self.window, self.color, (self.window_width//2 - 4, i * self.window_height//20, 8, self.window_height//20))

    def _handle_collision(self):
        for ball in [self.ball1, self.ball2]:
            if ball.y + ball.radius >= self.window_height or ball.y - ball.radius <= 0:
                ball.y_vel *= -1

            if ball.x_vel < 0:
                if ball.y >= self.paddle_l.y and ball.y <= self.paddle_l.y + self.paddle_height:
                    if ball.x - ball.radius <= self.paddle_l.x + self.paddle_width:
                        ball.x_vel *= -1

                        y_diff = abs(self.paddle_l.y + self.paddle_height//2 - ball.y)
                        scale = self.paddle_height/2 / ball.vel
                        ball.y_vel = -y_diff // scale
                        self.hits_l += 1

            else:
                if ball.y >= self.paddle_r.y and ball.y <= self.paddle_r.y + self.paddle_height:
                    if ball.x + ball.radius >= self.paddle_r.x:
                        ball.x_vel *= -1

                        y_diff = abs(self.paddle_r.y + self.paddle_height//2 - ball.y)
                        scale = self.paddle_height/2 / ball.vel
                        ball.y_vel = -y_diff // scale
                        self.hits_r += 1

    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.color_back)

        self._draw_net()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.paddle_l, self.paddle_r]:
            paddle.draw(self.window)

        for ball in [self.ball1, self.ball2]:
            ball.draw(self.window)

    def move_paddle(self, left=True, down=True):
        if left:
            if down and self.paddle_l.y + self.paddle_height + self.paddle_vel > self.window_height:
                return False
            if not down and self.paddle_l.y - self.paddle_vel < 0:
                return False
            self.paddle_l.move(down)
        else:
            if down and self.paddle_r.y + self.paddle_height + self.paddle_vel > self.window_height:
                return False
            if not down and self.paddle_r.y - self.paddle_vel < 0:
                return False
            self.paddle_r.move(down)

        return True

    def loop(self):
        for ball in [self.ball1, self.ball2]:
            ball.move()

            if ball.x < 0:
                self.ball1.reset()
                self.ball2.reset()
                self.score_r += 1
            elif ball.x > self.window_width:
                self.ball1.reset()
                self.ball2.reset()
                self.score_l += 1

        self._handle_collision()
        game_info = PongInfo(self.hits_l, self.hits_r, self.score_l, self.score_r)

        return game_info

    def reset(self):
        """Reset the entire game"""
        for ball in [self.ball1, self.ball2]:
            ball.reset()
        self.paddle_l.reset()
        self.paddle_r.reset()
        self.score_l = 0
        self.score_r = 0
        self.hits_l = 0
        self.hits_r = 0
