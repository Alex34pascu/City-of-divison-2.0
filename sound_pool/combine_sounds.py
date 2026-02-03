import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)
import soundfile as sf

def merge_audio_files(file1, file2, output_file):
    data1, samplerate1 = sf.read(file1)
    global data2
    global samplerate2
    if samplerate1 != samplerate2:
        raise ValueError("Samplerates moeten overeenkomen")

    combined_data = data1.tolist() + data2.tolist()

    sf.write(output_file, combined_data, samplerate1)


data2, samplerate2 = sf.read(r"sounds\\silence.ogg")
