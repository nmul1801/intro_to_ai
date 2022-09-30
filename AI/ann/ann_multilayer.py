import numpy as np
import random
import math
from numpy.core.fromnumeric import argmax
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

class Edge():
    def __init__(self, source, dest):
        self.w = random.uniform(0.01, 0.1)
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
    x = np.delete(data, -1, axis=1)
    scaler = MinMaxScaler().fit(x)
    x_train = scaler.transform(x)

    return x_train, y_train, scaler

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def create_NN(amt_hidden):

    sep_l = Neuron('sepal length')
    sep_w = Neuron('sepal width')
    petal_l = Neuron('petal length')
    petal_w = Neuron('petal width')

    hidden_layer = list()

    for i in range(amt_hidden):
        new_hidden = Neuron('hidden N ' + str(i + 1))
        hidden_layer.append(new_hidden)

    setosa = Neuron('Iris Setosa')
    versicolor = Neuron('Iris Versicolour')
    virginica = Neuron('Iris Virginica')

    input_layer = [sep_l, sep_w, petal_l, petal_w]

    output_layer = [setosa, versicolor, virginica]

    for input in input_layer: # connect input to output layer
        for hidden_n in hidden_layer:
            new_edge = Edge(input, hidden_n)
            input.output_edges.append(new_edge)
            hidden_n.input_edges.append(new_edge)

    for i, hidden_n in enumerate(hidden_layer): # connect hidden layer to output layer
        for j, output in enumerate(output_layer):
            new_edge = Edge(hidden_n, output)
            hidden_n.output_edges.append(new_edge)
            output.input_edges.append(new_edge)

    bias = Neuron('Bias')
    bias.output = 1

    for hidden_n in hidden_layer: # connect bias to hidden layer
        new_edge = Edge(bias, hidden_n)
        bias.output_edges.append(new_edge)
        hidden_n.input_edges.append(new_edge)

    for output_n in output_layer: # connect bias to output layer
        new_edge = Edge(bias, output_n)
        bias.output_edges.append(new_edge)
        output_n.input_edges.append(new_edge)

    return input_layer, hidden_layer, output_layer, bias

def convert_output(num):
    output = np.zeros(3)
    output[int(num)] = 1
    return output

def compute_err_o(output_n, correct):
    e_o = correct - output_n.output
    g_o = output_n.output * (1 - output_n.output)
    err = e_o * g_o
    return err

def computer_err_h(h_neuron):
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
        product = alpha * output_n * err
        curr_edge.w = curr_edge.w + product

def run_network(network, data):
    input_layer, hidden_layer, output_layer = network[0], network[1], network[2]
    for j, curr_n in enumerate(input_layer): # assign inputs to each input neuron
        curr_n.output = data[j]

    for j, curr_h in enumerate(hidden_layer):
        input_edgs = curr_h.input_edges
        sum = 0
        for edge in input_edgs:
            sum += edge.source.output * edge.w
        curr_h.output = sigmoid(sum)
    
    for j, curr_o in enumerate(output_layer):
        input_edgs = curr_o.input_edges
        sum = 0
        for edge in input_edgs:
            sum += edge.source.output * edge.w
        curr_o.output = sigmoid(sum)

    output = [curr.output for curr in output_layer]
    return output

x, y, scaler = preprocess('irisdata.txt')

input_layer, hidden_layer, output_layer, bias = create_NN(15)
network = [input_layer, hidden_layer, output_layer, bias]

### TRAINING NETWORK ###

for k in range(500):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    for i, data_pt in enumerate(x_train):
        
        correct_output = convert_output(y_train[i])

        ### FORWARD PROPOGATION ###
        
        output = run_network(network, data_pt)

        for j, curr_o in enumerate(output_layer): # assign inputs to each input neuron
            curr_o.output = output[j]

        ### BACK PROPOGATION ###

        for j, curr_o in enumerate(output_layer):
            curr_o.err = compute_err_o(curr_o, correct_output[j])
        
        for j, curr_h in enumerate(hidden_layer):
            curr_h.err = computer_err_h(curr_h)

        ### WEIGHT UPDATES ###

        for j, curr_o in enumerate(output_layer):
            update_incoming_weights(0.1, curr_o)

        for j, curr_h in enumerate(hidden_layer):
            update_incoming_weights(0.1, curr_h)

    ### VALIDATING NETWORK ###

    total_train = 0
    total_test = 0

    for i, run in enumerate(x_train):
        output = run_network(network, run)
        predicted = np.argmax(output)
        if predicted == y_train[i]:
            total_train += 1

    for i, run in enumerate(x_test):
        output = run_network(network, run)
        predicted = np.argmax(output)
        if predicted == y_test[i]:
            total_test += 1

    train_acc = total_train / len(x_train)
    test_acc = total_test / len(x_test)
    if (k + 1) % 50 == 0:
        print("Epoch " + str(k + 1) + ": ")
        print("Train Accuracy: " + str(int(train_acc * 100)) + "%", end = ", ")
        print("Test Accuracy: " + str(int(test_acc * 100)) + "%")


print()
dec = input("Would you like to input your own data? (y/n) ")

if dec == 'y':
    while True:
        sep_len = float(input('Sepal length: '))
        sep_wid = float(input('Sepal width: '))
        petal_len = float(input('Petal length: '))
        petal_wid = float(input('Petal width: '))

        inp = [[sep_len, sep_wid, petal_len, petal_wid]]

        inp_tran = scaler.transform(inp)

        output = run_network(network, inp_tran[0])
        prediction = argmax(output)
        prob = max(output) / sum(output)
        print()
        print('Network prediction: ', end = '') 
        if prediction == 0:
            print('Setosa', end = ' ')
        elif prediction == 1:
            print('Versicolor', end = ' ')
        else:
            print('Virginica', end = ' ')

        print('with probability of ' + str(int(prob * 100)) + '%')
        print()

        choice = input("Would you like to continue? (y/n) ")

        if choice == 'n':
            break