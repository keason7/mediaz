from pathlib import Path

from imgz.image.standard_image import StandardImage


def main():

    path = Path("/home/keason/Desktop/test_dir/")
    files = list(path.glob("*"))

    for i, item in enumerate(files):
        si = StandardImage()

        si.read(str(item))
        si.write(str(path), f"test{i}")


if __name__ == "__main__":
    main()
