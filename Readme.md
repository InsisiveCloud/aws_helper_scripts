## AWS Helper Scripts

### File: install_cloudwatch.py
 > This script is use to install CloudWatchAgent on the EC2 instances.
 > The Script requires to point to the desiered account using AWS Configure.
 > The Script also requires that ssm is installed on the local machine that is executing the script.
 > This Script will work for instances across all reagions.


```
$ python install_cloudwatch.py
```
```
Arguments
  -h, --help            show this help message and exit
  -f FILTERS, --filters FILTERS
              Tags for filtering instances eg: '{"<tagname>": "<value>"}, ...'
              
  -i INSTANCE_IDS, --instance-ids INSTANCE_IDS
              List of ',' seperated instance-ids where you want to install CloudWatch Agent
                        
Either filters or instance id list is required in order to execute script 
```

### File: c5_m5_checks_script.sh

 > We can use this script to do the pre-requisites checks before changing the instance type to M5/C5. This script performs the following actions:

    - Verify if NVMe module is installed on your instance. If yes then it will verify if it is loaded in the intiramfs image.

    - Verify if ENA module is installed on your instance.

    - Analyses the “/etc/fstab” and look for the block devices being mounted using device names. It will give you a prompt to ask if you want to regenerate and modify your  current “/etc/fstab” file to replace the device name of each partition with its UUID. The original fstab file will be saved as /etc/fstab.backup.$(date +%F-%H:%M:%S) for e.g /etc/fstab.backup.2018-05-01-22:06:05

    [WARNING: Provide "y" only if you want this script to rewrite the current "/etc/fstab" file. If you provide "n" or "No", it will just print the correct /etc/fstab file in the output but would not replace it]


------- Running the scrips -------

- Place the script on your instance and make it executable

    `# chmod +x c5_m5_checks_script.sh`

- Run the script as a "root" user or "sudo" otherwise it would fail with the following message "This script must be run as root"

    `# sudo ./c5_m5_checks_script.sh --targets \"Key=<key-name>,Values=<v1,v2,v3> [...]\" --fstab-rewrite {y|n}` \n

----------------------------------
