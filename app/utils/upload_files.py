from fastapi.responses import FileResponse
import os


class UploadFiles:

    def __init__(
        self,
        upload_path: str,
        module: str,
    ):
        self.upload_path = upload_path
        self.module = module


    def download_file_server(self, filename: str):
        try:
            new_upload_path = os.path.join(self.upload_path, self.module)
            file_path = os.path.join(new_upload_path, filename)

            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False

            return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
        except Exception as e:
            print(f"Error downloading the file: {e}")
            return False


    def upload_files_server(self, file: bytes):
        try:
            new_upload_path = f"{self.upload_path}/{self.module}"
            original_filename = file.filename
            file_path = os.path.join(new_upload_path, original_filename)

            file_count = 0
            while os.path.exists(file_path):
                file_count += 1

                filename, file_extension = os.path.splitext(original_filename)
                original_filename = f"{filename}_{file_count}{file_extension}"
                file_path = os.path.join(new_upload_path, original_filename)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file.file.read())

            return {"file": original_filename}

        except Exception as e:
            print(f"Error uploading the file: {e}")

            return False


    def delete_file_server(self, filename: str):
        try:
            new_upload_path = f"{self.upload_path}/{self.module}"
            file_path = os.path.join(new_upload_path, filename)

            if not os.path.exists(file_path):
                return False

            os.remove(file_path)
            return True

        except Exception as e:
            print(f"Error deleting the file: {e}")

            return False
