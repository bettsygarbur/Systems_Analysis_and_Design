import numpy as np
import pandas as pd

# -------------------------------
# 1. Cargar datos y preparar estado inicial
# -------------------------------

train = pd.read_csv("train.csv")

# Usar 'sii' si existe. Si no, derivarlo de 'PCIAT-PCIAT_Total'
if "sii" in train.columns:
    df = train.dropna(subset=["sii"]).copy()
    df["sii"] = df["sii"].astype(int)
else:
    def sii_from_pciat(x):
        if pd.isna(x):
            return np.nan
        x = float(x)
        if x <= 30:
            return 0
        elif x <= 49:
            return 1
        elif x <= 79:
            return 2
        else:
            return 3

    df = train.copy()
    df["sii"] = df["PCIAT-PCIAT_Total"].apply(sii_from_pciat)
    df = df.dropna(subset=["sii"]).copy()
    df["sii"] = df["sii"].astype(int)

print("Distribución real de sii en train (después de limpiar):")
print(df["sii"].value_counts().sort_index())

# Discretizar una variable de uso de internet (si existe)
internet_col = "PreInt_EduHx-computerinternet_hoursday"
if internet_col in df.columns:
    q1, q3 = df[internet_col].quantile([0.25, 0.75])

    def disc_internet(v):
        if pd.isna(v):
            return "missing"
        v = float(v)
        if v <= q1:
            return "low"
        elif v <= q3:
            return "medium"
        else:
            return "high"

    df["internet_level"] = df[internet_col].apply(disc_internet)
else:
    df["internet_level"] = "unknown"

print("\nNiveles de internet en los datos:")
print(df["internet_level"].value_counts())

# -------------------------------
# 2. Inicializar rejilla del autómata
# -------------------------------

N = 30  # tamaño de la rejilla: N x N
num_cells = N * N

# muestrear participantes reales para poblar la rejilla
sample = df[["sii", "internet_level"]].sample(
    num_cells, replace=True, random_state=42
).reset_index(drop=True)

grid_sii = sample["sii"].values.reshape(N, N)                  # estados sii
grid_internet = sample["internet_level"].values.reshape(N, N)  # nivel de internet

print(f"\nRejilla inicial creada con tamaño {N}x{N}.")
unique, counts = np.unique(grid_sii, return_counts=True)
print("Distribución de sii en la rejilla inicial:")
print(dict(zip(unique, counts)))

# -------------------------------
# 3. Reglas del autómata celular
# -------------------------------

def get_neighbours(i, j, N):
    """Vecindario de Moore (8 vecinos) con bordes periódicos."""
    neigh = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = (i + di) % N
            nj = (j + dj) % N
            neigh.append((ni, nj))
    return neigh

def internet_risk(level):
    """Riesgo según nivel de internet (parámetros ajustables)."""
    if level == "high":
        return 0.6
    elif level == "medium":
        return 0.3
    elif level == "low":
        return 0.1
    else:
        return 0.2  # missing/unknown

def step(grid_sii, grid_internet,
         w_self=0.4, w_neigh=0.6,
         up_th=0.7, down_th=0.3,
         rng=None):
    """Un paso de actualización del autómata celular."""
    if rng is None:
        rng = np.random.default_rng()

    N = grid_sii.shape[0]
    new_grid = grid_sii.copy()

    for i in range(N):
        for j in range(N):
            sii_ij = grid_sii[i, j]
            level_ij = grid_internet[i, j]

            # riesgo propio: depende de sii actual y nivel de internet
            self_risk = sii_ij / 3.0
            inet_r = internet_risk(level_ij)
            risk_self_part = 0.5 * self_risk + 0.5 * inet_r

            # riesgo vecinal: proporción de vecinos con sii >= 2
            neigh_idx = get_neighbours(i, j, N)
            neigh_sii = [grid_sii[ni, nj] for ni, nj in neigh_idx]
            high_neigh = sum(s >= 2 for s in neigh_sii) / len(neigh_sii)

            # riesgo total
            total_risk = w_self * risk_self_part + w_neigh * high_neigh
            total_risk = np.clip(total_risk + rng.normal(0, 0.05), 0, 1)

            u = rng.random()
            new_state = sii_ij

            # reglas:
            if total_risk > up_th and u < 0.5 and sii_ij < 3:
                new_state = sii_ij + 1
            elif total_risk < down_th and u < 0.5 and sii_ij > 0:
                new_state = sii_ij - 1

            new_grid[i, j] = new_state

    return new_grid


# -------------------------------
# 4. Bucle de simulación y salida
# -------------------------------

def run_simulation(grid_sii, grid_internet,
                   steps=50,
                   seed=123,
                   w_self=0.4,
                   w_neigh=0.6,
                   up_th=0.7,
                   down_th=0.3):
    """
    Ejecuta la simulación durante 'steps' pasos.
    Devuelve:
      - history_df: distribución de sii por paso.
      - final_grid: rejilla final de sii.
    """
    rng = np.random.default_rng(seed)
    current = grid_sii.copy()
    history = []

    for t in range(steps):
        unique, counts = np.unique(current, return_counts=True)
        counts_dict = {int(k): int(v) for k, v in zip(unique, counts)}

        row = {"step": t}
        for s in [0, 1, 2, 3]:
            row[f"sii_{s}"] = counts_dict.get(s, 0)
        history.append(row)

        current = step(current, grid_internet,
                       w_self=w_self,
                       w_neigh=w_neigh,
                       up_th=up_th,
                       down_th=down_th,
                       rng=rng)

    history_df = pd.DataFrame(history)
    return history_df, current


if __name__ == "__main__":
    print("\nEjecutando simulación del Escenario 2...")
    history_df, final_grid = run_simulation(
        grid_sii,
        grid_internet,
        steps=50,
        seed=123
    )

    print("\nPrimeras filas del historial de sii:")
    print(history_df.head())

    history_df.to_csv("scenario2_history.csv", index=False)
    print("\nSe guardó 'scenario2_history.csv' con la evolución de sii.")

    final_flat = final_grid.flatten()
    unique_f, counts_f = np.unique(final_flat, return_counts=True)
    print("\nDistribución de sii en la rejilla final:")
    print(dict(zip(unique_f, counts_f)))

    print("\nEscenario 2 completado.")