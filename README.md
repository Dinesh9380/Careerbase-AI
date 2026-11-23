# CareerBase AI
### AI-Powered Skill Assessment & Intelligent Career Guidance Platform

<p align="center">
  An intelligent career development platform designed to bridge the gap between academic learning and industry requirements.
</p>

<p align="center">
  **Artificial Intelligence · Machine Learning · Explainable AI · Blockchain · Big Data**
</p>

---

## Overview

CareerBase AI is a full-stack career intelligence platform that helps students evaluate their technical capabilities, identify skill gaps, explore suitable career opportunities, and generate personalized learning roadmaps.

The platform combines machine learning, explainable AI, blockchain-based credential verification, resume intelligence, and data analytics to support informed career decisions.

The project is aligned with **United Nations Sustainable Development Goal 4 – Quality Education**, particularly the objective of improving access to relevant technical and vocational skills.

## Key Features

### 1. AI-Powered Skill Assessment
- Intelligent evaluation of student skill profiles.
- Machine learning-based career suitability analysis.
- Identification of technical skill gaps.
- Personalized career recommendations.

### 2. Career Recommendation Engine
- Career suggestions based on student profiles.
- Industry-oriented role matching.
- Career readiness evaluation.
- Personalized development recommendations.

### 3. Explainable AI (XAI)
- Transparent machine learning predictions.
- Explanation of career recommendations.
- Identification of important influencing factors.

### 4. Blockchain Credential Verification
- Blockchain-based credential verification.
- SHA-256 hashing.
- Tamper-evident credential records.

### 5. Resume Intelligence
- Resume parsing and information extraction.
- OCR-based document processing.
- Resume skill identification.

### 6. Big Data Analytics
- Student performance analytics.
- Skill distribution analysis.
- Career readiness insights.
- Data-driven reporting.

### 7. Adaptive Learning Roadmaps
- Personalized learning pathways.
- Skill improvement recommendations.
- Career-focused development plans.

### 8. Security and Access Control
- Role-Based Access Control (RBAC).
- Secure authentication.
- Environment-based configuration.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn, Random Forest |
| AI Explainability | Explainable AI |
| Computer Vision | OCR, OpenCV |
| Blockchain | SHA-256, Blockchain Ledger |
| Big Data | Apache Spark |
| Database | Refer to project configuration |
| Deployment | Docker, Docker Compose |
| Version Control | Git, GitHub |

## Machine Learning

The project includes a Random Forest classification pipeline for evaluating student skill profiles and generating career recommendations.

**Reported model performance:**
- Test Accuracy: 96.42%
- Weighted F1-Score: 96.41%
- Training dataset: 5,000 synthetic student profiles
- Career categories: 20 technology career paths

*Note: Performance figures should be interpreted in the context of the dataset and evaluation methodology.*

## System Architecture

```text
             STUDENT / USER
                   |
                   v
          REACT FRONTEND
             (Vite)
                   |
                   v
             FASTAPI
             BACKEND
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   MACHINE     RESUME       CAREER
   LEARNING    ANALYSIS    ASSESSMENT
       |           |           |
       +-----------+-----------+
                   |
                   v
          CAREER RECOMMENDATION
                   |
          +--------+--------+
          |                 |
          v                 v
      LEARNING          ANALYTICS
      ROADMAPS           ENGINE
          |
          v
     STUDENT CAREER
      DEVELOPMENT
```

## Project Structure

```text
Careerbase-AI/
│
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   ├── blockchain/
│   │   └── ...
│   └── ...
│
├── frontend/
│
├── bigdata/
│   └── spark_jobs/
│
├── blockchain/
│   └── contracts/
│
├── docker/
│
├── .env.example
├── .gitignore
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── package.json
└── README.md
```

*Directory structure is summarized; refer to the repository for the complete implementation.*

## Getting Started

### Prerequisites

Install the following:

- Python 3.12
- Node.js and npm
- Git
- Docker (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/Dinesh9380/Careerbase-AI.git
cd Careerbase-AI
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend using the actual FastAPI application module:

```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

### 4. Docker Deployment

From the project root:

```bash
docker compose up --build
```

Check the Docker configuration for the actual service ports and environment variables.

## API Documentation

CareerBase AI uses FastAPI for backend services.

When the backend is running, access the interactive API documentation at:

```text
http://localhost:8000/docs
```

## Project Objectives

1. Help students understand their technical skill levels.
2. Identify gaps between academic knowledge and industry expectations.
3. Recommend suitable technology career paths.
4. Generate personalized learning roadmaps.
5. Support transparent and explainable AI-based recommendations.
6. Promote technology-driven educational development.

## Future Enhancements

- Integration with real-time job market data.
- Advanced AI-powered career assistant.
- Integration with additional learning platforms.
- More industry-specific skill assessments.
- Cloud-based deployment and scalability.
- Advanced student progress analytics.

## Contribution

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## Author

**Dinesh K V**

GitHub: [@Dinesh9380](https://github.com/Dinesh9380)

## License

This project is licensed under the MIT License, subject to the repository's license file.

---

<p align="center">
  **CareerBase AI – Transforming Skills into Career Opportunities.**
</p>