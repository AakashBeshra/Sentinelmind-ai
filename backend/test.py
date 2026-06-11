import sys 
print("Python path:", sys.path) 
try: 
   import app.main 
   print("Successfully imported app.main") 
except ImportError as e: 
   print(f"Error: {e}") 
   print("Checking if app folder exists...") 
   import os 
   print("app folder exists:", os.path.exists("app")) 
   print("app/main.py exists:", os.path.exists("app/main.py")) 
