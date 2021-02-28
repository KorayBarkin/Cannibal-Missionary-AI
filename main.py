from random import shuffle

MISSIONARIES = 6
CANNIBALS = 6
BOAT_CAPACITY = 5

debug_mode = 0

# True --> Left bank
# False --> Right bank

states = [[[MISSIONARIES, CANNIBALS, True]]]

solutions = []

# possible_states list consists of safe left bank states after transportation is completed
possible_states = []


# Check if bank states are safe

# choice[0] = missionary count on left bank
# choice[1] = cannibal count on left bank

# Conditions: !asa
# missionaries on the left bank is 0 or
# missionaries on the right bank is 0 or
# missionaries >= cannibals on both banks
def is_safe(left_bank):
    if left_bank[0] == 0 or MISSIONARIES - left_bank[0] == 0 or (left_bank[0] >= left_bank[1] and MISSIONARIES - left_bank[0] >= CANNIBALS - left_bank[1]):
        return True

    return False


# Fill possible bank states
# for every combination of total missionaries and cannibals
# check if banks are safe or not
# if safe add to posible_states list
for m in range(MISSIONARIES + 1):
    for c in range(CANNIBALS + 1):
        if is_safe((m, c)):
            possible_states.append((m, c))


# Problem solving process

# curr_state: list of transportation steps
def act(curr_state):
    global debug_mode

    # Shuffle possible_states list for nondeterministic approach
    choices = possible_states.copy()
    shuffle(choices)

    # Save initial curr_state for recovery in next steps
    curr_state_original = curr_state.copy()

    # state : last state of the left bank in the curr_state list
    # state[0] : missionary count on the left bank before transportation
    # state[1] : cannibal count on the left bank before transportation
    # state[2] : if True boat is currently at the left bank, will go right
    #            if False boat is currently at the right bank, will go left
    state = curr_state[-1]

    for ch in choices:

        # ch is the next step to add to curr_state list
        # ch[0] = missionary count on the left bank after transportation
        # ch[1] = cannibal count on the left bank after transportation

        # Check if next state is already in curr_state list to prevent duplicate states
        if [ch[0], ch[1], True] in curr_state or [ch[0], ch[1], False] in curr_state:
            continue

        # Check boat position

        # if boat is at the left bank:
        if state[2]:

            # Since choices list contains every possible states eliminate impossible ones

            # Compare next state missionary and cannibal counts with the current state's counts

            # Boat is going right:
            # missionary count of the left bank should decrease or stay the same
            # cannibal count of the left bank should decrease or stay the same
            # difference of sums of cannibal and missionary counts between states should be less than or equal to boat capacity
            if state[0] >= ch[0] and state[1] >= ch[1] and ((state[0] + state[1]) - (ch[0] + ch[1])) <= BOAT_CAPACITY:

                # Action is possible
                # convert next state choice (ch) to state format [missionary, cannibal, False] and append it to curr_state
                curr_state.append([ch[0], ch[1], False])

                # Append curr_state to states if it doesn't exist in the states list
                if curr_state not in states:
                    states.append(curr_state)

                # Solution can only be found when next boat position is right
                # if next state of the left bank is 0,0 that is a final step and solution:
                #   append curr state to solutions list
                if ch == (0, 0):
                    
                    if debug_mode == 2 or debug_mode == -1:
                        if len(curr_state) == 8:
                            solutions.append(curr_state)
                            print(curr_state)

                            if debug_mode == 2:
                                inp = input("Press 'enter' to continue, type 'exit' to terminate debug process:\n")
                                if inp == "exit":
                                    debug_mode = -1
                    else:
                        solutions.append(curr_state)


                    if debug_mode == 1:
                        print(curr_state)
                        inp = input("Press 'enter' to continue, type 'exit' to terminate debug process:\n")
                        if inp == "exit":
                            debug_mode = 0

                    

                # recover curr_state to its original for next iteration
                curr_state = curr_state_original.copy()
                if debug_mode == 3:
                        print(f"current_state:\n{curr_state}\n choice:\n{ch}\n")
                        inp = input("Press 'enter' to continue, type 'exit' to terminate debug process:\n")
                        if inp == "exit":
                            debug_mode = 0

        # if boat is at the right bank:
        else:

            # Compare next state missionary and cannibal counts with the current state's counts

            # Boat is going left:
            # missionary count of the left bank should increase or stay the same
            # cannibal count of the left bank should increase or stay the same
            # difference of sums of cannibal and missionary counts between states should be less than or equal to boat capacity
            # additionally state should not be a solution
            if state[0] <= ch[0] and state[1] <= ch[1] and ((ch[0] + ch[1]) - (state[0] + state[1])) <= BOAT_CAPACITY and state != [0, 0, False]:
                
                # Action is possible
                # convert next state choice (ch) to state format [missionary, cannibal, True] and append it to curr_state
                curr_state.append([ch[0], ch[1], True])
                states.append(curr_state)
                
                # recover curr_state to its original for next iteration
                curr_state = curr_state_original.copy()
                if debug_mode == 3:
                        print(f"current_state:\n{curr_state}\n choice:\n{ch}\n")
                        inp = input("Press 'enter' to continue, type 'exit' to terminate debug process:\n")
                        if inp == "exit":
                            debug_mode = 0


def main():
    global debug_mode
    print("Modes:")
    print("1: Stop at every solution")
    print("2: Stop at every 7 step solution")
    print("3: Single step")
    try:
        debug_mode = int(input("Enter mode number: "))
    except:
        pass

    while debug_mode not in [1,2,3]:
        try:
            debug_mode = int(input("Invalid choice! \n"))
        except:
            pass
        
    # As long as there is an unfinished path of states:
    # check popped state
    while(len(states) > 0):

        current_state = states.pop()
        act(current_state)

    if debug_mode != -1:
        print(f"Number of found solutions: {len(solutions)}")
        print("First 10 solutions:")
        for s in range(10):
            print(solutions[s])


    
main()
