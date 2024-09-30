

terraform {
    
    required_providers {
        
        aws = {
            
            source  = "hashicorp/aws"
            version = "~> 5.16.0"
        }
    }

    required_version = ">= 1.4.2"
}


provider "aws" {
    
    region                   = "us-east-1"
    shared_credentials_files = ["~/.aws/credentials"]
    profile                  = "live-api-user"
}