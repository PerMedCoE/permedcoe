

class ContainerImageException(Exception):
    """
    Container image exception.
    """

    def __init__(self, image_path):
        super(ContainerImageException, self).__init__("Container image " +
                                                      image_path +
                                                      " NOT FOUND!")


class PerMedCoEException(Exception):
    """
    Generic PerMedCoE exception.
    """

    def __init__(self, message):
        super(PerMedCoEException, self).__init__(message)
