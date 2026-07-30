# Brain Tumor MRI Classification

Deep learning pipeline that classifies brain MRI scans into four categories — **glioma**, **meningioma**, **pituitary tumor**, and **no tumor** — using PyTorch. Three architectures are trained and compared: a custom CNN built from scratch, a transfer-learned MobileNetV3-Large, and a fine-tuned EfficientNetV2-S.

## Dataset

[Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) (Kaggle) — MRI images across 4 classes, pre-split into Training and Testing sets. Downloaded via `kagglehub` directly inside the notebook.

## Models

| Model | Approach |
|---|---|
| Custom CNN | 4 conv blocks (Conv → BatchNorm → ReLU → MaxPool) trained from scratch |
| MobileNetV3-Large | ImageNet-pretrained, classifier head replaced and trained (frozen backbone) |
| EfficientNetV2-S | ImageNet-pretrained, last two blocks + classifier fine-tuned, trained with mixup augmentation |

## Results

| Model | Test Accuracy | Params (approx.) |
|---|---|---|
| Custom CNN | 88% | ~12M |
| MobileNetV3-Large | 92.50% | ~5M |
| EfficientNetV2-S | 93% | ~21M |

Full training curves, classification reports, and confusion matrices for each model are in the notebook.

## Repo structure

```
brain_tumor_cnn_resnet18_efficientnet.ipynb   # full pipeline: EDA, training, evaluation, deployment
```

## Running it

1. Open the notebook in Google Colab
2. Runtime → Change runtime type → GPU
3. Run all cells — the dataset downloads automatically via `kagglehub` (needs a Kaggle API token on first run)
4. Trained weights save locally as `.pth` files during training

## Inference

The notebook includes a `predict_single_image(image_path)` function that loads the best-performing model and returns the predicted class with per-class confidence scores for any single MRI image.

## Requirements

- torch, torchvision
- numpy, pandas, matplotlib, seaborn
- scikit-learn, pillow
- kagglehub
