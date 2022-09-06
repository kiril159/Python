from src.app.utils.messages import NOT_CORRECT_FORMAT

def str_format_verity(name):
    if name[0] in '.-' or name[:5] == '.atom' or name[:4] == '.git':
        return {'400': NOT_CORRECT_FORMAT}

