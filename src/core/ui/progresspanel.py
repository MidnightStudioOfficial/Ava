from threading import Thread, Lock
from time import time, sleep
from tkinter import ttk
from datetime import timedelta


class Progresspanel(ttk.Frame):
    """
    Task is a module that runs a loop in an indivisual thread that does
    something, and can be paused, resumed, and terminated. It has buttons and
    progress_bar pre-set in self.frame for easy use.
    """

    def __init__(self, parent, total: int = 1, task: callable = None,
                 title: str = None, verbose: bool = True):
        """
        :param parent: parent widget
        :param total: total number of iterations for self.i in task_loop to
            iterate. User can set this in set_iteration_num().
        :param task: user-defined task to be run in a loop. This should be
            customized. User can set this in set_task() or overwrite task().
        :param title: title of the task. It will be shown in the progress panel.
        :param verbose: whether to print out the status of the task to terminal
            in pre-defined after_ methods. User can also use it in overwritten
            after_ methods for debugging.
        :param i: current iteration number
        :param status: status of the task. It can be one of the following:
            _Status._RUNNING, _Status._PAUSING, _Status._PAUSED,
            _Status._TERMINATING, _Status._TERMINATED
        :param _time_per_iteration: time per iteration in seconds to estimate
            the remaining time.
        :param _remaining_time: remaining time in seconds to estimate the time
            when the task will be completed.
        :param _iteration_step: step size for updating progress bar. It is
            useful when user updates the progress bar with non-1 step size
            iteration numbers.
        :param _i_init: initial iteration number. It records the initial value
            of self.i when the task is started. It is useful for calculating
            remaining time accurately when user starts the task from a non-zero
            iteration number.
        :param _pause_resumed: whether the task is resumed just after it was
            paused. See is_pause_resumed() for more details.
        :param _iteration_timestamp: timestamp of the last iteration. It is
            useful for calculating remaining time.
        """
        super().__init__(parent)
        self.i = 0
        self.status = _Status._TERMINATED
        self._mutex_progress_notice = Lock()
        self.parent = parent
        self._set_total(total)
        self.set_task(task)
        self.title = title
        self.set_verbose(verbose)
        self._time_per_iteration = 0
        self._remaining_time = 0
        self._iteration_step = 1
        self._i_init = None
        self._create_widgets()
        self._pause_resumed = False
        self._iteration_timestamp = None

    def set_total(self, total):
        """
        Set the total number of iterations for the task. Exposed to users.
        """
        self._set_total(total)
        self._label_status.config(text=self._get_progress_notice())

    def set_task(self, task: callable):
        """
        Set the task callback function.
        """
        self.task = task

    def update(self, i: int):
        """
        Update the progress bar, status label, button states for user-inputted
        iteration number i. A common use case is to update with iteration i in a
        for or while loop defined in task() by the user.
        """
        self._update(i)

    def set_verbose(self, verbose: bool):
        """
        Set verbose mode.
        """
        self.verbose = verbose

    def is_pausing_or_terminating(self):
        """
        Check if the task is in PAUSING or TERMINATING state. This is useful for
        user to stop promptly before running other time-consuming operations in
        user-defined task() after user clicks pause or terminate button.
        """
        if self.status == _Status._PAUSING or self.status == _Status._TERMINATING:
            return True
        else:
            return False

    def is_pause_resumed(self):
        """
        Check whether a progress is resumed just after it was paused. It returns
        True if the progress is just resumed after it was paused, until the next
        iteration in which it returns False again. It also returns False in all
        other cases. This is useful if user wants to repeat current iteration
        after the work was resumed from pause, especially when the user
        configured to jump over some customized time-comsuming operations in
        task() using is_pausing_or_terminating() after the pause button was
        clicked.
        """
        return self._pause_resumed

    def after_started(self):
        """
        Placeholder for user-defined function to be run when the task is
        started.
        """
        if self.verbose:
            print("Started!")

    def after_resumed(self):
        """
        Placeholder for user-defined function to be run when the task is
        resumed.
        """
        if self.verbose:
            print("Resumed!")

    def after_paused(self):
        """
        Placeholder for user-defined function to be run when the task is paused.
        """
        if self.verbose:
            print("Paused!")

    def after_terminated(self):
        """
        Placeholder for user-defined function to be run when the task is
        terminated.
        """
        if self.verbose:
            print("Terminated!")

    def after_completed(self):
        """
        Placeholder for user-defined function to be run when the task is
        normally completed (automatically terminated after all interations are
        done).
        """
        if self.verbose:
            print("Done!")

    def _set_total(self, total):
        """
        Set the total number of iterations for self.i in task_loop to iterate.
        Not exposed to users.
        """
        if total <= 0:
            raise ValueError("Iteration number must be larger than 0.")
        self.total = total

    def _create_widgets(self):
        """
        Create widgets for progress panel, including buttons and progress bar.
        """
        frame_upper = ttk.Frame(self)
        frame_upper.pack()
        if self.title is not None:
            ttk.Label(frame_upper, text=self.title).pack(side="top")
        self._progress_bar = ttk.Progressbar(
            frame_upper, orient="horizontal", length=200, mode="determinate")
        self._progress_bar.pack(side="left")
        frame_middle = ttk.Frame(self)
        frame_middle.pack()
        self._label_status = ttk.Label(
            frame_middle, text=self._get_progress_notice())
        self._label_status.pack(side="left")
        frame_lower = ttk.Frame(self)
        frame_lower.pack()
        self._button_start = ttk.Button(
            frame_lower, text="Start", command=self._start)
        self._button_start.pack(side="left")
        self._button_pause = ttk.Button(
            frame_lower, text="Pause", command=self._pause)
        self._button_pause["state"] = "disabled"
        self._button_pause.pack(side="left")
        self._button_terminate = ttk.Button(
            frame_lower, text="Terminate", command=self._terminate)
        self._button_terminate["state"] = "disabled"
        self._button_terminate.pack(side="left")

    def _get_progress_notice(self, calculate_remaining_time=True):
        """
        Get the remaining time.
        """
        self._mutex_progress_notice.acquire()
        try:
            if calculate_remaining_time:
                self._remaining_time = int(
                    self._time_per_iteration * (self.total - self.i + (
                        self._i_init if self._i_init else 0)) /
                    self._iteration_step)
            if self.status == _Status._TERMINATED:
                return "Ready"
        except Exception as e:
            raise e
        finally:
            self._mutex_progress_notice.release()
        return "{}/{}. Time left: {}".format(
            self.i, self.total, timedelta(seconds=self._remaining_time)
            if self._remaining_time > 0 else "--:--:--")

    def _timer(self):
        """
        Update the progress bar and status label every second.
        """
        while self.status == _Status._RUNNING:
            self._remaining_time = max(0, self._remaining_time - 1)
            self._label_status.config(
                text=self._get_progress_notice(calculate_remaining_time=False))
            sleep(1)

    def _start(self):
        """
        Start the task loop in a thread.
        """
        if self.status != _Status._RUNNING:
            if self.status != _Status._PAUSED:
                self.after_started()
                self.status = _Status._RUNNING
                Thread(target=self._task).start()
                Thread(target=self._timer).start()
            else:
                self._pause_resumed = True
                self.after_resumed()
                self.status = _Status._RUNNING
            self._progress_bar["value"] = self.i / self.total * 100
            self._button_start["state"] = "disabled"
            self._button_pause["state"] = "normal"
            self._button_terminate["state"] = "normal"

    def _update(self, i):
        """
        Update the progress bar and status label. Action is taken here when the
        task is paused, resumed or terminated. Not exposed to users.
        """
        if self._i_init is None:
            self._i_init = i
        curr_timestamp = time()
        if self._iteration_timestamp is not None:
            self._iteration_step = i - self.i
            self._time_per_iteration = (self._time_per_iteration * (
                self.i - self._i_init) + (
                curr_timestamp - self._iteration_timestamp) *
                self._iteration_step) / (
                self.i - self._i_init + self._iteration_step)
        self._iteration_timestamp = curr_timestamp
        self._pause_resumed = False
        self.i = i
        self._label_status.config(text=self._get_progress_notice())
        self._progress_bar["value"] = self.i / self.total * 100
        if self.status == _Status._PAUSING:
            self._iteration_timestamp = None
            self._button_start["state"] = "normal"
            self.status = _Status._PAUSED
            self.after_paused()
            if self.i == self.total:
                self._reset()
                self._label_status.config(text="Done!")
        super().update()
        while self.status == _Status._PAUSED:
            pass
        if self.status == _Status._TERMINATING:
            raise Exception("Terminated")

    def _task(self):
        """
        Task to be executed with exception handling. Not exposed to users.
        """
        try:
            self.task()
        except Exception as e:
            self._reset()
            self.status = _Status._TERMINATED
            if e.args[0] == "Terminated":
                self._label_status.config(text="Ready")
                self.after_terminated()
            else:
                if not self.task:
                    e = Exception("Task not passed to Progresspanel.")
                self._label_status.config(
                    text="Error at {}/{}: {}".format(self.i, self.total, e))
                self.after_terminated()
                raise e
        else:
            self._reset()
            self._label_status.config(text="Done!")
            self.after_completed()

    def _reset(self):
        """
        Reset the task to the initial state.
        """
        self.status = _Status._TERMINATED
        self.i = 0
        self._time_per_iteration = 0
        self._iteration_timestamp = None
        self._button_terminate["state"] = "disabled"
        self._button_pause["state"] = "disabled"
        self._button_start["state"] = "normal"
        self._button_start.config(text="Start")
        self._progress_bar["value"] = 0
        self._label_status.config(text=self._get_progress_notice())

    def _pause(self):
        """
        Pause the task.
        """
        self.status = _Status._PAUSING
        self._button_pause["state"] = "disabled"
        self._button_start.config(text="Resume")

    def _terminate(self):
        """
        Terminate the task.
        """
        self.status = _Status._TERMINATING
        self._button_pause["state"] = "disabled"
        self._button_terminate["state"] = "disabled"


class _Status:
    """
    Status of the task. Notice, PAUSING and TERMINATING are not final states.
    PAUSING means that the user has clicked the pause button, and the task will
    be paused after the current iteration is done and goes into PAUSED state
    afterwards. Same for TERMINATING and TERMINATED.
    """
    _RUNNING = 1
    _PAUSING = 2
    _PAUSED = 3
    _TERMINATING = 4
    _TERMINATED = 5
