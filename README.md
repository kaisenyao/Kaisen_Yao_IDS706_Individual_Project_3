# IDS706 Individual Project 3: Movie Trends & Analytics Platform

[![Build and deploy container app to Azure Web App - ids706](https://github.com/bionicotaku/IDS706_Final_Project/actions/workflows/cicd.yml/badge.svg)](https://github.com/bionicotaku/IDS706_Final_Project/actions/workflows/cicd.yml)

## Project Description:
This project is a modified version of the group final project, repurposed as an individual assignment to build a publicly accessible, auto-scaling containerized web application using AWS Services and Flask. The group project focused on analyzing movie trends using Flask, PostgreSQL, and Azure, while this individual project transitions to a wider range of application. It demonstrates containerization, auto-scaling, and cloud deployment, applying Flask knowledge from previous lessons in a scalable, real-world context. This modification emphasizes scalability and efficiency in deployment for dynamic traffic loads.

## Links:
- **Website**: [https://www.ids706final.dingzhen.us/](https://www.ids706final.dingzhen.us/)
- **Introductory video**: [www.youtube.com](https://youtu.be/KIYtC2t5Xm0)

## Project Description:
This project applies the skills acquired in Data Engineering to develop an application that analyzes movie popularity and genre trends over time. Users can specify a start and end year to explore how the popularity of different movie genres has evolved. Additionally, they can input a specific year to view the most and least popular movies based on TMDB’s popularity scores. The platform also includes an AI chat assistant, powered by the X.AI API, for interactive user engagement. The project utilizes the following technologies:

- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![SQL](https://img.shields.io/badge/sql-%2307405e.svg?style=for-the-badge&logo=postgresql&logoColor=white)
- ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Project Architecture:
![Diagram](diagram.png)

This is a Flask-based web application that adopts a microservices architecture and consists of the following core components:

### 1. Frontend
- Uses HTML5, CSS3, and JavaScript to build the user interface
- Utilizes Chart.js for data visualization
- Implements responsive design to ensure proper display across different devices

### 2. Backend
- Flask as the web framework
- PostgreSQL as the database
- RESTful API design
- Grok3 LLM integration for AI chat functionality

### 3. DevOps (Automated Development and Deployment)
- Docker containerization, hosted on Docker Hub
- Azure Web App deployment, using Infrastructure as Code. Also uses Azure Database for PostgreSQL to build the database
- GitHub Actions for automated CI/CD
- Uses environment variables to handle sensitive information like API keys

### 4. CI/CD Pipeline

This CI/CD workflow defined in `.github/workflows` automates the process of building a Docker container from the code repository and deploying it to an Azure Web App whenever code is pushed to the `main` branch or the workflow is manually triggered. It ensures seamless integration and deployment to the production environment.

1. Code is pushed to GitHub main branch
2. GitHub Actions triggers automatic testing and building
3. Docker image is built
4. Image is pushed to Docker Hub
5. Automatic deployment to Azure Web App

## Infrastructure as Code

This project uses Azure Resource Manager (ARM) templates for deploying the IDS706 project infrastructure, automatically creating the following resources:

- Web App: Basic (B3) tier with Docker container
- Database: PostgreSQL Flexible Server (Standard_B1ms)
- Location: East US (web app) and East US 2 (database)

The process is as follows:
1. First, `az login` to log into Azure, then navigate to the project's `ids706-infrastructure` folder
2. Create resource group:
```
az group create --name ids706final --location eastus
```

3. Deploy infrastructure:
```
az deployment group create \
  --resource-group ids706final \
  --template-file template.json \
  --parameters @parameters.json \
  --parameters administratorLoginPassword=<your-secure-password>
```

4. Configure services (such as firewall):
```
az postgres flexible-server firewall-rule create \
  --resource-group ids706final \
  --name ids706 \
  --rule-name allowapp \
  --start-ip-address <web-app-ip> \
  --end-ip-address <web-app-ip>
```

## Load Testing:
We used the `Locust` library to perform load testing on our Flask application. The code can be found in load_test.py. The load test on Locust was configured to test 10,000 requests per second.
```
locust -f load_test.py --host=https://www.ids706final.dingzhen.us
```
Here are the test results:

<img width="1242" alt="Screenshot 2024-12-12 at 01 17 19" src="https://github.com/user-attachments/assets/cfc2e1ef-235d-48f6-96f8-544281ee4728" />

![total_requests_per_second_1733983092 742](https://github.com/user-attachments/assets/73f8beaf-ea43-4d1b-bfd2-782fb321bedb)

Due to limitations with our Azure Student Subscription, we were restricted to using the Standard S3 SKU with a maximum of 10 instances. Each instance was configured with 9 workers and 4 threads to maximize concurrent capacity. As illustrated in the graphs, the system achieved a peak of approximately 1,600 requests per second, with a stable maximum load of around 1,200 requests per second. At a load of 10,000 users per second, the 95th percentile latency exceeded 60,000ms, signaling the system’s maximum capacity. On average, 50% of the requests experienced a latency of 500ms or less.

## Local Deployment
Note that you need to create a `.env` file beforehand, containing the `XAI_API_KEY` environment variable to use the Grok3 large language model chat functionality.

You can use .devcontainer configuration for Github/Gitlab Codespaces:
- `make install` Install dependencies
- `make run` Run the application

Or directly use Docker:
- `make docker-build` Build Docker image
- `make docker-run` Run Docker container

## The Application:
The application is deployed on Azure Web App Services and uses CloudFlare for domain services to enable custom domain usage.

## Application Overview: Movie Trend Analysis and AI Chat Assistant

This project is a web application designed to analyze movie trends and provide an AI chat assistant. It features two main functionalities:

1. **AI Chat Assistant**
Users can interact with the latest released Grok3 large language model. If users have previously requested movie analysis data, this data will automatically be sent to the backend as context during subsequent conversations.

The design of the page is clean and modern, utilizing CSS to ensure a responsive and visually appealing experience across different devices.
<img width="1284" alt="Screenshot 2024-12-11 at 23 02 19" src="https://github.com/user-attachments/assets/00cac431-f5c2-4e56-9433-1dc2c7dbf983" />

2. **Explore Movie Genres Over Time**
This service allows users to analyze the popularity of different movie genres over a specified time range. It provides the following inputs:

- **Start Year**: The first year in the analysis range.  
- **End Year**: The last year in the analysis range.  

**Output**: A stacked bar chart where:  
- The x-axis represents the years within the selected range.
- The y-axis shows the count of movies released each year.
- Each genre is represented by a different color in the stack, showing its contribution to the total number of movies for that year.

This visualization helps users identify trends in genre preferences over time, such as the rise or decline of specific genres.
<img width="1164" alt="Screenshot 2024-12-11 at 23 02 39" src="https://github.com/user-attachments/assets/ccbbef56-a1e6-4a35-a49e-d6e5d5d78ef1" />

3. **Top Movies by TMDB Popularity**
This service displays the most and least popular movies based on TMDB's popularity scores. It provides the following input:  

- **Year**: Specify a year to analyze the movies released that year.  

**Output**: A bar chart where:  
- The top 5 movies are displayed in green bars, representing the highest popularity scores.
- The bottom 5 movies are displayed in red bars, representing the lowest popularity scores.
- The x-axis shows movie titles, and the y-axis shows their popularity scores.

This visualization highlights the standout successes and underperformers in terms of popularity for the selected year.
<img width="1186" alt="Screenshot 2024-12-11 at 23 03 19" src="https://github.com/user-attachments/assets/6e91859d-f776-4ebf-a7d9-0c782cdd2f25" />

## Chat Interface Page:
This page serves as the primary interface for users to interact with the AI chat assistant, which is powered by the X.AI API. The interface is designed using Flask and HTML to provide a seamless and user-friendly experience.

## Microservice
In this project, Flask serves as a microservice framework to build and deploy the web application for movie trend analysis and AI chat assistance. Flask, being lightweight, is ideal for creating small-scale microservices. It manages routing, handling requests for movie genre and popularity analysis, and returns data in JSON format. The application integrates with HTML templates to generate dynamic web pages, using JavaScript and Chart.js for data visualization. Flask is containerized using Docker, ensuring consistent deployment across environments, and is deployed on platforms like Azure Web App Services. This microservice architecture allows for modular, scalable design, facilitating future enhancements and maintenance.

## Data Engineering
Flask is utilized as a lightweight microservice framework to build and deploy the web application for movie trend analysis and AI chat assistance. It handles routing, processes requests for movie genre and popularity analysis, and delivers data in JSON format. HTML templates are integrated with Flask to create dynamic web pages, while JavaScript and Chart.js are used for data visualization. The application is containerized using Docker for consistent deployment across environments and deployed on platforms like Azure Web App Services. This microservice-based architecture ensures modularity, scalability, and ease of future enhancements and maintenance.

## AI Tools
1. ChatGPT: Used to debug and optimize the frontend UI, ChatGPT helped identify and resolve issues efficiently, improving the user interface design for a more intuitive and visually appealing experience.
2. Claude.AI: Utilized for enhancing the design and functionality of the application, ensuring smoother interactions and addressing backend optimization challenges.
