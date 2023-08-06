**Table of contents**
- [Installation](#installation)
  - [Requirements](#requirements)
    - [Git token](#git-token)
    - [Hot get Postman API Key](#hot-get-postman-api-key)
  - [Installing locally](#installing-locally)
  - [Configuring](#configuring)
- [How to use](#how-to-use)



# Installation
## Requirements
- `fzf`
- `git` + be setup with Staircase by ssh key
- [`git` token](#git-token)
- [Postman API Key](#hot-get-postman-api-key)
- Marketplace API key
- `pipenv` *optional*

### Git token
Used for clone product.
GitHub token. Go to GitHub.com/Settings/Developer settings/Personal access token/New/Enable SSO.
Add checks to enable repo access.

### Hot get Postman API Key
Follow steps via app or website:
- Click on profile pic 
- Settings 
- API keys 
- Generate API key
  Consider verify that expiration date is okay, you are going need to renew it after.

## Installing locally
- Clone this repo.  `git clone https://github.com/StaircaseAPI/staircasecli.git`
- Open terminal root working directory.
- Run command `pip install --editable .` if you don`t need to delete folder with repo after install, you want to develop cli or have access to files with config and envs.

## Configuring
- Open terminal.
- Run command `staircase config setup` or edit file `staircase config file-path`

`pip install staircase-cli`
# How to use
- Open terminal
- Run command `staircase`
- You can run `--help` to any command to get extra info.
