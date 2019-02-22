import time
import multiprocessing
import numbers
import sys
from multiprocessing import Queue

SLEEP_INTERVAL_MS = 250 # Sleep interval in milliseconds.
SLEEP_INTERVAL_S = SLEEP_INTERVAL_MS / 1000

### SPAWN ACTION TYPES ###

### PROTOCOL MESSAGES ###
EXIT_DATAGRAM = "EXIT"
SAVE_GAME_DATAGRAM = "SAVE_GAME"
SAVE_ACK_DATAGRAM = "SAVE_ACK"
SAVE_DONE_DATAGRAM = "SAVE_DONE"

class Spawn_Handler():
    pending_spawn_queue = None
    updated_spawn_queue = None

    @classmethod
    def init_spawn_queues(cls):
        cls.pending_spawn_queue = Queue()
        cls.updated_spawn_queue = Queue()

    @classmethod
    def push_to_pending_queue(cls, data, block=True, timeout=None):
        cls.pending_spawn_queue.put(data, block=block, timeout=timeout)

    @classmethod
    def push_to_updated_queue(cls, data, block=True, timeout=None):
        cls.updated_spawn_queue.put(data, block=block, timeout=timeout)

    @classmethod
    def pull_from_pending_queue(cls, block=True, timeout=None):
        cls.pending_spawn_queue.get(block=block, timeout=timeout)

    @classmethod
    def pull_from_updated_queue(cls, block=True, timeout=None):
        cls.updated_spawn_queue.get(block=block, timeout=timeout)

    @classmethod
    def terminate_spawn_handler(cls):
        cls.push_to_pending_queue(EXIT_DATAGRAM)

    @classmethod
    def save_pending_spawns(cls, pending_dict):
        # The previously received datagram should be SAVE_GAME_DATAGRAM
        # so we don't need to get anything else from the pending queue.

        # Send ACK message to updated spawn queue.
        cls.push_to_updated_queue(cls, SAVE_ACK_DATAGRAM)

        # Update the time counters on the pending spawn dict and send
        # the entire dict to the updated queue.
        for action_id, remaining_time_ms in pending_dict.items():
            pending_dict[action_id] = remaining_time_ms - SLEEP_INTERVAL_MS

        cls.push_to_updated_queue(cls, pending_dict)

        # Send SAVE DONE message to main process.
        cls.push_to_updated_queue(cls, SAVE_DONE_DATAGRAM)

    # Main spawn handler process.
    @classmethod
    def handle_spawns():
        # Maps spawn action IDs to the number of milliseconds for remaining
        # time.
        pending_spawn_dict = {}
        finished = False

        while not finished:
            # Sleep for the set interval.
            time.sleep(SLEEP_INTERVAL_S)

            # Check for items in the pending queue.
            checked_queue = False
            while (not cls.pending_spawn_queue.empty()) and (not checked_queue):
                incoming_action = None
                try:
                    incoming_action = cls.pull_from_updated_queue(
                            block=False,
                            timeout=None
                        )

                    # Check if the incoming action is a list of
                    # [action ID, time_left].
                    if isinstance(incoming_action, list)):
                        # Index 0 is the action ID, and index 1 is the
                        # remaining time in milliseconds.
                        action_id = incoming_action[0]
                        remaining_time = incoming_action[1]
                        if (action_id is not None) and (remaining_time is not None):
                            pending_spawn_dict[action_id] = remaining_time
                    elif incoming_action == SAVE_GAME_DATAGRAM:
                        # Initiate save game sequence.
                        finished = True
                        checked_queue = True
                        cls.save_pending_spawns(pending_spawn_dict)
                    elif incoming_action == EXIT_DATAGRAM:
                        # Break out of while loops.
                        finished = True
                        checked_queue = True
                    else:
                        # Unrecognized datagram.
                        logger.error("Unrecognized datagram.")
                        sys.stdout.flush()
                except queue.Empty as e:
                    checked_queue = True

            if not finished:
                # Update all entries in pending dict.
                for action_id, remaining_ms in pending_spawn_dict.items():
                    pending_spawn_dict[action_id] = remaining_ms - SLEEP_INTERVAL_MS

                # Check if remaining times <= 0. TODO

# set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
