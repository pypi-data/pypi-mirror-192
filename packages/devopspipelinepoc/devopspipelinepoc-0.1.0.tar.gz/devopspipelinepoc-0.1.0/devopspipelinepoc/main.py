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
    if not config_path:
        raise Exception('blackwidow_config.json does not exist')
    with open(config_path, 'r', encoding="utf-8-sig") as f:
        config = ScraperConfig.parse_obj(json.load(f))
    if config.image_type == 'scrapy':
        shutil.copy('./dockerfiles/scrapy/Dockerfile',path)
    elif config.image_type == 'selenium':
        shutil.copy('./dockerfiles/selenium/Dockerfile',path)
    else:
        raise Exception('image_type provided is invalid')
    # print(path+'/blackwidow_config.json')


@app.command()
def add_worker_file(path: str):
    sys.path.append(path)
    from scrape import scrape
    return_type = inspect.signature(scrape).return_annotation
    if return_type is str:
        shutil.copy('./worker_files/path_output/worker.py',path)
    elif return_type is list:
        shutil.copy('./worker_files/data_output/worker.py',path)
    else:
        raise Exception('scrape function must reutrn either a list or string')


@app.command()
def update_scraper_config(path: str):
    res = requests.get('https://skumapping-api.graphenesvc.com/', verify=False)
    print(res.text)

# if __name__ == "__main__":
#     app()