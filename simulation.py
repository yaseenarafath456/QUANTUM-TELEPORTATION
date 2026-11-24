"""
Quantum Teleportation Simulation
=================================
Simulates teleporting an arbitrary qubit state |ψ⟩ = α|0⟩ + β|1⟩
from Alice to Bob using PennyLane.

Steps:
  1. Prepare the qubit to teleport (wire 0) in an arbitrary state.
  2. Create a Bell pair (entangled pair) between Alice (wire 1) and Bob (wire 2).
  3. Alice performs a Bell measurement on her two qubits (wires 0 & 1).
  4. Bob applies correction gates conditioned on Alice's classical results.
  5. Bob's qubit (wire 2) is now in the original state |ψ⟩.
"""

import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ─── Device ───────────────────────────────────────────────────────────────────
dev = qml.device("default.qubit", wires=3)

# ─── Helper: Bloch sphere coordinates from state vector ───────────────────────
def bloch_coords(state):
    """Return (x, y, z) Bloch sphere coords for a single-qubit state."""
    alpha, beta = state[0], state[1]
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2
    return float(x), float(y), float(z)

# ─── Full Teleportation Circuit ────────────────────────────────────────────────
@qml.qnode(dev)
def teleportation_circuit(theta, phi):
    """
    Teleport a qubit prepared in state R_y(theta) R_z(phi)|0⟩.
    Returns the statevector of Bob's qubit after teleportation.
    """
    # Step 1: Prepare the state to teleport on wire 0
    qml.RY(theta, wires=0)
    qml.RZ(phi, wires=0)

    # Step 2: Create Bell pair between wire 1 (Alice) and wire 2 (Bob)
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 2])

    # Step 3: Alice's Bell measurement preparation
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)

    # Measure Alice's qubits
    m0 = qml.measure(0)
    m1 = qml.measure(1)

    # Step 4: Bob applies corrections based on Alice's results
    qml.cond(m1, qml.PauliX)(wires=2)
    qml.cond(m0, qml.PauliZ)(wires=2)

    # Return Bob's qubit state (density matrix for wire 2)
    return qml.density_matrix(wires=2)

# ─── Reference: Original state ────────────────────────────────────────────────
@qml.qnode(dev)
def original_state_circuit(theta, phi):
    """Prepare and return the state we want to teleport."""
    qml.RY(theta, wires=0)
    qml.RZ(phi, wires=0)
    return qml.density_matrix(wires=0)

# ─── Fidelity calculation ──────────────────────────────────────────────────────
def fidelity(rho1, rho2):
    """Compute quantum fidelity F(ρ1, ρ2) = Tr(ρ1 ρ2) for pure states."""
    return float(np.real(np.trace(rho1 @ rho2)))

# ─── Run the simulation ────────────────────────────────────────────────────────
def run_simulation(theta=np.pi / 3, phi=np.pi / 4, num_trials=20):
    print("=" * 60)
    print("    QUANTUM TELEPORTATION SIMULATION (PennyLane)")
    print("=" * 60)
    print(f"\n  Teleporting state: RY({theta:.3f}) RZ({phi:.3f})|0⟩")
    print(f"  = cos({theta/2:.3f})|0⟩ + e^(i·{phi:.3f})·sin({theta/2:.3f})|1⟩\n")

    # Compute density matrices
    rho_original = original_state_circuit(theta, phi)
    rho_teleported = teleportation_circuit(theta, phi)

    f = fidelity(rho_original, rho_teleported)
    print(f"  Original state ρ_Alice:\n{np.round(rho_original, 4)}\n")
    print(f"  Teleported state ρ_Bob:\n{np.round(rho_teleported, 4)}\n")
    print(f"  ✅ Fidelity: {f:.6f} (1.000 = perfect teleportation)\n")

    # ─── Fidelity vs. different input states ──────────────────────────────────
    print("  Running fidelity sweep across 20 random states...")
    angles = [(np.random.uniform(0, np.pi), np.random.uniform(0, 2*np.pi))
              for _ in range(num_trials)]
    fidelities = []
    for t, p in angles:
        r_orig = original_state_circuit(t, p)
        r_tele = teleportation_circuit(t, p)
        fidelities.append(fidelity(r_orig, r_tele))

    avg_f = np.mean(fidelities)
    print(f"  Average fidelity over {num_trials} random states: {avg_f:.6f}")
    print(f"  Min fidelity: {min(fidelities):.6f}")
    print(f"  Max fidelity: {max(fidelities):.6f}\n")

    return rho_original, rho_teleported, f, fidelities, angles

# ─── Visualisation ────────────────────────────────────────────────────────────
def plot_results(rho_original, rho_teleported, fidelity_val, fidelities, angles,
                 save_path="quantum_teleportation_results.png"):
    fig = plt.figure(figsize=(16, 10), facecolor="#0a0a1a")
    fig.suptitle("Quantum Teleportation Simulation Results",
                 fontsize=20, color="white", fontweight="bold", y=0.97)

    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    text_color = "white"
    accent1 = "#00e5ff"   # cyan  — Alice
    accent2 = "#ff4081"   # pink  — Bob
    grid_color = "#2a2a3a"

    # ── 1. Density matrix: Original ──────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    im1 = ax1.imshow(np.abs(rho_original), cmap="Blues", vmin=0, vmax=1)
    ax1.set_title("Alice's Qubit\nDensity Matrix |ρ_A|", color=accent1, fontsize=12)
    ax1.set_xticks([0, 1]); ax1.set_yticks([0, 1])
    ax1.set_xticklabels(["|0⟩", "|1⟩"], color=text_color)
    ax1.set_yticklabels(["|0⟩", "|1⟩"], color=text_color)
    for (i, j), val in np.ndenumerate(np.abs(rho_original)):
        ax1.text(j, i, f"{val:.3f}", ha="center", va="center",
                 color="black" if val > 0.5 else text_color, fontsize=11, fontweight="bold")
    plt.colorbar(im1, ax=ax1)

    # ── 2. Density matrix: Teleported ─────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(np.abs(rho_teleported), cmap="RdPu", vmin=0, vmax=1)
    ax2.set_title("Bob's Qubit\nDensity Matrix |ρ_B|", color=accent2, fontsize=12)
    ax2.set_xticks([0, 1]); ax2.set_yticks([0, 1])
    ax2.set_xticklabels(["|0⟩", "|1⟩"], color=text_color)
    ax2.set_yticklabels(["|0⟩", "|1⟩"], color=text_color)
    for (i, j), val in np.ndenumerate(np.abs(rho_teleported)):
        ax2.text(j, i, f"{val:.3f}", ha="center", va="center",
                 color="black" if val > 0.5 else text_color, fontsize=11, fontweight="bold")
    plt.colorbar(im2, ax=ax2)

    # ── 3. Fidelity gauge ─────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor("#0a0a1a")
    theta_arc = np.linspace(0, np.pi, 200)
    # background arc
    ax3.plot(np.cos(theta_arc), np.sin(theta_arc), color=grid_color, lw=20, solid_capstyle="round")
    # value arc
    filled = np.linspace(0, np.pi * fidelity_val, 200)
    color_now = "#00e5ff" if fidelity_val > 0.95 else "#ffab40"
    ax3.plot(np.cos(filled), np.sin(filled), color=color_now, lw=20, solid_capstyle="round")
    ax3.text(0, -0.1, f"{fidelity_val:.4f}", ha="center", va="center",
             fontsize=28, color=color_now, fontweight="bold")
    ax3.text(0, -0.42, "Fidelity", ha="center", va="center", fontsize=14, color=text_color)
    ax3.set_xlim(-1.3, 1.3); ax3.set_ylim(-0.6, 1.3)
    ax3.axis("off")
    ax3.set_title("Teleportation Fidelity\nF(ρ_A, ρ_B)", color=text_color, fontsize=12)

    # ── 4. Fidelity across random states ─────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, :2])
    ax4.set_facecolor("#0d0d1f")
    xs = range(len(fidelities))
    bars = ax4.bar(xs, fidelities, color=[accent1 if f > 0.98 else accent2 for f in fidelities],
                   alpha=0.85, edgecolor="none")
    ax4.axhline(y=1.0, color="white", linestyle="--", lw=1, alpha=0.4, label="Perfect (1.0)")
    ax4.axhline(y=np.mean(fidelities), color="#ffab40", linestyle="-.", lw=1.5,
                label=f"Mean = {np.mean(fidelities):.4f}")
    ax4.set_xlabel("Trial (random state)", color=text_color, fontsize=11)
    ax4.set_ylabel("Fidelity", color=text_color, fontsize=11)
    ax4.set_title("Fidelity Across 20 Random Input States", color=text_color, fontsize=13)
    ax4.set_ylim(0.9, 1.05)
    ax4.tick_params(colors=text_color)
    ax4.spines[:].set_color(grid_color)
    p1 = mpatches.Patch(color=accent1, label="F > 0.98")
    p2 = mpatches.Patch(color=accent2, label="F ≤ 0.98")
    ax4.legend(handles=[p1, p2] +
               [plt.Line2D([0], [0], color="white", ls="--", label="Perfect (1.0)"),
                plt.Line2D([0], [0], color="#ffab40", ls="-.", label=f"Mean = {np.mean(fidelities):.4f}")],
               facecolor="#0a0a1a", labelcolor="white", fontsize=9)

    # ── 5. Protocol steps ─────────────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_facecolor("#0a0a1a")
    ax5.axis("off")
    steps = [
        ("Step 1", "Prepare |ψ⟩ on Alice's qubit", accent1),
        ("Step 2", "Create Bell pair\n(Alice ⊗ Bob entangled)", "#b39ddb"),
        ("Step 3", "Alice performs\nBell measurement", accent1),
        ("Step 4", "Send 2 classical bits\nto Bob", "#ffab40"),
        ("Step 5", "Bob applies\ncorrection gates", accent2),
        ("Result", "Bob holds |ψ⟩\nFidelity ≈ 1.000", "#69f0ae"),
    ]
    for i, (label, desc, col) in enumerate(steps):
        y = 0.92 - i * 0.155
        ax5.add_patch(mpatches.FancyBboxPatch((0.02, y - 0.06), 0.96, 0.12,
            boxstyle="round,pad=0.01", facecolor=col+"22", edgecolor=col, lw=1.5))
        ax5.text(0.08, y, label, color=col, fontsize=9, fontweight="bold", va="center")
        ax5.text(0.35, y, desc, color=text_color, fontsize=8, va="center")
    ax5.set_title("Protocol Steps", color=text_color, fontsize=12)
    ax5.set_xlim(0, 1); ax5.set_ylim(0, 1)

    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"  📊 Saved plot → {save_path}")
    return fig

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rho_orig, rho_tele, f, fidelities, angles = run_simulation(
        theta=np.pi / 3, phi=np.pi / 4
    )
    plot_results(rho_orig, rho_tele, f, fidelities, angles)
    print("\n  ✅ Simulation complete! Check 'quantum_teleportation_results.png'\n")
