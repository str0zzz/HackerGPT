#!/usr/bin/env python3
"""
HackerGPT APK Build Script
Usage: python hackergpt_build.py [android|ios|windows|macos|linux]
"""

import sys
import os
import subprocess


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flet
        print("[+] Flet installed:", flet.__version__)
    except ImportError:
        print("[!] Installing Flet...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
    
    try:
        import groq
        print("[+] Groq installed")
    except ImportError:
        print("[!] Installing groq...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    
    try:
        import PyPDF2
        print("[+] PyPDF2 installed")
    except ImportError:
        print("[!] Installing PyPDF2...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    
    try:
        import docx
        print("[+] python-docx installed")
    except ImportError:
        print("[!] Installing python-docx...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    
    try:
        from PIL import Image
        print("[+] Pillow installed")
    except ImportError:
        print("[!] Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])


def build_apk():
    """Build Android APK using Flet"""
    print("[*] Building Android APK for HackerGPT...")
    print("[*] This may take a few minutes...")
    
    # Ensure all deps are installed first
    check_dependencies()
    
    # Create requirements file
    with open("build_requirements.txt", "w") as f:
        f.write("""flet==0.27.1
groq==0.19.1
PyPDF2==0.4.0
python-docx==1.1.2
Pillow==11.1.1
""")
    
    # Build command
    cmd = [
        sys.executable, "-m", "flet",
        "build", "apk",
        "hackergpt_app.py",
        "--name", "HackerGPT",
        "--package-name", "com.hydrastrozzz.hackergpt",
        "--description", "Unrestricted AI by Hydra Strozzz",
        "--product", "HackerGPT",
        "--org", "hydrastrozzz",
        "--icon", "icon.png" if os.path.exists("icon.png") else "",
    ]
    
    # Remove empty args
    cmd = [c for c in cmd if c]
    
    try:
        subprocess.check_call(cmd)
        print("\n[+] APK Build Successful!")
        print("[+] APK location: build/apk/HackerGPT.apk")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Build failed: {e}")
        print("[!] Try building manually:")
        print("    flet build apk hackergpt_app.py --name HackerGPT --package-name com.hydrastrozzz.hackergpt")
    except FileNotFoundError:
        print("\n[!] Flet not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
        build_apk()


def build_ios():
    """Build iOS app"""
    print("[*] iOS build requires macOS with Xcode installed.")
    print("[*] Building...")
    
    cmd = [
        sys.executable, "-m", "flet",
        "build", "ipa",
        "hackergpt_app.py",
        "--name", "HackerGPT",
        "--package-name", "com.hydrastrozzz.hackergpt",
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n[+] iOS Build Successful!")
    except:
        print("\n[!] iOS build failed. Ensure you're on macOS with Xcode.")


def build_desktop(platform):
    """Build desktop app"""
    print(f"[*] Building for {platform}...")
    
    cmd = [
        sys.executable, "-m", "flet",
        "build", platform,
        "hackergpt_app.py",
        "--name", "HackerGPT",
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"\n[+] {platform.title()} Build Successful!")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Build failed: {e}")


def create_app_icon():
    """Create a simple app icon if not exists"""
    if os.path.exists("icon.png"):
        return
    
    print("[*] Creating app icon...")
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        for size in [192, 512]:
            img = Image.new("RGB", (size, size), "#0a0a0f")
            draw = ImageDraw.Draw(img)
            
            # Try to find a font
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\arial.ttf",
            ]
            
            font = None
            for fp in font_paths:
                if os.path.exists(fp):
                    font = ImageFont.truetype(fp, int(size * 0.6))
                    break
            
            if not font:
                font = ImageFont.load_default()
            
            # Draw skull-like H
            bbox = draw.textbbox((0, 0), "H", font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = (size - tw) / 2
            y = (size - th) / 2 - size * 0.05
            
            draw.text((x, y), "H", fill="#00ff41", font=font)
            
            # Save
            if size == 192:
                img.save("icon.png")
            img.save(f"icon_{size}.png")
        
        print("[+] App icon created: icon.png")
    
    except Exception as e:
        print(f"[!] Could not create icon: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("HackerGPT Build Script")
        print("Usage:")
        print("  python hackergpt_build.py android    - Build APK")
        print("  python hackergpt_build.py ios        - Build iOS app (macOS only)")
        print("  python hackergpt_build.py windows    - Build Windows exe")
        print("  python hackergpt_build.py macos      - Build macOS app")
        print("  python hackergpt_build.py linux      - Build Linux binary")
        print("  python hackergpt_build.py run        - Run on desktop")
        print("")
        sys.exit(1)
    
    platform = sys.argv[1].lower()
    
    if platform == "run":
        # Just run the app on desktop
        print("[*] Running HackerGPT on desktop...")
        os.environ.setdefault("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        exec(open("hackergpt_app.py").read())
    
    elif platform == "android":
        create_app_icon()
        check_dependencies()
        build_apk()
    
    elif platform == "ios":
        create_app_icon()
        check_dependencies()
        build_ios()
    
    elif platform in ("windows", "macos", "linux"):
        create_app_icon()
        check_dependencies()
        build_desktop(platform)
    
    else:
        print(f"[!] Unknown platform: {platform}")
        print("Supported: android, ios, windows, macos, linux, run")
