from typing import List, Tuple
import cv2
import numpy as np

Size = Tuple[int, int]
Color = Tuple[int, int, int]
Image = cv2.Mat


class ImTools:
    @staticmethod
    def load(path: str) -> Image:
        return cv2.imread(path)

    @staticmethod
    def load_multiple(paths: List[str]) -> List[Image]:
        return [ImTools.load(path) for path in paths]

    @staticmethod
    def pad_square(image: Image, color: Color = (0, 0, 0)) -> Image:
        """
        Pads an image to fit in a square
        Args:
            image (Image): cv2.Image
        Returns:
            Image: cv2.Image
        """
        max_dim = max(image.shape[:-1])
        padded_image = ImTools.pad_to_output_size(image, (max_dim, max_dim), color)
        return padded_image

    @staticmethod
    def pad_to_ratio(image: Image, ratio: float, color: Color = (0, 0, 0)) -> Image:
        """
        Pads an image to the specified ratio

        Args:
            image (Image): cv2.Image
            ratio (float): width / height

        Returns:
            Image: cv2.Image
        """
        height, width = image.shape[:-1]
        image_ratio = width / height
        if image_ratio < ratio:
            # keep height
            dims = (height, int(round(height * ratio)))
        else:
            # keep width
            dims = (int(round(width / ratio)), width)

        return ImTools.pad_to_output_size(image, dims, color)

    @staticmethod
    def pad_to_output_size(
        image: Image,
        size: Size,
        color: Color = (0, 0, 0),
        interpolation: int = cv2.INTER_LINEAR,
    ) -> Image:
        """Pads an image to the specified size (adds black pixels)

        Args:
            image (Image): cv2.Image
            size (Size): height, width

        Returns:
            Image: cv2.Image
        """
        height, width = image.shape[:-1]

        out_h, out_w = size

        desired_ratio = out_w / out_h
        input_ratio = width / height

        if input_ratio > desired_ratio:
            resized = cv2.resize(
                image, (out_w, int(out_w / input_ratio)), interpolation=interpolation
            )
        else:
            resized = cv2.resize(
                image, (int(out_h * input_ratio), out_h), interpolation=interpolation
            )

        resized_h, resized_w, _ = resized.shape

        pad_top = int((out_h - resized_h) / 2)
        pad_left = int((out_w - resized_w) / 2)
        pad_bottom = int(out_h - pad_top - resized_h)
        pad_right = int(out_w - pad_left - resized_w)

        padded_image = cv2.copyMakeBorder(
            resized,
            pad_top,
            pad_bottom,
            pad_left,
            pad_right,
            cv2.BORDER_CONSTANT,
            value=color,
        )

        return padded_image

    @staticmethod
    def crop_image(
        image: Image,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        pad_color: Color = (0, 0, 0),
    ) -> Image:
        """Crops an image. It can also pad an image if numbers are < 0

        Args:
            image (Image): Input cv2 image
            top (int, optional): pixels to remvoe from the top. Defaults to 0.
            left (int, optional): pixels to remvoe from the left. Defaults to 0.
            bottom (int, optional): pixels to remvoe from the bottom. Defaults to 0.
            right (int, optional): pixels to remvoe from the right. Defaults to 0.
            pad_color (Color, optional): Color to use if padding.

        Returns:
            Image: The cv2 image cropped
        """

        h, w, channels = image.shape

        new_h = h - top - bottom
        new_w = w - left - right

        img = np.ones((new_h, new_w, channels), dtype=np.uint8) * pad_color

        left_source = max(left, 0)
        left_destination = max(-left, 0)

        top_source = max(top, 0)
        top_destination = max(-top, 0)

        copy_w = w - max(left, 0) - max(right, 0)
        copy_h = h - max(top, 0) - max(bottom, 0)

        img[
            top_destination : top_destination + copy_h,
            left_destination : left_destination + copy_w,
            :,
        ] = image[
            top_source : top_source + copy_h,
            left_source : left_source + copy_w,
            :,
        ]

        return img

    @staticmethod
    def draw_heatmap(image: Image, map: Image, alpha_map: float = 0.5) -> Image:
        """
        Args:
            image (Image): cv2.image (HWC)
            map (Image): [0-255] cv2.image (HW)
            alpha_map (float): [0-1] balance between image and map
        """

        heatmap_img = cv2.applyColorMap(np.array(map, dtype=np.uint8), cv2.COLORMAP_JET)

        heatmap_img = cv2.resize(
            heatmap_img, image.shape[:2][::-1], interpolation=cv2.INTER_LINEAR
        )

        output = cv2.addWeighted(
            heatmap_img,
            alpha_map,
            image,
            1 - alpha_map,
            0,
            dtype=cv2.PARAM_UNSIGNED_INT,
        )

        return output

    @staticmethod
    def draw_multiple_heatmaps(
        image: Image, maps: Image, alpha_map: float = 0.5
    ) -> Image:
        """
        Args:
            image (Image): cv2.image (HWC)
            map (Image): [0-255] cv2.image (HW)
            alpha_map (float): [0-1] balance between image and map
        """
        max_map: Image = np.max(maps, axis=-1)
        return ImTools.draw_heatmap(image, max_map, alpha_map=alpha_map)
