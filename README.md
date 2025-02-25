# Building and Deploying a Scalable Hello World CI/CD Pipeline on AWS Using ECS, ECR, Fargate, Docker, Github Actions, FastAPI and PostgreSQL on RDS**
---

**The Journey from Complexity to Simplicity**
----

Our adventure began with an ambitious goal: to deploy a fully containerized, scalable application on AWS using ECS and Fargate. Originally, we started with a complex multisystem approach, but as roadblocks piled up---configuration issues, deployment failures, and infrastructure inconsistencies---we realized we were biting off more than we could chew. Instead of continuing down that frustrating path, we made a strategic pivot.

The new goal? **Start simple.**

Before jumping into a complex SaaS product, we needed to **prove that we could reliably deploy even the simplest application: a "Hello World" page.** This meant **creating a frontend and backend, deploying them separately on AWS, and ensuring automated deployments worked seamlessly through GitHub Actions.**

By taking this approach, we set up a **solid foundation** that could later be expanded into a full-stack SaaS product. Below is a breakdown of how we methodically built and deployed a **static frontend and an API backend, containerized everything, and made it all work seamlessly in the cloud.**

* * * * *

**🏗️ The Steps We Took to Build and Deploy a Hello World Frontend and API**
---

### **Step 1: Setting Up the Frontend**

To start, we created a simple **HTML page** that displays "Hello, World!" We hosted this page in a **Docker container** and pushed it to **AWS Elastic Container Registry (ECR)** for deployment via **AWS ECS and Fargate.**

#### Key Milestones:

-   Created an **index.html** file with basic "Hello, World!" content.

-   Wrote a **Dockerfile** to containerize the frontend.

-   Used **AWS ECR** to store the Docker image.

-   Configured **AWS ECS with Fargate** to deploy the frontend container.

-   Linked the deployment to **GitHub Actions** to enable automatic updates when changes were pushed.

* * * * *

### **Step 2: Connecting the Backend API**

Once the frontend was up and running, the next goal was to **deploy an API backend** using **FastAPI** (a lightweight Python framework). The backend needed to:

1.  Return a "Hello, World!" message.

2.  Store and retrieve data from a **PostgreSQL database hosted on AWS RDS.**

3.  Allow CORS requests to support both local and cloud environments.

#### Key Milestones:

-   Built a **FastAPI server** with a single `/test-db` endpoint.

-   Containerized the API using **Docker**.

-   Used **AWS ECR** to store the backend Docker image.

-   Set up **AWS RDS PostgreSQL** as the database.

-   Configured **ECS and Fargate** to run the API.

-   Ensured proper CORS handling for both local and production environments.

* * * * *

### **Step 3: Automating Deployments**

To ensure every update was **automatically deployed**, we configured **GitHub Actions** for CI/CD.

#### Key Milestones:

-   Created a **deploy.yml** file for GitHub Actions to:

    -   Build the Docker images.

    -   Push them to AWS ECR.

    -   Update ECS tasks and services with the new images.

-   Ensured **environment variables** were injected correctly from **GitHub Secrets.**

-   Debugged multiple deployment failures related to missing environment variables, ECS task definitions, and misconfigurations.

* * * * *

### **Step 4: Debugging and Fixing Database Seeding**

The API was connected to the database, but returning empty results. This led to several debugging sessions:

-   Confirmed that **migrations were running** but seed data was missing.

-   Fixed issues with the `seed.py` script, ensuring **data was inserted correctly.**

-   Verified the database connection using **ECS logs and manual API testing.**

* * * * *

### **Step 5: Enabling HTTPS for Secure API Access**

Initially, [**www.razorit.com**](http://www.razorit.com) worked over HTTPS without any manual configuration---thanks to Cloudflare's auto-handling of SSL. However, **api.razorit.com** was still running on HTTP. We:

-   Enabled **HTTPS on Cloudflare for the API subdomain.**

-   Verified SSL worked across both frontend and backend.

-   Ensured **CORS was properly configured** for secure cross-origin requests.

* * * * *

**🚀 Step-by-Step Guide to Reproduce This Deployment**
------------------------------------------------------

### **Frontend Deployment**

1.  **Create a Simple Frontend**

    -   Create an `index.html` file:

        ```
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Hello, World!</title></head>
        <body><h1>Hello, World!</h1></body>
        </html>
        ```

2.  **Containerize the Frontend**

    -   Create a `Dockerfile`:

        ```
        FROM nginx:alpine
        COPY index.html /usr/share/nginx/html/index.html
        EXPOSE 80
        CMD ["nginx", "-g", "daemon off;"]
        ```

3.  **Deploy to AWS ECS**

    -   Create an ECS service for the frontend using **Fargate**:

    -   Navigate to AWS ECS and create a new cluster using the Fargate launch type.

    -   Define a new ECS task definition specifying the frontend container.

    -   Set up an ECS service linked to the task definition, ensuring it uses the existing ALB for routing traffic.

    -   Configure service auto-scaling and assign appropriate IAM roles for access control.

    -   Deploy the service and confirm that the frontend is accessible through the ALB's DNS.

    -   Configure an **Application Load Balancer (ALB)** to route traffic to the service.

* * * * *

### **Backend API Deployment**

1.  **Create a FastAPI Backend**

    -   Install dependencies:

        ```
        pip install fastapi uvicorn sqlalchemy asyncpg alembic
        ```

    -   Create `main.py`:

        ```
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/")
        def read_root():
            return {"message": "Hello from API!"}
        ```

2.  **Deploy the API to AWS ECS**

    -   Push the API image to ECR.

    -   Create an **ECS service** with **Fargate**.

    -   Configure a **database in AWS RDS** and inject secrets via **GitHub Actions.**

* * * * *

**🎯 Final Thoughts**
---------------------

This project evolved from **frustration with a complex system** to a **well-structured, automated deployment pipeline** for a scalable API and frontend. By breaking it into **small, testable components**, we eliminated headaches and built a **solid AWS infrastructure** ready to scale.

### **💡 Key Takeaways**

✅ Start **simple**---build up from a working foundation.\
✅ Use **GitHub Actions** for **automated CI/CD**.\
✅ Configure **secrets properly** to avoid deployment failures.\
✅ **Debug incrementally**---check logs, update configurations, and test frequently.

Now, we have **a reliable way to deploy full-stack apps on AWS with ECS, ECR, and Fargate.** 🚀
