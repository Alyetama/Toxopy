# Toxopy
Object-specific python package to run automated tasks in the Chase Lab

## Installation
```bash
$ pip install toxopy
```

## Functions details

### Improve DLC Output –– With Owner Trials

```python
toxopy.improve_dlc_output(cat, owner)
```


```python
cat: string
    Full path of the original DLC output .csv file for a 'cat head with owner' project as a string.

owner: string
    Full path of the original DLC output .csv file for a 'owner hand' project as a string.
````


### Improve DLC Output –– Cat Alone Trials

```python
toxopy.improve_dlc_output_cat_alone(cat, output_dir)
```


```python
cat: string
    Full path of the original DLC output .csv file for a 'cat alone' project as a string.

output_dir: string
    Full path of the output directory ending with a trailing slash.
````


### Analyze ROIs

```python
toxopy.analyze_rois(file, room_layout, output_dir, trial_type, span=10)
```


```python
file: string
    Full path of the improved .csv file as a string.

room_layout: string
    Full path of the room layout JSON file containing the specification for the ROIs as a string.

output_dir: string
    Full path of the output directory ending with a trailing slash.

trial_type: string
    The trial type in the .csv file.  This can take one of two arguments: "cat_alone" or "with_owner".

span: int
    The span value in the Loess smoothing variables.  The default is span=10 (0.10).  This can be changed to 0.50 or 0.25 by passing span=05 or span=025.
````


### Concatenate ROIs

```python
toxopy.concat_rois(directory, output_dir, trial_type)
```


```python
directory: string
    Full path of the input directory containing the ROIs .csv files.

output_dir: string
    Full path of the output directory ending with a trailing slash.

trial_type: string
    The trial type in the .csv file.  This can take one of two arguments: "cat_alone" or "with_owner".
```


### Calculate Mann-Whitney's U Statistics for ROIs

```python
toxopy.roi_calc_mw(data_file, voi)
```


```python
data_file: string
    Full path of the concatenated ROIs .csv file.  The file must indicate the "infection_status"!
voi: string
    Variable of interest.  This can take one of three arguments: "cumulative_time_in_roi_sec", "avg_time_in_roi_sec", or "avg_vel_in_roi".
```


### Convert .csv to .h5

```python
toxopy.csv2h5(directory=None, files=None)
```


```python
directory: string
    Full path of the input directory containing the .csv files.  To convert multiple files, use this option.
files: list
    Full path of .csv files as a list. For example, ['/usr/data/file1.csv', '/usr/data/file2.csv']
```


### FFmpeg Lazy Trim

```python
toxopy.lazytrim(select_cats, trial_times_json)
```


```python
select_cats: list
    List of cat name followed by id ["cat--id"].
trial_times_json: string
    Full path to json file containing trial times.
```


### Concatenate FFmpeg

```python
toxopy.ffconcat(cats, tvp, trial_type)
```


```python
cats: list
    List of cat name followed by id ["cat--id"].
tvp: string
    Full path of the input directory containing the video files.
trial_type: string
    The trial type in the .csv file.  This can take one of two arguments: "cat_alone" or "with_owner".
```
