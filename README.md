## Personalized Post Recommender System via API

This repository showcases an API-driven recommendation system tailored to deliver customized text post recommendations, leveraging user data for enhanced personalization.

**Repository Overview**
- **creating_features.ipynb**: A Jupyter notebook dedicated to feature engineering and data preprocessing. It offers a deep dive into the methods employed for data extraction, transformation, and subsequent loading (ETL).
- **training_model.ipynb**: This notebook encapsulates the core of our machine learning approach, detailing data manipulation, model training, and performance evaluation. A plethora of ML techniques find their application here.
- **service.py**: Acting as the backbone of our API, this script orchestrates the request-response cycle, leveraging the trained model to curate recommendations. It ensures seamless HTTP request handling, data processing, and response dispatching.

**Dataset Breakdown**
- **user_data**: Comprehensive user-centric data, encompassing fields like age, city, experience group, OS, and more, totaling 163,205 records.
- **post_text_df**: A dedicated dataset for text post details, inclusive of the post ID, text, and topic, spanning 7,023 records.
- **feed_data**: A rich dataset capturing the intricacies of user-post interactions, which includes fields like timestamp, user ID, post ID, and more, amassing 76,892,800 entries.

**Feature Generation**
By synergizing user and post data, a gamut of features was crafted. Techniques such as text length calculations, accumulative post metrics, and category encoding were employed. The Catboost model's innate feature importance was capitalized on to cherry-pick the most influential features, while features prone to data leakage were judiciously excluded.

**Model Insights**
The Catboost classifier was harnessed for its robustness, trained with precision metrics like AUC. A special focus was on the Hitrate@5 metric, a custom inclusion, ensuring alignment with the model's purpose.

**Performance Metrics**
On the testing dataset, the Hitrate@5 metric, indicative of the user's propensity to like at least one of the top 5 recommended posts, clocked in at an impressive 0.63.

**API Specifications**
Employing FastAPI, our service accepts:
- **id**: User ID requesting posts.
- **time**: Datetime stamp (e.g., `datetime.datetime(year=2023, month=8, day=18, hour=15)`).
- **limit**: Desired number of post recommendations.

On querying, the API reciprocates with a list of 5 posts structured as:

```json
[
  {"id": 123, "text": "Breaking: Major Tech Acquisition...", "topic": "tech"},
  ...
]
```

**Installation & Execution**
*Prerequisites*:
- Python 3.x+
- Jupyter Notebook
- Essential Python libraries (as mentioned in `requirements.txt`).

*Deployment Steps*:
1. Clone the repository locally.
2. Install requisite Python packages.
3. Execute `creating_features.ipynb` for data wrangling.
4. Run `training_model.ipynb` to initiate model training.
5. Launch the API via `service.py`.

**System Workflow**

A schematic representation of our recommendation system is as follows:

**Workflow Diagram**

1. `creating_features.ipynb` undertakes user data ETL.
2. Processed data finds its way to an SQL server.
3. `training_model.ipynb` trains our recommendation model using this data.
4. `service.py` manages API requests, utilizing the model for recommendation derivation.
5. Recommendations are routed back to the user.

**Contributions**
Open to contributions! Kindly peruse the contribution guidelines before diving in.
