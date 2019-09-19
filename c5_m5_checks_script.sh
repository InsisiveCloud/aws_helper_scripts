#!/bin/bash

set -e

if [ $# -eq 0 ]
then
   echo -e "\n
You can use this script to do the pre-requisites checks before changing the instance type to M5/C5. This script performs the following actions:

    - Verify if NVMe module is installed on your instance. If yes then it will verify if it is loaded in the intiramfs image.
    - Verify if ENA module is installed on your instance.
    - Analyses the “/etc/fstab” and look for the block devices being mounted using device names. It will give you a prompt to ask if you want to regenerate and modify your  current “/etc/fstab” file to replace the device name of each partition with its UUID. The original fstab file will be saved as /etc/fstab.backup.$(date +%F-%H:%M:%S) for e.g /etc/fstab.backup.2018-05-01-22:06:05

    [WARNING: Provide "y" only if you want this script to rewrite the current "/etc/fstab" file. If you provide "n" or "No", it will just print the correct /etc/fstab file in the output but would not replace it]

------- Running the scrips -------

- Place the script on your instance and make it executable

    # chmod +x c5_m5_checks_script.sh

- Run the script as a "root" user or "sudo" otherwise it would fail with the following message "This script must be run as root"

    # bash c5_m5_checks_script.sh --targets Key=<key-name>,Values=<v1,v2,v3> [...] \n
for more detail on filters visit:'https://docs.aws.amazon.com/systems-manager/latest/userguide/send-commands-multiple.html'

----------------------------------

   "
   exit
fi

targets="$*"
if [[ $targets =~ --targets.* ]];
then
    aws ssm send-command \
        --document-name "AWS-RunRemoteScript" \
        $targets \
        --parameters '{"sourceType":["GitHub"],"sourceInfo":["{\"owner\": \"awslabs\",\"repository\": \"aws-support-tools\", \"path\":\"EC2/C5M5InstanceChecks/c5_m5_checks_script.sh\"}"],"commandLine":[""]}'
    echo 'OK'
else
    echo 'Invalid target format'
    echo -e "USAGE:
    $ bash install_cloudwatch.sh --targets Key=<key-name>,Values=<v1,v2,v3> [...] \n
    for more detail on filters visit:'https://docs.aws.amazon.com/systems-manager/latest/userguide/send-commands-multiple.html'
"
fi
