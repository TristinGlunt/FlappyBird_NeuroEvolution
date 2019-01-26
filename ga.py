import numpy as np
import bird as bird_module
import random
import pickle
import operator
from collections import Counter

WINDOW_HEIGHT = 400
save = True


def nextGeneration(totalBirds, birds):
    # in place update of all the birds fitness values, also return max and min fitness
    max_score, min_score = calculate_fitness(birds)
    # generate a mating pool for 50% of birds
    # mating_pool = generate_mating_pool(birds, max_score, min_score)
    newBirds = generate_next_generation(birds)

    """TODO: Rewrite so we keep top 25% performing birds, no mutation. Lower 25% of birds,
            with mutation. 50% of other birds will be generate by breeding..."""

    # not doing any crossover for this demonstration
    # newBirds = []
    # for i in range(totalBirds):
    #     newBirds.append(pickOneBird(mating_pool))

    return newBirds


def pickOneBird(mating_pool):
    bird = random.choice(mating_pool)
    # mutation the birds brain a bit (flipping signs of weights randomly)

    # we won, don't mutate
    if bird.score >= 10000:
        return bird

    bird.mutate(0.1)
    # make new bird but copy this birds brain over to new bird
    newBird = bird_module.Bird(WINDOW_HEIGHT, bird.brain.parameters)
    newBird.score = 0

    return newBird

# in place function to mutate birds fitness values


def calculate_fitness(birds):

    max_score = -9999999
    min_score = 99999999
    sum_score = 0

    # normalize birds scores for fitness values
    for bird in birds:
        sum_score += bird.score
        if bird.score > max_score:
            max_score = bird.score
        if bird.score < min_score:
            min_score = bird.score
        if save:
            pkl_file = open('max_score_all_time', 'rb')
            max_score_all_time = pickle.load(pkl_file)

            if bird.score > max_score_all_time:
                print("Saving new bird with score: " + str(bird.score))
                output = open('best_bird.brain', 'wb')
                best_bird_all_time = bird
                pickle.dump(best_bird_all_time.brain, output)
                output.close()

                output = open('max_score_all_time', 'wb')
                pickle.dump(bird.score, output)
                output.close()
            pkl_file.close()

    for bird in birds:
        bird.fitness = bird.score / max_score

    print("Max score of bird!: " + str(max_score))
    print("Min score of generation: " + str(min_score))
    return max_score, min_score


"""
@generate_mating_pool: Based on the current fitness out of the maximum fitness, we will add
that entity to the mating pool that number of times.
EX: Fitness score = 15, maxFitness = 60, normalized_fitness = 0.25, 0.25 * 100 = 25, thus
there will be 25 adds of this entity. Therefore, the higher the fitness score, the more
likely that entity is to be a parent
"""


def generate_mating_pool(population, max_score, min_score):

    mating_pool = []

    # calculate max fitness in population
    maxFitness = max_score
    minFiness = min_score

    # chance to add a bad fitness score multiple times
    chance_to_add_bad_fitness_score = 0.2

    # normalize current fitness (converting current fitness to be between 0 and 1)
    for i in range(len(population)):
        # conver the # of times to add to an integer from it's fitness val (0, 1)
        num_times_to_add = int(population[i].fitness * 100)
        # we won, don't add anything but the best bird
        if population[i].score >= 10000:
            return [population[i]]
        # add some randomization feature to sometimes add more bad fitness entities
        # NOTE: this add on was a big deal, converging much more often and haven't gone
        # over max recursion depth. Instead go to 200-300 gens when it's not figured out
        # in first 100.
        # if population[i].fitness == minFiness:
        #     ran_num = random.uniform(0, 1)
        #     if ran_num < chance_to_add_bad_fitness_score:
        #         num_times_to_add += 10

        """ this drasically improved overall performance... wasn't picking best bird enough"""
        # if population[i].fitness == maxFitness:
        #     num_times_to_add += 200

        # add this current entity some n times to the mating pool
        for j in range(num_times_to_add):
            mating_pool.append(population[i])

    return mating_pool


def generate_next_generation(birds):

    elite_birds = int((0.65) * len(birds))
    loser_birds = int((0.10) * len(birds))
    mutated_birds = int((0.25) * len(birds))

    new_generation = []

    dict_birds_scores = {}
    for bird in birds:
        dict_birds_scores[bird] = bird.fitness

    # sort dictionary based on fitness
    sorted_birds = sorted(dict_birds_scores.items(), key=lambda kv: kv[1])
    # print(sorted_birds)
    reverse_sorted_birds = dict(list(reversed(sorted_birds)))
    # print(reverse_sorted_birds)
    dict_sorted_birds = dict(sorted_birds)

    # print(sorted_birds)
    counter = 0
    for key, value in dict_sorted_birds.items():
        # append loser birds
        if counter < loser_birds:
            newBird = bird_module.Bird(WINDOW_HEIGHT, key.brain.parameters)
            newBird.score = 0
            new_generation.append(newBird)
        else:
            break
        counter += 1
    print(len(new_generation))

    # reverse list append on elite birds
    counter = 0
    for k, v in reverse_sorted_birds.items():
        if counter < elite_birds:
            newBird = bird_module.Bird(WINDOW_HEIGHT, k.brain.parameters)
            newBird.score = 0
            new_generation.append(newBird)
        else:
            break
        counter += 1

    print(len(new_generation))

    # pick mutated birds
    for i in range(mutated_birds):
        new_generation.append(pickOneBird(birds))

    print(len(new_generation))

    # print(sorted_birds)
    return new_generation


def getBestBirdBrain():
    pkl_file = open('best_bird.brain', 'rb')

    best_brain = pickle.load(pkl_file)
    best_bird = bird_module.Bird(WINDOW_HEIGHT, None)
    best_bird.brain = best_brain

    return best_bird
