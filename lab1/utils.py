def ellipsis(msg, show_len=16):
    msg = repr(msg)
    if len(msg) <= show_len * 2:
        return msg
    return msg[:show_len] + "..." + msg[-show_len:]