# DSSAT AWS Lambda Function



## DSSAT Documentation

- [DSSAT](https://dssat.net/3865/)

## Input JSON

The input JSON consists of 2 fields:

1. "file_name" : A string containing the name of the input file.
2. "file_url" : The URL to access the input file.

As for now, only the execution of DSSAT with run mode "A" is supported, providing a fileX and running all pretreatments. So, the input file should be an fileX as in the example below. The file ."MZX" file in the code example should be available for download.

Example of input JSON:

~~~json
{
  "file_name": "BRPI0202.MZX",
  "file_url": "https://r-lambdas-dummy.s3.eu-central-1.amazonaws.com/BRPI0202.MZX"
}
~~~

## Using the Lambda Function in R

The proper way to use the Lambda function through a R script is shown below:

~~~R
# required libraries
library("httr")
library("jsonlite")

## Way to send data, loading from local json file and converting it to the appropriate format for the POST call
input_local_file_path = "dssat_input_json.json" #provide the correct path to JSON
input_json = fromJSON(input_local_file_path)
post_input_json = toJSON(input_json,auto_unbox=T)

## create the headers for the POST call
header = add_headers(.headers = c('Authorization'= 'SCIO_CROP_LAMBDAS', 'Content-Type' = 'application/json'))
## execute the POST call
response = POST(url = "https://lambda.qvantum.dssat.scio.services/", config = header , body = post_input_json)

## get the returned data as a R list
data_list = content(response)
## get the returned data as a json variable (can be saved as local json file)
data_json = toJSON(data_list)
~~~

## Output

The output of the Lambda Function is a JSON with the following format. It contains one field, with a list of all the produced files from the DSSAT run. Moreover, a .txt file is created with the output shown in the terminal screen when running the model, with the name "command_line_output.txt". All the files should be available to download from the returned URLs.

~~~json
{
  "files_list": [
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilWat.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/LUN.LST",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/PlantGro.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilTemp.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/OUTPUT.LST",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/N2O.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilNi.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilOrg.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/WARNING.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/command_line_output.txt",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilNiBal.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilCBalSum.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilCBal.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/Evaluate.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilWatBal.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/OVERVIEW.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilNoBal.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/DSSAT47.INH",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/RunList.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/SoilNBalSum.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/ET.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/Weather.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/INFO.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/PlantN.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/Mulch.OUT",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/DSSAT47.INP",
    "https://lambda-dssat.s3.eu-central-1.amazonaws.com/BRPI0202_MZX_20_12_2021_15_57_03/Summary.OUT"
  ]
}
~~~



## Deployment

![](https://scio-images.s3.us-east-2.amazonaws.com/dssat.png)

### Prerequistes

- AWS Account
- AWS CLI
- Python
- Docker

The AWS services that are being used are the the ones below:

- Lambda
- Elastic Container Registry
- API Gateway
- S3

The core component of this deployment is of course the Docker image that is serving DSSAT model. This has been built with Python 3.8 as base image and by installing gfortran & DSSAT model dependencies.

Once you clone this repo, you would need to build to the Docker image by provisioning the below "docker build" command with the build arguments for the AWS keys. Those are needed for S3 interaction and prior proceeding with building the image, you should have created a S3 bucket and created relevant AWS keys for access.

`docker build --build-arg AWS_KEY=xxxx --build-arg AWS_SECRET=yyyy .`

When the docker image is built, you can navigate to [AWS ECR](https://us-east-2.console.aws.amazon.com/ecr) in order to push the image to your AWS account by following the relevant push commands instructions.

Then you would have to configure your lambda function accordingly with "Container image" option. Make sure that you have adjusted the configuration of the function according to DSSAT model needs.

The recommended settings are **1024 MB for memory** and **1 minute timeout**.

Finally, you can navigate to API Gateway console and create a HTTP API. Go to "Routes" page and create a route. Then go to "Integrations" page and make one for the route you created by adding the lambda function you created using a POST request method.

`https://<random text>.execute-api.<your aws region>.amazonaws.com`

The lambda function is now ready to be used! 
