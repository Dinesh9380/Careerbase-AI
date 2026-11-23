import os
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.database import Base, engine, SessionLocal
from app.core.security import get_password_hash
from app.models.models import (
    User, StudentProfile, AcademicRecord, Skill, StudentSkill,
    StudentSoftSkill, StudentInterest, StudentProject, StudentCertification,
    CareerRole, CareerSkill, Assessment, Question, QuestionOption,
    LearningResource, Achievement, StudentAchievement, Notification,
    Credential, AuditLog
)
from app.blockchain.blockchain_ledger import blockchain_ledger

# Define 20 Career Roles
CAREER_ROLES_DATA = [
    {
        "title": "Full Stack Developer", "slug": "full-stack-developer",
        "description": "Designs and builds end-to-end web applications across modern frontend frameworks, scalable backend APIs, and distributed databases.",
        "industry": "Software & Web Services", "difficulty": "Intermediate", "entry_level_suitability": True,
        "education_requirement": "B.Tech/B.S. in Computer Science or equivalent practical portfolio",
        "average_salary": "$92,000 - $135,000 / ₹10-18 LPA", "market_demand": "Very High",
        "soft_skills": ["Problem Solving", "Team Collaboration", "Agile Methodologies"],
        "recommended_projects": ["Full-Stack E-Commerce SaaS with Stripe", "Real-Time Collaboration Workspace", "RESTful Task Management Engine"],
        "recommended_certifications": ["AWS Certified Developer Associate", "Meta Front-End & Back-End Professional Certificates"]
    },
    {
        "title": "Software Developer", "slug": "software-developer",
        "description": "Constructs robust, high-performance desktop, system, and backend software utilizing sound algorithmic principles and system architecture.",
        "industry": "Information Technology", "difficulty": "Intermediate", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science, Software Engineering, or related",
        "average_salary": "$90,000 - $130,000 / ₹9-16 LPA", "market_demand": "High",
        "soft_skills": ["Analytical Thinking", "Attention to Detail", "Code Review"],
        "recommended_projects": ["High-Performance In-Memory Cache", "Distributed Key-Value Store", "CLI Developer Tooling Suite"],
        "recommended_certifications": ["Oracle Certified Professional: Java SE", "C++ Certified Associate Programmer"]
    },
    {
        "title": "Data Scientist", "slug": "data-scientist",
        "description": "Leverages statistical modeling, machine learning, and exploratory data analytics to extract actionable business insights from complex data.",
        "industry": "Data & Analytics", "difficulty": "Advanced", "entry_level_suitability": True,
        "education_requirement": "Bachelor's or Master's in Data Science, Statistics, Mathematics, or CS",
        "average_salary": "$105,000 - $150,000 / ₹12-22 LPA", "market_demand": "High",
        "soft_skills": ["Data Storytelling", "Critical Thinking", "Stakeholder Communication"],
        "recommended_projects": ["Customer Churn Prediction with Explainable AI", "Market Basket Analysis Engine", "Algorithmic Trading Backtesting Model"],
        "recommended_certifications": ["IBM Data Science Professional Certificate", "Google Advanced Data Analytics"]
    },
    {
        "title": "Machine Learning Engineer", "slug": "machine-learning-engineer",
        "description": "Bridges the gap between data science experimentation and production software by architecting, training, and deploying ML pipelines.",
        "industry": "Artificial Intelligence", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Bachelor's/Master's in CS, AI/ML, or Applied Mathematics",
        "average_salary": "$120,000 - $165,000 / ₹14-25 LPA", "market_demand": "Very High",
        "soft_skills": ["Research Aptitude", "Systems Optimization", "Cross-Functional Collaboration"],
        "recommended_projects": ["End-to-End MLOps Pipeline with MLflow & Docker", "Real-Time Fraud Detection Inference API", "Recommendation Engine with Embeddings"],
        "recommended_certifications": ["AWS Certified Machine Learning - Specialty", "TensorFlow Developer Certificate"]
    },
    {
        "title": "AI Engineer", "slug": "ai-engineer",
        "description": "Specializes in modern Large Language Models, Generative AI applications, RAG pipelines, and multi-modal neural network systems.",
        "industry": "Artificial Intelligence", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Degree in Computer Science or specialized AI credentials",
        "average_salary": "$130,000 - $180,000 / ₹16-30 LPA", "market_demand": "Surging",
        "soft_skills": ["Prompt Engineering", "Ethical AI Principles", "Continuous Learning"],
        "recommended_projects": ["Context-Aware Enterprise RAG Assistant", "Autonomous Multi-Agent Task Orchestrator", "Fine-Tuned Domain LLM with LoRA"],
        "recommended_certifications": ["DeepLearning.AI Generative AI Specialization", "Microsoft Certified: Azure AI Engineer Associate"]
    },
    {
        "title": "Data Analyst", "slug": "data-analyst",
        "description": "Transforms raw transactional records into executive dashboards, metric reporting, and diagnostic business intelligence.",
        "industry": "Business Intelligence & Analytics", "difficulty": "Beginner", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Business Analytics, Economics, Statistics, or CS",
        "average_salary": "$70,000 - $95,000 / ₹6-12 LPA", "market_demand": "High",
        "soft_skills": ["Presentation Skills", "Data Interpretation", "Business Acumen"],
        "recommended_projects": ["Interactive Executive Sales Dashboard in Power BI", "E-Commerce Cohort Retention Analysis in SQL", "Web Traffic Exploratory Analysis with Pandas"],
        "recommended_certifications": ["Google Data Analytics Professional Certificate", "Microsoft Certified: Power BI Data Analyst"]
    },
    {
        "title": "Data Engineer", "slug": "data-engineer",
        "description": "Constructs reliable data pipelines, data warehouses, and ETL infrastructure supporting enterprise analytics and ML models.",
        "industry": "Data Infrastructure", "difficulty": "Advanced", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science, Information Systems, or related",
        "average_salary": "$110,000 - $155,000 / ₹12-24 LPA", "market_demand": "Very High",
        "soft_skills": ["Pipeline Reliability", "Root-Cause Analysis", "Data Modeling"],
        "recommended_projects": ["Streaming Analytics Pipeline with Kafka & Spark", "Data Lakehouse Warehouse Architecture using dbt & Snowflake", "Automated CDC Ingestion Pipeline"],
        "recommended_certifications": ["Google Cloud Professional Data Engineer", "Databricks Certified Data Engineer Associate"]
    },
    {
        "title": "Big Data Engineer", "slug": "big-data-engineer",
        "description": "Architects petabyte-scale distributed computing platforms, Spark jobs, and real-time streaming architectures.",
        "industry": "Enterprise Big Data", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "B.Tech/M.Tech in CS or extensive distributed systems experience",
        "average_salary": "$115,000 - $160,000 / ₹14-26 LPA", "market_demand": "High",
        "soft_skills": ["Distributed Systems Reasoning", "Performance Tuning", "Fault Tolerance"],
        "recommended_projects": ["Distributed Log Analysis on Apache Spark Cluster", "Real-Time Telemetry Pipeline with Kafka & Flink", "Hadoop HDFS to S3 Modernization"],
        "recommended_certifications": ["Cloudera Certified Associate Data Analyst", "AWS Certified Data Analytics"]
    },
    {
        "title": "Cloud Engineer", "slug": "cloud-engineer",
        "description": "Designs, deploys, and secures highly available cloud infrastructure across AWS, Azure, and Google Cloud Platform.",
        "industry": "Cloud Computing", "difficulty": "Intermediate", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science, Networking, or IT",
        "average_salary": "$100,000 - $145,000 / ₹10-20 LPA", "market_demand": "Very High",
        "soft_skills": ["Cost Optimization", "Security Mindset", "Troubleshooting"],
        "recommended_projects": ["Multi-Region High-Availability VPC Architecture on AWS", "Serverless Event-Driven Microservice with Lambda", "Automated Cloud Disaster Recovery Setup"],
        "recommended_certifications": ["AWS Certified Solutions Architect Associate", "Microsoft Certified: Azure Administrator"]
    },
    {
        "title": "DevOps Engineer", "slug": "devops-engineer",
        "description": "Automates continuous integration and deployment (CI/CD), manages Kubernetes container orchestration, and drives site reliability.",
        "industry": "DevOps & Infrastructure", "difficulty": "Advanced", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in CS, IT, or Systems Engineering",
        "average_salary": "$108,000 - $152,000 / ₹11-22 LPA", "market_demand": "Very High",
        "soft_skills": ["Automation First", "Incident Management", "Communication"],
        "recommended_projects": ["Zero-Downtime GitOps Kubernetes Deployment with ArgoCD", "Terraform Infrastructure-as-Code Module Library", "Prometheus & Grafana Observability Mesh"],
        "recommended_certifications": ["Certified Kubernetes Administrator (CKA)", "HashiCorp Certified: Terraform Associate"]
    },
    {
        "title": "Cybersecurity Analyst", "slug": "cybersecurity-analyst",
        "description": "Monitors security events, identifies vulnerabilities, performs threat analysis, and safeguards digital infrastructure.",
        "industry": "Cybersecurity", "difficulty": "Intermediate", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Cybersecurity, Computer Networks, or Computer Science",
        "average_salary": "$95,000 - $135,000 / ₹9-18 LPA", "market_demand": "Very High",
        "soft_skills": ["Threat Hunting", "Analytical Rigor", "Ethics & Confidentiality"],
        "recommended_projects": ["SIEM Security Operations Center (SOC) Lab with Wazuh", "Vulnerability Assessment & Remediation Report", "Automated Phishing Detection Pipeline"],
        "recommended_certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)"]
    },
    {
        "title": "Security Engineer", "slug": "security-engineer",
        "description": "Engineers cryptographic safeguards, builds secure authentication protocols, and performs application penetration testing.",
        "industry": "Cybersecurity & Cryptography", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Bachelor's/Master's in Cybersecurity or Computer Science",
        "average_salary": "$118,000 - $168,000 / ₹14-26 LPA", "market_demand": "Very High",
        "soft_skills": ["Defensive Architecture", "Secure Code Auditing", "Risk Modeling"],
        "recommended_projects": ["Secure OAuth2/OIDC Identity Provider with MFA", "Automated SAST/DAST CI/CD Security Gate", "Zero-Trust Network Access Prototype"],
        "recommended_certifications": ["Offensive Security Certified Professional (OSCP)", "CISSP"]
    },
    {
        "title": "Blockchain Developer", "slug": "blockchain-developer",
        "description": "Develops decentralized applications (dApps), audits Solidity smart contracts, and implements cryptographic consensus mechanisms.",
        "industry": "Web3 & Decentralized Technologies", "difficulty": "Advanced", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science or Software Engineering",
        "average_salary": "$115,000 - $165,000 / ₹13-25 LPA", "market_demand": "Moderate-High",
        "soft_skills": ["Cryptographic Reasoning", "Decentralized Architecture", "Security Auditing"],
        "recommended_projects": ["Decentralized Academic Credential Registry with Hardhat", "ERC-20 / ERC-721 Token Staking Protocol", "Decentralized Autonomous Organization (DAO) Governance Contract"],
        "recommended_certifications": ["Blockchain Council Certified Solidity Developer", "Certified Ethereum Developer"]
    },
    {
        "title": "Computer Vision Engineer", "slug": "computer-vision-engineer",
        "description": "Applies deep learning, image processing, and neural architectures to object detection, segmentation, and document intelligence.",
        "industry": "Artificial Intelligence & Robotics", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Bachelor's/Master's in CS, Electrical, or Mathematics",
        "average_salary": "$122,000 - $170,000 / ₹14-28 LPA", "market_demand": "High",
        "soft_skills": ["Visual Reasoning", "Mathematical Foundations", "Scientific Writing"],
        "recommended_projects": ["Real-Time Object Detection & Tracking with YOLOv8", "OCR Document & Invoice Parsing System", "Medical Image Classification with PyTorch"],
        "recommended_certifications": ["DeepLearning.AI Computer Vision Specialization", "PyTorch for Deep Learning Bootcamp"]
    },
    {
        "title": "NLP Engineer", "slug": "nlp-engineer",
        "description": "Designs language processing models, semantic search engines, sentiment classification, and transformer architectures.",
        "industry": "Artificial Intelligence & Language Tech", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Bachelor's/Master's in Computational Linguistics or CS",
        "average_salary": "$124,000 - $172,000 / ₹15-28 LPA", "market_demand": "Very High",
        "soft_skills": ["Linguistic Analysis", "Statistical NLP", "Creative Problem Solving"],
        "recommended_projects": ["Semantic Search Engine using Dense Embeddings & FAISS", "Multi-Language Text Summarizer with Transformers", "Domain-Specific Named Entity Recognition (NER) Pipeline"],
        "recommended_certifications": ["Hugging Face NLP Course Certification", "DeepLearning.AI Natural Language Processing Specialization"]
    },
    {
        "title": "Database Administrator", "slug": "database-administrator",
        "description": "Maintains mission-critical database instances, orchestrates replication, query tuning, and disaster recovery strategies.",
        "industry": "Enterprise Database Systems", "difficulty": "Intermediate", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science or Information Technology",
        "average_salary": "$88,000 - $125,000 / ₹8-16 LPA", "market_demand": "Steady",
        "soft_skills": ["Data Integrity Focus", "Disaster Readiness", "Patience & Systematic Troubleshooting"],
        "recommended_projects": ["PostgreSQL Streaming Replication & Failover Cluster", "Automated Backup & Point-in-Time Recovery Pipeline", "High-Throughput Index Benchmarking & Optimization"],
        "recommended_certifications": ["PostgreSQL Certified Associate", "Oracle Certified Associate MySQL Database Administrator"]
    },
    {
        "title": "Business Analyst", "slug": "business-analyst",
        "description": "Synthesizes technical capabilities with business goals, defines user requirements, and drives data-backed decision processes.",
        "industry": "Management & Technology Consulting", "difficulty": "Beginner", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Business, IT, Economics, or Engineering",
        "average_salary": "$82,000 - $115,000 / ₹8-15 LPA", "market_demand": "High",
        "soft_skills": ["Requirement Gathering", "Active Listening", "Negotiation & Consensus"],
        "recommended_projects": ["Enterprise Process Flow Re-engineering Specification", "Financial ROI Forecast Dashboard", "Product Feature Gap Analysis Document"],
        "recommended_certifications": ["Certified Business Analysis Professional (CBAP)", "PMI-PBA"]
    },
    {
        "title": "QA Automation Engineer", "slug": "qa-automation-engineer",
        "description": "Automates testing suites across UI, API, and load layers ensuring software reliability, regression safety, and CI/CD validation.",
        "industry": "Quality Assurance & Testing", "difficulty": "Beginner", "entry_level_suitability": True,
        "education_requirement": "Bachelor's in Computer Science or related",
        "average_salary": "$80,000 - $115,000 / ₹7-14 LPA", "market_demand": "High",
        "soft_skills": ["Defect Empathy", "Methodical Testing", "Documentation Clarity"],
        "recommended_projects": ["End-to-End Automated Test Framework with Cypress / Playwright", "API Load & Performance Benchmark Suite using Locust", "Mock Microservice Stubs for Contract Testing"],
        "recommended_certifications": ["ISTQB Certified Tester", "Certified Selenium Professional"]
    },
    {
        "title": "Research Scientist", "slug": "research-scientist",
        "description": "Pioneers novel algorithms, scientific hypotheses, and breakthrough architectures in computer science and artificial intelligence.",
        "industry": "Academic & Industrial Research", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Master's or Ph.D. in Computer Science, Mathematics, or Physics",
        "average_salary": "$135,000 - $190,000 / ₹18-35 LPA", "market_demand": "Selective-High",
        "soft_skills": ["Scientific Method", "Original Thought", "Peer-Review Publishing"],
        "recommended_projects": ["Novel Loss Function Formulation for Neural Convergence", "Formal Verification of Distributed Agreement Protocol", "Empirical Benchmarking of Attention Mechanisms"],
        "recommended_certifications": ["Published Papers in NeurIPS / ICML / CVPR", "Advanced Mathematics Specialization"]
    },
    {
        "title": "Systems Architect", "slug": "systems-architect",
        "description": "Defines high-level software organization, architectural blueprints, integration standards, and technology stack selection across enterprise platforms.",
        "industry": "Enterprise Architecture", "difficulty": "Advanced", "entry_level_suitability": False,
        "education_requirement": "Bachelor's/Master's in CS with 5+ years industry engineering experience",
        "average_salary": "$140,000 - $200,000 / ₹20-40 LPA", "market_demand": "Very High",
        "soft_skills": ["Strategic Vision", "Executive Presentation", "Trade-Off Analysis"],
        "recommended_projects": ["Distributed Event-Driven Core Banking Architecture", "Multi-Tenant Cloud Platform Blueprint", "High-Throughput Global Data Synchronization Topology"],
        "recommended_certifications": ["TOGAF 9 Certified", "AWS Certified Solutions Architect - Professional"]
    }
]

# 100+ Categorized Skills
SKILLS_DATA = [
    # Programming Languages
    ("Python", "Programming", "High-level interpreted language used extensively in AI, data science, and web APIs.", "Intermediate"),
    ("JavaScript", "Programming", "Ubiquitous scripting language powering the interactive modern web.", "Intermediate"),
    ("TypeScript", "Programming", "Typed superset of JavaScript providing static types and enterprise maintainability.", "Intermediate"),
    ("Java", "Programming", "Object-oriented, class-based language dominant in enterprise backend systems.", "Intermediate"),
    ("C++", "Programming", "High-performance compiled language used in systems, game engines, and low-latency engines.", "Advanced"),
    ("C#", "Programming", "Modern component-oriented language powering .NET and game development.", "Intermediate"),
    ("Go", "Programming", "Statically typed compiled language designed for concurrency and cloud microservices.", "Intermediate"),
    ("Rust", "Programming", "Memory-safe systems programming language without garbage collection.", "Advanced"),
    ("SQL", "Programming", "Declarative language for defining and querying relational database management systems.", "Intermediate"),
    ("HTML/CSS", "Programming", "Core structural and stylistic foundational languages of the World Wide Web.", "Beginner"),

    # Databases
    ("PostgreSQL", "Database", "Advanced open-source relational database supporting JSON, ACID, and high concurrency.", "Intermediate"),
    ("MySQL", "Database", "Widely deployed relational database powering popular web applications.", "Intermediate"),
    ("MongoDB", "Database", "Document-oriented NoSQL database storing BSON records with dynamic schemas.", "Intermediate"),
    ("Redis", "Database", "In-memory data structure store used as a distributed cache, message broker, and queue.", "Intermediate"),
    ("Cassandra", "Database", "Highly scalable distributed wide-column NoSQL store for high write workloads.", "Advanced"),
    ("Snowflake", "Database", "Cloud-native elastic data warehouse supporting multi-cluster compute architecture.", "Intermediate"),
    ("Neo4j", "Database", "Native graph database designed for complex connected data and relationship queries.", "Intermediate"),
    ("SQLite", "Database", "Self-contained, serverless, zero-configuration embedded SQL database engine.", "Beginner"),

    # Web & Frameworks
    ("React", "Web Development", "Declarative component-based frontend library for dynamic single-page applications.", "Intermediate"),
    ("Next.js", "Web Development", "React framework supporting server-side rendering, static generation, and edge API routes.", "Intermediate"),
    ("Vue.js", "Web Development", "Progressive frontend framework with an approachable reactive core.", "Intermediate"),
    ("Angular", "Web Development", "Comprehensive enterprise frontend framework featuring TypeScript and dependency injection.", "Advanced"),
    ("FastAPI", "Web Development", "High-performance Python web framework for building modern RESTful APIs with OpenAPI docs.", "Intermediate"),
    ("Node.js", "Web Development", "V8-powered asynchronous JavaScript runtime for scalable network applications.", "Intermediate"),
    ("Express.js", "Web Development", "Fast, unopinionated minimalist web framework for Node.js.", "Intermediate"),
    ("Django", "Web Development", "High-level Python web framework encouraging rapid development and clean design.", "Intermediate"),
    ("Spring Boot", "Web Development", "Production-grade Java framework for building stand-alone microservices.", "Advanced"),
    ("GraphQL", "Web Development", "Query language and runtime for APIs providing clients exact requested data.", "Intermediate"),
    ("Tailwind CSS", "Web Development", "Utility-first CSS framework for building modern, responsive responsive UIs.", "Beginner"),

    # Data Science & Analytics
    ("Pandas", "Data Science", "Python library providing fast, flexible data frames for structured data analysis.", "Intermediate"),
    ("NumPy", "Data Science", "Fundamental package for scientific computing with multi-dimensional arrays.", "Intermediate"),
    ("Data Analysis", "Data Science", "Methodology for inspecting, cleansing, transforming, and modeling data.", "Intermediate"),
    ("Data Visualization", "Data Science", "Visual representation of data via charts, heatmaps, and geospatial plots.", "Beginner"),
    ("Power BI", "Data Science", "Microsoft interactive business intelligence and reporting suite.", "Intermediate"),
    ("Tableau", "Data Science", "Visual analytics platform transforming raw data into shareable dashboards.", "Intermediate"),
    ("Statistics & Probability", "Data Science", "Mathematical theory of distributions, hypothesis testing, and inferential modeling.", "Intermediate"),
    ("Feature Engineering", "Data Science", "Process of using domain knowledge to extract predictors from raw data.", "Intermediate"),

    # Machine Learning & AI
    ("Machine Learning", "AI/ML", "Core algorithms enabling computers to learn patterns from training data.", "Intermediate"),
    ("Deep Learning", "AI/ML", "Multi-layered artificial neural networks capable of learning complex representations.", "Advanced"),
    ("Scikit-Learn", "AI/ML", "Standard Python library for classical machine learning algorithms and preprocessing.", "Intermediate"),
    ("TensorFlow", "AI/ML", "Open-source end-to-end platform for training and deploying deep learning models.", "Advanced"),
    ("PyTorch", "AI/ML", "Dynamic tensor computation and deep learning framework popular in research.", "Advanced"),
    ("NLP", "AI/ML", "Natural language processing techniques for understanding and generating human speech/text.", "Advanced"),
    ("Computer Vision", "AI/ML", "Visual perception algorithms enabling machines to extract information from digital imagery.", "Advanced"),
    ("Generative AI & LLMs", "AI/ML", "Foundation models and transformers for generating text, code, and synthetic media.", "Advanced"),
    ("MLOps", "AI/ML", "Practices for deploying, monitoring, and versioning machine learning models in production.", "Advanced"),
    ("Explainable AI (XAI)", "AI/ML", "Techniques for interpreting and explaining black-box model decisions transparently.", "Intermediate"),

    # Cloud & DevOps
    ("AWS", "Cloud Computing", "Market-leading public cloud platform with 200+ fully featured services.", "Intermediate"),
    ("Azure", "Cloud Computing", "Microsoft enterprise cloud computing platform supporting hybrid architectures.", "Intermediate"),
    ("Google Cloud (GCP)", "Cloud Computing", "Google infrastructure cloud suite known for data analytics and AI tools.", "Intermediate"),
    ("Docker", "DevOps", "Containerization platform packaging software with its complete runtime dependencies.", "Intermediate"),
    ("Kubernetes", "DevOps", "Production-grade container orchestration system automating scaling and management.", "Advanced"),
    ("CI/CD Pipelines", "DevOps", "Automated workflows for continuous code integration, testing, and continuous delivery.", "Intermediate"),
    ("Terraform", "DevOps", "Infrastructure as Code tool for building, changing, and versioning cloud resources.", "Intermediate"),
    ("Linux / Bash", "DevOps", "Open-source operating system kernel and shell scripting for server operations.", "Intermediate"),
    ("Git & GitHub", "DevOps", "Distributed version control system for tracking changes in source code repositories.", "Beginner"),
    ("Monitoring & Prometheus", "DevOps", "Time-series monitoring, metrics collection, and alerting infrastructure.", "Intermediate"),

    # Cybersecurity
    ("Cybersecurity Fundamentals", "Cybersecurity", "Core tenets of confidentiality, integrity, availability, and threat surfaces.", "Beginner"),
    ("Network Security", "Cybersecurity", "Protection of network infrastructure, firewalls, routing security, and IDS/IPS.", "Intermediate"),
    ("Cryptography", "Cybersecurity", "Symmetric, asymmetric ciphers, hashing algorithms, and digital signatures.", "Intermediate"),
    ("Penetration Testing", "Cybersecurity", "Authorized simulated cyberattacks on computer systems to evaluate security.", "Advanced"),
    ("Ethical Hacking", "Cybersecurity", "Application of security techniques to locate weaknesses before malicious hackers.", "Advanced"),
    ("OWASP Top 10", "Cybersecurity", "Standard awareness document representing broad consensus on web application risks.", "Intermediate"),
    ("SIEM & Incident Response", "Cybersecurity", "Security information and event management aggregating log telemetry.", "Intermediate"),
    ("Identity & Access Management", "Cybersecurity", "Framework of policies and technologies ensuring appropriate user access.", "Intermediate"),

    # Big Data
    ("PySpark", "Big Data", "Python API for Apache Spark supporting distributed batch processing and SQL.", "Intermediate"),
    ("Apache Spark", "Big Data", "Unified analytics engine for large-scale distributed data processing.", "Advanced"),
    ("Apache Kafka", "Big Data", "Distributed event store and stream-processing platform for high throughput.", "Advanced"),
    ("Hadoop & HDFS", "Big Data", "Framework allowing distributed storage and processing of large datasets.", "Intermediate"),
    ("Data Warehousing", "Big Data", "Central repository architecture aggregating data from diverse operational sources.", "Intermediate"),
    ("ETL Pipelines", "Big Data", "Extract, Transform, Load workflows ingesting disparate raw data stores.", "Intermediate"),

    # Blockchain
    ("Blockchain Fundamentals", "Blockchain", "Distributed, immutable decentralized ledger architecture.", "Intermediate"),
    ("Solidity", "Blockchain", "Object-oriented, statically typed programming language for Ethereum smart contracts.", "Advanced"),
    ("Smart Contracts", "Blockchain", "Self-executing digital contracts with terms directly written into lines of code.", "Advanced"),
    ("Web3 & Ethers.js", "Blockchain", "Libraries facilitating interaction with Ethereum nodes and decentralized wallets.", "Intermediate"),
    ("Consensus Algorithms", "Blockchain", "Proof of Work, Proof of Stake, and Byzantine fault-tolerant agreement models.", "Advanced"),

    # CS Fundamentals & Soft Skills
    ("Data Structures", "Computer Science", "Arrays, Linked Lists, Trees, Graphs, Hash Tables, and Heaps.", "Intermediate"),
    ("Algorithms", "Computer Science", "Sorting, searching, dynamic programming, and greedy optimization algorithms.", "Intermediate"),
    ("System Design", "Computer Science", "Architectural modeling of scalable, fault-tolerant, distributed platforms.", "Advanced"),
    ("Communication", "Soft Skills", "Clear oral, written, and technical documentation articulation.", "Beginner"),
    ("Critical Thinking", "Soft Skills", "Disciplined analysis and evaluation of evidence to form objective judgment.", "Beginner"),
    ("Problem Solving", "Soft Skills", "Systematic root-cause diagnosis and algorithmic decomposition.", "Beginner"),
    ("Teamwork & Leadership", "Soft Skills", "Collaborative achievement and empathetic mentorship in cross-functional squads.", "Beginner"),
    ("Time Management", "Soft Skills", "Prioritization, milestone roadmapping, and disciplined delivery execution.", "Beginner")
]

# Assessments Definition (16 categories)
ASSESSMENTS_DATA = [
    {"title": "Full Stack Web Development Assessment", "category": "Web Development", "desc": "Evaluates modern frontend, backend API, and database integration skills.", "mins": 20, "pass_pct": 60.0},
    {"title": "Data Structures & Algorithms Challenge", "category": "Computer Science Fundamentals", "desc": "Tests problem-solving, computational complexity, and algorithmic logic.", "mins": 25, "pass_pct": 65.0},
    {"title": "Relational Databases & SQL Mastery", "category": "Database/SQL", "desc": "Measures SQL querying, schema normalization, indexing, and transactions.", "mins": 15, "pass_pct": 60.0},
    {"title": "Data Science & Exploratory Analytics", "category": "Data Analytics", "desc": "Assesses pandas manipulation, statistical inference, and metric visualization.", "mins": 20, "pass_pct": 60.0},
    {"title": "Machine Learning & AI Evaluation", "category": "Machine Learning", "desc": "Tests supervised, unsupervised models, evaluation metrics, and overfitting.", "mins": 20, "pass_pct": 65.0},
    {"title": "Cloud Computing & AWS Architecture", "category": "Cloud Computing", "desc": "Evaluates cloud services, high-availability architecture, and security.", "mins": 15, "pass_pct": 60.0},
    {"title": "DevOps, Containers & CI/CD Pipelines", "category": "DevOps", "desc": "Tests Docker, Kubernetes orchestration, and continuous integration workflows.", "mins": 15, "pass_pct": 60.0},
    {"title": "Cybersecurity & Web Security Defense", "category": "Cybersecurity", "desc": "Assesses threat vectors, OWASP vulnerabilities, cryptography, and defense.", "mins": 20, "pass_pct": 60.0},
    {"title": "Big Data Engineering with Spark", "category": "Big Data", "desc": "Measures distributed computation, resilient datasets, and ETL pipelines.", "mins": 20, "pass_pct": 60.0},
    {"title": "Blockchain, Smart Contracts & Web3", "category": "Blockchain", "desc": "Tests cryptographic ledger concepts, Solidity mechanics, and consensus.", "mins": 15, "pass_pct": 60.0},
    {"title": "Python Core & Advanced Programming", "category": "Programming", "desc": "Tests memory management, generators, decorators, and OOP paradigms in Python.", "mins": 15, "pass_pct": 65.0},
    {"title": "Logical Reasoning & Problem Solving", "category": "Problem Solving", "desc": "Evaluates analytical deduction, algorithmic scenarios, and pattern resolution.", "mins": 15, "pass_pct": 60.0}
]

# Curated Questions (Realistic bank with options & explanations)
QUESTIONS_SAMPLE = [
    # Full Stack / Web
    {
        "cat": "Web Development", "skill": "React", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "What is the primary motivation for utilizing the Virtual DOM in modern libraries like React?",
        "code": None,
        "exp": "The Virtual DOM computes minimal reconciliation diffs in memory, minimizing expensive direct DOM tree reflows.",
        "opts": [
            ("To provide direct access to browser memory for faster execution", False),
            ("To compute declarative UI diffs in memory and batch efficient real DOM updates", True),
            ("To automatically eliminate all network latency during API calls", False),
            ("To compile React code directly into native WebAssembly binaries", False)
        ]
    },
    {
        "cat": "Web Development", "skill": "FastAPI", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "In FastAPI, how does dependency injection (Depends) enhance architectural design?",
        "code": "async def get_current_user(token: str = Depends(oauth2_scheme)): ...",
        "exp": "Depends promotes clean inversion of control, reusable authentication logic, and seamless mock testing.",
        "opts": [
            ("It compiles Python code into C++ at startup", False),
            ("It enables modular, testable, and reusable shared logic across endpoint handlers", True),
            ("It automatically converts relational database queries into GraphQL", False),
            ("It restricts endpoints to only accept synchronous thread pool calls", False)
        ]
    },
    # DSA
    {
        "cat": "Computer Science Fundamentals", "skill": "Data Structures", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "What is the average and worst-case lookup time complexity in a well-balanced Hash Table?",
        "code": None,
        "exp": "Average lookup is O(1) via hashing. In the worst case where all keys hash to the same bucket, it degrades to O(n).",
        "opts": [
            ("Average: O(log n), Worst: O(n)", False),
            ("Average: O(1), Worst: O(n)", True),
            ("Average: O(1), Worst: O(log n)", False),
            ("Average: O(n), Worst: O(n^2)", False)
        ]
    },
    {
        "cat": "Computer Science Fundamentals", "skill": "Algorithms", "diff": "Advanced", "type": "mcq", "marks": 3,
        "text": "Which algorithm is best suited to find the shortest path in a weighted graph containing no negative cycles?",
        "code": None,
        "exp": "Dijkstra's algorithm efficiently computes single-source shortest paths on non-negative weighted graphs in O((V + E) log V).",
        "opts": [
            ("Breadth-First Search (BFS)", False),
            ("Dijkstra's Algorithm", True),
            ("Depth-First Search (DFS)", False),
            ("Kruskal's Algorithm", False)
        ]
    },
    # SQL
    {
        "cat": "Database/SQL", "skill": "SQL", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "What is the key functional difference between WHERE and HAVING clauses in SQL?",
        "code": "SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id HAVING AVG(salary) > 80000;",
        "exp": "WHERE filters individual rows before grouping, while HAVING filters aggregated results produced by GROUP BY.",
        "opts": [
            ("HAVING is only valid in Oracle databases; WHERE is universal", False),
            ("WHERE filters rows prior to aggregation, while HAVING filters post-aggregated grouped data", True),
            ("WHERE performs index scans, while HAVING always forces a full table scan", False),
            ("There is no functional difference; they are interchangeable aliases", False)
        ]
    },
    {
        "cat": "Database/SQL", "skill": "PostgreSQL", "diff": "Advanced", "type": "mcq", "marks": 3,
        "text": "Under the ACID relational model, which isolation level prevents Dirty Reads and Non-Repeatable Reads, but may allow Phantom Reads in ANSI SQL?",
        "code": None,
        "exp": "Repeatable Read guarantees that data read twice in a transaction is identical, though phantom rows might appear under some engines.",
        "opts": [
            ("Read Uncommitted", False),
            ("Read Committed", False),
            ("Repeatable Read", True),
            ("Serializable", False)
        ]
    },
    # Machine Learning
    {
        "cat": "Machine Learning", "skill": "Machine Learning", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "What does a high training accuracy paired with a significantly lower validation accuracy indicate in a supervised classifier?",
        "code": "Train Acc: 99.2% | Validation Acc: 71.4%",
        "exp": "The model has memorized noise in the training set rather than generalizing underlying patterns, indicative of Overfitting.",
        "opts": [
            ("High bias and underfitting", False),
            ("High variance and overfitting", True),
            ("Optimal regularization convergence", False),
            ("Data leakage in the validation split", False)
        ]
    },
    {
        "cat": "Machine Learning", "skill": "Scikit-Learn", "diff": "Advanced", "type": "mcq", "marks": 3,
        "text": "When evaluating an imbalanced fraud detection dataset where fraudulent transactions comprise 0.1% of records, which metric is most meaningful?",
        "code": None,
        "exp": "Accuracy is misleading on imbalanced sets (99.9% trivial accuracy). Precision-Recall AUC or F1-Score captures true positive trade-offs.",
        "opts": [
            ("Raw Classification Accuracy", False),
            ("Precision, Recall, and F1-Score (or PR-AUC)", True),
            ("Mean Squared Error (MSE)", False),
            ("R-squared Coefficient of Determination", False)
        ]
    },
    # Cloud
    {
        "cat": "Cloud Computing", "skill": "AWS", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "Which AWS architectural pattern guarantees high availability across hardware failures within an AWS Region?",
        "code": None,
        "exp": "Deploying redundant instances across multiple Availability Zones (AZs) behind an Application Load Balancer ensures resilience against single datacenter outages.",
        "opts": [
            ("Hosting all servers in a single Availability Zone on the largest instance size", False),
            ("Deploying resources across multiple Availability Zones behind an Elastic Load Balancer", True),
            ("Using simple S3 static file replication without load balancers", False),
            ("Setting CPU burstable credits to unlimited", False)
        ]
    },
    # Cybersecurity
    {
        "cat": "Cybersecurity", "skill": "Cybersecurity Fundamentals", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "How do parameterized queries and prepared statements prevent SQL Injection attacks?",
        "code": "cursor.execute('SELECT * FROM users WHERE email = %s', (user_input,))",
        "exp": "Prepared statements send SQL code structure and data values through separate channels, treating user input strictly as literals rather than executable SQL.",
        "opts": [
            ("By encrypting all database files using AES-256 at rest", False),
            ("By distinguishing user data literals from SQL command syntax, preventing arbitrary code interpretation", True),
            ("By converting all incoming user characters into base64 strings", False),
            ("By restricting database connections strictly to localhost", False)
        ]
    },
    # Big Data
    {
        "cat": "Big Data", "skill": "PySpark", "diff": "Advanced", "type": "mcq", "marks": 3,
        "text": "What does lazy evaluation mean in Apache Spark computation graphs?",
        "code": "df_filtered = df.filter(df.score > 80).select('student_id')",
        "exp": "Transformations are recorded in a directed acyclic graph (DAG) and not executed until an action (like collect, count, save) is called.",
        "opts": [
            ("Spark skips query execution when CPU load exceeds 90%", False),
            ("Transformations build an execution plan (DAG) and are computed only when an action is invoked", True),
            ("Spark evaluates data only during scheduled nighttime batch hours", False),
            ("Memory is never released until the cluster restarts", False)
        ]
    },
    # Blockchain
    {
        "cat": "Blockchain", "skill": "Blockchain Fundamentals", "diff": "Intermediate", "type": "mcq", "marks": 2,
        "text": "Why are academic certificates hashed using SHA-256 before registering their verification IDs on a blockchain?",
        "code": "hash = SHA256(student_id + degree + cgpa + issuer)",
        "exp": "Storing cryptographic hashes guarantees tamper evidence while protecting student privacy and minimizing expensive on-chain storage costs.",
        "opts": [
            ("Blockchains cannot store any alphanumeric strings longer than 32 characters", False),
            ("Hashes ensure tamper evidence while preventing exposure of sensitive student PII on public ledgers", True),
            ("Because SHA-256 automatically sends emails to students upon transaction completion", False),
            ("It is required by Ethereum to convert Solidity into EVM bytecode", False)
        ]
    }
]

# Curated Learning Resources (100% genuine URLs and real platforms)
LEARNING_RESOURCES_DATA = [
    ("Python", "Python Official Documentation & Tutorial", "Documentation", "Python Software Foundation", "https://docs.python.org/3/tutorial/", 15, 4.9, "The authoritative reference and walkthrough for Python language syntax, standard library, and paradigms.", "Beginner"),
    ("Python", "CS50's Introduction to Programming with Python", "Course", "Harvard University / edX", "https://cs50.harvard.edu/python/", 40, 4.9, "Rigorous introduction to computational thinking, algorithms, and practical programming using Python.", "Beginner"),
    ("FastAPI", "FastAPI Official Interactive Tutorial", "Documentation", "Tiangolo / FastAPI", "https://fastapi.tiangolo.com/tutorial/", 12, 4.9, "Comprehensive step-by-step guide to building production-ready asynchronous REST APIs in Python.", "Intermediate"),
    ("React", "React Official Documentation: Quick Start", "Documentation", "Meta Open Source", "https://react.dev/learn", 20, 4.9, "Modern React guidance focusing on functional components, hooks, state management, and rendering cycles.", "Beginner"),
    ("SQL", "SQLBolt - Interactive SQL Lessons", "Tutorial", "SQLBolt", "https://sqlbolt.com/", 8, 4.8, "Interactive in-browser lessons with live query execution for mastering SELECT, JOINs, and aggregates.", "Beginner"),
    ("PostgreSQL", "PostgreSQL Tutorial for Developers", "Tutorial", "Postgres Tutorial", "https://www.postgresqltutorial.com/", 25, 4.8, "Deep dive into PostgreSQL query optimization, transactions, indexes, and full-text search.", "Intermediate"),
    ("Data Structures", "MIT 6.006: Introduction to Algorithms", "Course", "MIT OpenCourseWare", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/", 50, 5.0, "World-class lecture series covering asymptotic analysis, trees, dynamic programming, and graphs.", "Advanced"),
    ("Machine Learning", "Machine Learning Specialization", "Course", "DeepLearning.AI / Coursera", "https://www.coursera.org/specializations/machine-learning-introduction", 60, 4.9, "Andrew Ng's flagship foundational curriculum in supervised learning, neural networks, and ML best practices.", "Intermediate"),
    ("Deep Learning", "Practical Deep Learning for Coders", "Course", "fast.ai", "https://course.fast.ai/", 45, 4.9, "Top-down, hands-on deep learning curriculum using PyTorch and modern transformer architectures.", "Advanced"),
    ("Docker", "Docker Official Getting Started Guide", "Tutorial", "Docker Docs", "https://docs.docker.com/get-started/", 10, 4.8, "Learn container fundamentals, multi-stage Dockerfiles, Docker Compose, and image optimization.", "Beginner"),
    ("Kubernetes", "Kubernetes The Hard Way", "Tutorial", "Kelsey Hightower", "https://github.com/kelseyhightower/kubernetes-the-hard-way", 30, 4.9, "Bootstrap Kubernetes clusters from scratch to understand every component, cert, and network routing rule.", "Advanced"),
    ("AWS", "AWS Skill Builder: Cloud Practitioner Essentials", "Course", "Amazon Web Services", "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials", 12, 4.8, "Official foundational curriculum covering compute, storage, databases, networking, and cloud security.", "Beginner"),
    ("Cybersecurity Fundamentals", "Google Cybersecurity Certificate", "Certification", "Google / Coursera", "https://www.coursera.org/professional-certificates/google-cybersecurity", 80, 4.8, "Hands-on preparation for entry-level cybersecurity roles covering SIEM, Python automation, and networks.", "Intermediate"),
    ("Blockchain Fundamentals", "CryptoZombies - Learn Solidity & Ethereum", "Tutorial", "Loom Network", "https://cryptozombies.io/", 15, 4.8, "Gamified interactive curriculum teaching Solidity smart contracts, ERC-721, and Web3 development.", "Beginner"),
    ("PySpark", "Apache Spark Official Quick Start with Python", "Documentation", "Apache Software Foundation", "https://spark.apache.org/docs/latest/api/python/getting_started/index.html", 15, 4.7, "Learn distributed DataFrames, resilient distributed datasets (RDDs), and streaming queries with PySpark.", "Intermediate")
]

# Gamification Badges
ACHIEVEMENTS_DATA = [
    {"code": "ASSESSMENT_STARTER", "title": "Assessment Starter", "desc": "Completed your first adaptive skill assessment.", "badge_icon": "Award", "cat": "Assessment", "points": 50},
    {"code": "HIGH_SCORER", "title": "High Scorer", "desc": "Demonstrated top-tier mastery with 80%+ accuracy on an assessment.", "badge_icon": "Zap", "cat": "Assessment", "points": 100},
    {"code": "PYTHON_PRACTITIONER", "title": "Python Practitioner", "desc": "Reached Advanced proficiency level in Python programming.", "badge_icon": "Code", "cat": "Skill", "points": 75},
    {"code": "ROADMAP_FINISHER", "title": "Roadmap Finisher", "desc": "Completed all personalized learning modules for a target career.", "badge_icon": "CheckCircle", "cat": "Roadmap", "points": 150},
    {"code": "CREDENTIAL_HOLDER", "title": "On-Chain Verified", "desc": "Generated and anchored your first tamper-evident credential on the blockchain.", "badge_icon": "ShieldCheck", "cat": "Blockchain", "points": 120}
]

def seed_database():
    """Initializes schema and seeds realistic data."""
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Achievements
        for ach in ACHIEVEMENTS_DATA:
            if not db.query(Achievement).filter(Achievement.code == ach["code"]).first():
                db.add(Achievement(
                    code=ach["code"],
                    title=ach["title"],
                    description=ach["desc"],
                    badge_icon=ach["badge_icon"],
                    category=ach["cat"],
                    points=ach["points"]
                ))
        db.commit()

        # 2. Seed Skills
        skill_obj_map = {}
        for sname, scat, sdesc, sdiff in SKILLS_DATA:
            existing = db.query(Skill).filter(Skill.name == sname).first()
            if not existing:
                existing = Skill(name=sname, category=scat, description=sdesc, difficulty_level=sdiff)
                db.add(existing)
                db.commit()
                db.refresh(existing)
            skill_obj_map[sname] = existing

        # 3. Seed Career Roles & Skill Requirements
        for crole in CAREER_ROLES_DATA:
            existing_c = db.query(CareerRole).filter(CareerRole.slug == crole["slug"]).first()
            if not existing_c:
                existing_c = CareerRole(
                    title=crole["title"],
                    slug=crole["slug"],
                    description=crole["description"],
                    industry=crole["industry"],
                    difficulty=crole["difficulty"],
                    entry_level_suitability=crole["entry_level_suitability"],
                    education_requirement=crole["education_requirement"],
                    average_salary=crole["average_salary"],
                    market_demand=crole["market_demand"],
                    soft_skills=crole["soft_skills"],
                    recommended_projects=crole["recommended_projects"],
                    recommended_certifications=crole["recommended_certifications"]
                )
                db.add(existing_c)
                db.commit()
                db.refresh(existing_c)

                # Link primary skills
                core_skills = ["Python", "SQL", "Data Structures", "Algorithms", "System Design"]
                if "Web" in crole["industry"]: core_skills += ["React", "FastAPI", "JavaScript", "HTML/CSS"]
                if "Data" in crole["industry"]: core_skills += ["Pandas", "Machine Learning", "Data Analysis", "Statistics & Probability"]
                if "Cloud" in crole["industry"]: core_skills += ["AWS", "Docker", "Kubernetes", "Linux / Bash"]
                if "Security" in crole["industry"]: core_skills += ["Cybersecurity Fundamentals", "Network Security", "Cryptography"]
                if "Blockchain" in crole["industry"]: core_skills += ["Blockchain Fundamentals", "Solidity", "Smart Contracts"]

                for s_name in set(core_skills):
                    if s_name in skill_obj_map:
                        db.add(CareerSkill(
                            career_id=existing_c.id,
                            skill_id=skill_obj_map[s_name].id,
                            required_level=75.0,
                            is_mandatory=True,
                            importance_weight=1.2
                        ))
                db.commit()

        # 4. Seed Assessments & Questions
        for a_data in ASSESSMENTS_DATA:
            existing_a = db.query(Assessment).filter(Assessment.title == a_data["title"]).first()
            if not existing_a:
                existing_a = Assessment(
                    title=a_data["title"],
                    category=a_data["category"],
                    description=a_data["desc"],
                    time_limit_minutes=a_data["mins"],
                    passing_percentage=a_data["pass_pct"],
                    total_questions=10
                )
                db.add(existing_a)
                db.commit()
                db.refresh(existing_a)

        # Seed Questions to assessments
        for q_item in QUESTIONS_SAMPLE:
            # Find assessment matching category
            ass = db.query(Assessment).filter(Assessment.category == q_item["cat"]).first()
            if ass and not db.query(Question).filter(Question.question_text == q_item["text"]).first():
                skill_ref = skill_obj_map.get(q_item["skill"])
                q_db = Question(
                    assessment_id=ass.id,
                    skill_id=skill_ref.id if skill_ref else None,
                    question_text=q_item["text"],
                    question_type=q_item["type"],
                    difficulty=q_item["diff"],
                    marks=q_item["marks"],
                    explanation=q_item["exp"],
                    code_snippet=q_item.get("code")
                )
                db.add(q_db)
                db.commit()
                db.refresh(q_db)

                for opt_text, is_corr in q_item["opts"]:
                    db.add(QuestionOption(
                        question_id=q_db.id,
                        option_text=opt_text,
                        is_correct=is_corr
                    ))
                db.commit()

        # 5. Seed Curated Learning Resources
        for r_skill, r_title, r_type, r_prov, r_url, r_hrs, r_rating, r_desc, r_diff in LEARNING_RESOURCES_DATA:
            if not db.query(LearningResource).filter(LearningResource.title == r_title).first():
                db.add(LearningResource(
                    skill_name=r_skill,
                    title=r_title,
                    resource_type=r_type,
                    provider=r_prov,
                    url=r_url,
                    estimated_hours=r_hrs,
                    rating=r_rating,
                    description=r_desc,
                    difficulty=r_diff
                ))
        db.commit()

        # 6. Seed Demo Users (Student, Admin, Counselor)
        demo_password_hash = get_password_hash("Demo@123456")

        # Admin
        if not db.query(User).filter(User.email == "admin@demo.com").first():
            admin_user = User(
                email="admin@demo.com",
                hashed_password=demo_password_hash,
                full_name="Platform Administrator",
                role="admin",
                is_active=True
            )
            db.add(admin_user)

        # Counselor
        if not db.query(User).filter(User.email == "counselor@demo.com").first():
            counselor_user = User(
                email="counselor@demo.com",
                hashed_password=demo_password_hash,
                full_name="Dr. Elena Vance (Lead Counselor)",
                role="counselor",
                is_active=True
            )
            db.add(counselor_user)

        # Student
        student_user = db.query(User).filter(User.email == "student@demo.com").first()
        if not student_user:
            student_user = User(
                email="student@demo.com",
                hashed_password=demo_password_hash,
                full_name="Alex Chen",
                role="student",
                is_active=True
            )
            db.add(student_user)
            db.commit()
            db.refresh(student_user)

            # Profile
            stud_profile = StudentProfile(
                user_id=student_user.id,
                phone="+1 (555) 234-5678",
                date_of_birth="2003-05-14",
                location="San Francisco, CA",
                desired_job_role="Data Scientist",
                preferred_industry="Artificial Intelligence",
                preferred_location="Hybrid / Remote",
                higher_studies_preference="Not immediately (Focus on Industry)",
                job_preference="Full-Time Tech Role",
                profile_completeness=85.0,
                points=320,
                streak_days=5
            )
            db.add(stud_profile)
            db.commit()
            db.refresh(stud_profile)

            # Academic
            db.add(AcademicRecord(
                profile_id=stud_profile.id,
                college="Institute of Technology & Computer Science",
                degree="Bachelor of Technology (B.Tech)",
                branch="Computer Science & Engineering",
                year_of_study="4th Year (Senior)",
                cgpa=8.75,
                graduation_year=2026,
                academic_subjects=["Data Structures", "Database Management", "Machine Learning", "Cloud Systems"]
            ))

            # Initial Verified Skills
            skills_initial = [
                ("Python", 84.0, "Advanced"),
                ("SQL", 76.0, "Intermediate"),
                ("Machine Learning", 65.0, "Intermediate"),
                ("Data Structures", 78.0, "Advanced"),
                ("React", 60.0, "Intermediate"),
                ("Docker", 45.0, "Basic"),
                ("Cybersecurity Fundamentals", 40.0, "Basic")
            ]
            for sname, sscore, slevel in skills_initial:
                if sname in skill_obj_map:
                    db.add(StudentSkill(
                        profile_id=stud_profile.id,
                        skill_id=skill_obj_map[sname].id,
                        proficiency_score=sscore,
                        proficiency_level=slevel,
                        evidence_source={"assessment_score": sscore, "self_rating": 4}
                    ))

            # Soft Skills & Interests
            for ssk, srate in [("Communication", 4), ("Problem Solving", 5), ("Critical Thinking", 4), ("Teamwork & Leadership", 4)]:
                db.add(StudentSoftSkill(profile_id=stud_profile.id, skill_name=ssk, rating=srate))

            for intr, ipref in [("AI/ML", 5), ("Data Science", 5), ("Cloud Computing", 4), ("Software Development", 4)]:
                db.add(StudentInterest(profile_id=stud_profile.id, interest_name=intr, preference_level=ipref))

            # Projects
            db.add(StudentProject(
                profile_id=stud_profile.id,
                title="AI Career Recommendation & Skill Intelligence Engine",
                description="Built a full-stack platform utilizing scikit-learn classifiers, FastAPI backend, and React dashboard for predictive career guidance.",
                technologies=["Python", "FastAPI", "React", "scikit-learn", "PostgreSQL"],
                role="Full Stack & ML Architect",
                duration="3 Months",
                project_url="https://github.com/demo/career-intelligence"
            ))
            db.add(StudentProject(
                profile_id=stud_profile.id,
                title="Distributed Transaction Analytics Stream",
                description="Implemented high-throughput data aggregation using PySpark and PostgreSQL indexing.",
                technologies=["Python", "PySpark", "SQL", "Docker"],
                role="Data Engineer",
                duration="2 Months"
            ))

            # Certifications
            db.add(StudentCertification(
                profile_id=stud_profile.id,
                name="Python for Data Science and Machine Learning Bootcamp",
                issuer="Udemy / Pierian Data",
                issue_date="2025-11-20",
                credential_id="UC-89412-DS-2025"
            ))

            # Award Initial Badges
            ach_starter = db.query(Achievement).filter(Achievement.code == "ASSESSMENT_STARTER").first()
            if ach_starter:
                db.add(StudentAchievement(profile_id=stud_profile.id, achievement_id=ach_starter.id))

            # Seed a verified blockchain credential
            cred_id = "CRED-2026-EDU-8492"
            tx_info = blockchain_ledger.add_credential(
                credential_id=cred_id,
                student_id=stud_profile.id,
                title="Verified Skill Assessment: Python & Machine Learning",
                credential_type="Skill Assessment Certificate",
                metadata={"score": 88.0, "date": "2026-03-15", "grade": "Distinction"}
            )
            db.add(Credential(
                credential_id=cred_id,
                profile_id=stud_profile.id,
                title="Verified Skill Assessment: Python & Machine Learning",
                credential_type="Skill Assessment Certificate",
                credential_hash=tx_info["credential_hash"],
                issuer_address=tx_info["issuer"],
                blockchain_tx_hash=tx_info["tx_hash"],
                block_number=tx_info["block_number"],
                verification_status="VERIFIED",
                metadata_json={"score": 88.0, "grade": "Distinction"}
            ))

            # Welcome notification
            db.add(Notification(
                user_id=student_user.id,
                title="Welcome to EduCareer AI!",
                message="Your profile is initialized. Take an adaptive assessment to generate your personalized career intelligence roadmap.",
                notification_type="info"
            ))

            # Initial Audit Log
            db.add(AuditLog(
                user_id=student_user.id,
                action="USER_REGISTRATION",
                status="SUCCESS",
                ip_address="127.0.0.1",
                details={"message": "Demo student account initialized"}
            ))

        db.commit()
        print("Database initialized and successfully seeded with all realistic data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
