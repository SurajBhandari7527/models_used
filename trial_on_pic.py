import torch
from torchvision import models, transforms
from PIL import Image

# Load the pre-trained action recognition model
model = models.video.r3d_18(weights='R3D_18_Weights.DEFAULT')
model.eval()  # Set the model to evaluation mode

# Transformation for input images
preprocess = transforms.Compose([
    transforms.Resize((112, 112)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Test with a single image
frame_path = "C:/Users/Suraj Bhandari/OneDrive/Desktop/whatever/models/frame_extracted/frame_0.jpg"
try:
    # Open and ensure the image is in RGB
    frame = Image.open(frame_path).convert("RGB")
    print(f"Processing {frame_path} - Mode: {frame.mode}")  # Check the image mode

    # Preprocess the image
    input_tensor = preprocess(frame)  # Shape: [3, 112, 112]

    # Create a mini-batch of frames (simulate depth)
    depth = 16  # Number of frames to simulate
    # Create the input batch with the correct dimensions
    input_batch = input_tensor.unsqueeze(0).unsqueeze(0).expand(1, depth, 3, 112, 112)

    # Print the shape of input_batch
    print(f"Input batch shape: {input_batch.shape}")  # Should be [1, 16, 3, 112, 112]

    # Check for model input compatibility
    with torch.no_grad():
        output = model(input_batch)

    print("Model output obtained.")
except Exception as e:
    print(f"An error occurred: {e}")
