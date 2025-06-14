# MLOps - End to End Pipeline
Total End to End ML CI/CD Pipeline implementation

## Description:
A Machine Learning project with full end to end implementation of a
 ML Orchestration pipeline, version control for data and models using
 Jenkins, MLFlow, Airflow, DVC and Github Actions.

## How to Run (WSL) :
### Jenkins:-
- docker run -d -p 8070:8080 -p 50000:50000 jenkins/jenkins:lts

### Airflow:-
- docker compose up -d

### DVC (with Google Drive) :- 
- make gdrive service account
- connect gdrive public folder with it
- git init
- dvc remote list
- dvc remote add -d gdrive_remote gdrive://link_to_folder
- dvc remote modify gdrive_remote gdrive_use_service_account true
- dvc remote modify gdrive_remote gdrive_service_account_json_file_path src/dvc.json // api key for dvc generated
- dvc repro  // or dvc push
- dvc dag
- dvc pull

### MLFLOW :-
- mlflow ui
- python mlflow_.py

*Merge a Pull Request to Start the whole pipeline*
