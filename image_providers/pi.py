import io
import time
from typing import Generator, Union

from picamera import Picamera


from image_providers.image_provider import ImageProvider


class PicameraImageProvider(ImageProvider):

    _picamera = None

    def __init__(self, width: int = 1200, height: int = 900, framerate: int = 30, *args, **kwargs) -> None:
        self.width = width,
        self.height = height
        self.framerate = framerate

        ImageProvider.__init__(self, *args, **kwargs)

    def __enter__(self):
        if PicameraImageProvider._picamera is None:
            PicameraImageProvider._picamera = Picamera()

        PicameraImageProvider._picamera.resolution = self.width, self.height
        PicameraImageProvider._picamera.framerate = self.framerate

        if not PicameraImageProvider._picamera.started:
            PicameraImageProvider._picamera.start()
            time.sleep(2)

        return super().__enter__()

    def frames(self) -> Generator[io.BytesIO, None, None]:
        try:
            stream = io.BytesIO()
            while True:
                PicameraImageProvider._picamera.capture_file(
                    stream, format='jpeg')
                stream.seek(0)

                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
        finally:
            PicameraImageProvider._picamera.stop()
