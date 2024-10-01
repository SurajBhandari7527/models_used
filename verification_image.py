import torch
print(torch.__version__)  # Check the version
print(torch.cuda.is_available())  # Should return True
print(torch.cuda.current_device())  # Should return the current device ID
print(torch.cuda.get_device_name(0))  # Should return the name of your GPU
