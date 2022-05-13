# comcast-interview
InterviewTask

#### challenge-01:

I considered the given data stored in SQL query and written SELECT query to fetch the Employees whose devices not recorded into the system.


#### challenge-03

- Written a python script which accepts 3 arguments as explained in the question
   - `--env` A key to be updated in the config JSON
   - `--json` File path of JSON file to be updated
   - `--csv` File path of input CSV file

- Example Command to run a script

```
 python3 updatejson.py --env DEV --json configs/config.json --csv configs/input.csv
```

#### challenge-04

- Written a python script to fetch IP & time taken DNS query & HTTP request handshake for the given set of Domains

- You have to pass 3 arguments to script while executing
   - `--input` Input file which contains the list of FQDN
   - `--thread-count` How many simultaneous thread we can use to process the csv based on the system capacity
   - `--output` Path of the output file

- Example command to run a script
```
  python3 challenge_04.py --input input_fqdn.csv --thread-count 3 --output new_output.csv
```