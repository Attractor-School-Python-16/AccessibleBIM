import os


def custom_upload_to_func(instance, filename):
    return os.path.join('summernote_attachments', filename)
