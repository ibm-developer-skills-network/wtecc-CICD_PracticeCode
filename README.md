# lab-github-actions

[![Build Status](https://github.com/nyu-devops/lab-github-actions/actions/workflows/workflow.yml/badge.svg)](https://github.com/nyu-devops/lab-github-actions/actions)

This is for NYU DevOps lab on using GitHub Actions with Redis for Continuous Integration

## Introduction

This lab contains a `workflow.yml` file in the `.github/workflows/` folder that shows you how to run your tests and start a Redis service be attached while running them. It also uses Code Coverage to determine how complete your testing is.

GitHub Actions can be used as an alternative to Travis CI to run tests on every Pull Request to facilitate implementing Continuous Integration for your development team. Every Pull Request is an opportunity for a code review and any Pull Request that lowers the test coverage should be rejected until more test cases are added to bring the coverage back up to the threshold set by the team. (usually 90% to 95%)

## Setup

To complete this lab you will need to Fork this repo because you need to make a change in order to trigger GitHub Actions. When making a Pull Request, you want to make sure that your request is merging with your Fork because the Pull Request of a Fork will default to come back to this repo and not your Fork.

You can read about why in my article [Creating Reproducible Development Environments](https://medium.com/nerd-for-tech/creating-reproducible-development-environments-fac8d6471f35).

### Prerequisite Installation for Intel Mac & PC

The easiest way to use this lab is with **Vagrant** and **VirtualBox**. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

```bash
    git clone https://github.com/nyu-devops/lab-github-actions.git
    cd lab-github-actions
    vagrant up
    vagrant ssh
    cd /vagrant
    honcho start
```

You can also automatically set the environment variable FLASK_APP using a `.env` file.
There is an example in this repo called `dot-env-example` that you can simply copy.

```sh
    cp dot-env-example .env
```

The `.env` file will be loaded when you do `flask run` so that you don't have to specify
any environment variables.

### Alternate for M1 Macs using Vagrant and Docker

You can also use [Docker Desktop for Apple Silicon](https://docs.docker.com/docker-for-mac/apple-silicon/) as a provider instead of VirtualBox. This is useful for owners of Apple M1 Silicon Macs which cannot run VirtualBox because they have a CPU based on ARM architecture instead of Intel.

Just add `--provider docker` to the `vagrant up` command like this:

```sh
vagrant up --provider docker
```

This will use a Docker container instead of a Virtual Machine (VM). Of course Intel Macs and Windows PCs can use this as well. Just install the appropreate Docker Desktopo build.

### Alternate install using VSCode and Docker

You can also develop in Docker containers using **Visual Studio Code**. This project contains a `.devcontainer` folder that will set up a Docker environment in VSCode for you. You will need the following:

- Docker Desktop for [Mac](https://docs.docker.com/docker-for-mac/install/) or [Windows](https://docs.docker.com/docker-for-windows/install/)
- Microsoft Visual Studio Code ([VSCode](https://code.visualstudio.com/download))
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) VSCode Extension

It is a good idea to add VSCode to your path so that you can invoke it from the command line. To do this, open VSCode and type `Shift+Command+P` on Mac or `Shift+Ctrl+P` on Windows to open the command palete and then search for "shell" and select the option **Shell Command: Install 'code' command in Path**. This will install VSCode in your path.

Then you can start your development environment up with:

```bash
    git clone https://github.com/nyu-devops/lab-github-actions.git
    cd lab-github-actions
    code .
```

The first time it will build the Docker image but after that it will just create a container and place you inside of it in your `/app` folder which actually contains the repo shared from your computer. It will also install all of the VSCode extensions needed for Python development.

If it does not automatically prompt you to open the project in a container, you can select the green icon at the bottom left of your VSCode UI and select: **Remote Containers: Reopen in Container**.

### Alternate manual install using local Python

This option is not recommended because developing natively on your local computer does ensure that the code will work on anyone elses computer or in production.  I strongly recommend that you us one of thee reproducible development environments above but if you have Python 3 installed on your computer you can make a virtual environment and run the code locally with:

```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

You will also need Docker on your computer to run a container for the database.

```bash
docker run -d --name redis -p 6379:6379 -v redis:/data redis:alpine
```

This will run Redis on Alpine and have it forward port `6379` so that your application and communicate with it.

You can now run `nosetests` to run the TDD tests locally.

You can also test the application manually by running it with:

```bash
honcho start
```

## Manually running the Tests

Run the tests using `nosetests` and `coverage`

```bash
nosetests
```

Nose is configured to automatically include the flags `--with-spec --spec-color --with-coverage` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

## What's featured in the project?

```text
    * routes.py -- the main Service using Python Flask and Redis
    * test_service.py -- test cases using unittest
    * .github/workfloows/ci.yml -- the GitHub Actions file that automates testing
````

This repository is part of the NYU class CSCI-GA.2810-001: DevOps and Agile Methodologies taught by John Rofrano, Adjunct Instructor, NYU Courant Institute of Mathematical Sciences, Graduate Division, Computer Science, and NYU Stern School of Business.
