## 🔗 Dependencies

### Local dependencies

To install and run the project locally, you need the following dependencies.

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| pyenv | ≥2.3.36 | Multiple Python versions (optional) | [Install Guide](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) |
| Python | 3.11 | Runtime environment | [Download](https://www.python.org/downloads/) |
| Poetry | ≥1.8.3 | Package management | [Install Guide](https://python-poetry.org/docs/#installation) |
| Docker | ≥27.1.1 | Containerization | [Install Guide](https://docs.docker.com/engine/install/) |
| AWS CLI | ≥2.15.42 | Cloud management | [Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| Git | ≥2.44.0 | Version control | [Download](https://git-scm.com/downloads) |

### Cloud services

The code also uses and depends on the following cloud services:

| Service | Purpose |
|---------|---------|
| [HuggingFace](https://huggingface.com/) | Model registry |
| [Comet ML](https://www.comet.com/site/) | Experiment tracker |
| [Opik](https://www.comet.com/site/products/opik/) | Prompt monitoring |
| [ZenML](https://www.zenml.io/) | Orchestrator and artifacts layer |
| [AWS](https://aws.amazon.com/) | Compute and storage |
| [MongoDB](https://www.mongodb.com/) | NoSQL database |
| [Qdrant](https://qdrant.tech/) | Vector database |
| [GitHub Actions](https://github.com/features/actions) | CI/CD pipeline |

## 🗂️ Project Structure

Here is the directory overview:

```bash
.
├── code_snippets/       # Standalone example code
├── configs/             # Pipeline configuration files
├── llm_engineering/     # Core project package
│   ├── application/    
│   ├── domain/         
│   ├── infrastructure/ 
│   ├── model/         
├── pipelines/           # ML pipeline definitions
├── steps/               # Pipeline components
├── tests/               # Test examples
├── tools/               # Utility scripts
│   ├── run.py
│   ├── ml_service.py
│   ├── rag.py
│   ├── data_warehouse.py
```

`src/`  is the main Python package implementing LLM and RAG functionality. It follows Domain-Driven Design (DDD) principles:

- `domain/`: Core business entities and structures
- `application/`: Business logic, crawlers, and RAG implementation
- `model/`: LLM training and inference
- `infrastructure/`: External service integrations (AWS, Qdrant, MongoDB, FastAPI)

The code logic and imports flow as follows: `infrastructure` → `model` → `application` → `domain`

`pipelines/`: Contains the ZenML ML pipelines, which serve as the entry point for all the ML pipelines. Coordinates the data processing and model training stages of the ML lifecycle.

`steps/`: Contains individual ZenML steps, which are reusable components for building and customizing ZenML pipelines. Steps perform specific tasks (e.g., data loading, preprocessing) and can be combined within the ML pipelines.

`tools/`: Utility scripts used to call the ZenML pipelines and inference code:
- `run.py`: Entry point script to run ZenML pipelines.
- `ml_service.py`: Starts the REST API inference server.
- `rag.py`: Demonstrates usage of the RAG retrieval module.
- `data_warehouse.py`: Used to export or import data from the MongoDB data warehouse through JSON files.

`configs/`: ZenML YAML configuration files to control the execution of pipelines and steps.

`code_snippets/`: Independent code examples that can be executed independently.

## 💻 Installation

### 1. Clone the Repository

Start by cloning the repository and navigating to the project directory:

```bash
git clone https://github.com/abhimgkku/CO-Writer.git
cd CO-Writer 
```

Next, prepare your Python environment and its adjacent dependencies. 

### 2. Set Up Python Environment

The project requires Python 3.11. You can either use your global Python installation or set up a project-specific version using pyenv.

#### Option A: Using Global Python (if version 3.11 is installed)

Verify your Python version:

```bash
python --version  
```

#### Option B: Using pyenv (recommended)

1. Verify pyenv installation:

```bash
pyenv --version   
```

2. Install Python 3.11.8:

```bash
pyenv install 3.11.8
```

3. Verify the installation:

```bash
python --version  
```

4. Confirm Python version in the project directory:

```bash
python --version
# Output: Python 3.11.8
```
### 3. Install Dependencies

The project uses Poetry for dependency management.

1. Verify Poetry installation:

```bash
poetry --version  
```

2. Set up the project environment and install dependencies:

```bash
poetry env use 3.11
poetry install --without aws
poetry run pre-commit install
```

This will:

- Configure Poetry to use Python 3.11
- Install project dependencies (excluding AWS-specific packages)
- Set up pre-commit hooks for code verification

### 4. Activate the Environment

run all the scripts using [Poe the Poet](https://poethepoet.natn.io/index.html).

1. Start a Poetry shell:

```bash
poetry shell
```

2. Run project commands using Poe the Poet:

```bash
poetry poe ...
```
### Alternative Command Execution

If you're experiencing issues with `poethepoet`, you can still run the project commands directly through Poetry. Here's how:

1. Look up the command definition in `pyproject.toml`
2. Use `poetry run` with the underlying command

#### Example:
Instead of:
```bash
poetry poe local-infrastructure-up
```
Use the direct command from pyproject.toml:
```bash
poetry run <actual-command-from-pyproject-toml>
```
Note: All project commands are defined in the [tool.poe.tasks] section of pyproject.toml
</details>

### 5. Local Development Setup

After instaliing all the dependencies, create and fill a `.env` file with your credentials to appropriately interact with other services and run the project. and fill the .env file with essential variables, an example .env file is in the github repo.

2. Now, let's understand how to fill in all the essential variables within the `.env` file. The following are the mandatory settings:

#### OpenAI

To authenticate to OpenAI's API, must fill out the `OPENAI_API_KEY` env var with an authentication token.

```env
OPENAI_API_KEY=your_api_key_here
```
#### Hugging Face

To authenticate to Hugging Face, must fill out the `HUGGINGFACE_ACCESS_TOKEN` env var with an authentication token.

```env
HUGGINGFACE_ACCESS_TOKEN=your_token_here
```
#### Comet ML & Opik

To authenticate to Comet ML (required only during training) and Opik, must fill out the `COMET_API_KEY` env var with your authentication token.

```env
COMET_API_KEY=your_api_key_here
```

### 6. Deployment Setup

When deploying the project to the cloud, you must set additional settings for Mongo, Qdrant, and AWS. If you are just working locally, the default values of these env vars will work out of the box.

#### MongoDB

We must change the `DATABASE_HOST` env var with the URL pointing to your cloud MongoDB cluster.

```env
DATABASE_HOST=your_mongodb_url
```
#### Qdrant

Change `USE_QDRANT_CLOUD` to `true`, `QDRANT_CLOUD_URL` with the URL point to your cloud Qdrant cluster, and `QDRANT_APIKEY` with its API key.

```env
USE_QDRANT_CLOUD=true
QDRANT_CLOUD_URL=your_qdrant_cloud_url
QDRANT_APIKEY=your_qdrant_api_key
```
#### AWS

For your AWS set-up to work correctly, you need the AWS CLI installed on your local machine and properly configured with an admin user (or a user with enough permissions to create new SageMaker, ECR, and S3 resources; using an admin user will make everything more straightforward).

```bash
AWS_REGION=eu-central-1 # Change it with your AWS region.
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
```
```bash
cat ~/.aws/credentials
```
## 🏗️ Infrastructure

### Local infrastructure (for testing and development)

When running the project locally,host a MongoDB and Qdrant database using Docker. Also, a testing ZenML server is made available through their Python package.

For ease of use, you can start the whole local development infrastructure with the following command:
```bash
poetry poe local-infrastructure-up
```

Also, you can stop the ZenML server and all the Docker containers using the following command:
```bash
poetry poe local-infrastructure-down
```
Start the inference real-time RESTful API:
```bash
poetry poe run-inference-ml-service
```
#### ZenML

Dashboard URL: `localhost:8237`

Default credentials:
  - `username`: default
  - `password`: 

#### Qdrant

REST API URL: `localhost:6333`

Dashboard URL: `localhost:6333/dashboard`

#### MongoDB

Database URI: `your database url`

Database name: `cowriter`

Default credentials:
  - `username`: 
  - `password`: 

### Cloud infrastructure (for production)

First, reinstall your Python dependencies with the AWS group:
```bash
poetry install --with aws
```
#### AWS SageMaker

```bash
poetry poe create-sagemaker-role
```
It will create a `sagemaker_user_credentials.json` file at the root of your repository with your new `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` values. **But before replacing your new AWS credentials, also run the following command to create the execution role (to create it using your admin credentials).**

To create the IAM execution role used by AWS SageMaker to access other AWS resources on our behalf, run the following:
```bash
poetry poe create-sagemaker-execution-role
```
It will create a `sagemaker_execution_role.json` file at the root of your repository with your new `AWS_ARN_ROLE` value. Add it to your `.env` file. 

Once you've updated the `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, and `AWS_ARN_ROLE` values in your `.env` file, you can use AWS SageMaker. **Note that this step is crucial to complete the AWS setup.**

#### Training

start the training pipeline through ZenML by running the following:
```bash
poetry poe run-training-pipeline
```
This will start the training code using the configs from `configs/training.yaml` directly in SageMaker. You can visualize the results in Comet ML's dashboard.

start the evaluation pipeline through ZenML by running the following:
```bash
poetry poe run-evaluation-pipeline
```
This will start the evaluation code using the configs from `configs/evaluating.yaml` directly in SageMaker. You can visualize the results in `*-results` datasets saved to your Hugging Face profile.

#### Inference

To create an AWS SageMaker Inference Endpoint, run:
```bash
poetry poe deploy-inference-endpoint
```
To test it out, run:
```bash
poetry poe test-sagemaker-endpoint
```
To delete it, run:
```bash
poetry poe delete-inference-endpoint
```
#### AWS: ML pipelines, artifacts, and containers

The ML pipelines, artifacts, and containers are deployed to AWS by leveraging ZenML's deployment features.

#### GitHub Actions

We use GitHub Actions to implement CI/CD pipelines. To implement your own, you have to fork our repository and set the following env vars as Actions secrets in your forked repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ECR_NAME`
- `AWS_REGION`

## ⚡ Pipelines

All the ML pipelines will be orchestrated behind the scenes by [ZenML](https://www.zenml.io/). A few exceptions exist when running utility scrips, such as exporting or importing from the data warehouse.

The ZenML pipelines are the entry point for most processes throughout this project. They are under the `pipelines/` folder. Thus, when you want to understand or debug a workflow, starting with the ZenML pipeline is the best approach.

To see the pipelines running and their results:
- go to your ZenML dashboard
- go to the `Pipelines` section
- click on a specific pipeline (e.g., `feature_engineering`)
- click on a specific run (e.g., `feature_engineering_run_2024_06_20_18_40_24`)
- click on a specific step or artifact of the DAG to find more details about it

### Data pipelines

Run the data collection ETL:
```bash
poetry poe run-digital-data-etl
```
Run the feature engineering pipeline:
```bash
poetry poe run-feature-engineering-pipeline
```

Generate the instruct dataset:
```bash
poetry poe run-generate-instruct-datasets-pipeline
```

Generate the preference dataset:
```bash
poetry poe run-generate-preference-datasets-pipeline
```

Run all of the above compressed into a single pipeline:
```bash
poetry poe run-end-to-end-data-pipeline
```

### Utility pipelines

Export the data from the data warehouse to JSON files:
```bash
poetry poe run-export-data-warehouse-to-json
```

Import data to the data warehouse from JSON files (by default, it imports the data from the `data/data_warehouse_raw_data` directory):
```bash
poetry poe run-import-data-warehouse-from-json
```

Export ZenML artifacts to JSON:
```bash
poetry poe run-export-artifact-to-json-pipeline
```

This will export the following ZenML artifacts to the `output` folder as JSON files (it will take their latest version):
- cleaned_documents.json
- instruct_datasets.json
- preference_datasets.json
- raw_documents.json

You can configure what artifacts to export by tweaking the `configs/export_artifact_to_json.yaml` configuration file.

### Training pipelines

Run the training pipeline:
```bash
poetry poe run-training-pipeline
```

Run the evaluation pipeline:
```bash
poetry poe run-evaluation-pipeline
```
### Inference pipelines

Call the RAG retrieval module with a test query:
```bash
poetry poe call-rag-retrieval-module
```

Start the inference real-time RESTful API:
```bash
poetry poe run-inference-ml-service
```

Call the inference real-time RESTful API with a test query:
```bash
poetry poe call-inference-ml-service
```
### Linting & formatting (QA)

Check or fix your linting issues:
```bash
poetry poe lint-check
poetry poe lint-fix
```

Check or fix your formatting issues:
```bash
poetry poe format-check
poetry poe format-fix
```

Check the code for leaked credentials:
```bash
poetry poe gitleaks-check
```

### Tests

Run all the tests using the following command:
```bash
poetry poe test
```

## 🏃 Run project

Based on the setup and usage steps described above, assuming the local and cloud infrastructure works and the `.env` is filled as expected, follow the next steps to run the LLM system end-to-end:

### Data

1. Collect data: `poetry poe run-digital-data-etl`

2. Compute features: `poetry poe run-feature-engineering-pipeline`

3. Compute instruct dataset: `poetry poe run-generate-instruct-datasets-pipeline`

4. Compute preference alignment dataset: `poetry poe run-generate-preference-datasets-pipeline`

### Training

5. SFT fine-tuning Llamma 3.1: `poetry poe run-training-pipeline`

6. For DPO, go to `configs/training.yaml`, change `finetuning_type` to `dpo`, and run `poetry poe run-training-pipeline` again

7. Evaluate fine-tuned models: `poetry poe run-evaluation-pipeline`

### Inference

8. Call only the RAG retrieval module: `poetry poe call-rag-retrieval-module`

9. Deploy the LLM Twin microservice to SageMaker: `poetry poe deploy-inference-endpoint`

10. Test the LLM Twin microservice: `poetry poe test-sagemaker-endpoint`

11. Start end-to-end RAG server: `poetry poe run-inference-ml-service`

12. Test RAG server: `poetry poe call-inference-ml-service`
