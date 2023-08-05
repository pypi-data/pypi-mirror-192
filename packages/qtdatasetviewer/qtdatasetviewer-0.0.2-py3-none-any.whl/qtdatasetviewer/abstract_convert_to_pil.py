# -*- encoding: utf-8 -*-
# ! python3

from abc import ABC, abstractmethod
from torch.utils.data import Dataset
from PIL import Image


class AbstractConvertToPil(ABC):

    def __init__(self, dataloader: Dataset):
        self.dataloader = dataloader
        super().__init__()

    @abstractmethod
    def convert(self, item) -> Image:
        pass

    def get_dataloader(self) -> Dataset:
        return self.dataloader

    def get_size(self) -> int:
        return len(self.dataloader)
