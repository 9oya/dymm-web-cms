def allowed_image_file(filename):
    allowed_extensions = ['png', 'svg']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def allowed_license_file(filename):
    allowed_extensions = ['pdf']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
