---
layout: lab
title: "Lab 01: Software Setup (Git, Github, VS code)"
date: 2025-07-07
---
# Goal

In today's Lab session, we will:

- Install Git and VS code.
- Create a Github account and link it to VS code.
- Create a test repository and understand how it works.
- Create a group website.

# I. Git and Github

## I-0. Verify Your Installation

- If you don't have a **Github** account, go to I-1.
- Open **Terminal** (Mac) or **Command prompt (cmd)** (Windows).
- Type `git config list` and press enter.
  - If your name and email address of your **Github** account are correctly displayed, you already setup **Git** properly. Go to II. VS Code.
  - If you get an error message `command not found`, follow steps in [I-2](#I-2.-installation) and [I-3](#.

## I-1. Create a Github Account

- Go to <https://github.com> and create a new account.
- Use your **primary** email address.

## I-2. Installation

**Mac**

- The installation process will begin automatically.

**Windows**

- Go to <https://git-scm.com/downloads/win> and download the installer.
- During installation, when prompted for setting PATH environment, choose 'Git from the command line and also from 3rd-party software'.

### After installation

- Open **Terminal** (Mac) or **cmd** (Windows).
- Type `git --version` and press enter.
- If **Git** is successfully installed, then the version number will be displayed. Now, go to 3. Git Configuration.

## I-3. Git Configuration

- Open **Terminal** (Mac) or **cmd** (Windows).
- Set your name: `git config --global user.name <name>`.
- Set your email: `git config --global user.email <email>`. Here, `<email>` should be your **github account email**.
- To check your configuration: `git config list`. Press `q` to exit.

# II. VS Code

## II-0. Verify Your Installation

- Open **Terminal** (Mac) or **cmd** (Windows).
- Type `code .` and press enter.
  - If you get an error message `command not found`, follow steps in II-1 and II-2.
- Click the profile icon at the bottom left. If you can see your **Github** acount, then you already set up VS Code properly. If you know how to use Git (create repository / publish repository / push / pull), then go to IV. If not, go to III.

## II-1. Installation

- Go to <https://code.visualstudio.com/Download> and download the installer.
- (Mac) After installation, move **Visual Studio Code.app** to the **Applications** folder.
- (Windows) During installation, check "Add to PATH".

### After installation

**Mac**

- Open **VS Code**.
- Press `Cmd+Shift+P`, type `Shell Command`, and click `install 'code' command ...`.
- Open **Terminal** and type `code .`, then press enter. If **VS Code** is open, you're done. Go to II-2.

**Windows**

- Open  **cmd** and type `code .`, then press enter. If **VS Code** is open, you're done. Go to II-2.

## II-2. Link to Github

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

# IV. Create a Group Website

Every group will create a group website to present their final project.

- Go to <https://github.com/wonjun-seo/cosmos-demo> and follow the instructions. Only one member in each group should create a repository.

## Assignments

Update member information on the group website!

# Tomorrow

In tomorrow's Lab session, we will install Python.
