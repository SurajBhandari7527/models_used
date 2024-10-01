import os
import torch
import clip
from PIL import Image

# Define the path to the frames and where to save the matching frames
frame_folder = "D:/models/frame_extraction/frame_extracted"
matched_folder = "D:/models/frame_extraction/matching_frames"

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

# Keep track of matched descriptions
matched_descriptions = set()

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

    # Check for matches in order
    for i, description in enumerate(descriptions):
        # Skip already matched descriptions
        if description in matched_descriptions:
            continue

        similarity_score = similarities[0][i].item()
        
        # Set an individual threshold for each description if needed
        threshold = 0.8  # You can modify this threshold

        if similarity_score > threshold:
            # Save the matching frame
            matching_image_path = os.path.join(matched_folder, frame_name)
            Image.open(frame_path).save(matching_image_path)
            print(f"Saved matched frame: {frame_name} for description: '{description}' with similarity: {similarity_score:.2f}")

            # Mark this description as matched and exit the loop
            matched_descriptions.add(description)
            break  # Exit the loop once a match is found

    # Optional: Clean up the matched descriptions if a new match is found
    if len(matched_descriptions) > 1:
        matched_descriptions = set(descriptions[:1])  # Keep only the first matched description

print("Matching frames saved in the 'matched' folder!")
