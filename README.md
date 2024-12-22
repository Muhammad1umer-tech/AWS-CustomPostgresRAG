# Custom RAG Deployment with AWS Services

## Project Overview

This project showcases the deployment of a custom Retrieval-Augmented Generation (RAG) pipeline using AWS cloud infrastructure. It integrates a React-based frontend with a FastAPI backend while using AWS services such as S3, RDS, EC2, VPC, IAM, cloudMap and API Gateway for scalability, security, and performance.


**AWS Services**:  
    ![S3](https://img.shields.io/badge/AWS-S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
    ![RDS](https://img.shields.io/badge/AWS-RDS-527FFF?style=for-the-badge&logo=amazon-rds&logoColor=white)
    ![EC2](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
    ![VPC](https://img.shields.io/badge/AWS-VPC-232F3E?style=for-the-badge&logo=amazon-vpc&logoColor=white)
    ![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-FF4F00?style=for-the-badge&logo=amazon-api-gateway&logoColor=white)
    ![IAM](https://img.shields.io/badge/AWS-IAM-FF9900?style=for-the-badge&logo=amazon-iam&logoColor=white)
    ![Cloud Map](https://img.shields.io/badge/AWS-Cloud_Map-00A8E8?style=for-the-badge&logo=amazon-cloudmap&logoColor=white)
    ![Eraser.io](https://img.shields.io/badge/Eraser.io-00A8E8?style=for-the-badge&logo=eraser&logoColor=white)


## AWS Architecture
![Alt Text](https://github.com/Muhammad1umer-tech/AWS-CustomPostgresRAG/blob/main/images/AwsArchitecture.png)


### Key Components:

- **Frontend & Backend**: 
  - Developed using React to provide a responsive and user-friendly interface.
  - Built with FastAPI to handle API requests and communicate with the database.
  - Implements LangChain and custom RAG for processing CSV data.

- **AWS Services**:
  - **S3**: Used to store CSV files. IAM policies are configured with **read-only** access for security.
  - **RDS**: PostgreSQL database used to store vector embeddings and information extracted from the CSV files.
  - **EC2**: Hosts two services—frontend and backend.
  - **VPC**: Designed a custom network with public and private subnet for security.
  - **APIGateaway**: Configured to ensure backend is only accessible internally, not via browser or internet.
  - **Cloud Map**: Utilized for service discovery within the VPC.

    
---


## Deployment Architecture

### 1. Custom VPC
- **Public Subnet**: 
  - Hosts the EC2 instance for the frontend and backend services.
- **Two Private Subnets**: 
  - Host the RDS instance and fast availability.
    
![Alt Text](https://github.com/Muhammad1umer-tech/AWS-CustomPostgresRAG/blob/main/images/Pasted%20image%20(4).png)

### 2. Network Configuration
- **Public Subnet**:
  - Internet Gateway attached to enable internet access.
- **Private Subnets**:
  - NAT Gateway configured to allow one-way communication from the private subnet (RDS) to the internet for necessary updates.
    
![Alt Text](https://github.com/Muhammad1umer-tech/AWS-CustomPostgresRAG/blob/main/images/Pasted%20image%20(3).png)


### 3. Security Rules
- **Inbound Rules**:
  - Port `3000` accessible via the internet for the frontend.
  - Port `8000` not directly accessible from the internet.

- **API Gateway**:
  - Used to securely route frontend requests to the backend.
  - Configured with a private API to allow internal access to port `8000` through the API Gateway, ensuring secure communication.

### 4. EC2 & RDS
  - Hosts both frontend and backend services for seamless integration.
  - RDS: Stores PostgreSQL data including vector embeddings and extracted information.
  - RDS is placed in a private subnet with secure access, while EC2 uses a public subnet with controlled inbound rules.

![Alt Text](https://github.com/Muhammad1umer-tech/AWS-CustomPostgresRAG/blob/main/images/Pasted%20image.png)
---

## Features

1. **Custom RAG Implementation**:
   - Processes CSV data which is stored on AWS S3, to generate embeddings stored in PostgreSQL using LangChain.

2. **Secure and Scalable Deployment**:
   - IAM policy with read-only S3 access ensures minimal privileges.
   - Use of private subnets and NAT Gateway to isolate sensitive RDS resources.

3. **Optimized Networking**:
   - API Gateway ensures secure routing and restricts direct public access to backend services.

---

