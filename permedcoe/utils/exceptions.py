

class ContainerImageException(Exception):
    """
    Container image exception.
    """

    def __init__(self, image_path):
        super(ContainerImageException, self).__init__("Container image " +
                                                      image_path +
                                                      " NOT FOUND!")
