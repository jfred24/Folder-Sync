# Synchronizer Script

`usage: synchronizer.py [-h] [--log LOG] [--interval INTERVAL] [--use-hash] source replica`

Synchronize two folders: `source` and `replica`.

## Positional Arguments
- **`source`**  
  Path to the source folder.
  
- **`replica`**  
  Path to the replica folder.

## Optional Arguments
- **`-h`**  
  Show help message and exit.
  
- **`--log LOG`**  
  Path to the log file.  
  *(Default: `sync_log.txt`)*
  
- **`--interval INTERVAL`**  
  Time interval (in seconds) between synchronizations.  
  *(Default: `30` seconds)*

- **`--use-hash`**  
  Enable MD5 hash comparison to detect changes in files.
  
