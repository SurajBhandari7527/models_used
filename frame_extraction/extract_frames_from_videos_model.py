import cv2
import os

def extract_key_frames(video_path, output_folder, frame_rate=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    
    cap = cv2.VideoCapture(video_path)  # Open the video file
    frame_count = 0  # Initialize frame counter
    
    while cap.isOpened():
        print("frame",frame_count,"is extracted")
        ret, frame = cap.read()  # Read a frame from the video
        if not ret:
            break  # Exit the loop if there are no more frames
        
        if frame_count % frame_rate == 0:  # Extract every N-th frame
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)  # Save the frame as a JPEG file

        frame_count += 1  # Increment frame counter
    
    cap.release()  # Release the video capture object


# Specify paths
video_path = "C:/Users/Suraj Bhandari/Downloads/Video/spiderman.mp4"
output_folder = "C:/Users/Suraj Bhandari/OneDrive/Desktop/whatever/models/frame_extracted"

# Run the function to extract frames
extract_key_frames(video_path, output_folder, frame_rate=2)
print("frames extracted succesfully")

import os
import torch
import clip
from PIL import Image

# Define the path to the frames and where to save the matching frames
frame_folder = "C:/Users/Suraj Bhandari/OneDrive/Desktop/whatever/models/frame_extracted"
matched_folder = "C:/Users/Suraj Bhandari/OneDrive/Desktop/whatever/models/matching_frames"

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define the descriptions of events to match
descriptions = [
    "Peter enters the museum, excited and curious.",
    "Peter gazes at the exhibit on genetically modified spiders.",
    "A spider escapes from its enclosure, crawling toward Peter.",
    "The spider bites Peter on the hand, shocking him.",
    "Peter reacts, feeling dizzy and disoriented.",
    "Close-up of Peter's face, confusion turning to realization.",
    "The camera pans to the exhibit, highlighting the scientific themes.",
    "Peter stumbles away, hinting at his impending transformation."
]

# Prepare the descriptions for CLIP
text_inputs = clip.tokenize(descriptions).to(device)

# Create the output directory if it doesn't exist
os.makedirs(matched_folder, exist_ok=True)

# Get a sorted list of frame filenames
frame_names = sorted(os.listdir(frame_folder), key=lambda x: int(x.split('_')[1].split('.')[0]))

# Process each frame in the sorted order
for frame_name in frame_names:
    frame_path = os.path.join(frame_folder, frame_name)

    # Load and preprocess the frame
    image = preprocess(Image.open(frame_path)).unsqueeze(0).to(device)

    # Get the embeddings
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)

    # Normalize the features
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Calculate similarities
    similarities = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    # Check if any description matches with a high enough score
    for i, description in enumerate(descriptions):
        similarity_score = similarities[0][i].item()
        
        # Set an individual threshold for each description if needed
        threshold = 0.8  # You can modify this threshold

        if similarity_score > threshold:
            # Save the matching frame
            matching_image_path = os.path.join(matched_folder, frame_name)
            Image.open(frame_path).save(matching_image_path)
            print(f"Saved matched frame: {frame_name} for description: '{description}' with similarity: {similarity_score:.2f}")
            break  # Exit the loop once a match is found

print("Matching frames saved in the 'matched' folder!")

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
frame_folder = "C:/Users/Suraj Bhandari/OneDrive/Desktop/whatever/models/matching_frames"  # Replace with your frame folder path
output_video = 'spider.mkv'  # Output video file name
fps = 24  # Frames per second

# Create video from frames
create_video_from_frames(frame_folder, output_video, fps)
