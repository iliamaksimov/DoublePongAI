import pygame
from pongpython import PongGame
import neat
import os
import pickle


class PongGameAI:
    def __init__(self, window, width, height):
        self.game = PongGame(window, width, height)
        self.paddle_l = self.game.paddle_l
        self.paddle_r = self.game.paddle_r
        self.ball1, self.ball2 = self.game.ball1, self.game.ball2
        pygame.display.set_caption("Pong! Player - left side, AI - right side")

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.game.move_paddle(left=True, down=True)
            if keys[pygame.K_a]:
                self.game.move_paddle(left=True, down=False)

            if self.ball1.x < self.ball2.x:
                ball_l  = self.ball1 
                ball_r = self.ball2  
            else:
                ball_l = self.ball2
                ball_r = self.ball1

            output = net.activate(
                (self.paddle_r.y, ball_r.y, abs(self.paddle_r.x - ball_r.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, down=False)
            else:
                self.game.move_paddle(left=False, down=True)

            stats = self.game.loop()
            self.game.draw(True, True)
            pygame.display.flip()

        pygame.quit()

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if self.ball1.x < self.ball2.x:
                ball_l  = self.ball1 
                ball_r = self.ball2  
            else:
                ball_l = self.ball2
                ball_r = self.ball1

            output1 = net1.activate(
                (self.paddle_l.y, ball_l.y, abs(self.paddle_l.x - ball_l.x)))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.move_paddle(left=True, down=False)
            else:
                self.game.move_paddle(left=True, down=True)

            output2 = net2.activate(
                (self.paddle_r.y, ball_r.y, abs(self.paddle_r.x - ball_r.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_paddle(left=False, down=False)
            else:
                self.game.move_paddle(left=False, down=True)

            stats = self.game.loop()

            #self.game.draw(draw_score=False, draw_hits=True)
            #pygame.display.flip()

            if stats.score_l >= 1 or stats.score_r >= 1 or stats.hits_l > 50:
                self.calculate_fitness(genome1, genome2, stats)
                break

    def calculate_fitness(self, genome1, genome2, stats):
        genome1.fitness += stats.hits_l
        genome2.fitness += stats.hits_r


def eval_genomes(genomes, config):
    width, height = 680, 480
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGameAI(window, width, height)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    ### p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-0')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes, 100)
    with open("best1.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_ai(config):
    width, height = 640, 480
    window = pygame.display.set_mode((width, height))

    with open("best1.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGameAI(window, width, height)
    game.test_ai(winner, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    #run_neat(config)
    test_ai(config)
