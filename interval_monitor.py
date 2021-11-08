#the bpm is calculated by: 60 / average time between moments
import keyboard
import time

ACTIVATE_KEY = "shift"
STOP_KEY = "alt"

def main():
    timestamps = []
    bpm_averages = []
    bpms = []
    keyboard.wait(ACTIVATE_KEY)
    add_current_time(timestamps, bpm_averages, bpms)
    keyboard.add_hotkey(ACTIVATE_KEY, add_current_time, args=(timestamps, bpm_averages, bpms))
    keyboard.wait(STOP_KEY)
    print(timestamps)
    print(bpm_averages)
    print(bpms)

def add_current_time(timestamps, bpm_averages, bpms, write = True):
    timestamps.append(time.time())
    is_more_than_one_timestamp = len(timestamps) > 1
    average_bpm = calculate_average_bpm(timestamps) if is_more_than_one_timestamp else 0
    bpm_averages.append(average_bpm)
    last_bpm = calculate_last_bpm(timestamps) if is_more_than_one_timestamp else 0
    bpms.append(last_bpm)
    if write:
        print(f"{last_bpm}BPM, average: {average_bpm}BPM"
        if is_more_than_one_timestamp else "not enough data")

def calculate_last_bpm(timestamps):
    assert type(timestamps) == list, "input should be a list"
    return 60.0/(timestamps[-1] - timestamps[-2])

def calculate_average_bpm(timestamps):
    average_delta_time = calculate_average_delta_time(timestamps)
    is_string = type(average_delta_time) == str
    return average_delta_time if is_string else 60 / average_delta_time


def calculate_average_delta_time(timestamps):
    assert type(timestamps) == list, "input should be a list"
    all_delta_times = []
    previous_item = None
    for i in timestamps:
        if previous_item != None:   all_delta_times.append(i - previous_item)
        previous_item = i      
    return calculate_average(all_delta_times)

def calculate_average(sequence):
    assert type(sequence) == list, "input should be a list"
    total = sum(sequence)
    return total / len(sequence)

if __name__ == "__main__":
    main()