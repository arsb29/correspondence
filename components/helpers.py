def convert_a(match_obj):
    if match_obj.group() is not None:
        return '<a href="">' + match_obj.group() + '</a>'
