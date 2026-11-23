import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.models import Assessment, Question, QuestionOption, Skill, CareerRole

# Comprehensive bank of 23 Assessments with 6-8 Questions each (150+ Total Questions)
ASSESSMENTS_AND_QUESTIONS = [
    {
        "title": "Full Stack Developer Assessment",
        "category": "Web Development",
        "role_slug": "full-stack-developer",
        "desc": "Evaluates client-side UI frameworks, state management, asynchronous backend APIs, database integration, and web security.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "React", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary motivation for utilizing the Virtual DOM in modern libraries like React?",
                "code": None,
                "exp": "The Virtual DOM computes declarative diffs in memory, minimizing expensive real browser layout reflows and repaints.",
                "opts": [
                    ("To bypass browser security sandboxing for raw hardware access", False),
                    ("To compute declarative UI diffs in memory and batch efficient real DOM updates", True),
                    ("To completely eliminate client-to-server API network latency", False),
                    ("To compile JSX directly into machine bytecode ahead of time", False)
                ]
            },
            {
                "skill": "React", "diff": "Intermediate", "marks": 2,
                "text": "In React 18, what is the purpose of the useEffect hook cleanup function?",
                "code": "useEffect(() => {\n  const sub = eventEmitter.subscribe(handler);\n  return () => sub.unsubscribe();\n}, []);",
                "exp": "The cleanup function cancels subscriptions, timers, or aborts pending fetch requests before unmounting or re-running effects.",
                "opts": [
                    ("To free memory from JavaScript V8 heap garbage collection manually", False),
                    ("To tear down subscriptions, intervals, and observers to prevent memory leaks", True),
                    ("To force immediate synchronous re-rendering of child components", False),
                    ("To save component state directly into browser LocalStorage", False)
                ]
            },
            {
                "skill": "FastAPI", "diff": "Intermediate", "marks": 2,
                "text": "How does FastAPI achieve high performance when handling concurrent asynchronous I/O requests?",
                "code": "async def fetch_user_data(user_id: int): ...",
                "exp": "FastAPI leverages Python's asyncio event loop via Starlette and Uvicorn ASGI server to handle non-blocking concurrent I/O.",
                "opts": [
                    ("By spawning a separate operating system process for every incoming HTTP request", False),
                    ("By utilizing Python asyncio event loops on an ASGI server (Uvicorn) without blocking threads", True),
                    ("By transpiling all Python route functions into native AssemblyScript", False),
                    ("By running all requests synchronously in a single-threaded queue", False)
                ]
            },
            {
                "skill": "SQL", "diff": "Intermediate", "marks": 2,
                "text": "Which HTTP status code should be returned after successfully creating a resource via a POST endpoint?",
                "code": None,
                "exp": "HTTP 201 Created indicates that the request has succeeded and led to the creation of a new resource.",
                "opts": [
                    ("200 OK", False),
                    ("201 Created", True),
                    ("204 No Content", False),
                    ("302 Found", False)
                ]
            },
            {
                "skill": "JavaScript", "diff": "Advanced", "marks": 3,
                "text": "In JavaScript, what is the output order of the following event loop execution snippet?",
                "code": "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
                "exp": "Synchronous code runs first ('1', '4'), then microtasks (Promise callback '3'), then macrotasks (setTimeout '2'). Order: 1, 4, 3, 2.",
                "opts": [
                    ("1, 2, 3, 4", False),
                    ("1, 4, 3, 2", True),
                    ("1, 4, 2, 3", False),
                    ("1, 3, 4, 2", False)
                ]
            },
            {
                "skill": "HTML/CSS", "diff": "Beginner", "marks": 1,
                "text": "In modern CSS Flexbox, which property aligns flex items along the cross axis?",
                "code": None,
                "exp": "align-items aligns items along the cross axis, while justify-content aligns items along the main axis.",
                "opts": [
                    ("justify-content", False),
                    ("align-items", True),
                    ("flex-direction", False),
                    ("flex-wrap", False)
                ]
            }
        ]
    },
    {
        "title": "Software Developer & Architecture Assessment",
        "category": "Software Engineering",
        "role_slug": "software-developer",
        "desc": "Tests Object-Oriented design patterns, SOLID principles, concurrency, memory management, and algorithmic complexity.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "System Design", "diff": "Intermediate", "marks": 2,
                "text": "Which SOLID principle is violated if a derived class overrides a base class method in a way that breaks client expectations?",
                "code": None,
                "exp": "The Liskov Substitution Principle (LSP) requires subclasses to be substitutable for their base types without altering correctness.",
                "opts": [
                    ("Single Responsibility Principle", False),
                    ("Liskov Substitution Principle", True),
                    ("Interface Segregation Principle", False),
                    ("Dependency Inversion Principle", False)
                ]
            },
            {
                "skill": "Algorithms", "diff": "Advanced", "marks": 3,
                "text": "What is the time complexity of building a Binary Heap from an unordered array of N elements?",
                "code": None,
                "exp": "Bottom-up heap construction (heapify) runs in O(N) linear time, not O(N log N).",
                "opts": [
                    ("O(N log N)", False),
                    ("O(N)", True),
                    ("O(N^2)", False),
                    ("O(log N)", False)
                ]
            },
            {
                "skill": "Python", "diff": "Intermediate", "marks": 2,
                "text": "What design pattern is most suitable when an object needs to notify multiple dependent objects about state changes automatically?",
                "code": None,
                "exp": "The Observer pattern defines a one-to-many dependency between objects so that when one changes state, dependents are notified.",
                "opts": [
                    ("Singleton Pattern", False),
                    ("Observer Pattern", True),
                    ("Factory Method Pattern", False),
                    ("Decorator Pattern", False)
                ]
            },
            {
                "skill": "Data Structures", "diff": "Intermediate", "marks": 2,
                "text": "Which data structure is optimal for implementing an LRU (Least Recently Used) cache with O(1) get and put operations?",
                "code": None,
                "exp": "A Hash Map combined with a Doubly Linked List allows O(1) key lookup and O(1) node relocation upon access.",
                "opts": [
                    ("Single Array with Binary Search", False),
                    ("Hash Map combined with Doubly Linked List", True),
                    ("Red-Black Binary Search Tree", False),
                    ("Circular Queue", False)
                ]
            },
            {
                "skill": "System Design", "diff": "Advanced", "marks": 3,
                "text": "In distributed architectures, what does the CAP theorem state regarding network partitions?",
                "code": None,
                "exp": "When a network partition (P) occurs, a distributed system must choose between Consistency (C) and Availability (A).",
                "opts": [
                    ("A system can guarantee Consistency, Availability, and Partition Tolerance simultaneously", False),
                    ("In the presence of a network partition, a system must trade off Consistency or Availability", True),
                    ("Partition tolerance is only required in single-datacenter relational databases", False),
                    ("Availability is strictly guaranteed only when Consistency is 100%", False)
                ]
            },
            {
                "skill": "Git & GitHub", "diff": "Beginner", "marks": 1,
                "text": "What is the primary difference between 'git merge' and 'git rebase'?",
                "code": None,
                "exp": "git merge preserves commit history with a merge commit, while rebase rewrites project history by moving base commits.",
                "opts": [
                    ("git merge deletes remote branches, while git rebase downloads them", False),
                    ("git merge creates a merge commit preserving branches; rebase replays commits linearly on top of another branch", True),
                    ("git rebase cannot resolve merge conflicts", False),
                    ("git merge only works on local repositories", False)
                ]
            }
        ]
    },
    {
        "title": "Data Scientist & Advanced Analytics Assessment",
        "category": "Data Science",
        "role_slug": "data-scientist",
        "desc": "Evaluates exploratory data analysis, hypothesis testing, feature engineering, regression, clustering, and model validation.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Pandas", "diff": "Intermediate", "marks": 2,
                "text": "In Pandas, which method efficiently imputes missing NaN numerical values with the column median without copying the DataFrame?",
                "code": "df['age'] = df['age'].fillna(df['age'].median())",
                "exp": "fillna() replaces missing NaN values with specified aggregates like mean or median.",
                "opts": [
                    ("df.dropna()", False),
                    ("df['age'].fillna(df['age'].median())", True),
                    ("df.replace_nan()", False),
                    ("df.interpolate_median()", False)
                ]
            },
            {
                "skill": "Statistics & Probability", "diff": "Intermediate", "marks": 2,
                "text": "What does a p-value less than the significance level (alpha = 0.05) indicate in hypothesis testing?",
                "code": None,
                "exp": "A p-value < 0.05 provides statistically significant evidence to reject the null hypothesis in favor of the alternative.",
                "opts": [
                    ("The null hypothesis is definitively proven true", False),
                    ("We reject the null hypothesis because the observed effect is unlikely due to random chance", True),
                    ("The sample size is too small to draw any inference", False),
                    ("The test has zero probability of Type I error", False)
                ]
            },
            {
                "skill": "Machine Learning", "diff": "Advanced", "marks": 3,
                "text": "How does L1 regularization (Lasso) differ from L2 regularization (Ridge) in linear models?",
                "code": "L1: + lambda * sum(|w_i|)  vs  L2: + lambda * sum(w_i^2)",
                "exp": "L1 regularization drives regression coefficients to absolute zero, performing automatic feature selection.",
                "opts": [
                    ("L2 drives weights to exactly zero, whereas L1 keeps all weights non-zero", False),
                    ("L1 enforces sparsity by driving less important feature weights to exactly zero", True),
                    ("L1 can only be applied to classification problems", False),
                    ("L2 does not prevent overfitting in high-dimensional datasets", False)
                ]
            },
            {
                "skill": "Feature Engineering", "diff": "Intermediate", "marks": 2,
                "text": "Why should categorical features with high cardinality (e.g. 5,000 postal codes) generally NOT be One-Hot Encoded?",
                "code": None,
                "exp": "One-Hot Encoding high-cardinality features creates massive, sparse matrices leading to the curse of dimensionality and memory exhaustion.",
                "opts": [
                    ("One-hot encoding converts numbers into strings", False),
                    ("It causes extreme dimensional explosion and sparsity, increasing computational cost and risk of overfitting", True),
                    ("Scikit-learn forbids one-hot encoding on strings", False),
                    ("It destroys all variance in the target variable", False)
                ]
            },
            {
                "skill": "Data Visualization", "diff": "Beginner", "marks": 1,
                "text": "Which visualization plot is most suitable to examine the distribution, median, and outliers of a numerical variable?",
                "code": None,
                "exp": "A Box Plot (box-and-whisker) depicts the median, interquartile range (IQR), and outliers effectively.",
                "opts": [
                    ("Pie Chart", False),
                    ("Box Plot (Box-and-Whisker)", True),
                    ("Scatter Plot", False),
                    ("Treemap", False)
                ]
            },
            {
                "skill": "Machine Learning", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary advantage of K-Fold Cross Validation over a single Train/Test split?",
                "code": None,
                "exp": "K-Fold cross validation reduces variance in metric estimates by training and validating across multiple subsets of the data.",
                "opts": [
                    ("It guarantees 100% test accuracy on unseen data", False),
                    ("It provides a more reliable, lower-variance estimate of model generalization performance", True),
                    ("It speeds up model training time by a factor of K", False),
                    ("It eliminates the need for hyperparameter tuning", False)
                ]
            }
        ]
    },
    {
        "title": "Machine Learning Engineer Assessment",
        "category": "Machine Learning",
        "role_slug": "machine-learning-engineer",
        "desc": "Covers supervised/unsupervised algorithms, gradient descent optimization, loss functions, MLOps, model quantization, and serving.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Machine Learning", "diff": "Intermediate", "marks": 2,
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
                "skill": "Scikit-Learn", "diff": "Advanced", "marks": 3,
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
            {
                "skill": "MLOps", "diff": "Intermediate", "marks": 2,
                "text": "In production machine learning systems, what is 'Data Drift'?",
                "code": None,
                "exp": "Data drift refers to changes in the statistical distribution of input features over time, degrading model accuracy.",
                "opts": [
                    ("A bug where training data is deleted from the disk", False),
                    ("A shift in the statistical distribution of inference input features compared to training data", True),
                    ("When weights exceed 32-bit floating point precision limits", False),
                    ("Switching database drivers from PostgreSQL to MySQL", False)
                ]
            },
            {
                "skill": "Deep Learning", "diff": "Advanced", "marks": 3,
                "text": "Why do deep neural networks frequently utilize Batch Normalization layers during training?",
                "code": None,
                "exp": "Batch Normalization stabilizes internal covariate shift, allowing higher learning rates and acting as a mild regularizer.",
                "opts": [
                    ("To compress the model weights into 8-bit integers", False),
                    ("To normalize layer inputs across mini-batches, stabilizing training and accelerating convergence", True),
                    ("To replace backpropagation with genetic algorithms", False),
                    ("To prevent the model from accepting multi-dimensional tensors", False)
                ]
            },
            {
                "skill": "Machine Learning", "diff": "Beginner", "marks": 1,
                "text": "What type of machine learning problem is solved by the K-Means algorithm?",
                "code": None,
                "exp": "K-Means is an unsupervised clustering algorithm that partitions data into K groups based on feature similarity.",
                "opts": [
                    ("Supervised Binary Classification", False),
                    ("Unsupervised Clustering", True),
                    ("Continuous Value Regression", False),
                    ("Reinforcement Learning Policy Optimization", False)
                ]
            },
            {
                "skill": "MLOps", "diff": "Intermediate", "marks": 2,
                "text": "Which tool is standard for logging ML experiments, tracking parameters, metrics, and registering model artifacts?",
                "code": None,
                "exp": "MLflow is an open-source platform for managing the end-to-end machine learning lifecycle including tracking and model registry.",
                "opts": [
                    ("Postman", False),
                    ("MLflow", True),
                    ("Nginx", False),
                    ("Redis", False)
                ]
            }
        ]
    },
    {
        "title": "AI Engineer & Generative AI Assessment",
        "category": "Artificial Intelligence",
        "role_slug": "ai-engineer",
        "desc": "Tests Large Language Models (LLMs), prompt engineering, Retrieval-Augmented Generation (RAG), vector embeddings, and multi-agent workflows.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Generative AI & LLMs", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary role of a Vector Database in a Retrieval-Augmented Generation (RAG) architecture?",
                "code": None,
                "exp": "Vector databases index high-dimensional embeddings for fast approximate nearest neighbor (ANN) semantic document search.",
                "opts": [
                    ("To store relational SQL tables with strict foreign keys", False),
                    ("To perform fast semantic similarity searches using dense vector embeddings of documents", True),
                    ("To compile neural networks into WebAssembly", False),
                    ("To eliminate the need for GPU compute in LLMs", False)
                ]
            },
            {
                "skill": "Generative AI & LLMs", "diff": "Advanced", "marks": 3,
                "text": "What does Parameter-Efficient Fine-Tuning (PEFT) using LoRA (Low-Rank Adaptation) accomplish?",
                "code": None,
                "exp": "LoRA freezes the pre-trained model weights and injects trainable rank decomposition matrices into transformer layers, drastically reducing trainable parameters.",
                "opts": [
                    ("It converts text prompts into binary regex expressions", False),
                    ("It freezes base model weights and trains low-rank decomposition matrices, saving GPU VRAM", True),
                    ("It removes all attention heads from the transformer model", False),
                    ("It replaces neural tokens with dictionary lookups", False)
                ]
            },
            {
                "skill": "Generative AI & LLMs", "diff": "Intermediate", "marks": 2,
                "text": "Which metric evaluates semantic similarity between two embedding vectors in cosine space?",
                "code": "similarity = dot(A, B) / (norm(A) * norm(B))",
                "exp": "Cosine similarity measures the cosine of the angle between two non-zero vectors in inner product space.",
                "opts": [
                    ("Euclidean L1 Manhattan Distance", False),
                    ("Cosine Similarity", True),
                    ("Hamming Distance", False),
                    ("Jaccard Index on strings", False)
                ]
            },
            {
                "skill": "Generative AI & LLMs", "diff": "Beginner", "marks": 1,
                "text": "In Prompt Engineering, what is 'Few-Shot Prompting'?",
                "code": None,
                "exp": "Few-shot prompting provides the model with a few exemplar input-output pairs in the prompt context to guide target behavior.",
                "opts": [
                    ("Retraining the entire model weights on five GPUs", False),
                    ("Providing a few demonstration input-output examples in the prompt to condition the model's response", True),
                    ("Generating only five tokens per inference request", False),
                    ("Running the prompt with five different temperatures simultaneously", False)
                ]
            },
            {
                "skill": "Generative AI & LLMs", "diff": "Advanced", "marks": 3,
                "text": "In transformer self-attention mechanisms, why are query, key, and value vectors multiplied by 1 / sqrt(d_k)?",
                "code": "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V",
                "exp": "Scaling by 1/sqrt(d_k) prevents the dot products from growing excessively large in high dimensions, preventing vanishing softmax gradients.",
                "opts": [
                    ("To compress the sequence length by half", False),
                    ("To scale dot products down so softmax does not saturate with vanishingly small gradients", True),
                    ("To enforce sparsity in cross-entropy loss", False),
                    ("To convert multi-head attention into convolutional filters", False)
                ]
            },
            {
                "skill": "Generative AI & LLMs", "diff": "Intermediate", "marks": 2,
                "text": "What is 'Hallucination' in Large Language Models?",
                "code": None,
                "exp": "Hallucination refers to generating syntactically convincing, confident statements that are factually inaccurate or ungrounded.",
                "opts": [
                    ("A hardware memory overflow exception during token generation", False),
                    ("The generation of factually incorrect or ungrounded assertions presented with high confidence", True),
                    ("When a model generates foreign language words unexpectedly", False),
                    ("When temperature is set to exactly 0.0", False)
                ]
            }
        ]
    },
    {
        "title": "Data Analyst & SQL Mastery Assessment",
        "category": "Data Analytics",
        "role_slug": "data-analyst",
        "desc": "Evaluates relational SQL queries, window functions, aggregation, cohort retention analysis, and business dashboard metrics.",
        "mins": 20,
        "pass_pct": 60.0,
        "questions": [
            {
                "skill": "SQL", "diff": "Intermediate", "marks": 2,
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
                "skill": "SQL", "diff": "Advanced", "marks": 3,
                "text": "Which SQL Window function assigns sequential integers starting from 1 to each row within a partition, without skipping ranks for ties?",
                "code": "SELECT name, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) FROM staff;",
                "exp": "DENSE_RANK() computes sequential rank integers without gaps between rank values upon tie matches.",
                "opts": [
                    ("RANK()", False),
                    ("DENSE_RANK()", True),
                    ("ROW_NUMBER()", False),
                    ("NTILE()", False)
                ]
            },
            {
                "skill": "Data Analysis", "diff": "Intermediate", "marks": 2,
                "text": "In cohort analysis for customer retention, how is the monthly retention rate calculated?",
                "code": None,
                "exp": "Retention Rate = (Active users at month end who started in that cohort / Total initial cohort users) * 100.",
                "opts": [
                    ("Total revenue divided by total marketing expenditure", False),
                    ("Active users from the original cohort in month N divided by total users who joined in month 0", True),
                    ("Total new signups minus churned users in a single week", False),
                    ("Lifetime value multiplied by churn percentage", False)
                ]
            },
            {
                "skill": "SQL", "diff": "Beginner", "marks": 1,
                "text": "Which SQL JOIN returns all rows from the left table, and the matched rows from the right table (with NULLs for unmatched rows)?",
                "code": None,
                "exp": "A LEFT JOIN returns all records from the left table, and matched values from the right table.",
                "opts": [
                    ("INNER JOIN", False),
                    ("LEFT JOIN (or LEFT OUTER JOIN)", True),
                    ("FULL JOIN", False),
                    ("CROSS JOIN", False)
                ]
            },
            {
                "skill": "Power BI", "diff": "Intermediate", "marks": 2,
                "text": "In Power BI and DAX, what is the functional difference between a Calculated Column and a Measure?",
                "code": None,
                "exp": "Calculated Columns evaluate row-by-row and consume in-memory storage; Measures evaluate on-the-fly based on report filter context.",
                "opts": [
                    ("Measures are only used for text formatting, columns for math", False),
                    ("Calculated columns store values row-by-row in RAM; measures calculate dynamically based on active filter context", True),
                    ("Measures cannot be used in charts", False),
                    ("Calculated columns cannot reference other tables", False)
                ]
            },
            {
                "skill": "Data Analysis", "diff": "Beginner", "marks": 1,
                "text": "Which metric measures the middle value of an ordered dataset, making it robust against extreme outliers?",
                "code": None,
                "exp": "The Median is the middle value when data is sorted, remaining unaffected by extreme skew and outliers.",
                "opts": [
                    ("Arithmetic Mean", False),
                    ("Median", True),
                    ("Mode", False),
                    ("Standard Deviation", False)
                ]
            }
        ]
    },
    {
        "title": "Data Engineer & ETL Pipelines Assessment",
        "category": "Data Engineering",
        "role_slug": "data-engineer",
        "desc": "Assesses batch and streaming pipelines, schema design (Star/Snowflake), Kafka messaging, Airflow scheduling, and data lakehouses.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "ETL Pipelines", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary architectural difference between ETL and ELT data pipelines?",
                "code": None,
                "exp": "In ELT, raw data is loaded directly into modern cloud data warehouses (e.g. Snowflake, BigQuery) before transformations run using distributed SQL.",
                "opts": [
                    ("ETL works only with streaming Kafka data; ELT works with CSV files", False),
                    ("In ELT, data is loaded into the target warehouse first and transformed using warehouse compute", True),
                    ("ELT does not validate data types", False),
                    ("ETL cannot support relational databases", False)
                ]
            },
            {
                "skill": "Apache Kafka", "diff": "Advanced", "marks": 3,
                "text": "In Apache Kafka, what determines the maximum degree of consumer parallelism within a single Consumer Group for a Topic?",
                "code": None,
                "exp": "Each partition in a Kafka topic can only be consumed by at most one consumer thread in a given consumer group.",
                "opts": [
                    ("The total number of ZooKeeper nodes", False),
                    ("The number of partitions configured for that Kafka topic", True),
                    ("The number of producer worker threads", False),
                    ("The maximum network socket buffer size", False)
                ]
            },
            {
                "skill": "Data Warehousing", "diff": "Intermediate", "marks": 2,
                "text": "In dimensional data modeling, what is the defining characteristic of a Fact Table compared to a Dimension Table?",
                "code": None,
                "exp": "Fact tables store quantitative numerical metrics and foreign keys referencing descriptive dimension tables.",
                "opts": [
                    ("Fact tables store only user passwords and session cookies", False),
                    ("Fact tables contain measurable numerical metrics and foreign keys referencing dimension attributes", True),
                    ("Fact tables are never normalized", False),
                    ("Dimension tables contain transaction timestamps and revenue sums", False)
                ]
            },
            {
                "skill": "Data Warehousing", "diff": "Intermediate", "marks": 2,
                "text": "What is a Slowly Changing Dimension Type 2 (SCD Type 2) design pattern?",
                "code": None,
                "exp": "SCD Type 2 tracks historical changes by inserting a new record with effective start/end date timestamps and an active flag.",
                "opts": [
                    ("Overwriting the existing record directly, losing historical context", False),
                    ("Adding a new row with valid_from, valid_to timestamps to preserve full audit history", True),
                    ("Creating a new column for each year of user data", False),
                    ("Deleting expired user records immediately upon modification", False)
                ]
            },
            {
                "skill": "SQL", "diff": "Beginner", "marks": 1,
                "text": "What is the primary function of Apache Airflow in enterprise data engineering?",
                "code": None,
                "exp": "Apache Airflow is a programmatic platform to author, schedule, and monitor workflows as Directed Acyclic Graphs (DAGs).",
                "opts": [
                    ("A real-time message broker", False),
                    ("A workflow orchestrator and job scheduler utilizing Python DAGs", True),
                    ("A distributed columnar database engine", False),
                    ("A deep learning neural network framework", False)
                ]
            },
            {
                "skill": "ETL Pipelines", "diff": "Advanced", "marks": 3,
                "text": "What is 'idempotency' in data pipeline task design and why is it critical?",
                "code": None,
                "exp": "An idempotent task produces the exact same outcome whether executed once or retried multiple times, preventing duplicate records.",
                "opts": [
                    ("Executing queries in under 1 millisecond", False),
                    ("Ensuring that re-running a pipeline job produces identical results without duplicating data", True),
                    ("Encrypting all network packets with TLS 1.3", False),
                    ("Partitioning data exclusively by country code", False)
                ]
            }
        ]
    },
    {
        "title": "Cloud Engineer & AWS Architecture Assessment",
        "category": "Cloud Computing",
        "role_slug": "cloud-engineer",
        "desc": "Evaluates AWS core compute, VPC networking, security groups, IAM least privilege, serverless architecture, and multi-region resilience.",
        "mins": 20,
        "pass_pct": 60.0,
        "questions": [
            {
                "skill": "AWS", "diff": "Intermediate", "marks": 2,
                "text": "Which AWS architectural pattern guarantees high availability across hardware failures within an AWS Region?",
                "code": None,
                "exp": "Deploying redundant instances across multiple Availability Zones (AZs) behind an Application Load Balancer ensures resilience.",
                "opts": [
                    ("Hosting all servers in a single Availability Zone on the largest instance size", False),
                    ("Deploying resources across multiple Availability Zones behind an Elastic Load Balancer", True),
                    ("Using simple S3 static file replication without load balancers", False),
                    ("Setting CPU burstable credits to unlimited", False)
                ]
            },
            {
                "skill": "Identity & Access Management", "diff": "Intermediate", "marks": 2,
                "text": "In AWS IAM, what is the principle of least privilege?",
                "code": None,
                "exp": "Least privilege mandates granting users and roles only the minimum necessary permissions required to perform their specific tasks.",
                "opts": [
                    ("Granting full AdministratorAccess to every team developer for rapid debugging", False),
                    ("Granting only the minimal set of permissions required to complete authorized tasks", True),
                    ("Storing IAM secret access keys inside public git repositories", False),
                    ("Disabling multi-factor authentication on root accounts", False)
                ]
            },
            {
                "skill": "AWS", "diff": "Advanced", "marks": 3,
                "text": "In an AWS Virtual Private Cloud (VPC), how can an EC2 instance in a Private Subnet securely initiate outbound internet requests for software patches without being directly accessible from the public internet?",
                "code": None,
                "exp": "A NAT Gateway positioned in a Public Subnet routes outbound traffic from private instances while blocking inbound connections.",
                "opts": [
                    ("Assigning a Public Elastic IP directly to the private EC2 instance", False),
                    ("Routing outbound traffic through a NAT Gateway located in a Public Subnet with an Internet Gateway", True),
                    ("Disabling all security groups on the VPC router", False),
                    ("Using VPC Peering to route all traffic to AWS CloudWatch", False)
                ]
            },
            {
                "skill": "AWS", "diff": "Beginner", "marks": 1,
                "text": "What type of cloud computing service model is AWS Lambda?",
                "code": None,
                "exp": "AWS Lambda is a Function-as-a-Service (FaaS) / Serverless execution model where compute runs in response to events.",
                "opts": [
                    ("Infrastructure as a Service (IaaS)", False),
                    ("Function as a Service (FaaS) / Serverless", True),
                    ("Platform as a Service (PaaS)", False),
                    ("Software as a Service (SaaS)", False)
                ]
            },
            {
                "skill": "Terraform", "diff": "Intermediate", "marks": 2,
                "text": "In Infrastructure as Code (IaC) with Terraform, what is the purpose of the 'terraform.tfstate' file?",
                "code": None,
                "exp": "The state file maps real-world cloud resources to Terraform configuration files, tracking metadata and resource dependencies.",
                "opts": [
                    ("To store compiled C++ binaries of the Terraform CLI", False),
                    ("To record current state mappings between declared configurations and real cloud infrastructure", True),
                    ("To store unencrypted AWS root credentials", False),
                    ("To generate automated PDF billing invoices", False)
                ]
            },
            {
                "skill": "AWS", "diff": "Advanced", "marks": 3,
                "text": "What is the difference between AWS Security Groups and Network Access Control Lists (NACLs)?",
                "code": None,
                "exp": "Security Groups are stateful firewalls at the instance level; NACLs are stateless firewalls at the subnet level.",
                "opts": [
                    ("Security Groups are stateless; NACLs are stateful", False),
                    ("Security Groups operate at the instance level (stateful); NACLs operate at the subnet level (stateless)", True),
                    ("Security Groups only control outbound traffic; NACLs only control inbound traffic", False),
                    ("NACLs are only available in Azure, not AWS", False)
                ]
            }
        ]
    },
    {
        "title": "DevOps Engineer & CI/CD Pipelines Assessment",
        "category": "DevOps",
        "role_slug": "devops-engineer",
        "desc": "Assesses Docker containerization, Kubernetes orchestration, Helm packaging, GitHub Actions CI/CD, and GitOps deployments.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Docker", "diff": "Beginner", "marks": 1,
                "text": "What is the primary benefit of multi-stage Docker builds?",
                "code": "FROM golang:1.22 AS builder\n...\nFROM alpine:3.19\nCOPY --from=builder /app/server .",
                "exp": "Multi-stage builds separate the build environment from runtime artifacts, yielding tiny, secure, minimal production images.",
                "opts": [
                    ("Running five containers inside a single Linux thread", False),
                    ("Separating compilation tools from runtime binaries to drastically reduce production image size and attack surface", True),
                    ("Eliminating the need to write Dockerfiles", False),
                    ("Automatically pushing containers to Docker Hub without credentials", False)
                ]
            },
            {
                "skill": "Kubernetes", "diff": "Intermediate", "marks": 2,
                "text": "In Kubernetes, which controller guarantees that a specified number of Pod replicas are running at all times?",
                "code": None,
                "exp": "A ReplicaSet (managed via a Deployment) ensures the target count of pod replicas are running across worker nodes.",
                "opts": [
                    ("ConfigMap", False),
                    ("ReplicaSet (or Deployment controller)", True),
                    ("Ingress Controller", False),
                    ("PersistentVolumeClaim", False)
                ]
            },
            {
                "skill": "Kubernetes", "diff": "Advanced", "marks": 3,
                "text": "What is the difference between Kubernetes livenessProbe and readinessProbe?",
                "code": None,
                "exp": "livenessProbe restarts failed pods; readinessProbe determines whether the pod is ready to accept user network traffic.",
                "opts": [
                    ("livenessProbe is for CPU monitoring; readinessProbe is for memory limits", False),
                    ("livenessProbe restarts unhealthy pods; readinessProbe stops traffic routing to pods until they are ready to serve requests", True),
                    ("readinessProbe deletes the container image from the node cache", False),
                    ("They are interchangeable synonyms in Kubernetes API v1", False)
                ]
            },
            {
                "skill": "CI/CD Pipelines", "diff": "Intermediate", "marks": 2,
                "text": "What deployment strategy routes a small percentage (e.g. 5%) of live production user traffic to a new version to test stability?",
                "code": None,
                "exp": "Canary deployment exposes new versions to a small slice of users before rolling out to 100% of production traffic.",
                "opts": [
                    ("Blue/Green Deployment", False),
                    ("Canary Deployment", True),
                    ("Recreate Deployment", False),
                    ("Rolling Update without metrics", False)
                ]
            },
            {
                "skill": "Linux / Bash", "diff": "Beginner", "marks": 1,
                "text": "In Linux, which command displays real-time CPU, memory usage, and running process status?",
                "code": None,
                "exp": "top (or htop) displays dynamic real-time information about system resources and active processes.",
                "opts": [
                    ("ls -la", False),
                    ("top (or htop)", True),
                    ("chmod 777", False),
                    ("df -h", False)
                ]
            },
            {
                "skill": "Monitoring & Prometheus", "diff": "Intermediate", "marks": 2,
                "text": "In Prometheus monitoring architecture, how are metrics collected from target services by default?",
                "code": None,
                "exp": "Prometheus uses a pull model, periodically scraping HTTP metrics endpoints (/metrics) exposed by target services.",
                "opts": [
                    ("Targets write directly to MySQL database rows", False),
                    ("Prometheus periodically pulls (scrapes) HTTP /metrics endpoints exposed by targets", True),
                    ("Targets stream binary UDP packets to port 53", False),
                    ("Metrics are uploaded to AWS S3 buckets every 24 hours", False)
                ]
            }
        ]
    },
    {
        "title": "Cybersecurity Analyst & Threat Defense Assessment",
        "category": "Cybersecurity",
        "role_slug": "cybersecurity-analyst",
        "desc": "Measures vulnerability assessment, OWASP Top 10 web vulnerabilities, SIEM telemetry, incident response, and threat hunting.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Cybersecurity Fundamentals", "diff": "Intermediate", "marks": 2,
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
            {
                "skill": "OWASP Top 10", "diff": "Intermediate", "marks": 2,
                "text": "What web vulnerability allows attackers to inject malicious client-side JavaScript that executes in the browsers of other users?",
                "code": None,
                "exp": "Cross-Site Scripting (XSS) occurs when untrusted user input is rendered in an HTML document without proper sanitization.",
                "opts": [
                    ("Server-Side Request Forgery (SSRF)", False),
                    ("Cross-Site Scripting (XSS)", True),
                    ("Insecure Direct Object References (IDOR)", False),
                    ("Denial of Service (DoS)", False)
                ]
            },
            {
                "skill": "SIEM & Incident Response", "diff": "Advanced", "marks": 3,
                "text": "In a Security Operations Center (SOC), what is the primary role of a SIEM (Security Information and Event Management) system?",
                "code": None,
                "exp": "A SIEM aggregates, correlates, and analyzes security logs from across enterprise networks to identify real-time threat indicators.",
                "opts": [
                    ("Compiling frontend TypeScript code into bundle files", False),
                    ("Aggregating, normalizing, and correlating security event logs across network nodes for real-time threat detection", True),
                    ("Replacing database backups with encrypted zip archives", False),
                    ("Hosting customer-facing REST API gateways", False)
                ]
            },
            {
                "skill": "Network Security", "diff": "Intermediate", "marks": 2,
                "text": "What type of attack involves an adversary intercepting and potentially altering communications between two parties without their knowledge?",
                "code": None,
                "exp": "A Man-in-the-Middle (MitM) attack occurs when an attacker secretly relays and intercepts communications between two endpoints.",
                "opts": [
                    ("Buffer Overflow", False),
                    ("Man-in-the-Middle (MitM) Attack", True),
                    ("SQL Injection", False),
                    ("Brute Force Password Spray", False)
                ]
            },
            {
                "skill": "Cryptography", "diff": "Beginner", "marks": 1,
                "text": "Which cryptographic property ensures that a message has not been altered or tampered with during transmission?",
                "code": None,
                "exp": "Integrity guarantees that data has not been modified or corrupted in transit, typically verified via cryptographic hashes or HMACs.",
                "opts": [
                    ("Confidentiality", False),
                    ("Integrity", True),
                    ("Availability", False),
                    ("Non-repudiation", False)
                ]
            },
            {
                "skill": "OWASP Top 10", "diff": "Advanced", "marks": 3,
                "text": "What security header should be sent by web servers to prevent Clickjacking attacks inside iframes?",
                "code": None,
                "exp": "X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors 'none' prevents browsers from embedding pages in iframes.",
                "opts": [
                    ("X-Content-Type-Options: nosniff", False),
                    ("X-Frame-Options: DENY (or CSP frame-ancestors)", True),
                    ("Strict-Transport-Security", False),
                    ("Access-Control-Allow-Origin: *", False)
                ]
            }
        ]
    },
    {
        "title": "Blockchain Developer & Smart Contracts Assessment",
        "category": "Blockchain",
        "role_slug": "blockchain-developer",
        "desc": "Tests Ethereum EVM architecture, Solidity smart contract programming, gas optimization, ERC standards, and reentrancy defense.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Blockchain Fundamentals", "diff": "Intermediate", "marks": 2,
                "text": "Why are academic certificates hashed using SHA-256 before registering their verification IDs on a blockchain?",
                "code": "hash = SHA256(student_id + degree + cgpa + issuer)",
                "exp": "Storing cryptographic hashes guarantees tamper evidence while protecting student privacy and minimizing expensive on-chain storage costs.",
                "opts": [
                    ("Blockchains cannot store any alphanumeric strings longer than 32 characters", False),
                    ("Hashes ensure tamper evidence while preventing exposure of sensitive student PII on public ledgers", True),
                    ("Because SHA-256 automatically sends emails to students upon transaction completion", False),
                    ("It is required by Ethereum to convert Solidity into EVM bytecode", False)
                ]
            },
            {
                "skill": "Solidity", "diff": "Advanced", "marks": 3,
                "text": "What critical smart contract security vulnerability was exploited in the historic 2016 DAO hack?",
                "code": "(bool sent, ) = msg.sender.call{value: balance}(\"\");\nbalances[msg.sender] = 0;",
                "exp": "Reentrancy occurs when an external call is made before internal state updates, allowing recursive callback drain attacks.",
                "opts": [
                    ("Integer Underflow in SafeMath", False),
                    ("Reentrancy vulnerability due to state updates after external ether transfer calls", True),
                    ("Front-running miner transaction order manipulation", False),
                    ("Private variable storage leaks", False)
                ]
            },
            {
                "skill": "Smart Contracts", "diff": "Intermediate", "marks": 2,
                "text": "In Solidity, what is the best practice design pattern to defend against reentrancy attacks?",
                "code": None,
                "exp": "The Checks-Effects-Interactions pattern ensures conditions are checked and internal state variables updated BEFORE making external calls.",
                "opts": [
                    ("Increasing transaction gas limits to 10,000,000", False),
                    ("Checks-Effects-Interactions pattern (and ReentrancyGuard mutex locks)", True),
                    ("Using selfdestruct() at the beginning of functions", False),
                    ("Storing all balances in memory instead of storage", False)
                ]
            },
            {
                "skill": "Solidity", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary difference between 'storage' and 'memory' data locations in Solidity smart contracts?",
                "code": None,
                "exp": "storage variables are permanently written to the blockchain state (high gas cost); memory variables are temporary and cleared after function execution.",
                "opts": [
                    ("storage is wiped after transaction execution; memory is permanent", False),
                    ("storage is permanently persisted on the blockchain ledger; memory is temporary and exists only during function execution", True),
                    ("memory cannot store dynamic arrays", False),
                    ("There is no gas cost difference between storage and memory", False)
                ]
            },
            {
                "skill": "Blockchain Fundamentals", "diff": "Beginner", "marks": 1,
                "text": "What is the standard token interface for Non-Fungible Tokens (NFTs) on the Ethereum blockchain?",
                "code": None,
                "exp": "ERC-721 is the open standard that outlines how to build unique non-fungible tokens on EVM blockchains.",
                "opts": [
                    ("ERC-20", False),
                    ("ERC-721", True),
                    ("ERC-777", False),
                    ("ERC-223", False)
                ]
            },
            {
                "skill": "Consensus Algorithms", "diff": "Intermediate", "marks": 2,
                "text": "How does Proof of Stake (PoS) consensus determine which validator proposes the next block?",
                "code": None,
                "exp": "Validators are pseudo-randomly selected to propose blocks proportional to the economic stake of cryptocurrency they have locked in the network.",
                "opts": [
                    ("By solving computationally intensive mathematical puzzles with high electrical power", False),
                    ("By pseudo-random selection weighted by the quantity of native cryptocurrency staked as collateral", True),
                    ("By fastest internet upload bandwidth speed", False),
                    ("By alphabetical order of wallet addresses", False)
                ]
            }
        ]
    },
    {
        "title": "Computer Vision & Deep Learning Assessment",
        "category": "Computer Vision",
        "role_slug": "computer-vision-engineer",
        "desc": "Assesses convolutional neural networks, object detection (YOLO), image segmentation, OCR pipeline design, and OpenCV processing.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Computer Vision", "diff": "Intermediate", "marks": 2,
                "text": "In Convolutional Neural Networks (CNNs), what spatial transformation is performed by a MaxPooling2D layer?",
                "code": None,
                "exp": "MaxPooling reduces the spatial height and width dimensions of feature maps, providing translation invariance and reducing compute.",
                "opts": [
                    ("It increases image resolution by factor of 2", False),
                    ("It downsamples spatial dimensions (height/width) while retaining dominant feature activations", True),
                    ("It converts RGB images into grayscale single-channel matrices", False),
                    ("It inverts the pixel intensity values", False)
                ]
            },
            {
                "skill": "Computer Vision", "diff": "Advanced", "marks": 3,
                "text": "In modern real-time object detection models like YOLO, what metric measures bounding box prediction overlap against ground truth?",
                "code": "IoU = Area of Overlap / Area of Union",
                "exp": "Intersection over Union (IoU) measures the ratio of overlap area to the total combined union area of bounding boxes.",
                "opts": [
                    ("Mean Squared Error (MSE)", False),
                    ("Intersection over Union (IoU)", True),
                    ("Cross-Entropy Loss", False),
                    ("Structural Similarity Index (SSIM)", False)
                ]
            },
            {
                "skill": "Computer Vision", "diff": "Intermediate", "marks": 2,
                "text": "In Optical Character Recognition (OCR) document preprocessing, why is adaptive thresholding applied to scanned resume images?",
                "code": "cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, ...)",
                "exp": "Adaptive thresholding handles uneven lighting and shadow variations across documents by calculating local thresholds for small regions.",
                "opts": [
                    ("To colorize black-and-white documents", False),
                    ("To binarize text against backgrounds under non-uniform illumination and gradient shadows", True),
                    ("To translate Spanish text into English", False),
                    ("To compress the image into MP4 video format", False)
                ]
            },
            {
                "skill": "Deep Learning", "diff": "Beginner", "marks": 1,
                "text": "Which activation function is most widely used in hidden layers of modern deep convolutional neural networks?",
                "code": "f(x) = max(0, x)",
                "exp": "ReLU (Rectified Linear Unit) avoids vanishing gradient issues and is computationally cheap.",
                "opts": [
                    ("Sigmoid", False),
                    ("ReLU (Rectified Linear Unit)", True),
                    ("Linear Identity", False),
                    ("Hard Tanh", False)
                ]
            },
            {
                "skill": "Computer Vision", "diff": "Advanced", "marks": 3,
                "text": "What is the difference between Object Detection and Semantic Segmentation in computer vision?",
                "code": None,
                "exp": "Object detection classifies and localizes objects with rectangular bounding boxes; semantic segmentation classifies every single pixel in the image.",
                "opts": [
                    ("Detection works only on videos; segmentation works on text files", False),
                    ("Detection outputs bounding boxes around objects; segmentation classifies each individual pixel into a semantic class", True),
                    ("Segmentation cannot distinguish cats from dogs", False),
                    ("Detection requires 3D camera sensors", False)
                ]
            },
            {
                "skill": "Computer Vision", "diff": "Intermediate", "marks": 2,
                "text": "What is Data Augmentation in image classification and why is it employed?",
                "code": None,
                "exp": "Data augmentation applies random rotations, flips, and crops to artificially expand training diversity and prevent overfitting.",
                "opts": [
                    ("Purchasing more cloud GPU hardware instances", False),
                    ("Applying geometric and color transformations (rotations, flips, crops) to training images to improve generalization", True),
                    ("Deleting low-resolution training samples from the dataset", False),
                    ("Increasing the learning rate by 10x every epoch", False)
                ]
            }
        ]
    },
    {
        "title": "NLP Engineer & Language Models Assessment",
        "category": "Natural Language Processing",
        "role_slug": "nlp-engineer",
        "desc": "Evaluates tokenization, word embeddings, transformer architectures, sequence-to-sequence translation, and semantic search.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "NLP", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary advantage of subword tokenization algorithms (e.g. Byte-Pair Encoding, WordPiece) over simple whitespace tokenization?",
                "code": None,
                "exp": "Subword tokenization balances vocabulary size and handles Out-Of-Vocabulary (OOV) unseen words by decomposing them into known subword morphemes.",
                "opts": [
                    ("It converts text into sound frequencies", False),
                    ("It prevents Out-Of-Vocabulary (OOV) errors by decomposing rare or unseen words into recognizable subword units", True),
                    ("It eliminates the need for grammar checking", False),
                    ("It increases vocabulary size to over 10 million tokens", False)
                ]
            },
            {
                "skill": "NLP", "diff": "Advanced", "marks": 3,
                "text": "In transformer models like BERT, what was the primary architectural innovation compared to recurrent networks (LSTMs)?",
                "code": None,
                "exp": "Self-attention mechanisms allow parallel processing of entire sequences simultaneously without sequential recurrence bottlenecks.",
                "opts": [
                    ("Using analog neural circuits", False),
                    ("Replacing sequential recurrent loops with bidirectional self-attention, enabling massive parallel training across full sequences", True),
                    ("Restricting sequence lengths to exactly 10 tokens", False),
                    ("Requiring zero training labels for all NLP tasks", False)
                ]
            },
            {
                "skill": "NLP", "diff": "Intermediate", "marks": 2,
                "text": "What is the key functional difference between BERT and GPT architectural styles?",
                "code": None,
                "exp": "BERT uses an encoder-only architecture trained with masked language modeling (bidirectional context); GPT uses an autoregressive decoder-only architecture.",
                "opts": [
                    ("BERT is an image classifier; GPT is a database", False),
                    ("BERT is an encoder-only bidirectional model ideal for classification/embeddings; GPT is an autoregressive decoder-only model ideal for generation", True),
                    ("GPT cannot generate English text", False),
                    ("BERT does not use attention layers", False)
                ]
            },
            {
                "skill": "NLP", "diff": "Beginner", "marks": 1,
                "text": "Which traditional NLP technique reduces words to their base linguistic root forms (e.g. 'running', 'runs' -> 'run')?",
                "code": None,
                "exp": "Lemmatization uses vocabulary and morphological analysis to return the dictionary base form (lemma) of words.",
                "opts": [
                    ("One-Hot Vectorization", False),
                    ("Lemmatization (or Stemming)", True),
                    ("TF-IDF weighting", False),
                    ("Cross-Entropy Loss", False)
                ]
            },
            {
                "skill": "NLP", "diff": "Intermediate", "marks": 2,
                "text": "In Information Retrieval, what does the TF-IDF metric measure?",
                "code": None,
                "exp": "Term Frequency-Inverse Document Frequency reflects how important a word is to a document relative to an entire corpus.",
                "opts": [
                    ("The total byte size of an HTML document", False),
                    ("The frequency of a term in a document penalized by how frequently it appears across all documents in the corpus", True),
                    ("The translation accuracy of a neural translation model", False),
                    ("The network latency of an elasticsearch cluster", False)
                ]
            },
            {
                "skill": "NLP", "diff": "Advanced", "marks": 3,
                "text": "What is BLEU score used for in natural language processing evaluation?",
                "code": None,
                "exp": "BLEU (Bilingual Evaluation Understudy) measures n-gram overlap between machine translations and human reference translations.",
                "opts": [
                    ("Measuring sentiment polarity on social media", False),
                    ("Evaluating the quality of machine-translated text against human reference translations using n-gram precision", True),
                    ("Detecting grammar errors in student essays", False),
                    ("Measuring training loss during backpropagation", False)
                ]
            }
        ]
    },
    {
        "title": "QA Automation Engineer & Testing Assessment",
        "category": "Quality Assurance",
        "role_slug": "qa-automation-engineer",
        "desc": "Tests automated testing frameworks (Pytest, Playwright, Cypress), test pyramids, API mocking, and continuous test gates.",
        "mins": 20,
        "pass_pct": 60.0,
        "questions": [
            {
                "skill": "CI/CD Pipelines", "diff": "Intermediate", "marks": 2,
                "text": "In the standard Test Pyramid architecture, which layer of tests should constitute the largest volume of tests?",
                "code": None,
                "exp": "Unit tests form the base of the pyramid because they execute quickly, isolate failures easily, and are cheap to maintain.",
                "opts": [
                    ("Manual Exploratory UI Tests", False),
                    ("Unit Tests", True),
                    ("End-to-End (E2E) Browser Tests", False),
                    ("Performance Stress Tests", False)
                ]
            },
            {
                "skill": "Python", "diff": "Intermediate", "marks": 2,
                "text": "In Pytest, how are reusable setup and teardown test dependencies provided to test functions?",
                "code": "@pytest.fixture\ndef db_session():\n    db = init_db()\n    yield db\n    db.close()",
                "exp": "Pytest fixtures manage resource creation, injection into test arguments, and teardown cleanly.",
                "opts": [
                    ("Using global static variables across files", False),
                    ("Using Pytest fixtures with dependency injection", True),
                    ("Hardcoding database connections inside every assert statement", False),
                    ("Rebuilding the entire OS image before each test function", False)
                ]
            },
            {
                "skill": "FastAPI", "diff": "Intermediate", "marks": 2,
                "text": "What is the primary difference between Mocking and Stubbing in unit test isolation?",
                "code": None,
                "exp": "Stubs provide canned predetermined responses to calls; Mocks additionally verify that specific calls/interactions were made with expected arguments.",
                "opts": [
                    ("Mocking is only used in Java; Stubbing is only used in Python", False),
                    ("Stubs return pre-programmed data; Mocks verify specific interaction behavior and invocation counts", True),
                    ("Mocks cannot return JSON data", False),
                    ("There is no technical distinction between them", False)
                ]
            },
            {
                "skill": "Cybersecurity Fundamentals", "diff": "Beginner", "marks": 1,
                "text": "What is Regression Testing?",
                "code": None,
                "exp": "Regression testing re-executes tests to verify that new code additions or bug fixes have not broken existing functionality.",
                "opts": [
                    ("Testing software on older versions of Windows 95", False),
                    ("Re-running existing test suites to ensure that recent changes have not broken previously working features", True),
                    ("Deleting test cases that take longer than 2 seconds", False),
                    ("Deploying code directly to production without testing", False)
                ]
            },
            {
                "skill": "HTML/CSS", "diff": "Intermediate", "marks": 2,
                "text": "In browser end-to-end automation with Playwright or Cypress, why is selecting elements by 'data-testid' preferred over CSS class names?",
                "code": "page.locator('[data-testid=\"submit-btn\"]').click()",
                "exp": "CSS class names frequently change during UI styling refactors, whereas explicit test attributes provide stable test contracts.",
                "opts": [
                    ("data-testid attributes make JavaScript run 10 times faster", False),
                    ("Test IDs isolate automated test selectors from visual CSS styling and class refactors", True),
                    ("Browsers reject click events on standard CSS classes", False),
                    ("It is required by the W3C HTML5 specification", False)
                ]
            },
            {
                "skill": "CI/CD Pipelines", "diff": "Advanced", "marks": 3,
                "text": "What is Code Coverage and why is achieving 100% line coverage NOT a guarantee of bug-free software?",
                "code": None,
                "exp": "Line coverage only proves lines were executed; it does not test unexpected state permutations, edge boundary cases, or invalid user inputs.",
                "opts": [
                    ("Code coverage measures RAM memory consumption during testing", False),
                    ("It measures which lines of code were executed during tests, but cannot guarantee logical edge cases or business requirements are tested", True),
                    ("100% coverage mathematically guarantees zero runtime defects", False),
                    ("Coverage tools only work on compiled C++ programs", False)
                ]
            }
        ]
    },
    {
        "title": "Systems Architect & Distributed Systems Assessment",
        "category": "Software Architecture",
        "role_slug": "systems-architect",
        "desc": "Evaluates microservices partitioning, event-driven architectures, consensus protocols, database sharding, and resilience engineering.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "System Design", "diff": "Advanced", "marks": 3,
                "text": "In distributed microservices, how does the Saga Pattern handle distributed transaction consistency without two-phase commit (2PC)?",
                "code": None,
                "exp": "Sagas manage distributed transactions via a sequence of local transactions across services, applying compensating transactions if a step fails.",
                "opts": [
                    ("By locking all relational tables in a global master lock for 10 seconds", False),
                    ("By executing a series of local transactions coordinated by events or an orchestrator, executing compensating rollbacks on failure", True),
                    ("By routing all database transactions through an Nginx proxy", False),
                    ("By ignoring transaction failures and continuing execution", False)
                ]
            },
            {
                "skill": "System Design", "diff": "Advanced", "marks": 3,
                "text": "What is Database Sharding and what problem does Consistent Hashing solve when sharding across dynamic database nodes?",
                "code": None,
                "exp": "Consistent hashing minimizes key redistribution when nodes are added or removed from a distributed cluster (O(K/N) keys moved).",
                "opts": [
                    ("It encrypts all database passwords into 128-bit hashes", False),
                    ("It distributes data horizontally across nodes and minimizes the volume of keys re-mapped when nodes scale up or down", True),
                    ("It converts relational tables into MongoDB documents automatically", False),
                    ("It prevents concurrent read requests from locking database tables", False)
                ]
            },
            {
                "skill": "System Design", "diff": "Intermediate", "marks": 2,
                "text": "In high-throughput distributed messaging, what is the Circuit Breaker pattern?",
                "code": None,
                "exp": "A circuit breaker prevents cascading failures by stopping requests to failing services, returning immediate fallbacks until recovery.",
                "opts": [
                    ("A physical hardware switch in a datacenter", False),
                    ("A software failure-handling pattern that detects remote errors and fast-fails requests to prevent cascading system outages", True),
                    ("A method to encrypt SSL certificates on port 443", False),
                    ("An algorithm for sorting database index pages", False)
                ]
            },
            {
                "skill": "Redis", "diff": "Intermediate", "marks": 2,
                "text": "Why is Redis widely chosen as a distributed cache in high-traffic architectures?",
                "code": None,
                "exp": "Redis keeps datasets entirely in-memory with sub-millisecond response times, supporting versatile data structures (hashes, sets, lists).",
                "opts": [
                    ("It stores data exclusively on tape drives to reduce electricity costs", False),
                    ("It executes operations entirely in-memory with sub-millisecond latency and rich native data structures", True),
                    ("It replaces the operating system kernel on Linux servers", False),
                    ("It requires zero RAM on the host server", False)
                ]
            },
            {
                "skill": "System Design", "diff": "Beginner", "marks": 1,
                "text": "What is the primary difference between horizontal scaling and vertical scaling?",
                "code": None,
                "exp": "Horizontal scaling adds more machine nodes to the pool; vertical scaling upgrades CPU/RAM capacity on a single existing machine.",
                "opts": [
                    ("Horizontal scaling increases disk speed; vertical scaling increases internet bandwidth", False),
                    ("Horizontal scaling adds more instances/nodes to the pool; vertical scaling upgrades CPU/RAM resources of a single server", True),
                    ("Vertical scaling cannot be used with cloud providers", False),
                    ("Horizontal scaling only works with monolithic architectures", False)
                ]
            },
            {
                "skill": "System Design", "diff": "Advanced", "marks": 3,
                "text": "In distributed consensus protocols (e.g. Raft, Paxos), what is a 'Split-Brain' scenario and how is it prevented?",
                "code": None,
                "exp": "Split-brain happens when a network partition creates two disconnected leader nodes; quorum majorities ((N/2) + 1) prevent two valid leaders.",
                "opts": [
                    ("When two developers commit code to the same Git branch at once", False),
                    ("When network partitions cause two sub-clusters to elect conflicting leaders, prevented by requiring strict quorum majorities", True),
                    ("When a server motherboard loses power to one CPU socket", False),
                    ("When two SSL certificates expire at the same second", False)
                ]
            }
        ]
    },
    {
        "title": "Data Structures & Algorithms Challenge",
        "category": "Computer Science Fundamentals",
        "role_slug": "cs-fundamentals",
        "desc": "Tests computational complexity, tree traversals, dynamic programming, graph algorithms, and asymptotic memory efficiency.",
        "mins": 25,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Data Structures", "diff": "Intermediate", "marks": 2,
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
                "skill": "Algorithms", "diff": "Advanced", "marks": 3,
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
            {
                "skill": "Algorithms", "diff": "Intermediate", "marks": 2,
                "text": "What is the space complexity of a recursive Depth-First Search on a balanced binary tree of N nodes?",
                "code": None,
                "exp": "The call stack memory is proportional to the height of the tree, which is O(log N) for a balanced tree.",
                "opts": [
                    ("O(N^2)", False),
                    ("O(log N)", True),
                    ("O(1)", False),
                    ("O(N!)", False)
                ]
            },
            {
                "skill": "Data Structures", "diff": "Beginner", "marks": 1,
                "text": "Which principle describes the access behavior of a standard Stack data structure?",
                "code": None,
                "exp": "A Stack operates on the Last-In, First-Out (LIFO) order.",
                "opts": [
                    ("First-In, First-Out (FIFO)", False),
                    ("Last-In, First-Out (LIFO)", True),
                    ("Random Access", False),
                    ("Priority-Based Dequeue", False)
                ]
            },
            {
                "skill": "Algorithms", "diff": "Advanced", "marks": 3,
                "text": "In Dynamic Programming, what are the two essential properties a problem must possess to be solvable via DP?",
                "code": None,
                "exp": "Optimal substructure (optimal solution contains optimal sub-solutions) and overlapping subproblems (subproblems recur repeatedly).",
                "opts": [
                    ("Negative weight edges and acyclic structures", False),
                    ("Optimal Substructure and Overlapping Subproblems", True),
                    ("Linear memory scaling and binary representations", False),
                    ("Constant time transitions and greedy choices", False)
                ]
            },
            {
                "skill": "Algorithms", "diff": "Intermediate", "marks": 2,
                "text": "What is the worst-case time complexity of QuickSort and how can it be avoided in practice?",
                "code": None,
                "exp": "Worst-case is O(N^2) when poor pivots are chosen (e.g. sorted array with first element pivot). Randomized or median-of-three pivots avoid this.",
                "opts": [
                    ("O(N log N); avoided by allocating double memory", False),
                    ("O(N^2); avoided by picking randomized pivots or median-of-three pivot selection", True),
                    ("O(N); avoided by converting recursion to iteration", False),
                    ("O(log N); avoided by using bubble sort subroutine", False)
                ]
            }
        ]
    },
    {
        "title": "Python Core & Advanced Programming",
        "category": "Programming",
        "role_slug": "python-programming",
        "desc": "Evaluates Python memory management, GIL, decorators, generators, dunder methods, and asyncio concurrency.",
        "mins": 20,
        "pass_pct": 65.0,
        "questions": [
            {
                "skill": "Python", "diff": "Intermediate", "marks": 2,
                "text": "What is the purpose of Python's 'yield' keyword inside a function?",
                "code": "def count_up():\n    n = 1\n    while True:\n        yield n\n        n += 1",
                "exp": "yield turns a function into a Generator, pausing execution and returning a value lazily without storing the entire sequence in RAM.",
                "opts": [
                    ("It terminates the Python interpreter process immediately", False),
                    ("It converts the function into an in-memory generator, yielding items one by one on demand", True),
                    ("It forces the function to execute on a separate operating system thread", False),
                    ("It converts return types into string values", False)
                ]
            },
            {
                "skill": "Python", "diff": "Advanced", "marks": 3,
                "text": "What is the Global Interpreter Lock (GIL) in CPython and what constraint does it impose?",
                "code": None,
                "exp": "The GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously in CPython.",
                "opts": [
                    ("It restricts Python programs from consuming more than 4GB of RAM", False),
                    ("It is a mutex ensuring only one native thread executes Python bytecode at any given moment", True),
                    ("It prevents Python from opening network sockets on ports below 1024", False),
                    ("It disables garbage collection during file writes", False)
                ]
            },
            {
                "skill": "Python", "diff": "Intermediate", "marks": 2,
                "text": "In Python object-oriented programming, what do '__init__' and '__new__' methods do?",
                "code": None,
                "exp": "__new__ creates the class instance object in memory; __init__ initializes the newly created instance attributes.",
                "opts": [
                    ("__init__ creates the instance; __new__ deletes it from memory", False),
                    ("__new__ is the constructor that creates the instance; __init__ initializes the instance's attributes", True),
                    ("They are identical aliases for class constructors", False),
                    ("__new__ can only be called from static methods", False)
                ]
            },
            {
                "skill": "Python", "diff": "Beginner", "marks": 1,
                "text": "Which of the following Python standard data types is immutable?",
                "code": None,
                "exp": "Tuples are immutable; once created, their elements cannot be appended, removed, or modified.",
                "opts": [
                    ("List", False),
                    ("Tuple", True),
                    ("Dictionary", False),
                    ("Set", False)
                ]
            },
            {
                "skill": "Python", "diff": "Intermediate", "marks": 2,
                "text": "What is a Python Decorator and how is it implemented?",
                "code": "@timer\ndef process_data(): ...",
                "exp": "A decorator is a callable that takes another function as an argument, extends its behavior, and returns a modified function.",
                "opts": [
                    ("A syntax theme in VS Code", False),
                    ("A higher-order function that takes a function as input and extends or modifies its behavior without editing its code", True),
                    ("A compile-time directive to translate Python to C", False),
                    ("A database trigger in SQLite", False)
                ]
            },
            {
                "skill": "Python", "diff": "Advanced", "marks": 3,
                "text": "How does Python handle memory management and garbage collection for cyclical references?",
                "code": None,
                "exp": "Python primarily uses reference counting, supplemented by a cyclic garbage collector that periodically detects reference cycles.",
                "opts": [
                    ("Python relies solely on manual free() calls from developers", False),
                    ("It combines primary reference counting with a cyclic generational garbage collector that identifies unreachable cycles", True),
                    ("It reboots the application process when RAM reaches 90%", False),
                    ("It converts cyclical references into weak pointers automatically", False)
                ]
            }
        ]
    },
    {
        "title": "Logical Reasoning & Problem Solving Assessment",
        "category": "Problem Solving",
        "role_slug": "problem-solving",
        "desc": "Evaluates analytical deduction, algorithmic scenarios, pattern recognition, and systematic edge-case debugging.",
        "mins": 20,
        "pass_pct": 60.0,
        "questions": [
            {
                "skill": "Problem Solving", "diff": "Intermediate", "marks": 2,
                "text": "You have a 3-liter bucket and a 5-liter bucket, with unlimited water. How can you measure exactly 4 liters?",
                "code": None,
                "exp": "Fill 5L -> pour into 3L (leaving 2L in 5L bucket) -> empty 3L -> transfer 2L into 3L bucket -> fill 5L -> pour 1L into 3L bucket (until full) -> leaves 4L in 5L bucket.",
                "opts": [
                    ("Fill 3L bucket twice and estimate 4L visually", False),
                    ("Fill 5L bucket, pour into 3L (leaves 2L); empty 3L, move 2L to 3L bucket; fill 5L, pour 1L to fill 3L (leaves 4L in 5L bucket)", True),
                    ("It is mathematically impossible with odd-numbered capacities", False),
                    ("Fill both buckets half-way", False)
                ]
            },
            {
                "skill": "Critical Thinking", "diff": "Intermediate", "marks": 2,
                "text": "A software service failure rate increases exponentially during peak traffic hours, but CPU and RAM on server nodes stay below 35%. What is the most likely root cause?",
                "code": None,
                "exp": "When compute utilization is low while failures spike, bottlenecks typically lie in connection pool exhaustion (database/redis pool limits) or thread starvation.",
                "opts": [
                    ("The physical motherboard clock frequency is too high", False),
                    ("Database connection pool exhaustion or downstream thread pool starvation", True),
                    ("Python syntax indentation errors", False),
                    ("The hard drive has too many open terminal tabs", False)
                ]
            },
            {
                "skill": "Problem Solving", "diff": "Beginner", "marks": 1,
                "text": "If five machines take 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
                "code": None,
                "exp": "Each machine takes 5 minutes to make 1 widget. Thus, 100 machines working in parallel make 100 widgets in 5 minutes.",
                "opts": [
                    ("100 minutes", False),
                    ("5 minutes", True),
                    ("20 minutes", False),
                    ("1 minute", False)
                ]
            },
            {
                "skill": "Critical Thinking", "diff": "Advanced", "marks": 3,
                "text": "In a distributed binary search, if the search space size N is halved at each step, how many comparisons are needed for N = 1,000,000?",
                "code": "2^20 = 1,048,576",
                "exp": "log2(1,000,000) approx 20 comparisons.",
                "opts": [
                    ("1,000 comparisons", False),
                    ("At most 20 comparisons", True),
                    ("500,000 comparisons", False),
                    ("100 comparisons", False)
                ]
            },
            {
                "skill": "Problem Solving", "diff": "Intermediate", "marks": 2,
                "text": "When diagnosing an intermittent network timeout error that occurs once every 500 requests, what debugging methodology is most effective?",
                "code": None,
                "exp": "Distributed tracing with correlation IDs and percentile latency telemetry (p99/p99.9) isolates intermittent tail latency spikes.",
                "opts": [
                    ("Restarting the server every 10 minutes blindly", False),
                    ("Enabling distributed request tracing with correlation IDs and inspecting p99 tail latency logs", True),
                    ("Removing all error handling try/catch blocks", False),
                    ("Switching programming languages immediately", False)
                ]
            },
            {
                "skill": "Critical Thinking", "diff": "Beginner", "marks": 1,
                "text": "What is the logical fallacy of concluding that because event B occurred after event A, event A must have caused event B?",
                "code": None,
                "exp": "Post hoc ergo propter hoc ('after this, therefore because of this') conflates chronological sequence with causal relationship.",
                "opts": [
                    ("Confirmation Bias", False),
                    ("Post hoc ergo propter hoc (False Cause)", True),
                    ("Straw Man Fallacy", False),
                    ("Ad Hominem", False)
                ]
            }
        ]
    }
]

def seed_all_assessments():
    db: Session = SessionLocal()
    try:
        # Pre-load skills map
        skills = {s.name: s.id for s in db.query(Skill).all()}
        print(f"Loaded {len(skills)} skills from database.")

        total_questions_seeded = 0
        total_assessments_seeded = 0

        for a_data in ASSESSMENTS_AND_QUESTIONS:
            # Check or create assessment
            ass = db.query(Assessment).filter(Assessment.title == a_data["title"]).first()
            if not ass:
                ass = Assessment(
                    title=a_data["title"],
                    category=a_data["category"],
                    role_slug=a_data.get("role_slug"),
                    description=a_data["desc"],
                    time_limit_minutes=a_data["mins"],
                    passing_percentage=a_data["pass_pct"],
                    total_questions=len(a_data["questions"]),
                    is_active=True
                )
                db.add(ass)
                db.commit()
                db.refresh(ass)
                total_assessments_seeded += 1
            else:
                # Update role_slug, description, and total_questions
                ass.role_slug = a_data.get("role_slug")
                ass.description = a_data["desc"]
                ass.category = a_data["category"]
                ass.time_limit_minutes = a_data["mins"]
                ass.passing_percentage = a_data["pass_pct"]
                ass.total_questions = len(a_data["questions"])
                db.commit()

            # Seed questions for this assessment
            for q_data in a_data["questions"]:
                existing_q = db.query(Question).filter(
                    Question.assessment_id == ass.id,
                    Question.question_text == q_data["text"]
                ).first()

                skill_id = skills.get(q_data["skill"])

                if not existing_q:
                    new_q = Question(
                        assessment_id=ass.id,
                        skill_id=skill_id,
                        question_text=q_data["text"],
                        question_type="mcq",
                        difficulty=q_data["diff"],
                        marks=q_data["marks"],
                        explanation=q_data["exp"],
                        code_snippet=q_data.get("code")
                    )
                    db.add(new_q)
                    db.commit()
                    db.refresh(new_q)

                    # Add options
                    for opt_text, is_corr in q_data["opts"]:
                        opt = QuestionOption(
                            question_id=new_q.id,
                            option_text=opt_text,
                            is_correct=is_corr
                        )
                        db.add(opt)
                    db.commit()
                    total_questions_seeded += 1
                else:
                    # Update explanation and marks
                    existing_q.explanation = q_data["exp"]
                    existing_q.marks = q_data["marks"]
                    existing_q.difficulty = q_data["diff"]
                    existing_q.code_snippet = q_data.get("code")
                    existing_q.skill_id = skill_id
                    db.commit()

            # Update count on assessment
            count = db.query(Question).filter(Question.assessment_id == ass.id).count()
            ass.total_questions = count
            db.commit()

        print(f"SUCCESS: Seeded/Updated {len(ASSESSMENTS_AND_QUESTIONS)} assessments with {total_questions_seeded} questions!")

    except Exception as e:
        db.rollback()
        print(f"ERROR seeding questions: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_all_assessments()
