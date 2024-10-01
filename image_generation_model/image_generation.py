

from diffusers import StableDiffusionPipeline
import torch

# Load Stable Diffusion model
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id).to("cuda")  # Use 'cpu' if no GPU

# Define your text prompt
prompt =  [
    "Scene 1: Lila finds the hourglass in an attic, dusting it off and discovering its powers.",
    "Scene 2: Lila excitedly uses the hourglass, pausing time to play in the village while her friends work.",
    "Scene 3: Weeks pass, showing Lila's friends achieving their goals while she enjoys endless fun.",
    "Scene 4: Lila overhears her friends discussing their dreams and feels regret for not joining them.",
    "Scene 5: Lila decides to use her last hour to help her friends create a mural together.",
    "Scene 6: The village celebrates the mural, and Lila realizes the value of shared experiences."
]
count=0
for i in prompt:

    # Generate image
    image = pipe(prompt).images[0]

    # Save the output image
    image.save("generated_image{}.png".format(count))
    count=count+1
    
