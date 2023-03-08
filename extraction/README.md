# directory-reads

<a href="https://github.com/benepass/directory-read/actions"><img alt="Test" src="https://github.com/benepass/directory-read/actions/workflows/extraction-test.yml/badge.svg"></a>
<a href="https://github.com/benepass/directory-read/actions"><img alt="Security" src="https://github.com/benepass/directory-read/actions/workflows/extraction-security.yml/badge.svg"></a>
<a href="https://github.com/benepass/directory-read/actions"><img alt="Linting and formatters" src="https://github.com/benepass/directory-read/actions/workflows/extraction-formatters.yml/badge.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/PyCQA/bandit"><img alt="Security: bandit" src="https://img.shields.io/badge/security-bandit-green.svg"></a>

`directory-read/extraction` is a Python serverless application built on top of [Chalice](https://aws.github.io/chalice/quickstart.html).

- [directory-reads](#directory-reads)
    + [Requirements](#requirements)
    + [Installation](#installation)
    + [Pre-commit](#pre-commit)
    + [Testing](#testing)
    + [Deploy to AWS](#deploy-to-aws)
    + [Local Development](#local-development)
    + [Usage](#usage)

### Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- Python 3.9.11
- Updated .env file - make sure to check that with your peers
- Configured AWS crendetials
- Docker

### Installation

The application encourages developers to use `pyenv + virtualenv` to manage the Python version and the application needed libraries.

1. Install pyenv

```shell
curl https://pyenv.run | bash
```

2. Install pyenv-virtualenv

```shell
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

3. Install and set the project specific Python version

```shell
pyenv install 3.9.11
pyenv local 3.9.11
```

4. Create the virtualenv

```shell
pyenv virtualenv directory-read/extraction
```

5. Install project requirements

```shell
pip install -r requirements.txt
```

### Pre-commit

"Git hook scripts are useful for identifying simple issues before submission to code review. We run our hooks on every commit to automatically point out issues in code such as missing semicolons, trailing whitespace, and debug statements. By pointing these issues out before code review, this allows a code reviewer to focus on the architecture of a change while not wasting time with trivial style nitpicks."

Reference: https://pre-commit.com

1. Install dev requirements

``` shell
pip install -r requirements/dev.txt
```

2. Install pre-commit

``` shell
pre-commit install
```

Thats's it! Your next `git commit` command should take a while to install the dependencies but once they're installed it should be a smoothly process!

### Testing

1. Make sure that you have installed the test requirements.

```shell
pip install -r requirements/test.txt
```

2. `pytest` it!

```shell
make test
```


### Deploy to AWS

The application deploy is fully automated by Github Actions and is triggered whenever a release tag is published. The [terraform README.md file](terraform/README.md) has a step-by-step guide onto how to deploy the application to AWS.

### Local Development

The application leverages on AWS resources such as S3, Lambda, SQS, IAM Roles and so on and all these tools needs their proper configuration. Luckily using [LocalStack](https://docs.localstack.cloud/overview/) we're able to emulate all of them as well as executing the Lambdas the app comes with. We use the same [Terraform](http://terraform.io) files used for production so that we can replicate the exact same behaviour and thus have a more truthful environment.

1. Make sure you have all dev dependencies installed.

``` shell
pip install -r requirements/dev.txt
```

2. Launch localstack through docker.

``` shell
docker-compose up localstack
```

3. Add the following content on a new file in `terraform/main_override.tf` to override the terraform prod backend and use a local one instead. 

``` shell
terraform {
  backend "local" {}
}
```

4. On the first deploy ever you need to run the commands below. It will deploy all AWS resources locally. It will output a few environment variables, unless you're not deploying a new environment you won't need to do anything with them.

``` shell
make build-chalice-terraform env=dev
make local-deploy env=dev
```

5. Now on everytime you want to update ONLY the application code you'll need to:

``` shell
make build-chalice-terraform env=dev
make update-local-terraform
```

You should get some outputs about the lambda deployment progress. Once it's done you'll be able to invoke the lambda functions.

### More info

You can check `make help` for other instructions.

