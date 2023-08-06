import requests,urllib3,time
urllib3.disable_warnings()

class AsposeCompressor:
    def __init__(self, path_to_file: str):
        """`path_to_file`: Path to the file you want to compress
        ```py
        ac = AsposeCompressor("./video.mp4")
        ```
        """
        self.files = {
            '1': open(path_to_file, 'rb'),
            'VideoFormat': (None, 'mp4'),
        }

    def compress_video(self) -> str:
        """Returns the download link for the compressed file
        ```py
        ac = AsposeCompressor("./video.mp4")
        download_link = ac.compress_video()
        print(download_link)
        ```
        """
        response = requests.post('https://api.products.aspose.app/video/compress/api/compress', files=self.files, verify=False)
        file_request_id = response.json()["Data"]["FileRequestId"]
        params = {
            'fileRequestId': file_request_id,
        }
        response = None

        response = requests.get(
            'https://api.products.aspose.app/video/compress/api/compress/HandleStatus',
            params=params,
            verify=False,
        )

        while response.json()["Data"]["DownloadLink"] == None:
            print("[!] Failed! Retrying.")
            response = requests.get(
                'https://api.products.aspose.app/video/compress/api/compress/HandleStatus',
                params=params,
                verify=False,
            )
            time.sleep(5)
        return response.json()["Data"]["DownloadLink"]