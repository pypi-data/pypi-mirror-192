# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umlaut', 'umlaut.examples']

package_data = \
{'': ['*']}

install_requires = \
['mlflow==1.28.0', 'psycopg2==2.9.3']

setup_kwargs = {
    'name': 'umlaut',
    'version': '0.2.3',
    'description': 'Umlaut simplifies operational analytics for data teams',
    'long_description': '# Umlaut\n\nUmlaut simplifies operational analytics for data teams. Centralize critical business logic and track all uses of that logic in a single location. Umlaut is built on top of [MLflow](https://bit.ly/3eHJsx3) and offers a simple Python class to assist with tracking and running models. Umlaut is designed to be used by data teams of all sizes and is a great tool for small teams without dedicated data scientists.\n\n### Umlaut offers\n- simple commands to track and run models\n- history of all model query inputs and results\n- model lifecycle management\n- access to multiple versions of the same model\n- a user interface with `MLflow`\n- model audit tracking history (roadmap)\n- auto-deployed models that can be queried through an API (roadmap)\n\n### Installing Umlaut\n`pip install umlaut`\n___\n## MLflow Setup\n[MLflow](https://bit.ly/3eHJsx3) is a powerful machine learning library created by Databricks for data science teams. It offers an extensive API for tracking and querying models, but the learning curve can be a deterrent for small teams without dedicated data scientists. Umlaut strips away much of the complexity of MLflow while maintaining the immense value of tracking and running your models in a single location. \n\nMLflow has two requirements:\n1) A model artifact storage location\n- This can be a local directory or a cloud storage URI. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#artifact-stores).\n2) A model registry\n- The model registry is where model changes and query data are stored. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#backend-stores).\n\nAn `mlflow server` must be running in order to work with Umlaut. The command to start an MLflow server with local artifact storage and a Postgres model registry is as follows:\n\n`mlflow server --backend-store-uri postgresql+psycopg2://admin:password@localhost:5432/database --default-artifact-root "mlruns/"`\n\nOnce the server is running you can navigate to the MLflow UI and begin interacting with models.\n\n____\n## Core Functionality\nUmlaut offers a simple Python class to assist with saving and running business logic in MLflow. The class has two methods:\n\n- `track_model`: Converts a data science model or block of business logic into an MLflow compatible `model`\n- `run_model`: Runs a previously trained `model` and saves audit metadata\n\n### Deploying models with Umlaut\nCustom `models` can be deployed simply by running `track_model()`. Ensure that the model code block is in a Python `Class` and follow the example below.\n\n```\nclass ExampleModel():\n    """Example business logic that can be wrapped into a model.\n       The class must contain a \'run\' method with the input config\n       mapped to the corresponding model parameters."""\n\n    def business_logic(self, revenue: int) -> bool:\n        return revenue > 5\n\n    def run(self, model_input: dict) -> bool:\n        return self.business_logic(revenue=model_input.get("revenue"))\n\n\nif __name__ == "__main__":\n    """Saves the model to MLflow in an experiment run"""\n    from umlaut import Umlaut\n\n    Umlaut().track_model(\n        model=ExampleModel(),\n        model_name="Revenue Forecast",\n        run_name="Update",\n    )\n```\n\nThis will push the latest changes of `ExampleModel()` to MLflow as a new model version. Navigate to the MLflow server where you can find details for the example "Quarterly Revenue" model.\n\n\n### Querying models with Umlaut\nOnce a model is deployed in MLflow with `track_model()`, it can be queried by calling `run_model()`.\n\n```\nfrom umlaut import Umlaut\n\nresult = Umlaut().run_model(\n    model_name="Revenue Forecast",\n    input_config={"revenue": 3},\n    stage="Staging",\n)\nprint(f"Revenue will{\'\' if result else \' not\'} exceed target")\n```\n\nRunning the simple `Revenue Forecast` model with `revenue = 3` will return `False` as the revenue does not exceed the target of 5. The call to the model will be tracked in MLflow with model inputs and results.\n',
    'author': 'Andrew Dunkel',
    'author_email': 'andrew.dunkel1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andrewdunkel/uMLaut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.12,<4.0',
}


setup(**setup_kwargs)
