def user_avatar_path(instance, filename):
    return f"avatar/user_{instance.id}/{filename}"
