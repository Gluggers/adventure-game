### LANGUAGE CONSTANTS ###
LANG_ENGLISH = 0x0
LANG_ESPANOL = 0x1
DEFAULT_LANGUAGE = LANG_ENGLISH

class Language():
    current_language_id = DEFAULT_LANGUAGE
    valid_language_ids = set([
        LANG_ENGLISH,
        LANG_ESPANOL,
    ])

    @classmethod
    def set_current_language_id(cls, new_id):
        if new_id in cls.valid_language_ids:
            cls.current_language_id = new_id

    @classmethod
    def get_current_language_id(cls):
        return cls.current_language_id
