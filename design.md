# Project Design – Moodies CLV Dashboard

This project is a react dashboard that shows insights and machine learning predictions for a Shopify store using data from Shopify and Klaviyo.

The project follows a Domain-Driven Design (DDD) structure, which means we split the project into separate layers, each with its own responsibility.

---

## Overview of Layers

### 1. **Interface Layer**
- This is the user facing layer, it dependes on the application layer to retrieve data, that is served to the user.
- Folder: `interfaces`
- The ui made with react lives in `interfaces\ui\mu-ui`.
- It shows pages like:
  - Overview
  - Customer Segments
  - CLV Analysis
  - Next Purchase Prediction
- It also handles user login.
- The REST API made with Flask lives in `interfaces\rest\v1`.
- It exposes multiple endpoint for the:
  - insights
  - Customer Segments
  - CLV Analysis
  - Next Purchase Prediction
- It also handles user login.

### 2. **Application Layer**
- Folder: `application/`
- This layer connects the interface with the domain & infra layer
- Each business logic living in the domain is represented with its own service. (e.g. insights_service.py serves insights data that is outputed by the domain logic to the interface layer)
- 
### 3. **Domain Layer**
- Folder: `domains/`
- This is the business core logic lays.
- It has 5 domains:
  
  #### a. `authentication/`
  - Authenticates users that log in.
  - Validates them against a users in an SQLite database.

  #### b. `insights/`
  - Cleans and processes data to generate insights.
  - Saves results in `resources/data/processed/`.

  #### c. `clv/`, `npd/`, `segment/`
  - Each domain:
    - Cleans and prepares its own data.
    - Engineers features and prepares data needed by the model.
    - Loads and train machine learning models.

### 4. **Infrastructure Layer**
- This layer is created to interface with external services.
- Folder: `infra/clients/`
- This layer fetches data from external APIs:
  - `klaviyo.py` fetches customer data
  - `shopify.py` fetches order data
- Data is saved to `resources/data/raw/`

---


## 📁 Data Folders

- `resources/data/raw/` → raw data from APIs
- `resources/data/processed/` → cleaned and feature-engineered data

## UML


### Process Flow diagram:

``` mermaid
flowchart TD
    Start[Start] --> Login[User logs in via Streamlit]
    Login --> AuthService[Authenticate via user_service]
    AuthService --> CheckDataModels{Data & Models exist?}

    Force_Refresh --> run_clv_pipeline
    Force_Refresh --> run_npd_pipeline
    Force_Refresh --> run_segmentation_pipeline
    Force_Refresh --> run_insights_pipeline

    CheckDataModels -- No --> run_clv_pipeline[Run CLV model pipeline]
    run_clv_pipeline --> CLV_Clean[Clean CLV data]
    CLV_Clean --> CLV_Engineer[Feature engineer CLV]
    CLV_Engineer --> CLV_Prepare[Prepare CLV for model]
    CLV_Prepare --> TrainCLVModels[Train CLV models]
    TrainCLVModels --> ShowResults

    CheckDataModels -- No --> run_npd_pipeline[Run NPD model pipeline]
    run_npd_pipeline --> NPD_Clean[Clean NPD data]
    NPD_Clean --> NPD_Engineer[Feature engineer NPD]
    NPD_Engineer --> NPD_Prepare[Prepare NPD for model]
    NPD_Prepare --> TrainNPDModels[Train Next Purchase date models]
    TrainNPDModels --> ShowResults


    CheckDataModels -- No --> run_segmentation_pipeline[Run segmentaion model pipeline]
    run_segmentation_pipeline --> SEG_Clean[Clean Segment data]
    SEG_Clean --> SEG_Engineer[Feature engineer Segment]
    SEG_Engineer --> SEG_Prepare[Prepare Segment for model]
    SEG_Prepare --> TrainSEGModels[Train segmentaion models]
    TrainSEGModels --> ShowResults
    
    CheckDataModels -- No --> run_insights_pipeline[Run data insights pipeline]
    run_insights_pipeline --> INS_Clean[Clean Insights data]
    INS_Clean --> INS_Engineer[Engineer insights]
    INS_Engineer --> INS_Prepare[Prepare insights output]
    INS_Prepare --> ShowResults

    CheckDataModels -- Yes --> Predict[Run model predictions]
    TrainModels --> Predict

  
    Predict --> ShowResults[Display results in Streamlit UI]
    ShowResults --> End[Done]
```


### Activity Diagram:
``` mermaid
flowchart TD
    start([Start]) --> login[User logs in]
    login --> validate[Validate credentials]

    validate --> validCheck{Are credentials valid?}
    validCheck -- No --> deny[Access denied]
    deny --> stop1([Stop])

    validCheck -- Yes --> checkData{Is data & model available?}
    checkData -- No --> runPipelines[Run pipelines for all CLV, NPD, Segment and Insights]
    checkData -- Yes --> predict[Run model predictions]

    runPipelines --> processData[Clean and process data]
    processData --> trainModels[Train models]
    trainModels --> predict

    predict --> display[Display results in dashboard]
    display --> refreshOption{Did user click refresh?}
    refreshOption -- Yes --> runPipelines
    refreshOption -- No --> stop2([Stop])
```
### Use case diagram

``` mermaid
flowchart TD
    user(["🧑 User Actor"]) --> login["Login to Dashboard"] & viewInsights["View Insights Page"] & clvPage["Use CLV Predictor"] & segmentPage["Use Customer Segmentation"] & npdPage["Use Next Purchase Date Predictor"] & refresh["Refresh Pipelines"]
    clvPage --> clvLeaderboard["View CLV Leaderboard"] & clvEmail["Search CLV by Email"]
    segmentPage --> segmentKPI["See Segment KPIs"] & segmentChart["View Segment Clusters"]
    npdPage --> timeline["See Next Purchase Timeline"] & table["See Prediction Table"]
    n1(["System Actor: Authentication system"]) --> n6[" "]
    n4(["System Actor: CLV model service"]) --> clvPage
    n8(["System Actor: Segment model service"]) --> segmentPage
    n10(["System Actor: NPD model service"]) --> npdPage
    n6@{ shape: anchor}
```

### Class Diagram


``` mermaid
classDiagram

%% === Services ===
class CLVService {
    +run_pipeline()
    +predict(email)
    +other_methods
    -other_properties
}
class NPDService {
    +run_pipeline()
    +predict(email)
    +other_methods
    -other_properties
}
class SegmentService {
    +run_pipeline()
    +get_cluster(email)
    +other_methods
    -other_properties
}
class InsightsService {
    +generate_insights()
    +other_methods
    -other_properties
}
class UserService {
    +authenticate(email, password)
    +other_methods
    -other_properties
}

%% === DTOs ===
class KlaviyoCustomersDTO {
    +email
    +first_name
    +last_name
    +other_properties
    +other_methods
}
class ShopifyOrdersDTO {
    +order_id
    +total
    +lineitems
    +other_properties
    +other_methods
}

%% === Domain: CLV ===
class CLVClean {
    +clean(df)
    +other_methods
    -other_properties
}
class CLVFeatureEngineer {
    +engineer_features(df)
    +other_methods
    -other_properties
}
class CLVModelPreProcess {
    +prepare_model_input(df)
    +other_methods
    -other_properties
}
class XGBoostModel {
    +load_model(path)
    +predict(X)
    +other_methods
    -other_properties
}

%% === Domain: NPD ===
class NPDClean {
    +clean(df)
    +other_methods
    -other_properties
}
class NPDFeatureEngineer {
    +engineer_features(df)
    +other_methods
    -other_properties
}
class NPDModelPreProcess {
    +prepare_model_input(df)
    +other_methods
    -other_properties
}
class NPDModel {
    +predict_next_purchase(df)
    +other_methods
    -other_properties
}

%% === Domain: Segment ===
class SegmentClean {
    +clean(df)
    +other_methods
    -other_properties
}
class SegmentEngineer {
    +engineer_features(df)
    +other_methods
    -other_properties
}
class SegmentModelPreProcess {
    +prepare_model_input(df)
    +other_methods
    -other_properties
}
class SegmentModel {
    +predict_cluster(df)
    +other_methods
    -other_properties
}

%% === Domain: Insights ===
class InsightsClean {
    +clean(df)
    +other_methods
    -other_properties
}
class InsightsEngineer {
    +engineer_metrics(df)
    +other_methods
    -other_properties
}

%% === Domain: Auth ===
class UserModel {
    +validate_credentials(email, password)
    +get_user_by_email(email)
    +other_methods
    -other_properties
}

%% === Infra Clients ===
class KlaviyoClient {
    +fetch_customers()
    +other_methods
    -other_properties
}
class ShopifyClient {
    +fetch_orders()
    +other_methods
    -other_properties
}

%% === Config ===
class Config {
    +load_config()
    +get(key)
    +other_methods
    -other_properties
}

%% === Relationships ===
CLVService --> CLVClean
CLVService --> CLVFeatureEngineer
CLVService --> CLVModelPreProcess
CLVService --> XGBoostModel
CLVService --> KlaviyoClient
CLVService --> ShopifyClient
CLVService --> Config

NPDService --> NPDClean
NPDService --> NPDFeatureEngineer
NPDService --> NPDModelPreProcess
NPDService --> NPDModel
NPDService --> KlaviyoClient
NPDService --> ShopifyClient
NPDService --> Config

SegmentService --> SegmentClean
SegmentService --> SegmentEngineer
SegmentService --> SegmentModelPreProcess
SegmentService --> SegmentModel
SegmentService --> KlaviyoClient
SegmentService --> ShopifyClient
SegmentService --> Config

InsightsService --> InsightsClean
InsightsService --> InsightsEngineer
InsightsService --> KlaviyoClient
InsightsService --> ShopifyClient
InsightsService --> Config

UserService --> UserModel
UserService --> Config

```


### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Streamlit_UI
    participant UserService
    participant CLVService
    participant KlaviyoClient
    participant ShopifyClient
    participant CLVModel

    User ->> Streamlit_UI: Log in
    Streamlit_UI ->> UserService: authenticate(email, password)
    UserService ->> UserService: Check credentials
    UserService -->> Streamlit_UI: Auth success

    User ->> Streamlit_UI: Click "CLV Analysis"
    Streamlit_UI ->> ModelService: run_pipeline()
    ModelService ->> KlaviyoClient: fetch_customers()
    ModelService ->> ShopifyClient: fetch_orders()
    ModelService ->> ModelService: clean, feature engineer, prepare data
    ModelService ->> MLModels: predict(input)
    MLModels -->> ModelService: predicted
    ModelService -->> Streamlit_UI: return results
    Streamlit_UI -->> User: Display predictions
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> LoggedOut

    LoggedOut --> LoggingIn: User submits login
    LoggingIn --> AuthFailed: Invalid credentials
    LoggingIn --> LoggedIn: Credentials valid

    LoggedIn --> ViewingDashboard: Navigates to dashboard
    ViewingDashboard --> ViewingCLV: Opens CLV page
    ViewingDashboard --> ViewingSegments: Opens Segments page
    ViewingDashboard --> ViewingNPD: Opens Next Purchase page

    ViewingCLV --> RefreshingCLV: User clicks refresh
    RefreshingCLV --> ViewingCLV

    ViewingNPD --> RefreshingNPD: User clicks refresh
    RefreshingNPD --> ViewingNPD

    ViewingSegments --> RefreshingSegments: User clicks refresh
    RefreshingSegments --> ViewingSegments

    LoggedIn --> LoggedOut: User logs out
```
