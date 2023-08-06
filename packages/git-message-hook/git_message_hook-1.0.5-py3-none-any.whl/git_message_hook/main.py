import os
import shutil


def main():
    if not os.path.isdir(".git"):
        print(
            "error: .git directory not found in the current path. This is not a git repository?"
        )
        return

    template_path = os.path.expanduser("~/.git-templates/hooks/commit-msg")
    if not shutil.which("git"):
        print(
            "error: git not found on path. please install git and then run pip install --upgrade git-message-hook"
        )
        return
    if not os.path.exists(template_path):
        print(
            f"error: git hooks template not found on {template_path}, please run pip install git-message-hook"
        )
        return
    shutil.copy(template_path, ".git/hooks/")
    print("success: conventional git messages are enforced")


if __name__ == "__main__":
    main()
