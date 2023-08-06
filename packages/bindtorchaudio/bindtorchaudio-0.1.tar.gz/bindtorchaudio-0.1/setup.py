import setuptools
import torch

# Get the PyTorch version
pytorch_version = torch.__version__

# Set the torchaudio version based on the PyTorch version
if pytorch_version.startswith("1.13.1"):
    torchaudio_version = "0.13.1"
elif pytorch_version.startswith("1.13.0"):
    torchaudio_version = "0.12.1"
elif pytorch_version.startswith("1.12.1"):
    torchaudio_version = "0.12.1"
elif pytorch_version.startswith("1.12.0"):
    torchaudio_version = "0.12.1"
elif pytorch_version.startswith("1.11"):
    torchaudio_version = "0.11.0"
elif pytorch_version.startswith("1.10"):
    torchaudio_version = "0.10.0"
elif pytorch_version.startswith("1.9"):
    torchaudio_version = "0.9.1"
elif pytorch_version.startswith("1.8"):
    torchaudio_version = "0.8.1"
elif pytorch_version.startswith("1.7"):
    torchaudio_version = "0.7.2"
elif pytorch_version.startswith("1.6"):
    torchaudio_version = "0.6.0"
elif pytorch_version.startswith("1.5"):
    torchaudio_version = "0.5.0"
elif pytorch_version.startswith("1.4"):
    torchaudio_version = "0.4.0"
else:
    raise ValueError("Unsupported PyTorch version")

# Install torchaudio
setuptools.setup(
    name="bindtorchaudio",
    version="0.1",
    install_requires=[f"torchaudio=={torchaudio_version}"]
)
