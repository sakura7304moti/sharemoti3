from src.route.service.module import top_image

def get_image():
    """
    旅の画像をランダムに取得
    """
    path_list = top_image.image_list()
    path = top_image.get_image(path_list)
    return path