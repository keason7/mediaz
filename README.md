# mediaz

Simple CLI for bulk compression of pictures and videos.

## Installation

Clone the project.

```bash
git clone {repo_url}
cd mediaz/
```

Install the conda env.

```bash
conda env create -f environment.yml
conda activate mediaz
```

## Usage

Run a bulk compression task with specified config file path.

```bash
python run.py -pc /path/to/config_file.yml
```

Or just use the default config file path.

```bash
python run.py
```

Or run a job and store stdout and stderr to a log file.

```bash
nohup python run.py -nb > /path/to/log_file.log 2>&1 &
```

From the input folder path to compress, it will create an output compressed folder.

```txt
/path/to/input_folder/
/path/to/2025_06_10-15_54_25_output_folder/
```

Each file will be copied if format is not recognized, or else compressed.

Since every input format is mapped to an output format, naming issues can occur such as overwrite.

```txt
./file.png -> ./file.jpg
./file.nef -> ./file.jpg
```

Here file names can be changed if needed to avoid overwrite.

```txt
./file.png -> ./file.jpg
./file.nef -> ./file (1).jpg
```

## Config

```yaml
in_path: "/path/to/folder/to/compress/"

out_dtype:
  image:
    fmt: JPEG
    ext: .jpg

  video:
    fmt: MP4
    ext: .mp4

compression:
  JPEG:
    quality: 70
    optimize: True
    subsampling: 1

  MP4:
    vcodec: "libx265"
    crf: 28
    pix_fmt: "yuv420p10le"
    preset: "fast"
    acodec: "libopus"
    audio_bitrate: "96k"
    loglevel: "quiet"
    libx265_loglevel: "log-level=quiet"
```

Following config content specifies the parameters for the compression task.

Supported formats can be found [here](./mediaz/dtype/dtype_support.py).
