import logging
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from huggingface_hub import hf_hub_download

from core.config import settings


logger = logging.getLogger(__name__)


class PlantDiseaseEfficientNet(nn.Module):
    """
    EfficientNet-B0 model for 38-class plant disease classification.
    """

    def __init__(self, num_classes: int = 38):
        super().__init__()

        # Load EfficientNet-B0 architecture (without the wrapper)
        efficientnet = models.efficientnet_b0(weights=None)
        
        # Replace the classifier
        in_features = efficientnet.classifier[1].in_features
        efficientnet.classifier = nn.Sequential(
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(in_features, num_classes)
        )
        
        # Assign directly to self (not self.model)
        self.features = efficientnet.features
        self.avgpool = efficientnet.avgpool
        self.classifier = efficientnet.classifier

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


class ModelManager:
    """
    Manages model loading and inference.
    """

    def __init__(self):

        self.model: Optional[nn.Module] = None

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.is_loaded = False

        # IMPORTANT:
        # These MUST match dataset.classes
        # used during training.

        self.class_names = [
            'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
            'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
            'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
            'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
            'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
            'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
            'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
        ]

    def download_model(self) -> Path:
        """
        Download model from Hugging Face Hub.
        """

        try:

            logger.info(
                f"Downloading model from {settings.HF_MODEL_REPO}..."
            )

            models_dir = Path("models")
            models_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            model_path = hf_hub_download(
                repo_id=settings.HF_MODEL_REPO,
                filename=settings.HF_MODEL_FILE,
                local_dir=str(models_dir),
            )

            logger.info(
                f"Model downloaded to: {model_path}"
            )

            return Path(model_path)

        except Exception as e:

            logger.error(
                f"Error downloading model: {str(e)}"
            )

            raise

    def load_model(
        self,
        model_path: Optional[Path] = None
    ) -> None:
        """
        Load the trained model.
        """

        try:

            if model_path is None:
                model_path = Path(
                    settings.MODEL_PATH
                )

            # Download if model doesn't exist
            if not model_path.exists():

                logger.info(
                    "Model not found locally, downloading..."
                )

                model_path = self.download_model()

            logger.info(
                f"Loading EfficientNet-B0 model from {model_path}..."
            )

            # -------------------------
            # Initialize architecture
            # -------------------------

            self.model = PlantDiseaseEfficientNet(
                num_classes=len(self.class_names)
            )

            # -------------------------
            # Load trained weights
            # -------------------------

            checkpoint = torch.load(
                model_path,
                map_location=self.device
            )
            
            # Extract model state dict from checkpoint
            # The checkpoint contains: model_state_dict, class_names, etc.
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                # Update class names if available in checkpoint
                if 'class_names' in checkpoint:
                    self.class_names = checkpoint['class_names']
            else:
                state_dict = checkpoint

            self.model.load_state_dict(
                state_dict
            )

            # -------------------------
            # Move model to device
            # -------------------------

            self.model.to(self.device)

            # Evaluation mode
            self.model.eval()

            self.is_loaded = True

            logger.info(
                f"EfficientNet-B0 model loaded successfully on {self.device}"
            )

        except Exception as e:

            logger.error(
                f"Error loading model: {str(e)}"
            )

            self.is_loaded = False

            raise

    def predict(
        self,
        image_tensor: torch.Tensor
    ) -> dict:
        """
        Make prediction on an image tensor.

        Expected input shape:

        [1, 3, 224, 224]
        """

        if not self.is_loaded or self.model is None:

            raise RuntimeError(
                "Model not loaded"
            )

        try:

            with torch.no_grad():

                # Move image to same device as model
                image_tensor = image_tensor.to(
                    self.device
                )

                # -------------------------
                # Forward pass
                # -------------------------

                outputs = self.model(
                    image_tensor
                )

                # Convert logits → probabilities
                probabilities = F.softmax(
                    outputs,
                    dim=1
                )

                # -------------------------
                # Top prediction
                # -------------------------

                confidence, predicted_idx = torch.max(
                    probabilities,
                    dim=1
                )

                predicted_index = predicted_idx.item()

                predicted_class = self.class_names[
                    predicted_index
                ]

                confidence_score = confidence.item()

                # -------------------------
                # Top 5 predictions
                # -------------------------

                top5_prob, top5_idx = torch.topk(
                    probabilities,
                    k=5,
                    dim=1
                )

                top5_predictions = []

                for prob, idx in zip(
                    top5_prob[0],
                    top5_idx[0]
                ):

                    top5_predictions.append({
                        "class": self.class_names[
                            idx.item()
                        ],
                        "confidence": prob.item()
                    })

                # -------------------------
                # Response
                # -------------------------

                return {
                    "predicted_class": predicted_class,
                    "confidence": confidence_score,
                    "top5_predictions": top5_predictions
                }

        except Exception as e:

            logger.error(
                f"Error during prediction: {str(e)}"
            )

            raise

    def get_info(self) -> dict:
        """
        Get model information.
        """

        return {
            "model_loaded": self.is_loaded,
            "device": str(self.device),
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "pytorch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available()
        }


# ---------------------------------
# Global model manager instance
# ---------------------------------

model_manager = ModelManager()