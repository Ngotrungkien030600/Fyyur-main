from fabric.api import local, abort, prompt

# prepare for deployment


def test():
    result = local(
        "python test_tasks.py -v && python test_users.py -v", warn_only=True, capture=True
    )
    if result.failed and not prompt("Tests failed. Continue?", default=False):
        abort("Aborted at user request.")


def commit():
    message = prompt("Enter a git commit message: ")
    local("git add . && git commit -am '{}'".format(message))


def push():
    local("git push origin master")


def prepare():
    test()
    commit()
    push()

# deploy to heroku


def pull():
    local("git pull origin master")


def heroku():
    local("git push heroku master")


def heroku_test():
    local(
        "heroku run python test_tasks.py -v && heroku run python test_users.py -v"
    )


def deploy():
    pull()
    test()
    commit()
    heroku()
    heroku_test()

# rollback


def rollback():
    local("heroku rollback")
