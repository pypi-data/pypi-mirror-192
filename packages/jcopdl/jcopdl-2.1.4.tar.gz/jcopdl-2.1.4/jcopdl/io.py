import torch


def load_from_checkpoint(checkpoint_path):
    callback = torch.load(checkpoint_path)
    model = callback.model
    optimizer = callback.optimizer
    return model, optimizer, callback
