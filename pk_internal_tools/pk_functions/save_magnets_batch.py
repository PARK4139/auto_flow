import logging


def save_magnets_batch(magnets):
    #
    from urllib.parse import urlparse, parse_qs, unquote
    logging.debug(f"Saving {len(magnets)} magnets")
    conn = get_db_conn()
    cur = conn.cursor()
    data = [(m, parse_qs(urlparse(unquote(m)).query).get("dn", [""])[0]) for m in magnets]
    cur.executemany("INSERT IGNORE INTO nyaa_magnets(magnet,title) VALUES(%s,%s)", data)
    conn.commit()
    cur.close()
    conn.close()
    logging.debug("Batch saved")
