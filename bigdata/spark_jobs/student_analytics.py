"""
PySpark Batch Analytics Job: Student Skill & Career Telemetry
Processes enterprise student datasets at scale for institutional reporting.
"""

def run_spark_analytics(input_path: str = "datasets/sample_100k_students.parquet"):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F

        spark = SparkSession.builder \
            .appName("EduCareer_BigData_Analytics") \
            .master("local[*]") \
            .getOrCreate()

        print(f"Loading dataset from: {input_path}")
        df = spark.read.parquet(input_path)

        # 1. Skill Proficiencies
        print("Calculating skill aggregation metrics...")
        skill_metrics = df.groupBy("skill").agg(
            F.count("score").alias("total_assessments"),
            F.avg("score").alias("avg_score"),
            F.stddev("score").alias("score_variance")
        ).orderBy(F.desc("total_assessments"))
        skill_metrics.show(10)

        # 2. Career Demand & Gap Analysis
        print("Computing common skill gaps by career aspiration...")
        gaps = df.filter(df.score < 60).groupBy("desired_career", "skill").count().orderBy(F.desc("count"))
        gaps.show(10)

        spark.stop()
        print("PySpark Analytics completed successfully.")

    except ImportError:
        print("PySpark is not installed in the local environment. Use the FastAPI analytics API with Pandas vectorized engine.")

if __name__ == "__main__":
    run_spark_analytics()
