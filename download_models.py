#!/usr/bin/env python3
"""
Script to pre-download EasyOCR models
Run this once to avoid waiting during first image upload
"""

import easyocr
import sys

def download_models():
    print("Downloading EasyOCR models...")
    print("This may take several minutes depending on your internet connection.")
    print("Progress will be shown below:")
    print("-" * 50)
    
    try:
        # Initialize reader which will download models
        reader = easyocr.Reader(['en'])
        print("\n✅ Models downloaded successfully!")
        print("You can now use the image text extraction feature without waiting.")
        
    except Exception as e:
        print(f"\n❌ Error downloading models: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_models() 