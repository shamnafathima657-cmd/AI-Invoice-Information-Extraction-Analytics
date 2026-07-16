import json
import torch
import os

from models.transformer_model import InvoiceTransformer


BASE_DIR = os.path.dirname(__file__)

# Load vocabulary
with open(os.path.join(BASE_DIR, "vocab.json"), "r") as f:
    vocab = json.load(f)

# Load label map
with open(os.path.join(BASE_DIR, "label_map.json"), "r") as f:
    label_map = json.load(f)

reverse_label_map = {v: k for k, v in label_map.items()}

model = InvoiceTransformer(
    vocab_size=len(vocab),
    embed_dim=128,
    num_heads=4,
    num_layers=2,
    hidden_dim=256,
    num_classes=len(label_map)
)

# Load trained model
model.load_state_dict(
    torch.load(
        os.path.join(BASE_DIR, "invoice_transformer.pth")
    )
)

model.eval()


def predict(text):
    tokens = [
        vocab.get(word.lower(), vocab["<UNK>"])
        for word in text.split()
    ]

    x = torch.tensor([tokens], dtype=torch.long)

    with torch.no_grad():
        output = model(x)
        pred = torch.argmax(output, dim=1).item()

    return reverse_label_map[pred]


if __name__ == "__main__":
    sample = """
    BOOK TA .K (TAMAN DAYA)
    DATE 25/12/2018
    TOTAL 9.00
    """

    result = predict(sample)

    print("Prediction:")
    print(result)