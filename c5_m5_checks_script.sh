#!/bin/bash

set -e

if [ $# -eq 0 ]
then
   echo -e "\nThis script is use to install CloudWatchAgent on the EC2 instances,
with the given filter tags or instance ids. \n\
Either filters or instance id list is required in order to execute script
USAGE:
  $ bash install_cloudwatch.sh --targets Key=<key-name>,Values=<v1,v2,v3> [...] \n
for more detail on filters visit:'https://docs.aws.amazon.com/systems-manager/latest/userguide/send-commands-multiple.html'
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
