import matplotlib.pyplot as plt
import numpy as np

def read_fixations(samples_path):
    res_dict = {}
    with open(samples_path, 'r') as file:
        next(file)
        for line in file:
            # split line into each field
            cols = line.split(",")
      
            participant = cols[0]
            trial = cols[1]
            # resp_time = float(cols[2])
            orig_side = cols[6]
            fixation_start = float(cols[11])
            fixation_end = float(cols[13])
            fixation_interest_area = cols[14]

            # filter out nikki
            if participant != "0422a3":
                # label dict entries by participant
                if participant not in res_dict:
                    res_dict[participant] = {}
                
                # add a subdict for each trial
                if trial not in res_dict[participant]:
                    res_dict[participant][trial] = {}

                # add the response time to the trial subdict
                # if "resp_time" not in res_dict[participant][trial]:
                #     # adjust for the time only the fixation is visible
                #     res_dict[participant][trial]["resp_time"] = resp_time

                # add the side the original image is to the subdict
                if "orig_side" not in res_dict[participant][trial]:
                    res_dict[participant][trial]["orig_side"] = orig_side

                # adds a list of [start, end, interest_area] for each fixation for the trial to the subdict 
                if "fixation_intervals" not in res_dict[participant][trial]:
                    res_dict[participant][trial]["fixation_intervals"] = [[fixation_start, fixation_end, fixation_interest_area]]
                else:
                    res_dict[participant][trial]["fixation_intervals"] += [[fixation_start, fixation_end, fixation_interest_area]]
        
    return res_dict

def first_saccade_time_and_accuracy(fixation_dict):
    l_acc_times = []
    l_total_true = 0
    l_total_num = 0
    l_inacc_times = []

    r_acc_times = []
    r_total_true = 0
    r_total_num = 0
    r_inacc_times = []


    for participant in fixation_dict:
        for trial in fixation_dict[participant]:
            side = fixation_dict[participant][trial]["orig_side"]
            intervals = fixation_dict[participant][trial]["fixation_intervals"]
            if side == "Left":
                l_total_num += 1
            elif side == "Right":
                r_total_num += 1
            
            for i in range(1, len(intervals)):
                if side == "Left":
                    saccade_time = intervals[i][0] - intervals[i-1][1]
                    if intervals[i][2] == "[ 1]":
                        l_total_true += 1
                        l_acc_times += [saccade_time]
                        break
                    elif intervals[i][2] == "[ 2]":
                        l_inacc_times += [saccade_time]
                        break

                elif side == "Right":
                    saccade_time = intervals[i][0] - intervals[i-1][1]
                    if intervals[i][2] == "[ 2]":
                        r_total_true += 1
                        r_acc_times += [saccade_time]
                        break
                    elif intervals[i][2] == "[ 1]":
                        r_inacc_times += [saccade_time]
                        break
    
    acc_times = l_acc_times + r_acc_times
    total_true = l_total_true + r_total_true
    total_num = l_total_num + r_total_num
    inacc_times = l_inacc_times + r_inacc_times
    
    num_l_saccades = len(l_acc_times) + len(r_inacc_times)
    l_avg_time = (sum(l_acc_times) + sum(l_inacc_times))/l_total_num
    l_acc = l_total_true/l_total_num
    
    num_r_saccades = len(r_acc_times) + len(l_inacc_times)
    r_avg_time = (sum(r_acc_times) + sum(r_inacc_times))/r_total_num
    r_acc = r_total_true/r_total_num
    
    avg_time = (sum(acc_times) + sum(inacc_times))/total_num
    acc = total_true/total_num

    avg_acc_time = sum(acc_times)/total_true
    avg_inacc_time = sum(inacc_times)/(total_num - total_true)

    print("left")
    print("average first saccade time: " + str(l_avg_time))
    print("average first saccade accuracy: " + str(l_acc))
    print("number of saccades to the left: " + str(num_l_saccades))
    print("-----------------------------------------------------")
    print("right")
    print("average first saccade time: " + str(r_avg_time))
    print("average first saccade accuracy: " + str(r_acc))
    print("number of saccades to the right: " + str(num_r_saccades))
    print("-----------------------------------------------------")
    print("overall")
    print("average first saccade time: " + str(avg_time))
    print("average first saccade accuracy: " + str(acc))
    print("average first accurate saccade time: " + str(avg_acc_time))
    print("average first inaccurate saccade time: " + str(avg_inacc_time))
    print("-----------------------------------------------------")

    plot_time_proportions(acc_times, inacc_times, "Time to Initiate Saccade (ms)", "Proportions of Times to Initiate Saccades", 400, 10)
    plot_time_proportions(l_acc_times, l_inacc_times, "Time to Initiate Saccade (ms)", "Proportions of Times to Initiate Saccades (Left)", 400, 10)
    plot_time_proportions(r_acc_times, r_inacc_times, "Time to Initiate Saccade (ms)", "Proportions of Times to Initiate Saccades (Right)", 400, 10)



# def avg_response_time(fixation_dict):
#     l_total_resp_time = 0
#     l_total_num = 0

#     r_total_resp_time = 0
#     r_total_num = 0

#     for participant in fixation_dict:
#         for trial in fixation_dict[participant]:
#             resp_time = fixation_dict[participant][trial]["resp_time"]
#             if fixation_dict[participant][trial]["orig_side"] == "Left":
#                 l_total_resp_time += resp_time
#                 l_total_num += 1
#             else:
#                 r_total_resp_time += resp_time
#                 r_total_num += 1


#     total_resp_time = l_total_resp_time + r_total_resp_time
#     total_num = l_total_num + r_total_num

#     l_avg = l_total_resp_time/l_total_num
#     r_avg = r_total_resp_time/r_total_num
#     avg = total_resp_time/total_num


#     print("average response time left: " + str(l_avg))
#     print("average response time right: " + str(r_avg))
#     print("average response time overall: " + str(avg))
#     print("-----------------------------------------------------")

def avg_search_time(fixation_dict):
    left_times = []
    right_times = []
    acc_times = []
    in_acc_times = []
   
    for participant in fixation_dict:
        for trial in fixation_dict[participant]:
            start_time = 0
            end_time = 0
            i = 0
            intervals = fixation_dict[participant][trial]["fixation_intervals"]
            # find last fixation not on interest area

            while intervals[i][2] == "[ ]":
                start_time = intervals[i][1]
                i += 1
            
            i = 1
            # find first fixation on last interest area
            # skip all of the non interest area fixations
            while intervals[-i][2] == "[ ]":
                i += 1
            j = i
            # find the first of the interest area fixations
            while intervals[-i][2] == intervals[-j][2]:
                end_time = intervals[-j][0]
                j += 1
            j -= 1
            trial_time = end_time - start_time

            side = fixation_dict[participant][trial]["orig_side"]
            if side == "Left":
                left_times += [trial_time]
                if intervals[-j][2] == "[ 1]":
                    acc_times += [trial_time]
                else:
                    in_acc_times += [trial_time]
            else:
                right_times += [trial_time]
                if intervals[-j][2] == "[ 2]":
                    acc_times += [trial_time]
                else:
                    in_acc_times += [trial_time]

    l_max_time = max(left_times)
    l_min_time = min(left_times)
    l_avg_time = sum(left_times)/len(left_times)

    r_max_time = max(right_times)
    r_min_time = min(right_times)
    r_avg_time = sum(right_times)/len(right_times)

    times = left_times + right_times
    max_time = max(times)
    min_time = min(times)
    avg_time = sum(times)/len(times)
    print("left")
    print("average time: " + str(l_avg_time))
    print("maximum time: " + str(l_max_time))
    print("minimum time: " + str(l_min_time))
    print("----------------------------------")
    print("right")
    print("average time: " + str(r_avg_time))
    print("maximum time: " + str(r_max_time))
    print("minimum time: " + str(r_min_time))
    print("----------------------------------")
    print("overall")
    print("average time: " + str(avg_time))
    print("maximum time: " + str(max_time))
    print("minimum time: " + str(min_time))


    
    plot_time_proportions(acc_times, in_acc_times, "Time to Locate Target (ms)", "Proportions of Times to Locate Target", 4000, 75)

def plot_time_proportions(acc_times, in_acc_times, x_label, title, max_time, bin_size):
   
    bin_edges = np.arange(0, max_time, bin_size) 
    total_times = acc_times + in_acc_times
    total_count = len(total_times)

    acc_hist, _ = np.histogram(acc_times, bins=bin_edges)
    acc_proportions = acc_hist / total_count

    in_acc_hist, _ = np.histogram(in_acc_times, bins=bin_edges)
    in_acc_proportions = in_acc_hist / total_count

    
    total_times.sort() 
    percentile_index = int(total_count * 0.5)  # Index for 90th percentile
    acc_90_percentile = total_times[percentile_index]
    plt.axvline(x=acc_90_percentile, color='r', linestyle='--', label='50% of Times')

    # Plot the proportions˜
    plt.plot(bin_edges[:-1], acc_proportions, marker='o', label="Accurate Responses")
    plt.plot(bin_edges[:-1], in_acc_proportions, marker='x', label="Inaccurate Responses")
    plt.xlabel(x_label)
    plt.ylabel("Proportion of Times")
    plt.title(title)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    res = read_fixations("10viewers_fixations.csv")
    # print(len(res))
    # print(res)
    # print(len(res["SPa\n"]))
    # print(res["SPa\n"]["1"])
    # avg_response_time(res)
    # print(average)
    first_saccade_time_and_accuracy(res)
    avg_search_time(res)