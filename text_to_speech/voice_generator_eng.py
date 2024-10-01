# -*- coding: utf-8 -*-

import torch
from TTS.api import TTS
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

l1=[0]
def get_audio_length(audio_path):
    audio = AudioSegment.from_file(audio_path)
    duration_in_ms = len(audio)  # Duration in milliseconds
    duration_in_sec = duration_in_ms / 1000  # Convert to seconds
    l1.append(l1[-1]+duration_in_sec)
    return 

def remove_silence(input_file, gap_duration=200):
    output_file=input_file
    # Load the input audio
    audio = AudioSegment.from_wav(input_file)
    
    # Detect nonsilent ranges (start and end times) in the audio
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=150, silence_thresh=audio.dBFS - 70)
    
    # Create a new audio segment, starting empty
    no_silence_audio = AudioSegment.silent(duration=0)
    
    # Add each nonsilent part with a small gap between segments
    for start, end in nonsilent_ranges:
        no_silence_audio += audio[start:end]
        no_silence_audio += AudioSegment.silent(duration=gap_duration)  # Add small gap after each segment
    
    # Export the final audio to the output file
    no_silence_audio.export(output_file, format="wav")
    print(f"Audio without silence (but with small gaps) saved to: {output_file}")

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device,end="\n\n\n\n")
# Initialize the TTS model (you can choose any model as per your requirement)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS and save to file
# text = " As Peter Parker enters the museum, he's captivated by the wonders of science, unaware that he's about to encounter a genetically engineered spider. When he leans in for a closer look, the spider senses him and delivers a bite, injecting its powerful venom into his bloodstream. This venom triggers a rapid transformation as Peter's DNA begins to merge with that of the spider, enhancing his strength, agility, and reflexes in ways he could never imagine. Suddenly, he feels an incredible surge of power, his senses heightened, and as he instinctively catches a falling exhibit, he realizes his life is forever changed. With great power comes great responsibility, and Peter is about to embark on an extraordinary journey as a superhero, all thanks to that fateful bite. "  # Your text input
text="I am alright bro you dont need to worry."  # Your text input
list=text.split('.')
list.pop()
print(list)
speaker_wav_path = "D:/models/text_to_speech/clone_samples/my_voice_clone​.wav"  # Path to your cloning audio file
count=1
for i in list:
    output_file_path = "D:/models/text_to_speech/output/output{}.wav".format(count)  # Output file path
    # Generate speech and save it to a file
    tts.tts_to_file(text=i, speaker_wav=speaker_wav_path, language="en", file_path=output_file_path)
    count=count+1
    remove_silence(output_file_path ,gap_duration=200)
    get_audio_length(output_file_path)
#merging all the audio


def merge_wav_files(input_folder, output_file):
    # Create an empty AudioSegment
    combined = AudioSegment.empty()

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):  # Check for .wav files
            file_path = os.path.join(input_folder, filename)
            audio_segment = AudioSegment.from_wav(file_path)  # Load the WAV file
            combined += audio_segment  # Append to the combined audio

    # Export the combined audio to a new file
    combined.export(output_file, format="wav")
    print(f"Merged audio saved to: {output_file}")

def delete_files(count,input_folder):
    for i in range(1,count+1):
        audio_path=input_folder+"/output{}.wav".format(i)
        os.remove(audio_path)
# Example usage
input_folder = "D:/models/text_to_speech/output"  # Replace with your folder path
output_file = "D:/models/text_to_speech/output/final_output.wav"  # Replace with desired output path
merge_wav_files(input_folder, output_file)
print(l1)
# delete_files(count,input_folder) 