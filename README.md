# Python Testing Guide

## Read the guide

To read the guide, go to [this repo's github pages](https://libertyfi.github.io/python_testing_guide/).

## Development

### Prerequisites

- Install [Poetry](https://python-poetry.org/)
- Install dependencies with `poetry install`

### Local development

To generate the guide locally, run the following command:

```bash
poetry run mkdocs serve
```

This will start a local server and provide a link to view a live version of the guide in your default browser.

### Deploy to github pages

To deploy the guide to github pages, run the following command:

```bash
poetry run mkdocs gh-deploy
```
