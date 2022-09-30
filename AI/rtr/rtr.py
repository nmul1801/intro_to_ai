import numpy as np
from matplotlib import pyplot as plt
import math

# load data
data = np.loadtxt('data.txt', delimiter=',')
predictions = np.loadtxt('pdf.txt', delimiter=',')
bird_data = predictions[0]
plane_data = predictions[1]

# 1 is plane, 0 is bird
gt = [0, 1, 0, 0, 0, 1, 1, 1, 1, 0]

# retrieves the likelihood from the data after adjusting to correct index
def get_plane_bird_prob(data_pt, plane_data, bird_data):
    ind = round(data_pt * 2)
    return plane_data[ind], bird_data[ind]

# calculates current belief of either bird or aircraft
def calc_curr_belief(likelihood, aircraft_prior, bird_prior, aircraft, tol):
    belief = likelihood
    first = tol if aircraft else 1 - tol
    sum = (first * aircraft_prior) + ((1 - first) * bird_prior)
    belief *= sum
    return belief

# sigmoid function used for the feature addition, see README for more info
def sigmoid(x):
    exp = - (0.25 * x - 1.5)
    denom = 1 + math.e ** exp
    return 1 / denom


def calc_plane_likelihood(sample, plane_data, bird_data, tol, add_feat, feat_weight):
    # init variables
    curr_plane_proba, curr_bird_proba = 0.5, 0.5
    prev, total_change, num_valid_pts = 0, 0, 0
    start = False

    for i, curr_pt in enumerate(sample):
        curr_pt = sample[i]
        if math.isnan(curr_pt):
            continue
        num_valid_pts += 1
        # get likelihoods, calculate belief
        aircraft_likely, bird_likely = get_plane_bird_prob(curr_pt, plane_data, bird_data)
        belief_bird = calc_curr_belief(bird_likely, curr_plane_proba, curr_bird_proba, False, tol)
        belief_aircraft = calc_curr_belief(aircraft_likely, curr_plane_proba, curr_bird_proba, True, tol)

        # adjust to get probability
        curr_bird_proba = belief_bird / (belief_bird + belief_aircraft)
        curr_plane_proba = 1 - curr_bird_proba
        
        if add_feat: # added feature -> adjust weights
            if not start:
                prev = curr_pt
                start = True
            else:
                curr_change = abs(curr_pt - prev) # calculate current average change, get probability from signmoid
                total_change += curr_change
                curr_avg_change = total_change / num_valid_pts
                prob_bird_for_avg = sigmoid(curr_avg_change)

                weighted_bird = prob_bird_for_avg * feat_weight # get weights for bird and plane, adjust by weight
                weighted_plane = (1 - prob_bird_for_avg) * feat_weight

                curr_bird_proba = (curr_bird_proba * (1 - feat_weight)) + weighted_bird # calc new probabilities
                curr_plane_proba = (curr_plane_proba * (1 - feat_weight)) + weighted_plane
            
    return curr_plane_proba

def calc_all_tracks(data, plane_data, bird_data, tol, add_feat, w_feat):
    output = list()
    for i, curr_sample in enumerate(data):
        proba = calc_plane_likelihood(curr_sample, plane_data, bird_data, tol, add_feat, w_feat)
        class_plane = True if proba > 0.5 else False
        certainty = (proba if class_plane else 1 - proba) * 100
        rounded = math.ceil(certainty * 100) / 100
        print("Track " + str(i + 1) + ": With a confidence of " + str(rounded) + '%' + ", classified as ", end = "")
        print("Plane") if class_plane else print("Bird")
        output.append(1 if class_plane else 0)

    # calculate percent of correct classifications
    num_correct = 0
    for i, curr in enumerate(output):
        if curr == gt[i]:
            num_correct += 1
        else: 
            print("Incorrect classification for Track " + str(i + 1))

    perc_correct = num_correct / len(gt) * 100
    print(str(int(perc_correct)) + '%' + " correct classification")

choice = input("Welcome! Would you like to choose a transition tolerance? (Defalut is 0.9) (y/n): ")
tol = 0.9
if choice == "y":
    tol = float(input("Choose a transition tolerance betewen 0 and 1: "))
    if tol < 0 or tol > 1:
        print("ERROR: INVALID TOLERANCE")
        exit(1)

add_feat = False
w_feat = 0.4
choice = input("Would you like to add a feature (average change) to improve the classifer? (y/n): ")
if choice == "y":
    add_feat = True
    w_feat = float(input("Choose a weight for the feature between 0 and 1 (0.4 gives best performance): "))
    if w_feat < 0 or w_feat > 1:
        print("ERROR: INVALID WEIGHT")
        exit(1)

calc_all_tracks(data, plane_data, bird_data, tol, add_feat, w_feat)