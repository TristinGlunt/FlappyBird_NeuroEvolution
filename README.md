# FlappyBird_NeuroEvolution
Flappy bird game with agents controlled by neural networks using genetic algorithms

## How to run:
`python flappy_bird.py -t 'best'` or
`python flappy_bird.py -t 'train'`

where the `'best'` flag will be the single best bird to have played the game of
all time stored in `best_bird.brain` and their score in `max_score_all_time`.
and the `'train'` flag will be the entire population of birds training from
scratch.

## Purpose:

The following repository is a Flappy Bird game designed in PyGame. The game
engine is not the point of the repository. This repo is to demonstrate neural 
networks with genetic algorithms as the key learning mechanism instead of the 
canonical back-propagation methods.

This repo was a side-project I decided to implement after falling deeply
interested in genetic algorithms and neural networks. I always thought it
would be extremely interesting to train an AI with no specific rules to beat
some type of game. The choice of Flappy Bird was truthfully the first game
that came to mind and demonstrates no particular expertise.

As you will see, I spent little to no time on the aesthetics of the game engine.
Most time was spent ensuring the fundamental physics and rules of the game were
implemented. Following this, the rest of the time was spent developing the
neural network, which I refer to as the `brain.py` and also the genetic algorithm
in `ga.py`.

## Genetic algorithms:

Genetic algorithms are especially interesting for learning mechanisms as they
take a biology approach to learning, instead of a mathematical way in which
no actual organism uses.

The genetic algorithm is based on multiple papers I read for a survey on genetic
algorithms for training Spiking Neural Networks. One of the papers is the following:
"Evolving Spiking Neural Networks of artificial creatures using Genetic Algorithm,"
E. Eskandari, et. al.

Essentially, the algorithm calculates the fitness for each bird based on the birds
score in the game. It then sorts the birds by their fitness, the lowest score
being the worst bird and the highest score being the elite bird. The next generation
will have 65% elite birds, where each elite bird is a unique bird starting from
the very best bird and working backwards. 10% of the next generation will also
be loser birds, where each loser bird is a unique bird starting from the very
worst bird working forwards. The last 25% of the next generation will be randomly
mutated birds. We will randomly pick birds from throughout the entire population,
and there will be a slight chance, currently 10% that their brain (neural net)
is randomly mutated. However, if a bird that had a score of above 10,000 is chosen,
they will be guaranteed to not be mutated, as they have essentially beaten the game.

## How long to train new generation:

It really depends on the random started values, as good random values for the
weights of the neural network can surprisingly perform well with little to no
training. But, this is random and not guaranteed, thus, usually 10+ generations
will start to show a great increase in performance, and you can certainly get
birds that score high in thousands with less than that (I've seen 4k+ score with
only 2 generation iterations).
