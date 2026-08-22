import torch
import torch.nn as nn


class Sequence1DCNN(nn.Module):
    """
    1D-CNN Stream for Amino Acid Sequence Feature Extraction.
    Input: Tokenized Sequence Tensor (Batch Size, Seq Length)
    Output: Binary Classification Probabilities (Sensitive vs Resistant)
    """

    def __init__(self, vocab_size=21, embed_dim=64, num_classes=2):
        super(Sequence1DCNN, self).__init__()

        # Amino Acid Embedding Layer
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # 1D Convolutional Layer for Sequence Pattern Extraction
        self.conv1 = nn.Conv1d(in_channels=embed_dim,
                               out_channels=128, kernel_size=5, padding=2)
        self.relu = nn.ReLU()

        # Global Average Pooling to capture key features across length
        self.pool = nn.AdaptiveAvgPool1d(1)

        # Fully Connected Layer
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        # x shape: (batch_size, seq_len)
        # (batch_size, seq_len, embed_dim)
        x = self.embedding(x)
        # (batch_size, embed_dim, seq_len) for Conv1d
        x = x.permute(0, 2, 1)
        x = self.relu(self.conv1(x))          # (batch_size, 128, seq_len)
        x = self.pool(x).squeeze(-1)          # (batch_size, 128)
        logits = self.fc(x)                   # (batch_size, num_classes)
        return torch.softmax(logits, dim=1)
