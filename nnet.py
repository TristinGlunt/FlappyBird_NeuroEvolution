import numpy as np
import random

def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))

class NeuralNetwork(object):
    def __init__(self, layer_dims, parameters):
        self.layer_dims = layer_dims
        if parameters == None:
            self.parameters = {}
            # initialize networks parameters
            self.initialize_parameters()
        else:
            self.parameters = parameters

    def initialize_parameters(self):
        """
        parameters will be a dictionary, each layer contains a weight matrix
        with a weight for each input to every neuron (current_layer, previous layer) (4 neurons, 3 inputs)
        each neuron has 3 weights going to it. each neuron also has a bias initialized to 0
        """
        L = len(self.layer_dims)
        # first weight matrix will be (first_hidden_layer, num_of_inputs)

        for i in range(1, L):
            self.parameters["W" + str(i)] = np.random.uniform(-1, 1, (self.layer_dims[i], self.layer_dims[i-1]))
            self.parameters["b" + str(i)] = np.zeros([self.layer_dims[i], 1]) #needs to be wrapped in a list

        # return parameters

    def forward_propagation(self, X):
        counter = 0
        A = X   # set the last activation output to the inputs, for the first layer
        # print("Input shape: " + str(A.shape))
        L = len(self.parameters) // 2 #important! we only need to loop through half as many parameters there are since W & b, double slash is int divide
        activation_function = "relu"

        # go through each layer except the output layer
        for l in range(1, L):

            A_prev = A #get the last activation output (the inputs for the current layer)

            W = self.parameters["W" + str(l)]
            b = self.parameters["b" + str(l)]

            Z = np.dot(W, A_prev) + b #linear function

            # print("W" + str(l) + " shape: " + str(W.shape))
            # print("A_prev shape " + str(A_prev.shape))
            # print("Z dotted shape " + str(Z.shape))
            # print(Z)

            if(activation_function == "sigmoid"):
                A = sigmoid(Z)
            elif(activation_function == "relu"):
                A = Z

        # print("W" + str(L) + " " + str(self.parameters["W" + str(L)]))
        AL = sigmoid(np.dot(self.parameters["W" + str(L)], A) + self.parameters["b" + str(L)])

        return AL

    def mutate(self, mutate_perc, bird_score):
        L = len(self.parameters) // 2

        # higher the score, the lower the learning rate
        # NOTE: This was a big deal imo. Implement a style of learning rate decay
        # but for GA. That is, the better our simulation does, the less we mutate
        # if we are going to mutate.
        learning_rate = 1 - (bird_score / 10000)

        if bird_score >= 10000:
            learning_rate = 0

        if bird_score < 350:
            mutate_perc = .9

        # loop through each layer
        for i in range(L):

            chance = random.uniform(0, 1)
            shape_of_current_weight_layer = self.parameters["W" + str(i+1)].shape
            total_nums = shape_of_current_weight_layer[0] * shape_of_current_weight_layer[1]
            nums_to_mutate = int(0.1*total_nums)
            # print(shape_of_current_weight_layer)
            if chance < mutate_perc:
                for j in range(nums_to_mutate):
                    # print("MUTATING")

                    row_idx = random.randint(0, shape_of_current_weight_layer[0]-1)
                    col_idx = random.randint(0, shape_of_current_weight_layer[1]-1)
                    random_mutation = random.uniform(-0.2*learning_rate, 0.2*learning_rate)
                    # print(str(row_idx) + " " + str(col_idx))
                    # flip sign of that weight
                    self.parameters["W" + str(i+1)][row_idx][col_idx] += random_mutation
                    # if mutate_perc == 0.9:
                    #     self.parameters["W" + str(i+1)][row_idx][col_idx] = np.random.uniform(-1, 1)

    def train(self, X, y, num_iterations):
        """

        train will implemenet cost functions and back propagation to adjust
        weights

        """

        # initialize networks parameters
        self.initialize_parameters()

        for i in range(num_iterations):
            output = self.forward_propagation(X)
            # the most simple not useful error ever (MSE)
            output_errors = (np.sum(y - output) ** 2) / len(y)
            # will tell us how wrong we are... DO GA STUFF

        # TODO: update parameters here....


    def predict(self, input):
        output = self.forward_propagation(input)
        return output

    def get_params(self):
        return self.parameters

# inputs, hidden layer, output
# nnet_dims = [2, 4, 1]
# X_train = [[0, 0], [0, 1], [1, 0], [1, 1]]
#
# brain = NeuralNetwork(nnet_dims)
# brain.train(np.transpose(X_train), [0, 1, 1, 1], 1)
