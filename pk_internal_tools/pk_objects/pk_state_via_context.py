import time

# performance util
# for optimize using cpu resource
"""상태 변화 감지 및 속도 조절"""


class SpeedControlContext:
    def __init__(self):
        self.milliseconds_for_speed_control_origin = 100
        self.milliseconds_for_speed_control = self.milliseconds_for_speed_control_origin
        self.milliseconds_for_speed_control_max = 5000
        # self.milliseconds_for_speed_control_max = 3000
        self.milliseconds_for_speed_control_delta = 200
        self.state_previous = None
        self.time_changed_last = time.time()

    @classmethod
    def set_pk_context_state_milliseconds_for_speed_control_forcely(self, value: int):
        """
        milliseconds_for_speed_control 값을 강제로 설정합니다.
        자동 상태 변화 조정 로직과 무관하게 직접 제어할 때 사용합니다.
        """
        value = max(0, min(value, self.milliseconds_for_speed_control_max))
        self.milliseconds_for_speed_control = value

    @classmethod
    def set_pk_context_state(self, state_new, pk_context_state):
        import time
        if self.state_previous is None or state_new != self.state_previous:
            self.state_previous = state_new
            self.time_changed_last = time.time()
            self.milliseconds_for_speed_control = self.milliseconds_for_speed_control_origin
        else:
            elapsed_time = time.time() - self.time_changed_last
            if elapsed_time >= 2:
                pk_context_state.milliseconds_for_speed_control = min(pk_context_state.milliseconds_for_speed_control + pk_context_state.milliseconds_for_speed_control_delta, pk_context_state.milliseconds_for_speed_control_max)
