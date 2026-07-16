import os
import json
import torch
from torch.utils.data import Dataset

class InvoiceDataset(Dataset):
    def __init__(self, box_dir, entity_dir):

        self.box_dir = box_dir
        self.entity_dir = entity_dir

        self.files = [
            f for f in os.listdir(box_dir)
            if f.endswith(".txt")
        ]

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):

        filename = self.files[index]

        # Read OCR text
        box_path = os.path.join(self.box_dir, filename)

        words = []

        with open(box_path, "r", encoding="utf-8") as file:

            for line in file:

                parts = line.strip().split(",")

                if len(parts) > 8:
                    text = ",".join(parts[8:])
                    words.append(text)

        text = " ".join(words)

        # Read labels
        entity_path = os.path.join(self.entity_dir, filename)

        with open(entity_path, "r", encoding="utf-8") as file:
            labels = json.load(file)

        return text, {
            "company": labels.get("company", ""),
            "date": labels.get("date", ""),
            "address": labels.get("address", ""),
            "total": labels.get("total", "")
            }