# README

## Video Data Splitting Up

The main purpose of these Python scripts is to obtain a set of 1 minute long video cuts located in `video_clips` directory, build a CSV format data so it can be saved and such rows finally will be recorded in a MySQL database.

### Prerequisites

- Anaconda Navigator 2.4.2
- Environment with Python 3.6.x along with mysql-connector-python-rf, moviepy and pandas
- Any MySQL previously set up (Docker, VirtualMachine, Community Edition)
- Downloaded video [here](https://www.dropbox.com/sh/782f7a0hmw3mn59/AADcJpRoFB0IIfi7-nR-7Eifa?dl=0)) and plaec it in root directory project

### Installation

1. Download or clone this repository.
2. All proper Python set up and packages must be met before going further

### Usage

1. Modify DATABASE credentials in `database/migrations.py`

2. In order to create concerning DATABASE and TABLES execute:

```shell
python database/migrations.py
```

3. Once dataase tables are created we proceed to split our video target up with the following:

```shell
python air_show.py
```

4. Video segments will be placed in `video_clips` directory
5. CSV file will be saved in `reports` directory
6. Finally, CSV data will be recored in MySQL DATABASE TABLE

### [MIT License](https://github.com/juan-carrillo/video-handling/blob/main/LICENSE)