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

Each file will be copied if format is not recognized, or else compressed. If `copy_if_larger` is True in the config file, compressed files with larger size than the input file will be replaced by the original file.

The compressed output directory has two nested directories.

```txt
/path/to/2025_06_10-15_54_25_output_folder/data/
/path/to/2025_06_10-15_54_25_output_folder/summary/
```

- `data` contains the compressed files.
- `summary` contains the config file used and the statistics of the compression process.

The JSON stats file contains useful informations about compression process.

| index | in_path            | in_size | out_path          | out_compressed_size | out_size | status |
| :---- | :----------------- | :------ | :---------------- | :------------------ | :------- | :----- |
| 0     | /path/to/file.rgba | 30512   | /path/to/file.jpg | 378                 | 378      | 1      |
| 1     | /path/to/file.jp2  | 262     | /path/to/file.jp2 | 415                 | 262      | 2      |
| 2     | /path/to/file.gif  | 200     | /path/to/file.gif | 200                 | 200      | 0      |
| 3     | /path/to/file.jpg  | 262     | /path/to/file.jpg | 262                 | 262      | 3      |
| ...   | ...                | ...     | ...               | ...                 | ...      | ...    |

Where:

- `index` is the Dataframe row index
- `in_path` is the input file path
- `in_size` is the input file size
- `out_path` is the output file path
- `out_compressed_size` is the output compressed file size
- `out_size` is the final output file size (output compressed file can be replaced by input file if compression fails to create a smaller file: see `copy_if_larger` in config).
- `status` is the method applied for the current file:
  - `0`: Unknown format, input file is copied as output file.
  - `1`: Compressed file has been written as output file.
  - `2`: Compressed file has been replaced by input file as the final output file (`copy_if_larger`=True)
  - `3`: Is a recognized format with failed compression. File is then copied from input to output.

Since every input format is mapped to an output format, naming issues can occur such as overwrite.

```txt
./file.png -> ./file.jpg
./file.nef -> ./file.jpg
```

Here file names can be changed if needed to avoid overwriting.

```txt
./file.png -> ./file.jpg
./file.nef -> ./file (1).jpg
```

## Config

```yaml
in_path: "/path/to/folder/to/compress/"

copy_if_larger: False

apply_snake_case: True

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
