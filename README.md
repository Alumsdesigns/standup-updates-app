# Standup Updates App

<p align="center">
  <img src="" alt="mockup of how the website looks on desktop, laptop and tablet"/>
</p>

[Link to Website]()

[GitHub Repo]()


***


## About

The Daily Log App is a simple terminal tool that helps you keep track of what you’re working on each day. Instead of relying on sticky notes, random emails, or trying to remember everything right before a stand-up, the app gives you one clean place to jot down your updates. It keeps things structured and easy to review, so you always know what you did yesterday, what you’re doing today, and what might be blocking you.



## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

## Bug Fixes

### Fixed AttributeError in `edit_line` method

As i was creating the edit line functionality I resolved an issue where calling `edit_line` on the `DailyLog` object raised an `AttributeError` because the method was missing in the class definition. I fixed the instantiation of the `DailyLog` object to ensure proper usage.

Users reported encountering this error when trying to edit logs:

![Edit Attribute Error Fix](images/bug_fixes/edit_attr_error_fix.png)

This fix improves the stability and usability of the log editing feature.

---

