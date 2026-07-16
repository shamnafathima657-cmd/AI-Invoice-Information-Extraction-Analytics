import os
from dataset import InvoiceDataset

# Dataset paths
BOX_DIR = "../dataset/SROIE2019/train/box"
ENTITY_DIR = "../dataset/SROIE2019/train/entities"

# Load dataset
dataset = InvoiceDataset(BOX_DIR, ENTITY_DIR)

print("Total invoices:", len(dataset))

# Display first sample
text, label = dataset[0]

print("Invoice Text:")
print(text[:500])

print("\nGround Truth:")
print(label)

# Build Vocabulary
vocab = {
    "<PAD>": 0,
    "<UNK>": 1
}

for i in range(len(dataset)):

    text, _ = dataset[i]

    for word in text.lower().split():

        if word not in vocab:
            vocab[word] = len(vocab)

print("Vocabulary Size:", len(vocab))

# Convert text to token IDs
encoded_texts = []

for i in range(len(dataset)):
    text, labels = dataset[i]

    tokens = [
        vocab.get(word, vocab["<UNK>"])
        for word in text.lower().split()
    ]

    encoded_texts.append(tokens)

print("First 20 Token IDs:")
print(encoded_texts[0][:20])

# PyTorch DataLoader


import torch
from torch.utils.data import DataLoader, TensorDataset
from torch.nn.utils.rnn import pad_sequence

# Convert token lists to tensors
token_tensors = [torch.tensor(tokens, dtype=torch.long) for tokens in encoded_texts]

# Pad all sequences to the same length
padded_tokens = pad_sequence(
    token_tensors,
    batch_first=True,
    padding_value=vocab["<PAD>"]
)

# Create label mapping
label_map = {}

encoded_labels = []

for i in range(len(dataset)):
    _, label = dataset[i]

    key = (
        label["company"],
        label["date"],
        label["address"],
        label["total"]
    )

    if key not in label_map:
        label_map[key] = len(label_map)

    encoded_labels.append(label_map[key])

labels = torch.tensor(encoded_labels, dtype=torch.long)

print("Number of unique invoice labels:", len(label_map))

# Create Dataset and DataLoader
train_dataset = TensorDataset(padded_tokens, labels)

train_loader = DataLoader(
    train_dataset,
    batch_size=8,
    shuffle=True
)

print("Number of batches:", len(train_loader))

# Test one batch
for inputs, targets in train_loader:
    print("Input Shape:", inputs.shape)
    print("Target Shape:", targets.shape)
    break

import torch.nn as nn
import torch.optim as optim

from transformer_model import InvoiceTransformer

# Create the model
model = InvoiceTransformer(
    vocab_size=len(vocab),
    embed_dim=128,
    num_heads=4,
    num_layers=2,
    hidden_dim=256,
    num_classes=len(label_map)
)

# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5

print("Training Started...\n")

for epoch in range(epochs):

    total_loss = 0

    for inputs, targets in train_loader:

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = criterion(outputs, targets)

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss:.4f}")

# Save model
torch.save(model.state_dict(), "invoice_transformer.pth")

print("\nModel trained successfully!")
print("Model saved as invoice_transformer.pth")
import json

with open("vocab.json", "w") as f:
    json.dump(vocab, f, indent=4)

with open("label_map.json", "w") as f:
    json.dump({str(k): v for k, v in label_map.items()}, f, indent=4)

print("vocab.json saved")
print("label_map.json saved")