import os
# from pydub import AudioSegment

# def merge_wav_files(input_folder, output_file):
#     # Create an empty AudioSegment
#     combined = AudioSegment.empty()

#     # Iterate through all files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".wav"):  # Check for .wav files
#             file_path = os.path.join(input_folder, filename)
#             audio_segment = AudioSegment.from_wav(file_path)  # Load the WAV file
#             combined += audio_segment  # Append to the combined audio

#     # Export the combined audio to a new file
#     combined.export(output_file, format="wav")
#     print(f"Merged audio saved to: {output_file}")

# def delete_files(count,input_folder):
#     for i in range(1,count+1):
#         audio_path=input_folder+"/output{}.wav".format(i)
#         os.remove(audio_path)
# # Example usage
# input_folder = "D:/models/text_to_speech/output"  # Replace with your folder path
# output_file = "D:/models/text_to_speech/output/final_output.wav"  # Replace with desired output path
# merge_wav_files(input_folder, output_file)
# delete_files(count,input_folder)