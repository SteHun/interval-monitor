#the bpm is calculated by: 60 / average time between moments
import keyboard
import time

ACTIVATE_KEY = "shift"
STOP_KEY = "alt"

def main():
    timestamps = []
    keyboard.wait(ACTIVATE_KEY)
    add_current_time(timestamps)
    keyboard.add_hotkey(ACTIVATE_KEY , add_current_time, args=(timestamps,))
    keyboard.wait(STOP_KEY)

def add_current_time(timestamps, write = True):
    timestamps.append(time.time())
    if write:
        print(f"{calculate_last_bpm(timestamps)}, average: {calculate_average_bpm(timestamps)}")

def calculate_last_bpm(timestamps):
    assert type(timestamps) == list, "input should be a list"
    if len(timestamps) == 1: return "not enough data"
    return 60.0/(timestamps[-1] - timestamps[-2])

def calculate_average_bpm(timestamps):
    average_delta_time = calculate_average_delta_time(timestamps)
    is_string = type(average_delta_time) == str
    return average_delta_time if is_string else 60 / average_delta_time


def calculate_average_delta_time(timestamps):
    assert type(timestamps) == list, "input should be a list"
    if len(timestamps) == 1: return "not enough data"
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