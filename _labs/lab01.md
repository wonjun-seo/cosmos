---
layout: lab
title: "Lab 01: Software Setup (Git, Github, VS code)"
date: 2025-07-07
---
# Goal
In today's Lab session, we will:

- Install Git and VS code.
- Vreate a Github account and link it to VS code.
- Vreate a test repository and understand how it works.
- Vreate a group website.

# I. Git and Github

## 1. Installation

### Mac

- Open **Terminal**.
- Type `git --version` and press enter.
- If **Git** is already installed, then the version number will be displayed. If not, the installation process will begin automatically.
- After installation, type `git --version` and press enter.
- If **Git** is successfully installed, then the version number will be displayed.

### Windows

- Go to <https://git-scm.com/downloads/win> and download the installer.
- During installation, when prompted for setting PATH environment, choose 'Git from the command line and also from 3rd-party software'.
- After installation, open **Command propmt (cmd)**.
- Type `git--version` and press enter.
- If **Git** is successfully installed, then the version number will be displayed.

## 2. Create a Github account

- Go to <https://github.com> and create a new account.
- Use your **primary** email address.

## 3. Git Configuration

- Open **Terminal** (Mac) or **cmd** (Windows).
- Set your name: `git config --global user.name <name>`.
- Set your email: `git config --global user.email <email>`. Here, `<email>` should be your **github account email**.
- To heck your configuration: `git config list`. Press `q` to exit.

# II. VS code

## 1. Installation
- Go to <https://code.visualstudio.com/Download> and download the installer.

### Mac
- After installation, move **Visual Studio Code.app** to the **Applications** folder. 
- Open **VS code**.
- Press `Cmd+Shift+P`, type `Shell Command`, and click `install 'code' command ...`.
- Open **Terminal** and type `code .`, then press enter.

### Windows
- During installation, make sure to check "Add to PATH".
- After installation, open **cmd** and type `code .`, then press enter.

## 2. Link to Github
- Open **VS code**.
- Click the profile icon at the bottom left.
- Click `Backup and Sync Settings`.
- Click `Sign in`, then choose `Sign in with Github` and follow instructions.
- *(Optional)* Activate **Github Copilot**.

# III. Test Repository
- Create `test` directory anywhere on your computer (e.g.,Desktop).
- Open **VS code** and click `File-Open folder`, then choose the `test` folder.
- Create a file named `README.md`.
- Type anything you want. For markdown syntax, refer to: <https://www.markdownguide.org/cheat-sheet/>
- Save it: `Cmd+S` (Mac) or `Ctrl+S` (Windows).
- Click the source-control icon on the left sidebar.
- Click `Initialize repository`. This creates a hidden folder `.git` in your `test` directory.
- Stage and Commit.
- Click `Publish branch` and follow the instructions.
- Try Push and Pull.
- After enough exercises, you may delete this repository from both Github and your local computer.

**File status markers**

- **U**: Untracked (new file not yet added to the repository)
- **A**: Added (new file added to the repository)
- **M**: Modified
- **R**: Renamed
- **D**: Deleted

During the course, you will maintain the following three repositories:

1. Your own repository for lab and exercises.
2. Group project (possibly collaboration).
3. Group website (collaboration).

# IV. Create the Group Website

Every group will create a group website to present their final project.

- Go to <https://github.com/wonjun-seo/cosmos-demo> and follow the instructions.

## Assignments

Update member information on the group website!

# Tomorrow

In tomorrow's Lab session, we will install Python.

