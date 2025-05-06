import os, sys, socket
from glob import glob
hostname = socket.gethostname()

if hostname == "hjpui-MacBookPro.local":
    # PROJECT_ROOT    = "/Users/hjp/HJP/KUAICV/VTO/florence-tailor"
    DATASET_ROOT    = "/Users/hjp/HJP/KUAICV/VTO/DATASET/PoC59"
    PYGARMENT_ROOT  = "/Users/hjp/HJP/KUAICV/VTO/GarmentCodeAnalysis"

elif hostname == "hjp-Z690-AERO-G":
    DATASET_ROOT = ""
    PYGARMENT_ROOT = r"E:\HJP\KUAICV\VTO\REFERENCES\GarmentCodeAnalysis"