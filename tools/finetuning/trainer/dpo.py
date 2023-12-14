from omegaconf import OmegaConf

class DPOTrainer:
    def __init__(self, config: OmegaConf):
        self.config = config

