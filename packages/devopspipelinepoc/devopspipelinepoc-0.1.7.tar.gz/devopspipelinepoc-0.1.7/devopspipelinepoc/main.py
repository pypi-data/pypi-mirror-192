import pkg_resources
import json
import sys
import inspect
from pathlib import Path

import requests
from pydantic import BaseModel
import typer

app = typer.Typer()


class ScraperConfig(BaseModel):
    name: str
    queue: str
    website_name: str
    image_type: str
    scraper_type: str


@app.command()
def add_dockerfile(path: str):
    scraper_path = Path(path)
    config_path = scraper_path.joinpath("blackwidow_config.json")
    dockerfile_path = scraper_path.joinpath("Dockerfile")

    if not config_path:
        raise Exception('blackwidow_config.json does not exist')
    
    with open(config_path, 'r', encoding="utf-8-sig") as f:
        config = ScraperConfig.parse_obj(json.load(f))
    
    if config.image_type == 'scrapy':
        with open(dockerfile_path, "wb") as f:
            f.write(pkg_resources.resource_stream('devopspipelinepoc', 'data/scrapy_dockerfile.txt').read())
    elif config.image_type == 'selenium':
        with open(dockerfile_path, "wb") as f:
            f.write(pkg_resources.resource_stream('devopspipelinepoc', 'data/selenium_dockerfile.txt').read())
    else:
        raise Exception('image_type provided is invalid')


@app.command()
def list_data():
    print(type(pkg_resources.resource_filename('devopspipelinepoc', 'data/data_output_worker.txt')))
    print(pkg_resources.resource_filename('devopspipelinepoc', 'data/data_output_worker.txt'))
    pkg_resources.resource_stream()


@app.command()
def add_worker_file(path: str):
    worker_file_path = Path(path).joinpath("worker.py")

    sys.path.append(path)
    from scrape import scrape
    return_type = inspect.signature(scrape).return_annotation

    if return_type is str:
        with open(worker_file_path, "wb") as f:
            f.write(pkg_resources.resource_stream('devopspipelinepoc', 'data/path_output_worker.txt').read())
    elif return_type is list:
        with open(worker_file_path, "wb") as f:
            f.write(pkg_resources.resource_stream('devopspipelinepoc', 'data/data_output_worker.txt').read())
    else:
        raise Exception('scrape function must return either a list or string')


@app.command()
def update_scraper_config(path: str):
    res = requests.get('https://skumapping-api.graphenesvc.com/', verify=False)
    print(res.text)

# if __name__ == "__main__":
#     app()