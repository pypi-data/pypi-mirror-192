from typing import Any

import lightning.pytorch as pl
import torch
import torchvision
from torch import nn, optim
from torch.functional import F


class SimCLR(pl.LightningModule):
    def __init__(self, hidden_dim, num_classes, lr, temperature, weight_decay, max_epochs=500):
        super().__init__()
        self.save_hyperparameters()

        assert temperature > 0.0, "The temperature must be a positive float!"

        # Base model f(.)
        self.encoder = torchvision.models.shufflenet_v2_x1_0(
            pretrained=False, num_classes=num_classes * hidden_dim
        )  # num_classes is the output size of the last linear layer

        in_features = self.encoder.fc.in_features

        self.encoder.fc = nn.Identity()

        # The MLP for g(.) consists of Linear->ReLU->Linear
        self.projector = nn.Sequential(
            nn.Linear(in_features, in_features, bias=False),  # Linear(ResNet output, 4*hidden_dim)
            nn.ReLU(),
            nn.Linear(in_features, projection_dim, bias=False),
        )
    
    def forward(self, *x: list[Any]):
        for 

    def configure_optimizers(self):
        optimizer = optim.AdamW(self.parameters(), lr=self.hparams.lr, weight_decay=self.hparams.weight_decay)
        lr_scheduler = optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=self.hparams.max_epochs, eta_min=self.hparams.lr / 50
        )
        return [optimizer], [lr_scheduler]

    def info_nce_loss(self, batch, mode="train"):
        imgs, _ = batch
        imgs = torch.cat(imgs, dim=0)

        # Encode all images
        feats = self.convnet(imgs)
        # Calculate cosine similarity
        cos_sim = F.cosine_similarity(feats[:, None, :], feats[None, :, :], dim=-1)
        # Mask out cosine similarity to itself
        self_mask = torch.eye(cos_sim.shape[0], dtype=torch.bool, device=cos_sim.device)
        cos_sim.masked_fill_(self_mask, -9e15)
        # Find positive example -> batch_size//2 away from the original example
        pos_mask = self_mask.roll(shifts=cos_sim.shape[0] // 2, dims=0)
        # InfoNCE loss
        cos_sim = cos_sim / self.hparams.temperature
        nll = -cos_sim[pos_mask] + torch.logsumexp(cos_sim, dim=-1)
        nll = nll.mean()

        # Logging loss
        self.log(mode + "_loss", nll)
        # Get ranking position of positive example
        comb_sim = torch.cat(
            [cos_sim[pos_mask][:, None], cos_sim.masked_fill(pos_mask, -9e15)],  # First position positive example
            dim=-1,
        )
        sim_argsort = comb_sim.argsort(dim=-1, descending=True).argmin(dim=-1)
        # Logging ranking metrics
        self.log(mode + "_acc_top1", (sim_argsort == 0).float().mean())
        self.log(mode + "_acc_top5", (sim_argsort < 5).float().mean())
        self.log(mode + "_acc_mean_pos", 1 + sim_argsort.float().mean())

        return nll

    def training_step(self, batch, batch_idx):
        return self.info_nce_loss(batch, mode="train")

    def validation_step(self, batch, batch_idx):
        self.info_nce_loss(batch, mode="val")