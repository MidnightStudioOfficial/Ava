import time

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    average_time = calculate_average_time(iteration)
    estimated_time = calculate_estimated_time(iteration, total, average_time)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} ETA: {estimated_time} Avg: {average_time:.2f}s', end='\r')
    if iteration == total:
        print()

def calculate_estimated_time(iteration, total, average_time):
    remaining_iterations = total - iteration
    estimated_time = average_time * remaining_iterations
    hours = int(estimated_time // 3600)
    minutes = int((estimated_time % 3600) // 60)
    seconds = int(estimated_time % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def calculate_average_time(iteration):
    if iteration == 0:
        return 0

    elapsed_time = time.perf_counter() - start_time
    average_time = elapsed_time / iteration
    return average_time

# Usage example
total_iterations = 100
start_time = time.perf_counter()

for i in range(total_iterations):
    # Simulating some task
    time.sleep(0.1)

    # Update the progress bar
    print_progress_bar(i + 1, total_iterations, prefix='Progress:', suffix='Complete', length=50)
