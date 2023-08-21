-   Step 1
    
    Choose pipeline settings
    
    * * *
    
-   Step 2
    
    Add source stage
    
    * * *
    
-   Step 3
    
    Add build stage
    
    * * *
    
-   Step 4
    
    Add deploy stage
    
    * * *
    
-   Step 5
    
    Review
    

Review

Info

### Step 1: Choose pipeline settings

Pipeline settings

Pipeline name

hellowWorldFlaskAWSElasticBeanstalkPipeline

Artifact location

A new Amazon S3 bucket will be created as the default artifact store for your pipeline

Service role name

AWSCodePipelineServiceRole-ap-southeast-1-hellowWorldFlaskAWSEl

### Step 2: Add source stage

Source action provider

Source action provider

GitHub (Version 2)

OutputArtifactFormat

CODE\_ZIP

ConnectionArn

arn:aws:codestar-connections:ap-southeast-1:278772452195:connection/8e1e50b9-a37b-4c56-83f3-441c34d44509

FullRepositoryId

juliuschou/juliuschou-hellowWorldFlaskAWSElasticBeanstalkPipeline

BranchName

master

### Step 3: Add build stage

Build action provider

Build action provider

AWS CodeBuild

ProjectName

helloworldFlaskAwsCodeBuild

### Step 4: Add deploy stage

Deploy action provider

Deploy action provider

AWS Elastic Beanstalk

ApplicationName

helloworldFlaskEnv

EnvironmentName

my-helloworldFlask
