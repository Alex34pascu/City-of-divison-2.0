import os

with open("compid.txt", "r") as f:
    comp_id = f.read().strip()

print("laten we beginnen")
script_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_path, 'players')
print("lets go")

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r') as file:
        content = file.read()
        if comp_id in content:
            print(filename)

print("done")