import tracemalloc

# Start tracing memory allocations
tracemalloc.start()
import os

# Get a snapshot of the current memory usage
snapshot = tracemalloc.take_snapshot()

# Find the top 5 memory blocks and print their sizes and traceback information
top_blocks = snapshot.statistics('lineno')
for i, block in enumerate(top_blocks[:5], start=1):
    print(f"#{i}: {block.size / (1024 * 1024)} MB")
    print(block.traceback.format())
    print()
import tracemalloc

# Start tracing memory allocations
tracemalloc.start()
import logger

# Stop tracing memory allocations
tracemalloc.stop()

# Get the top 10 memory-consuming lines of code
top_stats = tracemalloc.get_traced_memory()
top_stats = sorted(top_stats, key=lambda x: x.size, reverse=True)[:10]

# Print the results
print("Top 10 memory-consuming lines:")
for stat in top_stats:
    traceback = stat.traceback.format()
    print(f"{stat.size/1024/1024:.1f} MB - {traceback}")
