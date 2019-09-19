## AWS Helper Scripts

### File: install_cloudwatch.py
 > This script is use to install CloudWatchAgent on the EC2 instances, 

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
