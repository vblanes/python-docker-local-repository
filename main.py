import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from os import environ
import json

REGISTRY_USERNAME = environ.get('REGISTRY_USERNAME')
REGISTRY_PASSWORD = environ.get('REGISTRY_PASSWORD')


def list_catalog(ip: str, port: int = 5000) -> dict:
    response = requests.get(f'https://{ip}:{port}/v2/_catalog',
                            auth=HTTPBasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD))
    return response.json()


def list_repository_tags(repository: str, ip: str, port: int = 5000) -> dict:
    response = requests.get(f'https://{ip}:{port}/v2/{repository}/tags/list',
                            auth=HTTPBasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD))
    return response.json()


def get_digest_value(repository: str, tag: str, ip: str, port: int = 5000) -> CaseInsensitiveDict:
    # The important information of the digest does not come in the json but in the headers
    response = requests.get(f'https://{ip}:{port}/v2/{repository}/manifests/{tag}',
                            auth=HTTPBasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD),
                            headers={"Accept": "application/vnd.oci.image.manifest.v1+json"})
    return response.headers


def delete_image(repository: str, digest: str, ip: str, port: int = 5000):
    # $ curl -sS -X DELETE <domain-or-ip>:5000/v2/<repo>/manifests/<digest>
    response = requests.delete(f'https://{ip}:{port}/v2/{repository}/manifests/{digest}',
                               auth=HTTPBasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD))
    return response


if __name__ == '__main__':
    pass
