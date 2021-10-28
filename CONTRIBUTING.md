# Contributing Guidelines

This documentation contains a set of guidelines to help you during the contribution process.
We are happy to welcome all the contributions from anyone willing to improve/add new features to this project.
Thank you for helping out and remember, **no contribution is too small.**

### Need some help regarding the basics?🤔

You can refer to the following articles on basics of Git and Github and also contact the Project Mentors,
in case you are stuck:

- [Forking a Repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
- [Cloning a Repo](https://help.github.com/en/desktop/contributing-to-projects/creating-an-issue-or-pull-request)
- [How to create a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
- [Getting started with Git and GitHub](https://iread.ga/series/1/git-and-github)
- [Learn GitHub from Scratch](https://lab.github.com/githubtraining/introduction-to-github)


## Submitting Contributions👩‍💻👨‍💻

This project requires the following tools:
 * Python - The programming language used by Flask.
 * Pipenv or Virtualenv - Tools used for managing virtual environments.

To get started, install Python from [here](https://python.org) on your local computer if you don't have already.

Below you will find the process and workflow used to review and merge your changes.

**Step 0 : Find an issue**

- Take a look at the Existing Issues or create your **own** Issues!
- Wait for the Issue to be assigned to you after which you can start working on it.
- Note : Every change in this project should/must have an associated issue.

![issues](https://raw.githubusercontent.com/ashutoshkrris/EazyLoader/main/demo/issues.png)

**Step 1. Fork the repository from [here](https://github.com/ashutoshkrris/EazyLoader/fork).**

![fork](https://raw.githubusercontent.com/ashutoshkrris/EazyLoader/main/demo/fork.png)

**Step 2. Clone the forked repository into a fresh folder**

```
$ git clone https://github.com/<your-username>/EazyLoader.git
$ cd EazyLoader
```
> Note : Replace `<your-username>` with your own username in the above command.

- Keep a reference to the original project in `upstream` remote. 
    ```bash
    git remote add upstream https://github.com/ashutoshkrris/EazyLoader
    ```

- If you have already forked the project, update your copy before working.
    ```bash
    git remote update
    git checkout main
    git rebase upstream/main
    ```  

**Step 3. Create a Virtual Environment and install Dependencies.**

- We'll be using `venv` module that comes in-built with Python 3.4 and above. Learn more about [Virtual Environments](http://flask.pocoo.org/docs/1.0/installation/#virtual-environments).

    - Create virtual environment using the following command on Windows, Linux or MacOS :
        ```bash
        python -m venv env
        ```

        - Activate the virtual environment:
            - On Windows:
                ```terminal
                env\Scripts\activate.bat
                ```

            - On Linux and MacOS:
                ```bash
                source env/bin/activate
                ```
            
        - Deactivate the virtual environment (not needed at this stage):
            ```
            deactivate
            ```

- Instead of using `venv` module, you can also use `pipenv` to manage virtual environment. If you don't have it installed, use the command to install it:
    ```bash
    pip install pipenv
    ```
    - To create new virtual environment and activate it using `pipenv`:
        ```bash
        pipenv shell
        ```
    
    - To deactivate the virtual environment (not needed at this stage):
        ```bash
        exit
        ```

Next, we need to install the project dependencies, which are listed in `requirements.txt` or `Pipfile`.

- If you've used `venv` module in the previous step, use this command :
    ```bash
    pip install -r requirements.txt
    ```

- If you've used `pipenv` module in the previous step, use this command : 
    ```bash
    pipenv install
    ```

**Step 4: Update environment variables and run the Server.**

Create a new file named `.env` and update the new file with the following data. It should look similar to this:

```
SECRET_KEY=fdkjshfhjsdfdskfdsfdcbsjdkfdsdf
DEBUG=True
APP_SETTINGS=config.DevelopmentConfig
GOOGLE_CLIENT_API_KEY=None
GITHUB_API_TOKEN=None
IG_USERNAME=None
IG_PASSWORD=None
ADMIN_EMAIL=None
EMAIL_ADDRESS=None
EMAIL_PASSWORD=None
```

> Note : 
> - Every time you modify the environment variables,you need to deactivate the virtual environment and activate it again.
> - Get started with YouTube Data API [here](https://developers.google.com/youtube/v3/getting-started).
> - Learn how to generate Personal Access Tokens on Github [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
> - Learn more about the Environment Variables [here](https://iread.ga/posts/49/do-you-really-need-environment-variables-in-python).


Now we're ready to start our server which is as simple as:

```
(venv) $ python main.py
```

Open http://127.0.0.1:5000 to view it in your browser.

The app will automatically reload if you make changes to the code.
You will see the build errors and warnings in the console.

> If you get BadCredentialsException, checkout this [discussion](https://github.com/ashutoshkrris/EazyLoader/discussions/41)


**Step 5 : Work on the issue assigned**

- Work on the issue(s) assigned to you.
- Add all the files/folders needed.
- After you've made changes or made your contribution to the project add changes to the branch you've just created by:

    ```bash  
    # To add all new files to your branch
    git add .  

    # To add only a few files to Branch_Name
    git add <some files>
    ```

**Step 6 : Commit**

- To commit give a descriptive message for the convenience of reviewer by:

    ```bash
    # This message get associated with all files you have changed  
    git commit -m "message"  
    ```

- **NOTE**: A PR should have only one commit. Multiple commits should be squashed.

**Step 7 : Work Remotely**

- Now you are ready to your work to the remote repository.
- When your work is ready and complies with the project conventions, upload your changes to your fork:

    ```bash  
    # To push your work to your remote repository
    git push -u origin <branch-name>
    ```

**Step 8 : Pull Request**

- Go to your repository in browser and click on compare and pull requests. Then add a title and description to your pull request that explains your contribution.
- Voila! Your Pull Request has been submitted and will be reviewed by the moderators and merged.🥳


<br>
<h5 align="center">
< Happy Contributing />
<br>
<a href="https://ashutoshkrris.tk">Ashutosh Krishna</a> | © 2021
</h5>
