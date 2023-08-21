

## 1. Prerequisite
### Understand how to install the AWS Elastic Benastalk on Linux from the link below:

[Install the EB CLI on Linux](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html)

This document describes how to install the EB CLI (Elastic Beanstalk Command Line Interface) on Linux. The EB CLI is a tool that you can use to manage your Elastic Beanstalk environments from the command line.

To install the EB CLI, you can use the following steps:

1. Install Python 3.7 and pip.
2. Install the EB CLI using the installation script.
3. Add the path to the EB CLI executable to your PATH environment variable.

Once the EB CLI is installed, you can use it to create, manage, and deploy your Elastic Beanstalk environments.

### Understand how to manage multiple version on the same machine from the link below:

[Introducing pyenv: A Simple Way to Manage Python Versions](https://realpython.com/intro-to-pyenv/)

Pyenv is a tool that allows you to easily install and manage multiple versions of Python on your system. This can be useful for a variety of reasons, such as:

* Testing different versions of Python
* Developing projects that require specific versions of Python
* Creating isolated Python environments for different projects

### Know the concept: [What is AWS Elastic Beanstalk?](https://blog.back4app.com/what-is-aws-elastic-beanstalk/)

AWS Elastic Beanstalk is a service that makes it easy to deploy and manage web applications in the Amazon Web Services (AWS) cloud. It provides a high-level abstraction for managing the underlying infrastructure, so you can focus on your application code.

## 2. set up the AWS Command Line Interface (CLI) properly before you can execute aws eb create or any other AWS CLI command 

### Here are the steps you should follow:

1.  Install the AWS CLI:
    
    If you haven't already, you can install the AWS CLI on Ubuntu using `pip`:
    
    ```
    sudo apt-get install python3-pip
    pip3 install awscli --upgrade --user 
    ```
    Ensure the AWS CLI binary is in your path. You might need to add `$HOME/.local/bin` to your `PATH`.
    
3.  Configure AWS CLI:
    
    After you've installed the AWS CLI, you need to configure it with your AWS credentials and default settings. You can do this by running:
    
    
    `aws configure` 
    
    This command will prompt you to provide the following:
    
    -   `AWS Access Key ID`
    -   `AWS Secret Access Key`
    -   `Default region name` (e.g., `us-west-1`, `eu-west-1`)
    -   `Default output format` (e.g., `json`, `text`)
    
    The access key and secret key are provided to you when you create an IAM (Identity and Access Management) user in the AWS Management Console. Ensure that the IAM user has necessary permissions for Elastic Beanstalk operations.

4.   Install the Elastic Beanstalk Command Line Interface (EB CLI):

    `pip install awsebcli`


## 3. Setting Up a Flask Application:

Let's create a simple Flask application:

![image](https://github.com/juliuschou/aws-code-build-exercise/assets/4725611/4d0f24be-4bbf-4864-b9cb-20fd02c403e3)


1.  Create a new directory for your project:
    
    ```
    mkdir my_flask_app
    cd my_flask_app
    ``` 
    
2.  Create a virtual environment:
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate
    ``` 

3.  Install Flask:
    
    `pip install Flask` 
    
4.  Make a file named `app.py`. Here's a more robust version with error handling:

```
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run()
```

## 4. Deploy using AWS Elastic Beanstalk:

1.   Initialize your application:

Navigate to your project directory and run:

    `eb init -i`

![image](https://github.com/juliuschou/aws-code-build-exercise/assets/4725611/74ee75d4-2349-4a58-918c-f1d942fc69e0)

![image](https://github.com/juliuschou/aws-code-build-exercise/assets/4725611/03f2c725-7db4-42e2-bc2c-dbb24a0fd562)

![image](https://github.com/juliuschou/aws-code-build-exercise/assets/4725611/f75da3fb-af95-485a-b132-f5b45b214ebd)



2. create Flask config

```
mkdir .ebextensions
cd .ebextensions
vim 01_flask.config

option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  aws:elasticbeanstalk:container:python:
    WSGIPath: "app:app"

```


3. create an Elastic Bean application    
    `eb create [your-env-name]`
    
    
After the deployment completes, you can access your Flask application via the URL provided by Elastic Beanstalk.

## 5. Push Code to GitHub

Configuring GitHub to Avoid Using Username and Password

To interact with GitHub without the need for entering a username and password every time, you can configure SSH authentication. Here are the steps:

### 1. Generate SSH Key

- Open a terminal on your CentOS 7 machine and run the following command to generate an SSH key pair:
    
    `ssh-keygen -t ed25519 -C "your_email@example.com"` 
    

### 2. Add SSH Key to GitHub Account

1.  Log into your GitHub account.
2.  Click on your profile picture → Settings → SSH and GPG keys → New SSH key.
3.  Paste the contents of your `id_ed25519.pub` file into the "Key" field, give your key a descriptive title, and click "Add SSH key".

### 3. Install Git

- Install Git with the following command:
    
    `sudo yum install git` 
    

### 4. Configure Git to Use SSH

- Set your Git username and email address, and configure Git to use SSH. Use the following commands:
    ```
    git config --global user.name "Your GitHub Username"
    git config --global user.email "your_email@example.com"
    ```

### 5. Created an empty repository on GitHub, you can push your code to GitHub:

```
# Navigate to your project directory (the directory where your code is located) 
cd /path/to/your/project # Initialize Git (if not already initialized) 
git init

# Add the files you want to commit to the staging area 
git add . 

# Commit the changes with a meaningful message 
git commit -m "Your commit message here" 

# set remote github repository
git remote add origin git@github.com:YourUsername/YourRepository.git

![image](https://github.com/juliuschou/aws-code-build-exercise/assets/4725611/5d5d35a6-8926-4b0e-87e2-fce719ec2edf)


# Push the committed changes to the master branch of your GitHub repository 
git push origin master
```

### 6\. Set up Continuous Delivery with AWS CodeBuild:

#### a. In AWS Management Console, navigate to AWS CodeBuild and create a new build project.

#### b. Connect it with your GitHub repository.

Choose "GitHub" as the source provider. You'll be prompted to connect your AWS account to GitHub.

#### c. Configure a `buildspec.yml` file:

Create a `buildspec.yml` in the root directory of your repository. A simple example for this project might look like:


```
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.7
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt
  build:
    commands:
      - echo Build completed.
``` 

#### d. Use AWS CodePipeline:

1.  Navigate to the AWS CodePipeline console and create a new pipeline.
2.  Connect your GitHub repository as the source stage.
3.  For the build stage, select the AWS CodeBuild project you set up earlier.
4.  For the deployment stage, select AWS Elastic Beanstalk and choose the application and environment you set up.
