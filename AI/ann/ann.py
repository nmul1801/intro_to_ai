import numpy as np
import random
import math
from numpy.core.fromnumeric import argmax
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# 4 attirbutes, 3 categories
# for each input, the output should be an array of three probs, one for each category
# so we gotta convery the y_train to an array, too for the training

class Edge():
    def __init__(self, source, dest, rand, num):
        if rand:
            self.w = random.uniform(0.01, 0.1)
        else:
            self.w = num
        self.source = source
        self.dest = dest

class Neuron():
    def __init__(self, name):
        self.name = name
        self.output = 0
        self.input_edges = list()
        self.output_edges = list()
        self.err = 0


def type_to_num(iris_type):
    iris_type = iris_type.decode("utf-8")
    if iris_type == 'Iris-setosa':
        return 0
    elif iris_type == 'Iris-versicolor':
        return 1
    else:
        return 2

def preprocess(filename):
    data = np.loadtxt(filename, delimiter=',', converters={4: type_to_num})
    y_train = data[:,-1]
    x_train = np.delete(data, -1, axis=1)
    x_train = MinMaxScaler().fit_transform(x_train)

    return x_train, y_train

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def create_NN(random_weights, start_w):

    sep_l = Neuron('sepal length')
    sep_w = Neuron('sepal width')
    petal_l = Neuron('petal length')
    petal_w = Neuron('petal w')

    setosa = Neuron('Iris Setosa')
    versicolor = Neuron('Iris Versicolour')
    virginica = Neuron('Iris Virginica')

    input_layer = [sep_l, sep_w, petal_l, petal_w]

    output_layer = [setosa, versicolor, virginica]

    for input in input_layer: # connect input to output layer
        for output in output_layer:
            new_edge = Edge(input, output, random_weights, start_w)
            input.output_edges.append(new_edge)
            output.input_edges.append(new_edge)

    return input_layer, output_layer

def print_network(output_layer):
    print("OUTPUT LAYER INPUT: ")
    for output in output_layer:
        for edge in output.input_edges:
            print(edge.source.name, "---", edge.w, "----> ", edge.dest.name)
        print()

def convert_output(num):
    output = np.zeros(3)
    output[int(num)] = 1
    return output

def compute_err_output_layer(output, correct):
    e_o = correct - output
    g_o = output * (1 - output)
    err = e_o * g_o
    return err

def compute_err_hidden_layer(h_neuron):
    g_o = h_neuron.output * (1 - h_neuron.output)
    e_o = 0
    for out_edge in h_neuron.output_edges:
        w = out_edge.w
        curr_err = out_edge.dest.err
        e_o += curr_err * w
    err = g_o * e_o
    return err

def update_incoming_weights(alpha, neuron):
    err = neuron.err
    for i, curr_edge in enumerate(neuron.input_edges):
        output_n = curr_edge.source.output
        input_w = curr_edge.w
        product = alpha * output_n * err
        curr_edge.w = input_w + product

def run_network(input_layer, output_layer, data):
    for j, curr_n in enumerate(input_layer): # assign inputs to each input neuron
        curr_n.output = data[j]
    
    for j, curr_o in enumerate(output_layer):
        input_edgs = curr_o.input_edges
        sum = 0
        for edge in input_edgs:
            sum += edge.source.output * edge.w
        curr_o.output = sigmoid(sum)

    output = [curr.output for curr in output_layer]
    return output


x, y = preprocess('irisdata.txt')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

choice = input("Welcome! Would you like to choose a learning rate? (Default is 1) (y/n) ")
alpha = int(input("Enter the learning rate: ")) if choice == 'y' else 1

choice = input("Would you like to initalize the weights randomly or input a uniform weight distribution? (r: random / u: uniform) ")
random_weights = True if choice == 'r' else False
start_w = float(input("Enter a uniform weight: ")) if not random_weights else 0

input_layer, output_layer = create_NN(random_weights, start_w)

### TRAINING NETWORK ###

for k in range(20):
    for i, data_pt in enumerate(x_train):
        
        correct_output = convert_output(y_train[i])

        ### FORWARD PROPOGATION ###
        
        output = run_network(input_layer, output_layer, data_pt)

        print(output)

        for j, curr_o in enumerate(output_layer): # assign inputs to each input neuron
            curr_o.output = output[j]

        ### BACK PROPOGATION ###

        for j, curr_o in enumerate(output_layer):
            curr_o.err = compute_err_output_layer(curr_o.output, correct_output[j])

        ### WEIGHT UPDATES ###

        for j, curr_o in enumerate(output_layer):
            update_incoming_weights(alpha, curr_o)

### TESTING NETWORK ###

total_train = 0
total_test = 0

for i, run in enumerate(x_train):
    output = run_network(input_layer, output_layer, run)
    predicted = np.argmax(output)
    if predicted == y_train[i]:
        total_train += 1

for i, run in enumerate(x_test):
    output = run_network(input_layer, output_layer, run)
    predicted = np.argmax(output)
    if predicted == y_test[i]:
        total_test += 1

train_acc = total_train / len(x_train)
test_acc = total_test / len(x_test)

print("Train Acc: " + str(train_acc))
print("Test Acc: " + str(test_acc))