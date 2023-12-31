from tqdm import tqdm
import math
import pandas as pd
from sqlalchemy import create_engine
import time

X = pd.read_csv('/Users/ilya/Desktop/GitHub_Repositories/My_knowledge_base/Курс Start ML/Финальный проект/DataSets/data_5_percent.csv')

def upload_dataframe_in_chunks(data, table_name, engine, chunksize=10000):
    total_chunks = math.ceil(len(data) / chunksize)
    for i in tqdm(range(total_chunks), desc=f"Uploading to {table_name}"):
        chunk = data[i * chunksize : (i + 1) * chunksize]
        if_exists = "replace" if i == 0 else "append"
        chunk.to_sql(table_name, con=engine, if_exists=if_exists, index=False, method="multi")


engine = create_engine(
    "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
    "postgres.lab.karpov.courses:6432/startml"
)
chunksize = 10000
upload_dataframe_in_chunks(X, "ilia_svetlichnyi_features_lesson_22_v1", engine, chunksize=chunksize)