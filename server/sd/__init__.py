import os
import json
import traceback

# Interne cache voor bestandsnamen per directory
_case_insensitive_cache = {}

def reset_case_insensitive_cache(directory):
    """Reset de cache voor een bepaalde map"""
    _case_insensitive_cache.pop(directory, None)

def get_case_insensitive_map(directory):
    """Cache de bestandsnamen in een map, lowercase als sleutel"""
    if directory not in _case_insensitive_cache:
        try:
            files = os.listdir(directory)
            _case_insensitive_cache[directory] = {
                f.lower(): f for f in files
            }
        except FileNotFoundError:
            _case_insensitive_cache[directory] = {}
    return _case_insensitive_cache[directory]

def find_case_insensitive_filename(directory, filename):
    """Zoek een bestandsnaam in een map, ongeacht hoofdletters"""
    filename_map = get_case_insensitive_map(directory)
    match = filename_map.get(filename.lower())
    if match:
        return os.path.join(directory, match)
    return os.path.join(directory, filename)

def get(name, filename, default, subfolder=""):
    base_path = os.path.join(os.getcwd(), subfolder) if subfolder else os.getcwd()
    filepath = find_case_insensitive_filename(base_path, filename)

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data.get(name, default)
    except Exception:
        return default

def get_all_data(filename, subfolder=""):
    base_path = os.path.join(os.getcwd(), subfolder) if subfolder else os.getcwd()
    filepath = find_case_insensitive_filename(base_path, filename)

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data
    except Exception:
        return {}

def save(name, value, filename, subfolder=""):
    base_path = os.path.join(os.getcwd(), subfolder) if subfolder else os.getcwd()
    if subfolder and not os.path.exists(base_path):
        os.makedirs(base_path)

    filepath = find_case_insensitive_filename(base_path, filename)

    data = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)

        data[name] = value

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        reset_case_insensitive_cache(base_path)  # Cache reset na schrijven
    except Exception as e:
        print("Fout bij opslaan:", str(e))

def save_multiple_things(new_data, filename, subfolder=""):
    base_path = os.path.join(os.getcwd(), subfolder) if subfolder else os.getcwd()
    if subfolder and not os.path.exists(base_path):
        os.makedirs(base_path)

    filepath = find_case_insensitive_filename(base_path, filename)

    data = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)

        data.update(new_data)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        reset_case_insensitive_cache(base_path)  # Cache reset na schrijven
    except Exception:
        pass
