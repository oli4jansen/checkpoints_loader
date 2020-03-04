import os
from urllib import request, urlparse
import torch
import shutil

device = 'cuda' if torch.cuda.is_available() else 'cpu'


class CheckpointsLoader():

  def __init__(self, checkpoints_directory='checkpoints/'):
    """Initialise the loader with the directory where checkpoints should be stored"""
    self.checkpoints_directory = checkpoints_directory
    # Make sure local checkpoints directory exists
    os.makedirs(self.checkpoints_directory, exist_ok=True)

  def load(self, model, url, strict=True, checkpoints_key=None):
    # Extract filename from URL
    filename = os.path.basename(urlparse(url).path)
    # Build local path to checkpoints file
    filepath = os.path.join(self.checkpoints_directory, filename)

    # Download the checkpoints file if it does not exist yet
    if not os.path.isfile(filepath):
      with urllib.request.urlopen(url) as download, open(filename, 'wb') as file:
        shutil.copyfileobj(download, file)

    # Open the checkpoints file
    checkpoints = torch.load(filepath, map_location=device)

    # If a key was provided, traverse the dict to that location
    if checkpoints_key:
      keys = checkpoints_key.split('.')
      for key in keys:
        checkpoints = checkpoints[key]

    # Load the checkpoints
    model.load_state_dict(checkpoints, strict=strict)

    return model