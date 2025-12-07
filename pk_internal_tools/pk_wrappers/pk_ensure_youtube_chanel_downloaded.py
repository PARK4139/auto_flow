from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_youtube_videos_downloaded_v_2025_10_08_1256 import ensure_youtube_videos_downloaded_v_2025_10_08_1256
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.get_videos_urls_from_youtube_channel_main_page import get_videos_urls_from_youtube_channel_main_page
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        while 1:
            url_youtube_channel_main_page = input('url_youtube_channel_main_page=')
            url_youtube_channel_main_page = url_youtube_channel_main_page.strip()
            video_urls = get_videos_urls_from_youtube_channel_main_page(url_youtube_channel_main_page=url_youtube_channel_main_page)
            ensure_youtube_videos_downloaded_v_2025_10_08_1256(video_urls=video_urls)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
