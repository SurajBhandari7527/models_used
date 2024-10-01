import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video_with_photos_from_folder(image_folder, audio_path, timestamps, output_path, duration):
    """
    Create a video that changes images at specified timestamps while playing audio.
    
    Parameters:
    - image_folder: Path to the folder containing images named sequentially (e.g., 1.png, 2.png).
    - audio_path: Path to the audio file.
    - timestamps: List of timestamps where the images should change.
    - output_path: Path to save the final output video.
    - duration: Duration of the entire video.
    """
    # Load audio
    audio = AudioFileClip(audio_path)

    # Get list of image paths sorted by filename
    image_paths = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

    # Create a list to hold the image clips
    clips = []

    # Start time for the first clip
    current_time = 0

    # Iterate over the images and timestamps
    for i, timestamp in enumerate(timestamps):
        if i >= len(image_paths):
            break  # Stop if we run out of images

        # Duration for each image clip
        image_duration = timestamp - current_time

        # Create an ImageClip and set the duration
        image_clip = ImageClip(image_paths[i]).set_duration(image_duration)

        # Append the image clip to the clips list
        clips.append(image_clip)

        # Update current time
        current_time = timestamp

    # Handle the last image to play till the end of the video
    if len(image_paths) > len(timestamps):
        last_image_clip = ImageClip(image_paths[-1]).set_duration(duration - timestamps[-1])
        clips.append(last_image_clip)

    # Concatenate all the image clips
    video = concatenate_videoclips(clips, method="compose")

    # Set the audio for the video
    video = video.set_audio(audio)

    # Write the final video to a file
    video.write_videofile(output_path, codec="libx264", fps=24)

# Example usage
image_folder = "D:/models/text_to_speech/photos"  # Path to the folder containing images
audio_path = "D:/models/text_to_speech/output/final_output.wav"  # Path to your audio file
timestamps = [3.173, 6.525, 14.392, 16.557, 20.982, 22.314999999999998, 25.86, 29.288999999999998, 33.799, 37.259]  # Time (in seconds) when each image should change
output_path = "D:/models/text_to_speech/output_video.mp4"  # Path for the final video
duration = 35.2  # Duration of the final video in seconds

create_video_with_photos_from_folder(image_folder, audio_path, timestamps, output_path, duration)
