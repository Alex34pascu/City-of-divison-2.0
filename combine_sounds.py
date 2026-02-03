import traceback
import soundfile as sf
import numpy as np
import accessible_output2.outputs.auto

speatch = accessible_output2.outputs.auto.Auto()

def speak(text):
    speatch.output(text)

def add_silence(file1, output_file):
    try:
        # Laad het audiobestand
        data1, samplerate1 = sf.read(file1)
        
        # Laad de stilte (verondersteld wordt dat "silence.ogg" stil is en dezelfde sample rate heeft)
        silence, samplerate2 = sf.read("silence.ogg")
        
        if samplerate1 != samplerate2:
            raise ValueError("Sample rates van de bestanden komen niet overeen.")
        
        # Voeg de stilte toe aan het originele geluid
        combined = np.concatenate((data1, silence))
        
        # Exporteer het gecombineerde bestand
        sf.write(output_file, combined, samplerate1)
        return True
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        speak("error: " + error_message)
        return False
