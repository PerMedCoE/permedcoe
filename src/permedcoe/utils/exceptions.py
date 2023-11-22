class ContainerImageException(Exception):
    """
    Container image exception.
    """

    def __init__(self, image_path):
        super().__init__(f"Container image {image_path} NOT FOUND!")


class PerMedCoEException(Exception):
    """
    Generic PerMedCoE exception.
    """

    def __init__(self, message):
        super().__init__(message)
