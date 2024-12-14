import torch

print(f"CUDA disponible : {torch.cuda.is_available()}")
print(f"Nom du GPU : {torch.cuda.get_device_name(0)}" if torch.cuda.is_available() else "Aucun GPU détecté")
