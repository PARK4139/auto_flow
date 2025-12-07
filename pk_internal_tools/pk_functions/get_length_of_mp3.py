def get_length_of_mp3(f: str):
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import traceback

    import mutagen
    try:
        from mutagen.mp3 import MP3
        audio = MP3(f)
        return audio.info.length
    except mutagen.MutagenError:
        # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")   # gtts 모듈 불능? mutagen 모듈 불능? license 찾아보자 으로 어쩔수 없다.
        return
    except Exception:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
