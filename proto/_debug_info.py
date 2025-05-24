import sys
import os

print("--- Debug Info from debug_info.py ---")
print("Current Working Directory: {os.getcwd()}")
print("sys.path:")
for p in sys.path:
    print(f"  {p}")
print("--- End Debug Info ---")
