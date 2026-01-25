#!/usr/bin/env python3
"""Renomeia arquivos adicionando um hash do conteúdo ao final do nome.

Usage examples:
  python hash_renamer.py --dir ./images --recursive --dry-run
  python hash_renamer.py --dir "C:\\Users\\Mateus\\Pictures\\GambiarraCDN\\images" --length 8
"""
from pathlib import Path
import argparse
import hashlib
import sys


def compute_hash(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def target_name(path: Path, sep: str, hshort: str) -> Path:
    return path.with_name(f"{path.stem}{sep}{hshort}{path.suffix}")


def process(directory: Path, recursive: bool, algorithm: str, length: int, sep: str, dry_run: bool):
    if recursive:
        files = [p for p in directory.rglob("*") if p.is_file()]
    else:
        files = [p for p in directory.iterdir() if p.is_file()]

    for p in files:
        try:
            full = compute_hash(p, algorithm)
        except Exception as e:
            print(f"Erro lendo {p}: {e}")
            continue
        hshort = full[:length]
        if p.stem.endswith(sep + hshort):
            print(f"Pular (já possui hash): {p}")
            continue

        newp = target_name(p, sep, hshort)

        if newp.exists():
            try:
                if newp.read_bytes() == p.read_bytes():
                    print(f"Arquivo destino idêntico existe, removendo original: {p} -> {newp}")
                    if not dry_run:
                        p.unlink()
                    continue
            except Exception:
                pass

            base = newp.stem
            ext = newp.suffix
            i = 1
            candidate = newp
            while candidate.exists():
                candidate = newp.with_name(f"{base}-{i}{ext}")
                i += 1
            newp = candidate

        action = f"{p} -> {newp}"
        if dry_run:
            print("DRY-RUN: " + action)
        else:
            print(action)
            try:
                p.replace(newp)
            except Exception as e:
                print(f"Falha ao renomear {p}: {e}")


def main():
    ap = argparse.ArgumentParser(description="Append content hash to filenames for cache-busting.")
    ap.add_argument("--dir", "-d", default=".", help="Diretório alvo")
    ap.add_argument("--recursive", "-r", action="store_true", help="Processar recursivamente")
    ap.add_argument("--algorithm", default="sha256", help="Algoritmo de hash (sha1, sha256, md5, etc.)")
    ap.add_argument("--length", "-l", type=int, default=8, help="Número de caracteres do hash a adicionar")
    ap.add_argument("--sep", default="-", help="Separador entre nome e hash")
    ap.add_argument("--dry-run", action="store_true", help="Mostrar o que seria renomeado, sem alterar")

    args = ap.parse_args()
    directory = Path(args.dir)
    if not directory.exists() or not directory.is_dir():
        print(f"Diretório inválido: {directory}")
        sys.exit(1)

    process(directory, args.recursive, args.algorithm, args.length, args.sep, args.dry_run)


if __name__ == "__main__":
    main()
