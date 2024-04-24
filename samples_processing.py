

def read_samples(samples_path):
    res_dict = {}
    with open(samples_path, 'r') as file:
        next(file)
        for line in file:
            # split line into each field
            cols = line.split(",")
            participant = cols[0]
            trial = cols[1]
            orig_side = cols[-1]
            interest_area = cols[5]
            time = cols[2]
            file_name = cols[-2]
            condition = cols[-3]

            # filter out nikki
            if participant != "0422a3":

                # label dict entries by participant
                if participant not in res_dict:
                    res_dict[participant] = {}
                
                # add a subdict for each trial
                if trial not in res_dict[participant]:
                    res_dict[participant][trial] = {}

                # add the side the original image is on to the trial subdict
                if "orig_side" not in res_dict[participant][trial]:
                    res_dict[participant][trial]["orig_side"] = orig_side
            
                if interest_area != "[]":
                    # creates a list of the areas of interest saccaded to 
                    if "order_of_saccades" not in res_dict[participant][trial]:
                        res_dict[participant][trial]["order_of_saccades"] = [interest_area[2]]
                        res_dict[participant][trial]["first_saccade_time"] = time
                    else:
                        if interest_area[2] != res_dict[participant][trial]["order_of_saccades"][-1]:
                            res_dict[participant][trial]["order_of_saccades"] += [interest_area[2]]

                # add filename
                if "file_name" not in res_dict[participant][trial]:
                    res_dict[participant][trial]["file_name"] =  file_name

                # add condition
                if "condition" not in res_dict[participant][trial]:
                    res_dict[participant][trial]["condition"] =  condition

    return res_dict

def saccade_accuracy_helper(samples_dict, field):
    left_true_num = 0
    left_total_num = 0

    right_true_num = 0
    right_total_num = 0

    a_true_num = 0
    a_total_num = 0

    b_true_num = 0
    b_total_num = 0

    for participant in samples_dict:
        for trial in samples_dict[participant]:
            condition = samples_dict[participant][trial]["condition"]
            if condition == "A":
                a_total_num += 1
            elif condition == "B":
                b_total_num += 1


            if samples_dict[participant][trial]["orig_side"] == "Left\n":
                left_total_num += 1
                if samples_dict[participant][trial]["order_of_saccades"][field] == "1":
                    left_true_num += 1
                    if condition == "A":
                        a_true_num += 1
                    elif condition == "B":
                        b_true_num += 1

            elif samples_dict[participant][trial]["orig_side"] == "Right\n":
                right_total_num += 1
                if samples_dict[participant][trial]["order_of_saccades"][field] == "2":
                    right_true_num += 1
                    if condition == "A":
                        a_true_num += 1
                    elif condition == "B":
                        b_true_num += 1
    
    true_num = left_true_num + right_true_num
    total_num = left_total_num + right_total_num

    percent_true = true_num/total_num
    left_percent_true = left_true_num/left_total_num
    right_percent_true = right_true_num/right_total_num

    a_percent_true = a_true_num/a_total_num
    b_percent_true = b_true_num/b_total_num

    return left_percent_true, right_percent_true, percent_true, a_percent_true, b_percent_true

def saccade_accuracy(samples_dict):
    f_left, f_right, f_total, f_a, f_b = saccade_accuracy_helper(samples_dict, 0)
    l_left, l_right, l_total, l_a, l_b = saccade_accuracy_helper(samples_dict, -1)
    print("first saccade to interest area accuracies")
    print("left: " + str(f_left))
    print("right: " + str(f_right))
    print("total: " + str(f_total))
    print("condition A: " + str(f_a))
    print("condition B: " + str(f_b))
    print("----------------------------------------")
    print("last saccade to interest area accuracies")
    print("left: " + str(l_left))
    print("right: " + str(l_right))
    print("total: " + str(l_total))
    print("condition A: " + str(l_a))
    print("condition B: " + str(l_b))
    print("----------------------------------------")
    print("")

def num_interest_saccades_stats(samples_dict):
    total_num_saccades = 0
    total_num = 0
    max_num_saccades = 0

    difficult_images = []

    for participant in samples_dict:
        for trial in samples_dict[participant]:
            num_saccades = len(samples_dict[participant][trial]["order_of_saccades"])
            total_num_saccades += num_saccades
            max_num_saccades = max(num_saccades, max_num_saccades)

            if num_saccades > 3:
                difficult_images += [samples_dict[participant][trial]["file_name"]]
            
            total_num += 1

    average_per_trial = total_num_saccades/total_num

    print("average number of saccades per trial: " + str(average_per_trial))
    print("most saccades in a trial: " + str(max_num_saccades))
    print("difficult stimuli" + str(difficult_images))
    # return average_per_trial, max_num_saccades, difficult_images

if __name__ == "__main__":
    res = read_samples("10viewers_samples.csv")
    saccade_accuracy(res)
    num_interest_saccades_stats(res)
    
    
