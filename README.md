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
toxopy.analyze_rois(file, room_layout, output_dir, trial_type)
```


```python
file: string
    Full path of the improved .csv file as a string.

room_layout: string
    Full path of the room layout JSON file containing the specification for the ROIs as a string.

output_dir: string
    Full path of the output directory ending with a trailing slash.

trial_type: string
    The trial type in the .csv file.  This can take two arguments: "cat_alone" or "with_owner".
````

