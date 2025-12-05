import logging
import os

from airflow.models import DagBag

DAGS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "dags")


def test_dags_load_with_no_errors():
    """
    Verify that all DAGs in the 'dags' folder can be imported without errors.
    This catches syntax errors and missing dependencies.
    """
    logging.info(f"Looking for DAGs in: {DAGS_FOLDER}")

    dag_bag = DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

    # If there are import errors, fail the test and list them
    assert len(dag_bag.import_errors) == 0, f"DAG import errors: {dag_bag.import_errors}"


def test_dags_have_owners():
    """
    Verify that every loaded DAG has an 'owner' defined.
    This is a simple example of a policy test.
    """
    dag_bag = DagBag(dag_folder=DAGS_FOLDER, include_examples=False)

    for dag_id, dag in dag_bag.dags.items():
        assert dag.owner is not None, f"DAG {dag_id} has no owner defined"
        assert dag.owner != "airflow", f"DAG {dag_id} should not use default 'airflow' owner"
