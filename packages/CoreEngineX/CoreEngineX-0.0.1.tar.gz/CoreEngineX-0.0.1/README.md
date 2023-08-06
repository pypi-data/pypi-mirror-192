# CoreEngineX
CoreEngineX will fetch the python files from the directory/sub-directories. Display those files in the command line interface menu. Execute the files sequentially. The option to check the pylint score of the files is provided and also the option to load the environment variables.

## Installation
```python -m pip install coreenginex```

## Example Usage

### Read input from command line
```python
import sys
from coreenginex import CoreEngineX

if __name__ == "__main__":
    ce = CoreEngineX()
    code_folder = sys.argv[1]
    ce.run_coreenginex(folder_path = code_folder)

```

### Read input from the script
```python
from coreenginex import CoreEngineX

if __name__ == "__main__":
    ce = CoreEngineX()
    code_folder = './test'
    ce.run_coreenginex(folder_path = code_folder)

```

### Load environment variables
```python
from coreenginex import CoreEngineX

if __name__ == "__main__":
    ce = CoreEngineX()
    code_folder = './test'
    ce.run_coreenginex(folder_path = code_folder)
    ce.load_environment_variables(key_value = {"key": "value"})

```