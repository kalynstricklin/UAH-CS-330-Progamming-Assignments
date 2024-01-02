#
# Project: CS 330
# Program: State Machines
# Author: Kalyn Stricklin
# Created: 11/12/2023
# 
# Purpose: Implement a passing maneuver state machine


import random


scenario = 1 # scenario 1 or 2 
scenario_trace = [True, False][scenario - 1]
iterations = [100, 1000000][scenario - 1]
intervals = [1, 10000][scenario - 1]
transition_probability = [
    [0.8, 0.4, 0.3, 0.4, 0.3, 0.3, 0.8, 0.8, 0.8],
    [0.9, 0.6, 0.3, 0.2, 0.2, 0.4, 0.7, 0.9, 0.7]
][scenario-1]
state_sequence = [list(range(1,8)), [7] + list(range(1,7))]
state_sequence = state_sequence[scenario - 1]

transition_sequence = [list(range(1,10)), [9]+ list(range(1,9))]
transition_sequence = transition_sequence[scenario - 1]

# Initalize output file
output_file = "CS 330 Program 4 Scenario "+ str(scenario)+ " Output.txt"

# Function to write text to file
def write_text(text_file, text, first = False):
    mode = 'w' if first else 'a'
    with open(text_file, mode) as f:
        f.write(text + '\n')
    
# Initalize constants for states
FOLLOW = 0
PULL_OUT = 1
ACCELERATE = 2
PULL_IN_AHEAD = 3
PULL_IN_BEHIND = 4
DECELERATE = 5
DONE = 6

# initalize program state and transition counters
stateCount = [0,0,0,0,0,0,0]
transitionCount = [0,0,0,0,0,0,0,0,0]

# Define state 'action' function stubs
def followAction():
    #write_text(output_file, "state = 1 Follow")
    stateCount[FOLLOW] += 1 
    
def pullOutAction():
    #write_text(output_file, "state = 2 Pull Out")
    stateCount[PULL_OUT] += 1 
    
def accelerateAction():
    #write_text(output_file, "state = 3 Accelerate")
    stateCount[ACCELERATE] += 1 
    
def pullInAheadAction():
    #write_text(output_file, "state = 4 Pull in Ahead")
    stateCount[PULL_IN_AHEAD] += 1 
    
def pullInBehindAction():
    #write_text(output_file, "state = 5 Pull in Behind")
    stateCount[PULL_IN_BEHIND] += 1 
    
def decelerateAction():
    #write_text(output_file, "state = 6 Decelerate")
    stateCount[DECELERATE] += 1 
    
def doneAction():
    #write_text(output_file, "state = 7 Done\n")
    stateCount[DONE] += 1 


# Execute Iterations and transitions
for i in range(iterations):
    #write_text(output_file, "iterations={} ".format(i))

    state = FOLLOW
    followAction()
    
    while state != DONE:
        
        # Random Number Generator between 0 and 1
        r = random.randrange(0,10,1)/10
        
        # Check transtions
        if (state == FOLLOW):
            if (r < transition_probability[0]):
                transitionCount[0] += 1
                state = PULL_OUT
                pullOutAction()
            else:
                state = FOLLOW
                followAction()
        elif(state == PULL_OUT):
            if (r < transition_probability[1]):
                transitionCount[1] += 1
                state = ACCELERATE
                accelerateAction()
            elif(r < sum(transition_probability[i] for i in [1,3])):
                transitionCount[3] += 1
                state = PULL_IN_BEHIND
                pullInBehindAction()
            else: 
                state = PULL_OUT
                pullOutAction()
        elif(state == ACCELERATE):
            if (r < transition_probability[2]):
                transitionCount[2] += 1
                state = PULL_IN_AHEAD
                pullInAheadAction()
            elif(r < sum(transition_probability[i] for i in [2,4])):
                transitionCount[4] += 1
                state = PULL_IN_BEHIND
                pullInBehindAction()
            elif(r < sum(transition_probability[i] for i in [2,4,5])):
                transitionCount[5] += 1
                state = DECELERATE
                decelerateAction()
            else:
                state = ACCELERATE
                accelerateAction()
        elif(state == PULL_IN_AHEAD):
            if (r < transition_probability[8]):
                transitionCount[8] += 1
                state = DONE
                doneAction()
            else:
                state = PULL_IN_AHEAD
                pullInAheadAction()
        elif(state == PULL_IN_BEHIND):
            if (r < transition_probability[6]):
                transitionCount[6] += 1
                state = FOLLOW
                followAction()
            else:
                state = PULL_IN_BEHIND
                pullInBehindAction()
                
        elif(state == DECELERATE):
            if (r < transition_probability[7]):
                transitionCount[7] += 1
                state = PULL_IN_BEHIND
                pullInBehindAction()
            else:
                state = DECELERATE
                decelerateAction()
        elif(state == DONE):
           break
                
    if i % intervals == 0:
        print(".")
    

# Report scenario and execution statisitics
state_freq = [count / sum(stateCount) for count in stateCount]
transition_freq = [count / sum(transitionCount) for count in transitionCount]
# Header in text file
write_text(output_file, "CS 330, State Machines, Begin", True)
write_text(output_file, f"scenario                = {scenario}")
write_text(output_file, f"trace                   = {scenario_trace}")
write_text(output_file, f"iterations              = {iterations}")
write_text(output_file, f"transition probabilities= {transition_probability}")
write_text(output_file, f"state counts            = {stateCount}")
write_text(output_file, f"state frequencies       = {state_freq}")
write_text(output_file, f"transition counts       = {transitionCount}")
write_text(output_file, f"transition frequencies  = {transition_freq}")

