# Scrape masterofmalt.com
![Test status](https://github.com/memsb/scrape_masterofmalt/workflows/Python%20package/badge.svg)

Scans the [new whiskies](https://www.masterofmalt.com/new-arrivals/whisky-new-arrivals/) section of [Master of Malt](https://www.masterofmalt.com/) periodically to build a database of whiskey releases. Can be combined with a search and notification system to alert people looking for items meeting their requirements.

##Running Locally
Can be run locally provided DynamoDB is set up with your AWS credentials set locally

#Infrastructure
Uses Terraform to manage AWS infrastructure including:

 * Lambda running code
 * EventBus to periodically trigger Lambda
 * IAM role for Lambda
 * S3 bucket to store Lambda code
 * CodePipeline to automate building and deployment
 * CodeBuild to use SAM to build and deploy Lambda

##Setting up DynamoDB Table
Deploying just the DynamoDB table would allow script to be run locally
```commandline
cd infrastructure/storage
terraform init
terraform apply
```

Running locally
```commandline
pipenv install
pipenv run python main.py
```

##Deploying to the Cloud
Creation of all other infrastructure can be done through Terraform

```commandline
cd infrastructure
terraform init
terraform apply
```

#Continuous Integration
Uses [github actions](https://github.com/memsb/scrape_masterofmalt/blob/main/.github/workflows/test.yml) to lint and test the code automatically on merge to main branch.
![Test status](https://github.com/memsb/scrape_masterofmalt/workflows/Python%20package/badge.svg)

#Continuous Delivery
Uses AWS CodePipeline to build and deploy latest code on Main branch to Lambda.


