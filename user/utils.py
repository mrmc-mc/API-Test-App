def user_upload_dir(instance , filename):
    """  set upload directroy by user id and change file name   """

    return f'user_{instance.user.id}/{instance.user.id}_{filename}_{timezone.now()}.{filename.split(".")[-1]}'