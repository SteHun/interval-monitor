#the bpm is calculated by: 60 / average time between moments
import keyboard
import time

timestamps = []
keyboard.wait("space")

def add_current_time(timestamps):
    timestamps.append(time.time())
    print(f"{calculate_last_bpm(timestamps)}, average: {calculate_average_bpm(timestamps)}BPM")

def calculate_average_bpm(timestamps):
    average_delta_time = calculate_average_delta_time(timestamps)
    if type(average_delta_time) == str:
        return average_delta_time
    else:
        return 60 / average_delta_time

def calculate_last_bpm(timestamps):
    if type(timestamps) != list: raise RuntimeError("input should be a list")
    if len(timestamps) == 1: return "not enough data"
    return 60/(timestamps[-1] - timestamps[-2])

def calculate_average_delta_time(timestamps):
    if type(timestamps) != list: raise RuntimeError("input should be a list")
    if len(timestamps) == 1: return "not enough data"
    all_delta_times = []
    previous_item = None
    for i in timestamps:
        if previous_item == None:
            previous_item = i
        else:
            all_delta_times.append(i - previous_item)
            previous_item = i
    return calculate_average(all_delta_times)

def calculate_average(sequence):
    if type(sequence) != list: raise RuntimeError("input should be a list")
    total = 0
    for i in sequence:
        total += i
    return total / len(sequence)
add_current_time(timestamps)
keyboard.add_hotkey("space", add_current_time, args=(timestamps,))
keyboard.wait("alt")