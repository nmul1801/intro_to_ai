Nicholas Mulligan
CS 131 - Intro To AI

ASSUMPTIONS
The learning rate I chose for the network was 0.1 with 15 neurons on the hidden layer. The network is fully 
connected, meaning every neuron in the input layer is connected to every neuron in the hidden layer, and every neuron 
in the hidden layer is connected to every neuron in the the output layer. The data was scaled using the MinMaxScaler 
library from sklearn, and the data arrays were created using the numpy library. The weights were initialized 
randomly with a number between 0.01 and 0.1. The training for the data used the train_test_split function 
from the sklearn library. With each epoch, the data was split randomly, with 20% of the data being reserved 
for validation purposes, and 80% of the data being reserved for training. After using the training data to train 
the network, the network was then tested, or validated, reporting whether the model had improved.

After 500 epochs, the user is then prompted as to whether they would prefer to enter their own data about
a given flower to see what type of iris it is. They can repeat a query as many times as they'd like to, until 
they choose to respond with a 'n', which exits the program.