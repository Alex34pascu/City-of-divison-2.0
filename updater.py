import sys
import subprocess
import os
import pygame
import urllib.request
import ssl
import shutil
import zipfile
import time
import socket

pygame.init()

import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()

def speak(text):
    speatch.output(text)

import sound_pool
import v
import dlg
import menus

# SSL context dat certificaten negeert (zoals verify=False)
ssl_context = ssl._create_unverified_context()

def check_for_updates(url):
    try:
        print("Proberen verbinding te maken met urllib...")
        with urllib.request.urlopen(url, timeout=10, context=ssl_context) as response:
            latest_version = response.read().decode().strip()

        if latest_version != v.version:
            s = sound_pool.sound.sound()
            s.load(r"sounds\\updatefound.ogg", True)
            s.play()
            time.sleep(2)
            dlg.dlg("There is a new update available. Your version: " + v.version + ". Latest version: " + latest_version)
            y = menus.yesno("Do you want to update now?", False)

            if y == 1:
                try:
                    download_url = "https://fire-gaming.eu/city_of_division/city%20of%20division%20setup.exe"
                    download_path = os.path.join(os.path.expanduser('~'), "City of division setup.exe")
                    download_file(download_url, download_path)
                    dlg.dlg("The update has been downloaded. The installer will now be launched.")
                    subprocess.Popen([download_path])
                    sys.exit()
                except Exception as e:
                    dlg.dlg("Error downloading the file: " + str(e))
            else:
                return
    except SystemExit:
                    sys.exit()
    except Exception as e:
        dlg.dlg("Error checking for updates: " + str(e))
        return


def download_file(url, destination):
    beep_frequency = 1
    retries = 5
    timeout = 10

    if os.path.exists(destination):
        os.remove(destination)

    downloaded_size = 0

    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            total_size = int(response.headers.get('Content-Length', 0))
    except Exception as e:
        print("Failed to retrieve file size:", e)
        total_size = 0

    if downloaded_size >= total_size:
        os.remove(destination)
        return

    while retries > 0:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
                with open(destination, 'ab') as file:
                    while True:
                        data = response.read(1024)
                        if not data:
                            break
                        file.write(data)
                        downloaded_size += len(data)

                        if total_size > 0:
                            percentage_complete = (downloaded_size / total_size) * 100
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    speak(f"{round(percentage_complete, 1)}%")

                            if percentage_complete > beep_frequency:
                                try:
                                    v.msp.play_stationary_extended(r"sounds\\progressbeep.ogg", 0, 0, 0, beep_frequency + 50, False, False)
                                except Exception as e:
                                    print(f"Error playing progress beep: {e}")
                                beep_frequency += 1

            return

        except Exception as e:
            retries -= 1
            print(f"Retrying download... ({retries} left) Error: {e}")
            time.sleep(5)

    print("Download failed.")


def extract_and_replace(zip_filename):
    destination_folder = os.path.dirname(os.path.abspath(zip_filename))

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

    zip_folder = os.path.splitext(os.path.basename(zip_filename))[0]
    source_folder = os.path.join(destination_folder, zip_folder)

    for source_file in os.listdir(source_folder):
        source_path = os.path.join(source_folder, source_file)
        destination_path = os.path.join(destination_folder, source_file)

        if os.path.isfile(destination_path):
            os.remove(destination_path)
        shutil.move(source_path, destination_path)

    shutil.rmtree(source_folder)
