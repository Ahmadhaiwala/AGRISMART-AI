import logging
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from huggingface_hub import hf_hub_download

from core.config import settings


logger = logging.getLogger(__name__)


class PlantDiseaseCNN(nn.Module):
    """
    CNN model used for the 15-class PlantVillage
    plant disease classification model.
    """

    def __init__(self, num_classes: int = 15):
        super().__init__()

        # -------------------------
        # Convolutional layers
        # -------------------------

        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=32,
            kernel_size=3,
            padding=1
        )

        self.conv2 = nn.Conv2d(
            in_channels=32,
            out_channels=64,
            kernel_size=3,
            padding=1
        )

        self.conv3 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=3,
            padding=1
        )

        # -------------------------
        # Pooling
        # -------------------------

        self.pool = nn.MaxPool2d(
            kernel_size=2,
            stride=2
        )

        # -------------------------
        # Fully connected layers
        # -------------------------

        # Input image:
        # 224 x 224
        #
        # After 3 pooling operations:
        # 224 -> 112 -> 56 -> 28
        #
        # Therefore:
        # 128 feature maps x 28 x 28

        self.fc1 = nn.Linear(
            128 * 28 * 28,
            256
        )

        self.fc2 = nn.Linear(
            256,
            num_classes
        )

    def forward(self, x):

        # Conv block 1
        x = self.pool(
            F.relu(self.conv1(x))
        )

        # Conv block 2
        x = self.pool(
            F.relu(self.conv2(x))
        )

        # Conv block 3
        x = self.pool(
            F.relu(self.conv3(x))
        )

        # Flatten
        x = torch.flatten(x, 1)

        # Fully connected
        x = F.relu(self.fc1(x))

        # Output logits
        x = self.fc2(x)

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
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_healthy",
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
                f"Loading model from {model_path}..."
            )

            # -------------------------
            # Initialize architecture
            # -------------------------

            self.model = PlantDiseaseCNN(
                num_classes=len(self.class_names)
            )

            # -------------------------
            # Load trained weights
            # -------------------------

            state_dict = torch.load(
                model_path,
                map_location=self.device
            )

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
                f"Model loaded successfully on {self.device}"
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