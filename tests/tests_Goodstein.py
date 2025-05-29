import matplotlib.pyplot as plt
from src.Goodstein import goodstein_sequence

def plot_goodstein(m, n, max_steps=20):
    seq = goodstein_sequence(m, n, max_steps=max_steps)

    plt.figure(figsize=(10,6))
    plt.plot(range(len(seq)), seq, marker='o')
    plt.title(f"Goodstein sequence (m={m}, n={n})")
    plt.xlabel("steps")
    plt.ylabel("Value")
    plt.yscale('log')
    plt.grid(True)
    plt.show()

# ================================
# Main
# ================================

m = 10
n = 3
plot_goodstein(m, n, max_steps=200)