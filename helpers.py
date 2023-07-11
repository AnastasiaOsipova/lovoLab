
def get_photo(extension=None):
    file = f"profile_pics/profile_pic.{extension}" if extension else f"profile_pics/profile_pic.jpg"
    return {"photo": open(file, "rb")}

