---
layout: lab
title: "Lab 02: Software Setup (Python)"
date: 2025-07-08
---
# Goal

In today's Lab session, we will:

1. Install Python via Miniconda.
2. Create a virtual environment for the course.
3. *(Optional)* Initialize an individual repository for the course.
4. Learn basic codes with examples.

# I. Miniconda
## I.0. Verify Your Installation
- Open **Terminal** (Mac) or **cmd** (Windows).
- Type `conda --version` and press enter.
  - If your version is not very outdated (latest: 25.5.1), you may use it. Go to [II](#ii-virtual-environment).
  - If not, update by running `conda update conda`. After updating, check the version again, and go to [II](#ii-virtual-environment).
  - If you get an error message `command not found`, follow steps in [I.1](#i1-installation).

## I.1. Installation

- Go to <https://www.anaconda.com/download/success> and download the installer for **Miniconda**.
- **(Windows)** During installation, check "Add Miniconda3 to my **PATH** environment variable".

### After Installation

- Open **Terminal** (Mac) or **cmd** (Windows).
- You may see `(base)` on your terminal.
- Type `conda --version` and press enter.
- If **Miniconda** is successfully installed, then the version number will be displayed. Now, go to [II](#ii-virtual-environment).

# II. Virtual Environment
- Create a new directory anywhere on your computer (e.g. create `cosmos` in Desktop).
- Download [this yaml file](/cosmos/static_files/environment.yml) and locate it to the folder you created.
- Open VS Code.
- Click File -> Open Folder... -> choose the folder you created.
- Click Terminal -> New Terminal
- Type `conda env create` and press enter. This creates conda environment `cosmos` with specified packages in `environment.yml` file in your computer.
- Type `conda activate cosmos`. This activates the environment `cosmos`. You may see `(cosmos)` on your terminal.
- Create `test.py` and select `cosmos` interpreter. Run `print("Hello, world").
- Create `test.ipynb` and select `cosmos` kernel. Run `print("Hello, world").

# III. (Optional) Create repository
If you want to create a repository for the version control, repeat the process that we learned in [Lab 01](/cosmos/labs/lab01/#iii-test-repository).

# IV. Basic codes.
