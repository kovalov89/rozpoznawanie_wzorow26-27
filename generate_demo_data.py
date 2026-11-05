from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def generate_binary_clusters(
    num_clusters: int,
    num_features: int,
    objects_per_cluster: int,
    random_seed: int,
) -> list[dict[str, object]]:
    if num_clusters < 1:
        raise ValueError("Liczba klastrów musi być większa od zera.")
    if num_features < 1:
        raise ValueError("Liczba cech musi być większa od zera.")
    if objects_per_cluster < 1:
        raise ValueError("Liczba obiektów w klastrze musi być większa od zera.")

    rng = np.random.default_rng(random_seed)
    rows: list[dict[str, object]] = []
    object_number = 1

    for cluster_id in range(1, num_clusters + 1):
        seed_vector = rng.integers(0, 2, size=num_features, dtype=np.uint8)
        flip_probability = 0.1 * float(np.sum(seed_vector)) / num_features
        seed_string = "".join(str(int(bit)) for bit in seed_vector)

        for position in range(objects_per_cluster):
            if position == 0:
                sample = seed_vector.copy()
                is_seed = True
            else:
                flip_mask = (rng.random(num_features) < flip_probability).astype(np.uint8)
                sample = np.bitwise_xor(seed_vector, flip_mask)
                is_seed = False

            vector_string = "".join(str(int(bit)) for bit in sample)
            rows.append(
                {
                    "object_id": f"x{object_number:03d}",
                    "cluster_label": cluster_id,
                    "is_seed": is_seed,
                    "seed_vector": seed_string,
                    "flip_probability": f"{flip_probability:.8f}",
                    "popcount": int(np.sum(sample)),
                    "binary_vector": vector_string,
                }
            )
            object_number += 1

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generator demonstracyjnego zbioru binarnych klastrów CLASSIX_T."
    )
    parser.add_argument("--clusters", type=int, default=3)
    parser.add_argument("--features", type=int, default=16)
    parser.add_argument("--objects-per-cluster", type=int, default=6)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/demo_small.csv"),
    )
    args = parser.parse_args()

    rows = generate_binary_clusters(
        num_clusters=args.clusters,
        num_features=args.features,
        objects_per_cluster=args.objects_per_cluster,
        random_seed=args.seed,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with args.output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Zapisano {len(rows)} obiektów do: {args.output}")
    print(f"Liczba klastrów: {args.clusters}")
    print(f"Liczba cech: {args.features}")
    print(f"Obiektów w klastrze (łącznie z bazowym): {args.objects_per_cluster}")
    print("Wektory bazowe i p:")
    for row in rows:
        if row["is_seed"]:
            print(
                f"  Klaster {row['cluster_label']}: {row['seed_vector']} "
                f"(p={row['flip_probability']})"
            )


if __name__ == "__main__":
    main()
