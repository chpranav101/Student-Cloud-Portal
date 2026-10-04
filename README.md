\# ☁ Student Cloud Portal



A secure cloud-based student management application developed using \*\*Flask\*\* and deployed on \*\*Amazon EC2\*\*. The application uses \*\*AWS IAM\*\* for controlled cloud access and \*\*Amazon S3\*\* for secure private document storage.



\---



\## 📌 Project Overview



The Student Cloud Portal provides a centralized platform for managing student information and documents.



The application supports separate \*\*Student\*\* and \*\*Admin\*\* roles with role-based access control.



Students can register, log in, view their dashboard, and upload documents. Administrators can manage student information and securely access uploaded documents.



The application demonstrates how cloud services such as \*\*Amazon EC2, IAM, and S3\*\* can be integrated into a secure web application.



\---



\## 🎯 Objectives



\- Develop a secure cloud-based student management system

\- Implement Student and Admin authentication

\- Implement role-based access control

\- Deploy the Flask application on Amazon EC2

\- Use an EC2 IAM Role for AWS permissions

\- Store student documents securely in Amazon S3

\- Provide controlled access to private S3 documents

\- Generate temporary presigned URLs for document access



\---



\## 🚀 Key Features



\### 👨‍🎓 Student



\- Student registration

\- Secure login

\- Student dashboard

\- View personal information

\- Upload documents

\- View uploaded documents

\- Secure document access

\- Logout



\### 👨‍💼 Admin



\- Separate Admin login

\- Admin dashboard

\- View registered students

\- View uploaded documents

\- Securely open student documents

\- Logout



\### 🔐 Security



\- Role-based access control

\- AWS IAM Role attached to EC2

\- Private Amazon S3 bucket

\- No public S3 document access

\- Temporary S3 presigned URLs

\- AWS Signature Version 4

\- No AWS access keys stored in the application



\---



\## 🏗️ System Architecture



```text

&#x20;                ┌──────────────────────┐

&#x20;                │       User           │

&#x20;                │ Student / Admin      │

&#x20;                └──────────┬───────────┘

&#x20;                           │

&#x20;                           ▼

&#x20;                ┌──────────────────────┐

&#x20;                │   Flask Web App      │

&#x20;                │  Student Cloud       │

&#x20;                │      Portal          │

&#x20;                └──────────┬───────────┘

&#x20;                           │

&#x20;             ┌─────────────┴─────────────┐

&#x20;             │                           │

&#x20;             ▼                           ▼

&#x20;    ┌─────────────────┐        ┌─────────────────┐

&#x20;    │  SQLite Database │        │   Amazon S3     │

&#x20;    │                 │        │ Private Bucket  │

&#x20;    │ Students / Users│        │ Student Files   │

&#x20;    └─────────────────┘        └────────┬────────┘

&#x20;                                       ▲

&#x20;                                       │

&#x20;                             ┌─────────┴─────────┐

&#x20;                             │    AWS IAM Role   │

&#x20;                             │ StudentCloud      │

&#x20;                             │ EC2Role           │

&#x20;                             └─────────┬─────────┘

&#x20;                                       │

&#x20;                             ┌─────────▼─────────┐

&#x20;                             │   Amazon EC2      │

&#x20;                             │ Flask + Gunicorn  │

&#x20;                             └───────────────────┘







☁️ AWS Services Used

AWS Service	Purpose

Amazon EC2	Hosts the Flask web application

AWS IAM	Controls AWS permissions

IAM Role	Allows EC2 to access S3 securely

Amazon S3	Stores student documents privately

Security Groups	Controls network access to EC2





🔑 IAM Implementation



The application uses an EC2 IAM Role:



StudentCloudEC2Role



The role provides the EC2 instance with controlled permissions to interact with the project S3 bucket.



The application does not store AWS access keys on the server.



This follows the principle of:



Least Privilege



The IAM policy allows only the required S3 operations such as:



List bucket

Upload objects

Read objects



Delete permission is intentionally not provided.



🗄️ Amazon S3 Security



Student documents are stored in a private S3 bucket.



Documents are not exposed through a public S3 URL.



When an authorized user requests a document, the Flask application generates a temporary presigned URL.



User

&#x20; │

&#x20; ▼

Flask Application

&#x20; │

&#x20; ▼

Verify User Authorization

&#x20; │

&#x20; ▼

Generate Presigned URL

&#x20; │

&#x20; ▼

Private Amazon S3

&#x20; │

&#x20; ▼

Temporary Secure Access



This provides controlled and time-limited access to stored documents.



🔐 Authentication and Authorization



The application has two roles:



Student

&#x20;  │

&#x20;  └── Student Dashboard

&#x20;       ├── View Information

&#x20;       ├── Upload Documents

&#x20;       └── View Documents



Admin

&#x20;  │

&#x20;  └── Admin Dashboard

&#x20;       ├── View Students

&#x20;       └── View Documents



Application authentication is separate from AWS IAM.



Application Login → controls Student/Admin access

AWS IAM → controls application access to AWS resources

🛠️ Technologies Used

Backend

Python

Flask

SQLite

Gunicorn

Boto3

Frontend

HTML5

CSS3

JavaScript

Cloud

Amazon EC2

AWS IAM

Amazon S3

EC2 Security Groups

Development Tools

Git

GitHub

VS Code

PowerShell

📁 Project Structure

Student-Cloud-Portal/

│

├── app.py

├── README.md

├── .gitignore

│

├── static/

│   └── style.css

│

└── templates/

&#x20;   ├── add\_student.html

&#x20;   ├── admin\_dashboard.html

&#x20;   ├── admin\_documents.html

&#x20;   ├── index.html

&#x20;   ├── login.html

&#x20;   ├── my\_documents.html

&#x20;   ├── register.html

&#x20;   ├── student\_dashboard.html

&#x20;   ├── students.html

&#x20;   └── upload\_document.html

⚙️ Local Setup

1\. Clone the repository

git clone https://github.com/chpranav101/Student-Cloud-Portal.git

2\. Navigate to the project

cd Student-Cloud-Portal

3\. Create a virtual environment

python -m venv venv

4\. Activate the virtual environment



Windows:



venv\\Scripts\\activate

5\. Install dependencies

pip install flask boto3 gunicorn

6\. Run the application

python app.py



The application will be available at:



http://127.0.0.1:5000

☁️ AWS Deployment



The application was deployed on:



Amazon EC2



The deployment uses:



Flask

&#x20;  ↓

Gunicorn

&#x20;  ↓

systemd

&#x20;  ↓

Amazon EC2



The EC2 instance uses the IAM Role:



StudentCloudEC2Role



for secure access to Amazon S3.



📊 Database



The application uses SQLite for storing:



Users

id

name

email

password

role

Students

id

name

email

course

year



The database file is intentionally excluded from GitHub using .gitignore.



🔒 Security Considerations



The project follows several cloud security practices:



Private S3 document storage

IAM role-based AWS access

Least-privilege permissions

Role-based application authorization

Temporary presigned URLs

No AWS credentials stored in source code

EC2 Security Group network controls



Note: Production deployments should additionally use HTTPS, environment-based secrets, stronger secret management, and a production database.



🎓 Academic Relevance



This project demonstrates practical implementation of:



Cloud Computing

AWS IAM

Amazon EC2

Amazon S3

Cloud Security

Role-Based Access Control

Web Application Development

Database Management

Secure Cloud Storage



📌 Future Enhancements

HTTPS with a domain name

PostgreSQL / Amazon RDS

AWS CloudWatch monitoring

Email notifications

Password reset functionality

Multi-factor authentication

Docker deployment

CI/CD using GitHub Actions



👨‍💻 Author



Pranav Chougule



MCA Student | Software Development \& Data Analytics



GitHub:

https://github.com/chpranav101

