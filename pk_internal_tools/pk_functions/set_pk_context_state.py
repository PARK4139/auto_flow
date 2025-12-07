def set_pk_context_state(state_new, pk_context_state):
    import time
    if pk_context_state.state_previous is None or state_new != pk_context_state.state_previous:
        pk_context_state.state_previous = state_new
        pk_context_state.time_changed_last = time.time()
        pk_context_state.milliseconds_for_speed_control = pk_context_state.milliseconds_for_speed_control_origin
    else:
        elapsed_time = time.time() - pk_context_state.time_changed_last
        if elapsed_time >= 2:
            pk_context_state.milliseconds_for_speed_control = min(pk_context_state.milliseconds_for_speed_control + pk_context_state.milliseconds_for_speed_control_delta, pk_context_state.milliseconds_for_speed_control_max)
