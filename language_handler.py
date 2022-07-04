from en_dict import get_en_dict

LANG_LIST = ['en']

lang_dicts = {
  "en": get_en_dict(),
}


def get_for_all_langs(accessor):
    response = ''

    for lang in lang_dicts:
        response = response + get_translation(lang, accessor)

    return response


def get_translation(lang, accessor):
    key_list = accessor.split('.')
    partial_result = lang_dicts[lang]

    for key in key_list:
        if key not in partial_result:
            return None

        partial_result = partial_result[key]

    return partial_result


def is_invalid_lang(lang):
    return lang not in LANG_LIST
