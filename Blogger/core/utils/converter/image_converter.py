from PIL import Image


class ImageConverter:
    def __init__(self):
        pass

    def resize(self, image_paths, resolution=(512, 512)):
        try:
            for image_path in image_paths:
                im = Image.open(image_path)
                im = im.resize(resolution)
                im.save(image_path)
            return True
        except Exception as e:
            print(f"Error resizing image: {str(e)}")
            return False
