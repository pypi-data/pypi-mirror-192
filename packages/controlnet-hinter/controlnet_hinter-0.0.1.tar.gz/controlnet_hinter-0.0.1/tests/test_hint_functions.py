import pytest
from diffusers.utils import load_image
from PIL import Image
from controlnet_hinter import *
import os

def test_functions_without_exception():
    result_folder = 'result/'
    os.makedirs(result_folder, exist_ok=True)

    original_image = load_image(
        "https://huggingface.co/datasets/diffusers/test-arrays/resolve/main/stable_diffusion_imgvar/input_image_vermeer.png")

    Image.fromarray(hint_canny(original_image)).save(
        result_folder + 'canny.png')
    Image.fromarray(hint_depth(original_image)).save(
        result_folder + 'depth.png')
    Image.fromarray(hint_fake_scribble(original_image)).save(
        result_folder + 'fake_scribble.png')
    Image.fromarray(hint_hed(original_image)).save(result_folder + 'hed.png')
    Image.fromarray(hint_hough(original_image)).save(
        result_folder + 'hough.png')
    Image.fromarray(hint_normal(original_image)).save(
        result_folder + 'normal.png')
    Image.fromarray(hint_openpose(original_image)).save(
        result_folder + 'openpose.png')
    Image.fromarray(hint_scribble(original_image)).save(
        result_folder + 'scribble.png')
    Image.fromarray(hint_segmentation(original_image)
                    ).save(result_folder + 'segmentation.png')
