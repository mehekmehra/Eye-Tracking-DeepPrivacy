

def read_messages(samples_path):
    res_dict = {}
    with open(samples_path, 'r') as file:
        next(file)
        for line in file:
            # split line into each field
            cols = line.split(",")
      
            participant = cols[-1]
            trial = cols[0]
            resp_time = cols[3]
            file_name = cols[5]

            # label dict entries by participant
            if participant not in res_dict:
                res_dict[participant] = {}
            
            # add a subdict for each trial
            if trial not in res_dict[participant]:
                res_dict[participant][trial] = {}

            # add the response time to the trial subdict
            if "resp_time" not in res_dict[participant][trial]:
                # adjust for the time only the fixation is visible
                res_dict[participant][trial]["resp_time"] = float(resp_time) 

            if "orig_side" not in res_dict[participant][trial]:
                if "left" in file_name:
                    res_dict[participant][trial]["orig_side"] = "left"
                else:
                    res_dict[participant][trial]["orig_side"] = "right"
    return res_dict

def avg_response_time(messages_dict):
    l_total_resp_time = 0
    l_total_num = 0

    r_total_resp_time = 0
    r_total_num = 0

    for participant in messages_dict:
        for trial in messages_dict[participant]:
            resp_time = messages_dict[participant][trial]["resp_time"]
            if messages_dict[participant][trial]["orig_side"] == "left":
                l_total_resp_time += resp_time
                l_total_num += 1
            else:
                r_total_resp_time += resp_time
                r_total_num += 1


    total_resp_time = l_total_resp_time + r_total_resp_time
    total_num = l_total_num + r_total_num

    l_avg = l_total_resp_time/l_total_num
    r_avg = r_total_resp_time/r_total_num
    avg = total_resp_time/total_num

    return l_avg, r_avg, avg

if __name__ == "__main__":
    res = read_messages("Pilot_messages.csv")
    # print(len(res))
    # print(res)
    # print(len(res["SPa\n"]))
    # print(res["SPa\n"]["1"])
    average = avg_response_time(res)
    print(average)