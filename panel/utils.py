def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    try:
        return 'user_{0}/{1}'.format(instance.owner.id, filename)
    except:
        return 'user_{0}/{1}'.format(instance.sender.id, filename)