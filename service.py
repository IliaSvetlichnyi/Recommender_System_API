import os
from catboost import CatBoostClassifier, CatBoost
import pandas as pd
from sqlalchemy import create_engine
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
import pydantic
from tqdm import tqdm
from typing import List


'''
MODEL LOADING FUNCTIONS
'''
# Check if the code runs in LMS or locally
def get_model_path(path: str) -> str:

    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH

class CatBoostWrapper(CatBoost):
    def predict_proba(self, X):
        return self.predict(X, prediction_type='Probability')

# Loading model
def load_models():
    model_path = get_model_path("/Users/ilya/Desktop/GitHub_Repositories/My_knowledge_base/Курс Start ML/Финальный проект/DataSets/catboost_model_data10_best_hitrate.cbm")
    model = CatBoostWrapper()
    model.load_model(model_path)
    return model

'''
FETCHING DATA FROM DATABASE
'''
# Define a function to fetch data from the PostgreSQL database
def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    total_rows_for_5_percent = 3844565
    # total_rows_for_10_percent = 7689263  # total number of rows in your dataset

    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
        "postgres.lab.karpov.courses:6432/startml"
    )
    conn = engine.connect().execution_options(stream_results=True)

    chunks = []
    with tqdm(total=total_rows_for_5_percent, desc="Loading data") as pbar:
        for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
            chunks.append(chunk_dataframe)
            pbar.update(CHUNKSIZE)

    conn.close()

    return pd.concat(chunks, ignore_index=True)

def load_features() -> pd.DataFrame:
    query = "ilia_svetlichnyi_features_lesson_22_5_percent"
    return batch_load_sql(query)


def predict_posts(user_id: int, limit: int):
    # Filter records related to the specific user_id
    user_features = features[features.user_id == user_id]

    # Calculate probabilities for each post_id for the specific user_id
    user_features['probas'] = model.predict_proba(user_features.drop('user_id', axis=1))[:, 1]

    # Sort the DataFrame by 'probas' in descending order and get the first 'limit' records
    top_posts = user_features.sort_values('probas', ascending=False).iloc[:limit]

    # Return the 'post_id' of the best records as a list
    return top_posts['post_id'].tolist()


def load_post_texts_df():
    global post_texts_df
    print("Uploading all the texts of the posts...")
    query = "SELECT * FROM post_text_df"
    engine = create_engine(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@"
        "postgres.lab.karpov.courses:6432/startml"
    )
    post_texts_df = pd.read_sql(query, con=engine)
    print("All the texts of the posts have been successfully loaded into memory.")


def load_post_texts(post_ids: List[int]) -> List[dict]:
    global post_texts_df
    if post_texts_df is None:
        raise ValueError("The table with the texts of the posts is not loaded. First call the 'load_post_text_df()' function.")

    # Extracting records from memory
    records_df = post_texts_df[post_texts_df['post_id'].isin(post_ids)]
    return records_df.to_dict("records")


'''
LOADING MODELS AND FEATURES (WITHOUT THREADING)
'''

model = load_models()
print("Model loaded")
features = load_features()
print("Data loaded")
# Global variable to store data
post_texts_df = None
load_post_texts_df()


'''
FASTAPI
'''
class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


app = FastAPI()

@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
        id: int,
        time: datetime,
        limit: int = 5) -> List[PostGet]:
    post_ids = predict_posts(id, limit)
    records = load_post_texts(post_ids)

    posts = []
    for rec in records:
        rec["id"] = rec.pop("post_id")
        try:
            posts.append(PostGet(**rec))
        except pydantic.error_wrappers.ValidationError as e:
            print(f"Validation error for record {rec}: {e}")
    return posts
