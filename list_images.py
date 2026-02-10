from pathlib import Path
import argparse


def list_images(images_dir: Path) -> list:
    if not images_dir.exists():
        raise FileNotFoundError(f"Directory not found: {images_dir}")
    return sorted([p.name for p in images_dir.iterdir() if p.is_file()])


def write_list(file_path: Path, names: list):
    file_path.write_text("\n".join(names) + ("\n" if names else ""))


def main():
    parser = argparse.ArgumentParser(
        description="List image filenames and write to a text file"
    )
    parser.add_argument(
        "--images-dir", default="images", help="Directory containing images"
    )
    parser.add_argument(
        "--out", default="images_list.txt", help="Output text file"
    )
    args = parser.parse_args()

    images_dir = Path(args.images_dir)
    out_file = Path(args.out)

    names = list_images(images_dir)
    write_list(out_file, names)
    print(f"Wrote {len(names)} entries to {out_file}")


if __name__ == "__main__":
    main()
