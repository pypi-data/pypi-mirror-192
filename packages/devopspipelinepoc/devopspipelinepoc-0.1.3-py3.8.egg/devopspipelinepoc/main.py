import pkg_resources
import json
import sys
import shutil
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
    config_path = Path(path).joinpath("blackwidow_config.json")
    pkg_dir = Path(sys.modules['devopspipelinepoc'].__path__[0])
    
    if not config_path:
        raise Exception('blackwidow_config.json does not exist')
    
    with open(config_path, 'r', encoding="utf-8-sig") as f:
        config = ScraperConfig.parse_obj(json.load(f))
    
    if config.image_type == 'scrapy':
        docker_file_path = pkg_dir.joinpath('dockerfiles/scrapy/Dockerfile')
        shutil.copy(docker_file_path,path)
    elif config.image_type == 'selenium':
        docker_file_path = pkg_dir.joinpath('dockerfiles/selenium/Dockerfile')
        shutil.copy(docker_file_path,path)
    else:
        raise Exception('image_type provided is invalid')
    # print(path+'/blackwidow_config.json')


@app.command()
def list_data():
    print(type(pkg_resources.resource_filename('devopspipelinepoc', 'data/data_output_worker.txt')))
    print(pkg_resources.resource_filename('devopspipelinepoc', 'data/data_output_worker.txt'))


@app.command()
def add_worker_file(path: str):
    sys.path.append(path)
    pkg_dir = Path(sys.modules['devopspipelinepoc'].__path__[0])

    from scrape import scrape
    return_type = inspect.signature(scrape).return_annotation

    if return_type is str:
        worker_file_path = pkg_dir.joinpath('worker_files/path_output/worker.py')
        shutil.copy(worker_file_path,path)
    elif return_type is list:
        worker_file_path = pkg_dir.joinpath('worker_files/data_output/worker.py')
        shutil.copy(worker_file_path,path)
    else:
        raise Exception('scrape function must return either a list or string')


@app.command()
def update_scraper_config(path: str):
    res = requests.get('https://skumapping-api.graphenesvc.com/', verify=False)
    print(res.text)

# if __name__ == "__main__":
#     app()