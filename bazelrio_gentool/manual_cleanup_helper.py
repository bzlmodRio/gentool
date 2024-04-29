
def manual_cleanup_helper(filename, callback):
    with open(filename, "r") as f:
        contents = f.read()

    new_contents = callback(contents)
    if new_contents == contents:
        raise Exception("Nothing was replaced!")

    with open(filename, "w") as f:
        f.write(new_contents)