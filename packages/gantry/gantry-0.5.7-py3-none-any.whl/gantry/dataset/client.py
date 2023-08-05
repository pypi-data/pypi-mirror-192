import logging
from pathlib import Path, PurePath
from typing import Any, Dict, List, Optional

from typeguard import typechecked

from gantry.api_client import APIClient
from gantry.dataset.gantry_dataset import GantryDataset
from gantry.exceptions import DatasetNotFoundError, GantryRequestException

logger = logging.getLogger(__name__)


class GantryDatasetClient:
    def __init__(
        self,
        api_client: APIClient,
        working_directory: str = str(Path().absolute()),
    ):
        self._api_client = api_client
        self._workspace = working_directory

    @property
    def working_directory(self) -> str:
        return self._workspace  # type: ignore

    @working_directory.setter
    def working_directory(self, value: str):
        if not PurePath(value).is_absolute():
            logger.warning(
                f"{value} is not an absolute path, will use {Path(value).resolve()} instead."
            )
        else:
            logger.info(f"Set dataset working directory to {value}")
        self._workspace = str(Path(value).resolve())
        Path(self._workspace).mkdir(exist_ok=True)

    def set_working_directory(self, working_dir: str) -> None:
        """
        Set the  dataset client working directory. Your dataset will be pulled into this folder
        when running ``pull()``.

        Args:
            working_dir (str): absolute path of the directory used to store local copy of dataset.

        Returns:
            ``None``
        """
        self.working_directory = working_dir

    @typechecked
    def create_dataset(
        self, name: str, bucket_name: Optional[str] = None, app_name: Optional[str] = None
    ) -> GantryDataset:
        """
        Create a dataset in your organization with the provided name, optionally providing a
        storing bucket if desired.

        Args:
            name (str): dataset name
            bucket_name (str): Provide bucket name if you want to use your own bucket. If not
                provided we will use a gantry managed bucket.
            app_name (Optional[str], optional): gantry application name which will be used to set
                dataset schema if provided.

        Returns:
            :class:`gantry.dataset.GantryDataset`: an object representing the crated dataset.
        """
        data = {
            "name": name,
        }

        if app_name:
            res = self._api_client.request(
                "GET", f"/api/v1/applications/{app_name}/schemas", raise_for_status=True
            )
            data["model_id"] = res["data"]["id"]

        if bucket_name:
            data.update(
                {
                    "bucket_name": bucket_name,
                }
            )

        res = self._api_client.request("POST", "/api/v1/datasets", json=data, raise_for_status=True)

        return GantryDataset(
            api_client=self._api_client,
            dataset_name=res["data"]["name"],
            dataset_id=res["data"]["id"],
            bucket_name=res["data"]["bucket_name"],
            aws_region=res["data"]["aws_region"],
            dataset_s3_prefix=f"{res['data']['organization_id']}/{res['data']['s3_prefix']}",
            workspace=self._workspace,
        )

    @typechecked
    def get_dataset(self, name: str) -> GantryDataset:
        """
        Query Gantry for a dataset object corresponding to the provided name.

        Args:
            name (str): the name of the dataset to be retrieved.

        Returns:
            :class:`gantry.dataset.GantryDataset`: An object representing the dataset name.
        """
        try:
            res = self._api_client.request("GET", f"/api/v1/datasets/{name}", raise_for_status=True)
        except GantryRequestException as e:
            if e.status_code == 404:
                raise DatasetNotFoundError(f'Could not find dataset with name "{name}"') from e
            raise

        if res["data"]["disabled"]:
            logger.warning("This dataset is marked as deleted")

        return GantryDataset(
            api_client=self._api_client,
            dataset_name=res["data"]["name"],
            dataset_id=res["data"]["id"],
            bucket_name=res["data"]["bucket_name"],
            aws_region=res["data"]["aws_region"],
            dataset_s3_prefix=f"{res['data']['organization_id']}/{res['data']['s3_prefix']}",
            workspace=self._workspace,
        )

    @typechecked
    def list_dataset_versions(self, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Provide a list of versions of this dataset, and metadata associated
        with those versions.

        Args:
            name (str): the name of the dataset.

        Returns:
            ``List[Dict[str, Any]]``: list of dictionaries with metadata.
        """
        dataset = self.get_dataset(dataset_name)

        return dataset.list_versions()

    @typechecked
    def list_datasets(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """
        List datasets all datasets in the organizations' namespace.

        Args:
            include_deleted (bool): include deleted datasets, defaults to ``False``.

        Returns:
            ``List[Dict[str, Any]]``: List of dictionaries, each representing one
            dataset and associated metadata.
        """
        res = self._api_client.request(
            "GET",
            "/api/v1/datasets",
            raise_for_status=True,
            params={"include_deleted": include_deleted},
        )

        return [self._prune_dataset_info(dataset_info) for dataset_info in res["data"]]

    @typechecked
    def delete_dataset(self, name: str):
        """
        Delete the named dataset.

        Args:
            name (str): the name of the dataset to be deleted.

        Returns:
            ``None``
        """
        dataset = self.get_dataset(name)

        return dataset.delete()

    def ping(self) -> bool:
        """
        Pings the API client server to check if it is alive.
        Returns ``True`` if alive, ``False`` if there is an error during ping process.

        Returns
            ``bool``: flag indicating liveness.
        """
        try:
            # Cannot use /healthz/* endpoints as those will be answered by nginx
            # need to use /.
            # See https://linear.app/gantry/issue/ENG-2978/revisit-ping-in-sdk
            self._api_client.request("GET", "/api/ping", raise_for_status=True)
            return True
        except Exception as e:
            logger.error(f"Error during ping: {e}")
            return False

    def ready(self) -> bool:
        """
        Checks whether the API is ready to receive traffic with the provided API Key.
        """
        try:
            self._api_client.request("GET", "/api/v1/auth-ping", raise_for_status=True)
            return True
        except Exception as e:
            logger.error(f"Error during api key check: {e}")
            return False

    @staticmethod
    def _prune_dataset_info(dataset_info):
        return {
            "name": dataset_info["name"],
            "dataset_id": dataset_info["id"],
            "created_at": dataset_info["created_at"],
        }
