import cv2
import os
import re  # Import regex for numeric sorting

def sort_key(frame_name):
    """Extract the numeric part from the frame name for sorting."""
    return int(re.search(r'(\d+)', frame_name).group())

def create_video_from_frames(frame_folder, output_video, fps=24):
    # Get the list of frame filenames
    frames = [f for f in os.listdir(frame_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Sort frames by the numeric value extracted from the filename
    frames.sort(key=sort_key)

    # Check if frames are available
    if not frames:
        print("No frames found in the specified folder.")
        return

    # Get the size of the first frame
    first_frame = cv2.imread(os.path.join(frame_folder, frames[0]))
    height, width, _ = first_frame.shape
    
    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for frame in frames:
        # Read each frame
        print("combined",frame)
        
        img = cv2.imread(os.path.join(frame_folder, frame))
        if img is None:
            print(f"Warning: {frame} could not be read.")
            continue
        video_writer.write(img)  # Write the frame to the video

    video_writer.release()  # Finalize the video file
    print(f"Video saved as {output_video}")

# Set parameters
frame_folder = "D:/models/frame_extraction/matching_frames"  # Replace with your frame folder path
output_video = 'D:/models/frame_extraction/spider.mkv'  # Output video file name
fps = 24  # Frames per second

# Create video from frames
create_video_from_frames(frame_folder, output_video, fps)
