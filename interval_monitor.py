#the bpm is calculated by: 60 / average time between moments
import keyboard
import time
from pathlib import Path

ACTIVATE_KEY = "shift"
STOP_KEY = "ctrl"
FILE_NAME = "output.txt"
AVERAGE_FILE_NAME = "output_average.txt"
FILE_PATH = Path(FILE_NAME)
AVERAGE_FILE_PATH = Path(AVERAGE_FILE_NAME)

def main():
    file_path_exists = FILE_PATH.is_file()
    average_file_path_exists = AVERAGE_FILE_PATH.is_file()

    if file_path_exists or average_file_path_exists:
        if file_path_exists and average_file_path_exists:
            print(f"The files '{FILE_NAME}' and '{AVERAGE_FILE_NAME}' already exist! Do you want to overwrite them?")
        elif file_path_exists:
            print(f"The file '{FILE_NAME}' already exists! Do you want to overwrite it?")
        else:
            print(f"The file '{AVERAGE_FILE_NAME}' already exists! Do you want to overwrite it?")
        while 1:
            answer = input("y/N>").lower()
            if answer == "" or answer.startswith("n"):  return
            elif answer.startswith("y"):    break
            else:   print("Please answer with yes or no")
    timestamps = []
    bpm_averages = []
    bpms = []
    print(f"Press {ACTIVATE_KEY} every time the event occurs. Press {STOP_KEY} to finish and save")
    keyboard.wait(ACTIVATE_KEY)
    add_current_time(timestamps, bpm_averages, bpms)
    keyboard.add_hotkey(ACTIVATE_KEY, add_current_time, args=(timestamps, bpm_averages, bpms))
    keyboard.wait(STOP_KEY)
    print(generate_string(convert_timestamps(timestamps), bpms), "\n")
    print(generate_string(convert_timestamps(timestamps), bpm_averages), "\n")
    print(bpm_averages)

    with open(FILE_PATH, "w") as file, open(AVERAGE_FILE_PATH, "w")  as average_file:
        file.write(generate_string(convert_timestamps(timestamps), bpms))
        average_file.write(generate_string(convert_timestamps(timestamps), bpm_averages))

def add_current_time(timestamps, bpm_averages, bpms, write = True):
    timestamps.append(time.time())
    is_more_than_one_timestamp = len(timestamps) > 1
    average_bpm = calculate_average_bpm(timestamps) if is_more_than_one_timestamp else 0.0
    bpm_averages.append(average_bpm)
    last_bpm = calculate_last_bpm(timestamps) if is_more_than_one_timestamp else 0.0
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

def convert_timestamps(timestamp):
    return [i - timestamp[0] for i in timestamp]

def generate_string(converted_timestamps, bpms, use_comma = True):
    if use_comma:
        converted_timestamps = [str(i).replace(".", ",") for i in converted_timestamps]
        bpms = [str(i).replace(".", ",") for i in bpms]
    return "".join(f"{t}\t{b}\n" for t,b in zip(converted_timestamps[1:], bpms[1:]))

if __name__ == "__main__":
    main()