import betterproto
from dbt.constants import METADATA_ENV_PREFIX
from dbt.events.base_types import BaseEvent, Cache, EventLevel, NoFile, NoStdOut, EventMsg
from dbt.events.eventmgr import EventManager, LoggerConfig, LineFormat
from dbt.events.helpers import env_secrets, scrub_secrets
from dbt.events.types import Formatting
from dbt.flags import get_flags, ENABLE_LEGACY_LOGGER
from dbt.logger import GLOBAL_LOGGER, make_log_dir_if_missing
from functools import partial
import json
import os
import sys
from typing import Callable, Dict, Optional, TextIO
import uuid


LOG_VERSION = 3
metadata_vars: Optional[Dict[str, str]] = None


def setup_event_logger(
    log_path: str,
    log_format: str,
    use_colors: bool,
    debug: bool,
    log_cache_events: bool,
    quiet: bool,
) -> None:
    cleanup_event_logger()
    make_log_dir_if_missing(log_path)

    if ENABLE_LEGACY_LOGGER:
        EVENT_MANAGER.add_logger(_get_logbook_log_config(debug))
    else:
        EVENT_MANAGER.add_logger(
            _get_stdout_config(log_format, debug, use_colors, log_cache_events, quiet)
        )

        if _CAPTURE_STREAM:
            # Create second stdout logger to support test which want to know what's
            # being sent to stdout.
            # debug here is true because we need to capture debug events, and we pass in false in main
            capture_config = _get_stdout_config(
                log_format, True, use_colors, log_cache_events, quiet
            )
            capture_config.output_stream = _CAPTURE_STREAM
            EVENT_MANAGER.add_logger(capture_config)

        # create and add the file logger to the event manager
        EVENT_MANAGER.add_logger(
            _get_logfile_config(os.path.join(log_path, "dbt.log"), use_colors, log_format)
        )


def _get_stdout_config(
    log_format: str, debug: bool, use_colors: bool, log_cache_events: bool, quiet: bool
) -> LoggerConfig:
    fmt = LineFormat.PlainText
    if log_format == "json":
        fmt = LineFormat.Json
    elif debug:
        fmt = LineFormat.DebugText
    level = EventLevel.DEBUG if debug else EventLevel.INFO
    return LoggerConfig(
        name="stdout_log",
        level=level,
        use_colors=use_colors,
        line_format=fmt,
        scrubber=env_scrubber,
        filter=partial(
            _stdout_filter,
            log_cache_events,
            debug,
            quiet,
            log_format,
        ),
        output_stream=sys.stdout,
    )


def _stdout_filter(
    log_cache_events: bool, debug_mode: bool, quiet_mode: bool, log_format: str, msg: EventMsg
) -> bool:
    return (
        not isinstance(msg.data, NoStdOut)
        and (not isinstance(msg.data, Cache) or log_cache_events)
        and (EventLevel(msg.info.level) != EventLevel.DEBUG or debug_mode)
        and (EventLevel(msg.info.level) == EventLevel.ERROR or not quiet_mode)
        and not (log_format == "json" and type(msg.data) == Formatting)
    )


def _get_logfile_config(log_path: str, use_colors: bool, log_format: str) -> LoggerConfig:
    return LoggerConfig(
        name="file_log",
        line_format=LineFormat.Json if log_format == "json" else LineFormat.DebugText,
        use_colors=use_colors,
        level=EventLevel.DEBUG,  # File log is *always* debug level
        scrubber=env_scrubber,
        filter=partial(_logfile_filter, bool(get_flags().LOG_CACHE_EVENTS), log_format),
        output_file_name=log_path,
    )


def _logfile_filter(log_cache_events: bool, log_format: str, msg: EventMsg) -> bool:
    return (
        not isinstance(msg.data, NoFile)
        and not (isinstance(msg.data, Cache) and not log_cache_events)
        and not (log_format == "json" and type(msg.data) == Formatting)
    )


def _get_logbook_log_config(debug: bool) -> LoggerConfig:
    # use the default one since this code should be removed when we remove logbook
    config = _get_stdout_config("", debug, False, False, False)
    config.name = "logbook_log"
    config.filter = lambda e: not isinstance(e.data, Cache)
    config.logger = GLOBAL_LOGGER
    config.output_stream = None
    return config


def env_scrubber(msg: str) -> str:
    return scrub_secrets(msg, env_secrets())


def cleanup_event_logger():
    # Reset to a no-op manager to release streams associated with logs. This is
    # especially important for tests, since pytest replaces the stdout stream
    # during test runs, and closes the stream after the test is over.
    EVENT_MANAGER.loggers.clear()
    EVENT_MANAGER.callbacks.clear()


# Since dbt-rpc does not do its own log setup, and since some events can
# currently fire before logs can be configured by setup_event_logger(), we
# create a default configuration with default settings and no file output.
EVENT_MANAGER: EventManager = EventManager()
# Problem: This needs to be set *BEFORE* we've resolved any flags (even CLI params)
EVENT_MANAGER.add_logger(
    _get_logbook_log_config(debug=False)  # type: ignore
    if ENABLE_LEGACY_LOGGER
    else _get_stdout_config(
        log_format="text", debug=False, use_colors=True, log_cache_events=False, quiet=False
    )  # type: ignore
)

# This global, and the following two functions for capturing stdout logs are
# an unpleasant hack we intend to remove as part of API-ification. The GitHub
# issue #6350 was opened for that work.
_CAPTURE_STREAM: Optional[TextIO] = None


# used for integration tests
def capture_stdout_logs(stream: TextIO):
    global _CAPTURE_STREAM
    _CAPTURE_STREAM = stream


def stop_capture_stdout_logs():
    global _CAPTURE_STREAM
    _CAPTURE_STREAM = None


# returns a dictionary representation of the event fields.
# the message may contain secrets which must be scrubbed at the usage site.
def msg_to_json(msg: EventMsg) -> str:
    msg_dict = msg_to_dict(msg)
    raw_log_line = json.dumps(msg_dict, sort_keys=True)
    return raw_log_line


def msg_to_dict(msg: EventMsg) -> dict:
    msg_dict = dict()
    try:
        msg_dict = msg.to_dict(casing=betterproto.Casing.SNAKE, include_default_values=True)  # type: ignore
    except AttributeError as exc:
        event_type = type(msg).__name__
        raise Exception(f"type {event_type} is not serializable. {str(exc)}")
    # We don't want an empty NodeInfo in output
    if (
        "data" in msg_dict
        and "node_info" in msg_dict["data"]
        and msg_dict["data"]["node_info"]["node_name"] == ""
    ):
        del msg_dict["data"]["node_info"]
    return msg_dict


def warn_or_error(event, node=None):
    flags = get_flags()
    if flags.WARN_ERROR or flags.WARN_ERROR_OPTIONS.includes(type(event).__name__):

        # TODO: resolve this circular import when at top
        from dbt.exceptions import EventCompilationError

        raise EventCompilationError(event.message(), node)
    else:
        fire_event(event)


# an alternative to fire_event which only creates and logs the event value
# if the condition is met. Does nothing otherwise.
def fire_event_if(
    conditional: bool, lazy_e: Callable[[], BaseEvent], level: EventLevel = None
) -> None:
    if conditional:
        fire_event(lazy_e(), level=level)


# top-level method for accessing the new eventing system
# this is where all the side effects happen branched by event type
# (i.e. - mutating the event history, printing to stdout, logging
# to files, etc.)
def fire_event(e: BaseEvent, level: EventLevel = None) -> None:
    EVENT_MANAGER.fire_event(e, level=level)


def get_metadata_vars() -> Dict[str, str]:
    global metadata_vars
    if metadata_vars is None:
        metadata_vars = {
            k[len(METADATA_ENV_PREFIX) :]: v
            for k, v in os.environ.items()
            if k.startswith(METADATA_ENV_PREFIX)
        }
    return metadata_vars


def reset_metadata_vars() -> None:
    global metadata_vars
    metadata_vars = None


def get_invocation_id() -> str:
    return EVENT_MANAGER.invocation_id


def set_invocation_id() -> None:
    # This is primarily for setting the invocation_id for separate
    # commands in the dbt servers. It shouldn't be necessary for the CLI.
    EVENT_MANAGER.invocation_id = str(uuid.uuid4())
