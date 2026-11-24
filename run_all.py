"""
Quantum Teleportation Project — Master Runner
=============================================
Run this single script to generate ALL project outputs:
  1. Run the PennyLane simulation + save results PNG
  2. Generate the animated video demo (MP4 or GIF)
  3. Build the PowerPoint presentation
  4. Write the Word report
"""

import subprocess, sys, os

scripts = [
    ("simulation.py",     "🔬 Running PennyLane quantum teleportation simulation..."),
    ("generate_demo.py",  "🎬 Generating animated video demo..."),
    ("generate_pptx.py",  "📊 Building PowerPoint presentation..."),
    ("generate_report.py","📄 Writing Word report..."),
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for script, msg in scripts:
    print(f"\n{'='*60}")
    print(msg)
    print('='*60)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"⚠️  {script} exited with code {result.returncode}")

print("\n" + "="*60)
print("🎉  ALL OUTPUTS GENERATED SUCCESSFULLY!")
print("="*60)
print("\nFiles in this folder:")
for f in sorted(os.listdir(".")):
    if not f.endswith(".py"):
        size = os.path.getsize(f) / 1024
        print(f"  📁 {f:<45} {size:>7.1f} KB")
