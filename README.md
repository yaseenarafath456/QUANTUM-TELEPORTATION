# ⚛ Quantum Teleportation Project

A complete quantum computing mini-project simulating quantum teleportation using **PennyLane**, with an animated demo video, PowerPoint presentation, and Word report.

---

## 📂 Project Structure

```
quantum_teleportation/
├── simulation.py          # Core PennyLane simulation + fidelity analysis
├── generate_demo.py       # Matplotlib animated video (MP4/GIF)
├── generate_pptx.py       # PowerPoint slide deck (7 slides, dark theme)
├── generate_report.py     # Word report (.docx)
├── run_all.py             # 🚀 Master runner — generates all outputs
└── README.md              # This file
```

### Generated Outputs
| File | Description |
|------|-------------|
| `quantum_teleportation_results.png` | Density matrices + fidelity bar chart |
| `quantum_teleportation_demo.mp4` | 8-second animated video demo |
| `quantum_teleportation.pptx` | 7-slide dark-theme presentation |
| `quantum_teleportation_report.docx` | Full technical Word report |

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install pennylane matplotlib numpy python-pptx python-docx Pillow

# Generate ALL outputs at once
python run_all.py

# Or run individually:
python simulation.py        # PennyLane sim + PNG
python generate_demo.py     # Animated video
python generate_pptx.py     # PowerPoint
python generate_report.py   # Word report
```

---

## 🧪 What the Simulation Does

1. **Prepares** an arbitrary qubit state |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
2. **Creates** a Bell pair (entangled pair) between Alice (wire 1) and Bob (wire 2)
3. **Performs** Alice's Bell measurement via CNOT + Hadamard + mid-circuit measure
4. **Applies** conditional X and Z gates on Bob's qubit based on Alice's 2 classical bits
5. **Verifies** teleportation by computing density matrices and quantum fidelity F(ρ_A, ρ_B)

### Results
- **Single state fidelity**: F = 1.0000 ✅
- **Average over 20 random states**: F ≈ 1.0000 ✅
- **Backend**: PennyLane `default.qubit` (noise-free simulator)

---

## 🧠 Key Quantum Concepts

| Concept | Role in Teleportation |
|---------|----------------------|
| **Superposition** | Input qubit is in α\|0⟩ + β\|1⟩ |
| **Entanglement** | Bell pair is the quantum channel |
| **Bell Measurement** | Collapses 3-qubit state into 4 cases |
| **No-Cloning Theorem** | Original state is destroyed (not copied) |
| **Fidelity** | Measures accuracy of state transfer |

---

## 📦 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| `pennylane` | ≥ 0.45 | Quantum circuit simulation |
| `numpy` | ≥ 2.0 | Linear algebra |
| `matplotlib` | ≥ 3.11 | Visualisation & animation |
| `python-pptx` | ≥ 1.0 | PowerPoint generation |
| `python-docx` | ≥ 1.2 | Word document generation |
| `Pillow` | ≥ 13.0 | GIF export fallback |

---

## 📖 Reference

Bennett, C.H. et al. (1993). *Teleporting an Unknown Quantum State via Dual Classical and Einstein-Podolsky-Rosen Channels*. Phys. Rev. Lett. 70, 1895.
