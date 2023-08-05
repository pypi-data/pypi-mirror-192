#   ______ __| _/  | __         _____  ______ |__|
#  /  ___// __ ||  |/ /  ______ \__  \ \____ \|  |
#  \___ \/ /_/ ||    <  /_____/  / __ \|  |_> >  |
# /____  >____ ||__|_ \         (____  /   __/|__|
#      \/     \/     \/              \/|__|

"""
sdk.api
~~~~~~~
This module abstracts access to various services of the superb data kraken (SDK) via the SDKClient class:
To use this module valid credentials for the configured sdk environment are required.

:copyright: (c) 2023 e:fs Techhub GmbH
:license: Apache2, see LICENSE for more details.
"""
import os
import sys
from copy import deepcopy
from typing import List

import requests
from azure.storage.blob import BlobClient, ContainerClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from ._internal_utils import TokenHolder, _get_azure_storage_url, _sanitize_url
from .config import _ENVS, _ACCESS_TOKEN_ENV_KEY, _REFRESH_TOKEN_ENV_KEY


class SDKClient:
    f"""
    client class providing methods for accessing SDK services: 
        - organizationmanager (access to organizations/spaces)
        - opensearch
        - ... (to be expanded)

    Authorization at the sdk services is done using JWT tokens which are kept in-memory.
    On every request the access token gets refreshed, if it is about to or has alreadyexpired.
    If no Login information are passed to this module's main class 'SDKClient' on initialization, access/refresh token are expected to be stored in environment 
    variables of the execution environment.

    Usage::
        If access/refresh token can be found int the env-variables {_ACCESS_TOKEN_ENV_KEY} / {_REFRESH_TOKEN_ENV_KEY}
        >>> import sdk.api
        >>> client = sdk.api.SDKClient()
        >>> client.organization_get_all()

        or with explicit login:
        >>> import sdk.api
        >>> sdk.api.SDKClient(username='hasslethehoff', password='lookingforfreedom')
        >>> client.organization_get_all()
        
        this module is pre configured for usage with the default instance of the SDK (found here https://sdk.efs.ai) and comes with settings for various different instances
        
        choosing different environment:
        >>> client = sdk.api.SDKClient(env='sdk-dev')
        
        overwriting settings:
        >>> client = sdk.api.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
        
    """

    def __init__(self, **kwargs):
        self._env = deepcopy(_ENVS.get(kwargs.get('env', 'sdk')))

        # overwrite settings from args
        if 'domain' in kwargs:
            self._env.domain = kwargs.get('domain')
        if 'realm' in kwargs:
            self._env.realm = kwargs.get('realm')
        if 'client_id' in kwargs:
            self._env.client_id = kwargs.get('client_id')
        if 'api_version' in kwargs:
            self._env.api_version = kwargs.get('api_version')
        self.org_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/organization'
        self.space_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/space'

        if 'username' in kwargs and 'password' in kwargs:
            self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm, client_id=self._env.client_id)
            self._token_holder.get_tokens_with_credentials(kwargs['username'], kwargs['password'])
        else:
            try:
                access_token = os.environ[_ACCESS_TOKEN_ENV_KEY]
                refresh_token = os.environ[_REFRESH_TOKEN_ENV_KEY]
                self._token_holder = TokenHolder(domain=self._env.domain,
                                                 realm=self._env.realm,
                                                 client_id=self._env.client_id,
                                                 access_token=access_token,
                                                 refresh_token=refresh_token)
            except KeyError:
                print(f'Cannot read token environment variables {_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}', file=sys.stderr)
                print('Assert that variables are set or try login initializing with username and password.', file=sys.stderr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ organizations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def organization_get_all(self):
        """
        Fetches all Organizations the user has access to.

        :return:
            organizations
        """
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(self.org_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_id(self, org_id):
        """
        Fetch organization by id.

        :param org_id:
            id of the organization to be fetched
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_name(self, org_name: str) -> dict:
        """
        Fetches organization by name.

        :param org_name:
            name of the organization
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/name/{org_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ spaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def space_get_all(self, org_id: int) -> List[dict]:
        """
        Gets all spaces of a given organization if the user has access to.
        :param org_id:
            Organization id.
        :return:
            list of spaces
        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_id(self, org_id: int, space_id: int) -> dict:
        """
        Fetch space by id.

        :param space_id:
            id of the space to be fetched
        :return:
            dictionary of the space
        """
        url = f'{self.space_endpoint}/{org_id}/{space_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_name(self, org_id: int, space_name: str) -> dict:
        """
        Fetches space by name.

        :param space_name:
            name of the space
        :return:
            dictionary of the space
        """
        url = f'{self.space_endpoint}/{org_id}/name/{space_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_create(self, org_id: int, space: dict) -> dict:
        """
        Creates a space within the organization specified by id.
        :param org_id:
            organization id within which the space should be created.
        :param space:
            dictionary defining space properties
        :return:
            response body of the http request
        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=space, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ indexing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def index_get_all(self) -> dict:
        """
        Fetches all indices accessible
        :return:
            indices
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def index_search(self, index: str, query: dict) -> dict:
        """
        searches a given index with the given query
        :param index:
        :param query:
        :return:
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/elastic/api/{index}/_search'

        response = requests.get(url, headers=headers, json=query)
        response.raise_for_status()
        res = [hit['_source'] for hit in response.json()['hits']['hits']]

        return res

    def index_get_document(self, index: str, doc_id: str) -> dict:
        """
        Fetches a document from a given opensearch index and returns it's content
        :param index:
            index name
        :param doc_id:
            document id
        :return:
            document
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/elastic/api/{index}/_doc/{doc_id}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        doc = response.json()['_source']

        return doc

    def index_documents(self, documents: List[dict], index_name: str, timeout: int = 60, chunk_size=10000) -> None:
        """
        indexes multiple documents to a given index.
        :param timeout:
            timeout for the bulk operation
        :param chunk_size:
        :param documents:
            list of dictionaries to index
        :param index_name:
            index name to index documents to
        :return:
        """
        url = f'https://{self._env.domain}/elastic/api/_bulk'
        es = Elasticsearch(url, use_ssl=True, headers={"Authorization": "Bearer " + self._token_holder.get_token()}, timeout=timeout)

        # Create data for bulk api
        actions = [
            {
                "_index": index_name,
                "_id": entry.pop('_id') if '_id' in entry else None,
                "_source": entry
            } for entry in documents
        ]

        # Bulk ingest data
        bulk(es, actions, chunk_size=chunk_size)

        # Close Elasticsearch
        es.close()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ storage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def storage_list_blobs(self, organization: str, space: str) -> List[str]:
        """
        Lists blobs in storage container
        :param organization:
        :param space:
        :return:
            list of blob names
        """
        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')
        blob_client = ContainerClient.from_container_url(f'{storage_url}?{sas_token}')
        blobs = blob_client.list_blobs()
        result = [(b['name']) for b in blobs]
        return result

    def storage_download_files(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Downloads files from storage directory to local directory.
        :param organization:
        :param space:
        :param files:
        :param local_dir:
        :param storage_dir:
        :return:
        """
        return self._storage_download_files_azure(organization, space, files, local_dir, storage_dir)

    def _storage_download_files_azure(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Downloads files from Azure storage directory to local directory.

        For nested blobs local directories are created inside the temporary directory as well.

        Args:
            organization (str): Azure storage account
            space (str): Azure storage container
            storage_dir (str): root directory inside the space (Azure container) to be used
            files (List[str]): list of files to be downloaded
            local_dir (str): local directory to download the files to
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')

        # download blobs to local directory
        for file in files:
            blob_url = _sanitize_url(f'{storage_url}/{storage_dir}/{file}?{sas_token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                dest_file = os.path.join(local_dir, file)

                # for nested blobs, create local path as well!
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                with open(dest_file, "wb") as f:
                    data = blob_client.download_blob()
                    data.readinto(f)

    def _get_azure_sas_token(self, organization: str, space: str, reqtype: str = 'read') -> str:
        """
        Generates an upload-token via accessmanager (version > 1)

        Parameters
        ----------
        organization : str
            Organization the token shall be created for.
        space : str
            The space the token shall be created fro
        reqtype : str
            Type of request. read|upload|delete

        Returns
        -------
        _type_
            The created SAS token.
        """
        url = f'{self._env.accessmanager_url}/{reqtype}?organization={organization}&space={space}'
        url = _sanitize_url(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)

        response.raise_for_status()

        return response.text
