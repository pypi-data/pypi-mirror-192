# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigeye_airflow',
 'bigeye_airflow.airflow_ext',
 'bigeye_airflow.aws',
 'bigeye_airflow.bigeye_requests',
 'bigeye_airflow.functions',
 'bigeye_airflow.models',
 'bigeye_airflow.operators']

package_data = \
{'': ['*']}

install_requires = \
['Flask-OpenID>=1.3.0,<2.0.0',
 'apache-airflow==2.4.3',
 'bigeye-sdk>=0.4.45,<0.5.0']

setup_kwargs = {
    'name': 'bigeye-airflow',
    'version': '0.1.20',
    'description': 'Bigeye Airflow Library supports Airflow 2.4.3 and offers custom operators for interacting with your your bigeye workspace.',
    'long_description': '# Bigeye Airflow Operators for Airflow Versions 2.x\n\n## Operators\n### Create Metric Operator (bigeye_airflow.oerators.create_metric_operator)\n\nThe CreateMetricOperator creates metrics from a list of metric configurations provided to the operator.\nThis operator will fill in reasonable defaults like setting thresholds.  It authenticates through an Airflow connection \nID and offers the option to run the metrics after those metrics have been created.  Please review the link below to \nunderstand the structure of the configurations.\n\n[Create or Update Metric Swagger](https://docs.bigeye.com/reference/createmetric)\n\n#### Parameters\n1. connection_id: str - The Airfow connection ID used to store the required Bigeye credential.\n2. warehouse_id: int - The Bigeye source/warehouse id to which the metric configurations will be deployed.\n3. configuration: List[dict] - A list of metric configurations conforming to the following schema.\n    ```\n    schema_name: str\n    table_name: str\n    column_name: str\n    metric_template_id: uuid.UUID\n    metric_name: str\n    description: str\n    notifications: List[str]\n    thresholds: List[dict]\n    filters: List[str]\n    group_by: List[str]\n    user_defined_metric_name: str\n    metric_type: SimpleMetricCategory\n    default_check_frequency_hours: int\n    update_schedule: str\n    delay_at_update: str\n    timezone: str\n    should_backfill: bool\n    lookback_type: str\n    lookback_days: int\n    window_size: str\n    _window_size_seconds\n    ```\n4. run_after_upsert: bool - If true it will run the metrics after creation.  Defaults to False.\n\n### Run Metrics Operator\n\nThe RunMetricsOperator will run metrics in Bigeye based on the following:\n\n1. All metrics for a given table, by providing warehouse ID, schema name and table name.\n2. Any and all metrics, given a list of metric IDs.  \n\nCurrently, if a list of metric IDs is provided these will be run instead of metrics provided for\nwarehouse_id, schema_name, table_name.\n\n#### Parameters\n1. connection_id: str - The Airfow connection ID used to store the required Bigeye credential.\n2. warehouse_id: int - The Bigeye source/warehouse id for which metrics will be run.\n3. schema_name: str - The schema name for which metrics will be run.\n4. table_name: str - The table name for which metrics will be run.\n5. metric_ids: List[int] - The metric ids to run.',
    'author': 'Bigeye',
    'author_email': 'support@bigeye.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://docs.bigeye.com/docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
