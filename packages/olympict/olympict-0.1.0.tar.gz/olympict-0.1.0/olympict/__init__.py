import os
import shutil
from glob import glob
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    cast,
)

import cv2
import numpy as np
from olympipe import Pipeline

from olympict.video_saver import PipelineVideoSaver

from .image_tools import ImTools

# from nptyping import NDArray, Int, Shape
# Img = NDArray[Shape["2, 2"], Int]

Img = cv2.Mat
Point = Tuple[float, float]
Size = Tuple[int, int]
Color = Tuple[int, int, int]
ImgFormat = Literal["png", "jpeg", "bmp"]
VidFormat = Literal["mp4", "mkv", "avi"]


class OlympFile:
    def __init__(self, path: Optional[str] = None):
        self.path = path or ""

    @property
    def size(self) -> Size:
        raise NotImplementedError("No size for this object")


class OlympImage(OlympFile):
    __id = 0

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        if path is None:
            self.path = f"./{self.__id}.png"
            self.__id += 1
            self.img: Img = np.zeros((1, 1, 3), dtype=np.uint8)
        else:
            self.img: Img = cv2.imread(path)
        self.metadata: Dict[str, Any] = {}

    @staticmethod
    def resize(
        size: Size,
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Callable[["OlympImage"], "OlympImage"]:
        def r(o: "OlympImage") -> "OlympImage":
            if pad_color is None:
                o.img = cv2.resize(o.img, size, interpolation=interpolation)
            else:
                o.img = ImTools.pad_to_output_size(
                    o.img, size, pad_color, interpolation=interpolation
                )
            return o

        return r

    @staticmethod
    def rescale(
        scales: Tuple[float, float],
        pad_color: Optional[Color] = None,
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Callable[["OlympImage"], "OlympImage"]:
        """Rescale function
        This function applies a scale [x_s, y_s] to a given image
        The resulting image dimensions are [w * x_s, h * y_s]
        """

        def r(o: "OlympImage") -> "OlympImage":
            w, h = o.size
            x_scale, y_scale = scales
            size = (int(round(w * x_scale)), int(round(h * y_scale)))
            if pad_color is None:
                o.img = cv2.resize(o.img, size, interpolation=interpolation)
            else:
                o.img = ImTools.pad_to_output_size(
                    o.img, size, pad_color, interpolation=interpolation
                )
            return o

        return r

    def move_to_path(self, path: str):
        """This function moves images to a new location. If path is a directory, then it will keep its old name and move to the new directory.
        Else it will be given path as a new name (This might be bad for multiple images).
        """
        #  TODO: Ensure folder or not
        if os.path.isdir(path):
            _, filename = os.path.split(self.path)
            path = os.path.join(path, filename)
        shutil.move(self.path, path)
        self.path = os.path.abspath(path)

    def change_folder_path(self, new_folder_path: str):
        self.path = os.path.join(new_folder_path, os.path.basename(self.path))

    def move_to(self, func: Callable[[str], str]):
        output = func(self.path)
        self.move_to_path(output)

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        _ = cv2.imwrite(self.path, self.img)

    def save_as(self, path: str):
        if os.path.isdir(path):
            _, filename = os.path.split(self.path)
            path = os.path.join(path, filename)

        self.path = os.path.abspath(path)
        self.save()

    @property
    def size(self) -> Size:
        h, w, _ = self.img.shape
        return (w, h)

    @staticmethod
    def load(path: str, metadata: Dict[str, Any] = {}) -> "OlympImage":
        o = OlympImage()
        o.path = path
        o.img = cv2.imread(o.path)
        o.metadata = metadata
        return o

    @staticmethod
    def from_buffer(
        buffer: Img, path: str = "", metadata: Dict[str, Any] = {}
    ) -> "OlympImage":
        o = OlympImage()
        o.path = path
        o.img = buffer
        o.metadata = metadata
        return o


class OlympBatch(OlympFile):
    def __init__(self, data: Img, metadata: List[Dict[str, Any]] = []):
        assert len(data.shape) >= 4
        self.data = data
        self.metadata = metadata

    @property
    def size(self) -> Size:
        _, h, w, _ = self.data.shape
        return (w, h)

    @staticmethod
    def from_images(images: List[OlympImage]) -> "OlympBatch":
        data = np.array([i.img for i in images])
        metadata = [i.metadata for i in images]

        return OlympBatch(data, metadata)


class OlympVid(OlympFile):
    __id = 0

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        if path is None:
            self._tmp_path = f"./{self.__id}.mp4"
            self.__id += 1
        self._tmp_path = ""
        self._fps = 25

    def get_fps(
        self,
    ) -> int:
        raise NotImplementedError()

    def to_format(self, fmt: VidFormat) -> "OlympImage":
        raise NotImplementedError()

    def get_temp_path(self) -> str:
        raise NotImplementedError()


class ObjPipeline:
    def resize(self, size: Size, count: int = 1):
        """
        Args:
            size (Size): width, height
        """

    def from_generator(self, generator: Generator[Img, None, None]) -> "ObjPipeline":
        raise NotImplementedError()

    def rescale(self, size: Tuple[float, float], count: int = 1) -> "ObjPipeline":
        """
        Args:
            size (Tuple[float, float]): width multiplier, height multiplier
        """
        raise NotImplementedError()

    def crop(self, size: Size, count: int = 1) -> "ObjPipeline":
        """
        Args:
            size (Size): width, height
        """
        raise NotImplementedError()

    def img_task(self, img_func: Callable[[Img], Img]) -> "ObjPipeline":
        raise NotImplementedError()

    def path_task(self, path_func: Callable[[str], str]) -> "ObjPipeline":
        raise NotImplementedError()


class OPipeline:
    def __init__(self, source: Iterable[OlympFile]):
        self._data = source
        self._pipeline: Optional[Pipeline[OlympFile]] = None

    @staticmethod
    def load_folder(
        path: str, extensions: List[str] = [""], recursive: bool = False
    ) -> "OPipeline":
        raise NotImplementedError()

    def wait_for_completion(self) -> None:
        if self._pipeline is None:
            return
        return self._pipeline.wait_for_completion()

    def wait_for_results(self) -> List[OlympFile]:
        if self._pipeline is None:
            return []
        return self._pipeline.wait_for_results()


class ImagePipeline(OPipeline):
    def __init__(self, data: Optional[Iterable[OlympImage]] = None):
        self._pipeline: Optional[Pipeline[OlympImage]] = None
        if data is not None:
            self._pipeline = Pipeline(data)

    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympImage(p) for p in paths]

        if metadata_function is not None:
            for d in data:
                d.metadata = metadata_function(d.path)

        return ImagePipeline(data)

    @staticmethod
    def load_folders(
        paths: List[str],
        extensions: List[str] = ["png", "jpg", "jpeg", "bmp"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
        metadata_function: Optional[Callable[[str], Any]] = None,
    ) -> "ImagePipeline":
        all_data: List[OlympImage] = []
        for path in paths:
            sub_paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)

            sub_paths = [
                p for p in sub_paths if os.path.splitext(p)[1].strip(".") in extensions
            ]

            if order_func is not None:
                sub_paths.sort(key=order_func, reverse=reverse)

            data = [OlympImage(p) for p in sub_paths]

            if metadata_function is not None:
                for d in data:
                    d.metadata = metadata_function(d.path)

            all_data.extend(data)

        return ImagePipeline(all_data)

    def task(
        self, func: Callable[[OlympImage], OlympImage], count: int = 1
    ) -> "ImagePipeline":
        output = ImagePipeline()
        if self._pipeline is None:
            raise Exception("Undefined pipeline")
        output._pipeline = self._pipeline.task(func, count)

        return output

    def task_img(self, func: Callable[[Img], Img], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.img = func(o.img)
            return o

        return self.task(r, count)

    def task_path(self, func: Callable[[str], str], count: int = 1) -> "ImagePipeline":
        def r(o: OlympImage) -> OlympImage:
            o.path = func(o.path)
            return o

        return self.task(r, count)

    def rescale(
        self,
        size: Tuple[float, float],
        pad_color: Optional[Tuple[int, int, int]] = None,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.rescale(size, pad_color), count)

    def resize(
        self,
        size: Tuple[int, int],
        pad_color: Optional[Tuple[int, int, int]] = None,
        interpolation: int = cv2.INTER_LINEAR,
        count: int = 1,
    ) -> "ImagePipeline":
        return self.task(OlympImage.resize(size, pad_color, interpolation), count)

    def crop(
        self,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        pad_color: Color = (0, 0, 0),
    ) -> "ImagePipeline":
        def r(img: Img) -> Img:
            return ImTools.crop_image(
                img, top=top, left=left, bottom=bottom, right=right, pad_color=pad_color
            )

        return self.task_img(r)

    def keep_each_frame_in(
        self, keep_n: int = 1, discard_n: int = 0
    ) -> "ImagePipeline":
        if self._pipeline is None:
            raise Exception("No defined pipeline")

        def discarder():
            while True:
                for _ in range(keep_n):
                    yield True
                for _ in range(discard_n):
                    yield False

        d = discarder()

        def get_next(_: Any) -> bool:
            return next(d)

        output = ImagePipeline()
        output._pipeline = self._pipeline.filter(get_next)

        return output

    def debug_window(self) -> "ImagePipeline":
        def d(o: "OlympImage") -> "OlympImage":
            return o

        return self.task(d)

    def to_video(
        self, img_to_video_path: Callable[[OlympImage], str]
    ) -> "VideoPipeline":
        output = VideoPipeline()
        output._pipeline = self._pipeline.class_task(
            PipelineVideoSaver,
            PipelineVideoSaver.process_file,
            [img_to_video_path],
            PipelineVideoSaver.finish,
        )

        return output

    def to_format(self, format: ImgFormat) -> "ImagePipeline":
        def change_format(path: str) -> str:
            base, _ = os.path.splitext(path)

            fmt = f".{format}" if "." != format[0] else format

            return base + fmt

        return self.task_path(change_format)

    def save_to_folder(self, folder_path: str) -> "ImagePipeline":
        os.makedirs(folder_path, exist_ok=True)

        def s(o: "OlympImage") -> "OlympImage":
            o.change_folder_path(folder_path)
            o.save()
            return o

        return self.task(s)

    def save(self) -> "ImagePipeline":
        def s(o: "OlympImage") -> "OlympImage":
            o.save()
            return o

        return self.task(s)


class VideoPipeline(OPipeline):
    def __init__(self, data: Optional[Iterable[OlympVid]] = None):
        self._pipeline: Optional[Pipeline[OlympVid]] = None
        if data is not None:
            self._pipeline = Pipeline(data)

    @staticmethod
    def load_folder(
        path: str,
        extensions: List[str] = ["mkv", "mp4"],
        recursive: bool = False,
        order_func: Optional[Callable[[str], int]] = None,
        reverse: bool = False,
    ) -> "VideoPipeline":
        paths: List[str] = glob(os.path.join(path, "**"), recursive=recursive)
        paths = [p for p in paths if os.path.splitext(p)[1].strip(".") in extensions]

        if order_func is not None:
            paths.sort(key=order_func, reverse=reverse)

        data = [OlympVid(p) for p in paths]

        return VideoPipeline(data)

    def task(
        self, func: Callable[[OlympVid], OlympVid], count: int = 1
    ) -> "VideoPipeline":
        raise NotImplementedError()

    def split_duration(self, duration: float) -> "VideoPipeline":
        raise NotImplementedError()

    def change_fps(self, fps: int) -> "VideoPipeline":
        raise NotImplementedError()

    def move_to_folder(self, path: str) -> "VideoPipeline":
        raise NotImplementedError()

    def move_to(self, path: str) -> "VideoPipeline":
        raise NotImplementedError()

    def format(self, format: Literal["mkv"]) -> "VideoPipeline":
        raise NotImplementedError()

    def to_sequence(self) -> "ImagePipeline":
        if self._pipeline is None:
            raise Exception("No defined pipeline")

        def generator(o: "OlympVid") -> Generator[OlympImage, None, None]:
            capture: Any = cv2.VideoCapture(o.path)
            res, frame = cast(Tuple[bool, Img], capture.read())
            idx = 0
            while res:
                new_path = f"{o.path}_{idx}.png"
                yield OlympImage.from_buffer(
                    frame, new_path, {"video_path": o.path, "video_frame": idx}
                )
                res, frame = cast(Tuple[bool, Img], capture.read())
                idx += 1

        output = ImagePipeline()
        output._pipeline = self._pipeline.explode(generator)

        return output

    def draw_polygons(self, polygons: List[List[Point]]) -> "ImagePipeline":
        raise NotImplementedError()

    def draw_polygon(self, polygon: List[Point]) -> "ImagePipeline":
        raise NotImplementedError()

    def draw_heatmap(self, heatmap_func: Callable[[Img], Img]) -> "ImagePipeline":
        raise NotImplementedError()
