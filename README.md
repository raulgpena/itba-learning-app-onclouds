# learning-app-onclouds
Machine Learning Applications in the Cloud

## Run on Docker.
cd to docker folder and then execute: docker-compose up --build. Once executed, going to the next url: http://127.0.0.1:58080, you must receive a message so: Hello, World! 

*** Remember this instrucctions must be executed from a command windows: bash, powerchell, etc

## Run on AWS (Using lambda/api)
cd to lambda_package folder and then execute: 

* pip install -r requirements.txt -t . 
* find . -name "*.dist-info" -type d -exec rm -rf {} +
* zip -r ../lambda_function.zip .
* terraform apply
* terraform destroy once used.

*** Remember this instrucctions must be executed from a command windows: bash, powerchell, etc