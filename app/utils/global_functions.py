from fastapi import HTTPException, status
import secrets
import string
import git


class GlobalFunctions:
    @staticmethod
    def validate_file_extension(filename: str, extensions: list):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions

    @staticmethod
    def generate_temporary_password(length: int):
        alphabet = string.ascii_letters + string.digits
        temp_password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return temp_password

    @staticmethod
    def get_exception_details(key: str, custom_detail: str = None):
        exceptions = {
            "401": (status.HTTP_401_UNAUTHORIZED, "Token not available"),
            "404": (status.HTTP_404_NOT_FOUND, "Could not find the action"),
            "400": (status.HTTP_400_BAD_REQUEST, "Could not process the action"),
        }

        http_status_code, default_detail = exceptions.get(
            key, (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
        )
        detail = custom_detail if custom_detail is not None else default_detail

        raise HTTPException(status_code=http_status_code, detail=detail)

    @staticmethod
    def get_app_version() -> str:
        try:
            repo = git.Repo(search_parent_directories=True)
            tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            latest_tag = tags[-1] if tags else "0.0.0"
            return str(latest_tag)
        except Exception as e:
            print(f"Error getting git tag: {e}")
            return "0.0.0"

global_functions = GlobalFunctions()
