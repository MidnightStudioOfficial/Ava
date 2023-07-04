import tqdm
import os

class ProgressBar:
    def __init__(self, data_file_paths):
        self.data_file_paths = data_file_paths
        self.total_files = len(data_file_paths)
    
    def get_file_size(self, file_path):
        return os.path.getsize(file_path)

    def load_data(self):
        for file_path in self.data_file_paths:
            file_size = self.get_file_size(file_path)
            bytes_read = 0

            # Create a progress bar for each file
            prog = tqdm.tqdm(total=file_size, desc=f"Loading {file_path}", unit="bytes", unit_scale=True, dynamic_ncols=True)
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(1024)
                    if not chunk:
                        break

                    # Process each chunk of data
                    # Replace this with your actual processing logic
                    # Example: process_chunk(chunk)
                    # This is just a placeholder
                    processed_chunk = chunk

                    # Update the progress bar
                    prog.update(len(chunk))
                    bytes_read += len(chunk)

                    # Calculate and display the file progress
                    progress_percentage = (bytes_read / file_size) * 100
                    prog.set_postfix(file_progress=f"{progress_percentage:.2f}%")

                    # Simulate some processing time
                    # Remove this in your actual implementation
                    import time
                    time.sleep(0.1)

            # Add a new line after each file is loaded
            print()

    def load(self):
        prog = tqdm.tqdm(self.data_file_paths, desc="Loading files", unit="file")
        for file_path in prog:
            prog.set_description_str(f"Loading {file_path}")
            self.load_data()
            prog.update(1)

# Example usage
data_file_paths = ["file1.txt", "file2.txt", "file3.txt"]
progress_bar = ProgressBar(data_file_paths)
progress_bar.load()
