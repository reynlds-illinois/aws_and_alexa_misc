#!/bin/bash

# I use this to package my AWS dev projects for upload to Lambda
#
#     Usage: ./aws_pkg_4_lambda.sh PROJ_NAME S3_BUCKET_NAME
#     Example:  ./aws_pkg_4_lambda.sh my-aws-project my-s3-bucket
#     Requires:  AWS SDK


PROJ_PATH="/home/pub/projects"
PY36_LIB="/usr/lib/python3.6/dist-packages/"

rm -f "$PROJ_PATH/$1/$1.zip"
cd "$PROJ_PATH/$1/"
zip -r "$PROJ_PATH/$1.zip" .
cd "$PY36_LIB"
zip -ur "$PROJ_PATH/$1.zip" .
aws s3 cp "$PROJ_PATH/$1.zip" "s3://$2"


# At some point I may push this directly to my project in Lambda:
#
#     "aws lambda update-function-code --function-name $1 --zip-file s3://$2"
