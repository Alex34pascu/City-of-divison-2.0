import os

old_name=input("type the old name of the weapon")
new_name=input("type the replacement for this weapon.")
print("laten we beginnen")
script_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_path, 'players')
print("lets go")
for filename in os.listdir(folder_path):
 print(filename)
 file_path = os.path.join(folder_path, filename)
 with open(file_path, 'r') as file:
  content = file.read()
  with open(file_path, 'w') as f:
   f.write(content.replace(old_name,new_name))
print("done")
