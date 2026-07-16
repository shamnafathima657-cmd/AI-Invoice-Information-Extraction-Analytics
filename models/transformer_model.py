import torch
import torch.nn as nn

class InvoiceTransformer(nn.Module):
    def __init__(
        self,
        vocab_size,
        embed_dim=128,
        num_heads=4,
        num_layers=2,
        hidden_dim=256,
        num_classes=4
    ):
        super(InvoiceTransformer, self).__init__()

        # Word Embedding
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        # Output Layer
        self.fc = nn.Linear(embed_dim, num_classes)

    def forward(self, x):

        x = self.embedding(x)

        x = self.transformer(x)

        x = x.mean(dim=1)

        output = self.fc(x)

        return output