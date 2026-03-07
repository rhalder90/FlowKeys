# player.py — Handles all sound playback for FlowKeys.
# Pre-loads WAV files into RAM at startup so there's zero disk access on each keypress.
# Uses pygame.mixer for low-latency, non-blocking audio.

# === IMPORTS ===
import os       # For checking if sound files exist
import pygame   # The game library — we only use its audio mixer
import config   # Our settings: file paths, volume, channel count
import logging  # For recording what happens

# Get the FlowKeys logger (set up in logger_setup.py).
logger = logging.getLogger("FlowKeys")

# === MODULE-LEVEL VARIABLES ===
# These variables are shared across all functions in this file.
# They hold the loaded sounds and track which sound is currently active.

# Dictionary that will hold pygame Sound objects, keyed by name.
# Example: {"mechanical": <Sound>, "soft": <Sound>}
_sounds = {}

# The name of the currently active sound (e.g., "mechanical").
_current_sound_name = None

# The pygame Sound object that's currently active (the one that plays on keypress).
_current_sound = None

# A flag to track if the mixer has been initialized successfully.
_initialized = False

# A flag to prevent infinite reinit loops if the audio device keeps failing.
_reinit_attempted = False


def init():
    """
    Initialize the audio system and pre-load all sound files into RAM.
    Call this once at startup before any sounds can be played.
    """
    # We need to modify these module-level variables, so declare them as global.
    global _sounds, _current_sound_name, _current_sound, _initialized

    try:
        # Initialize pygame's audio mixer with low-latency settings.
        # frequency=44100: CD-quality sample rate (44,100 samples per second).
        # size=-16: 16-bit signed audio (negative means signed).
        # channels=1: mono output (uses less CPU than stereo).
        # buffer=512: small buffer = lower latency (~12ms at 44100 Hz).
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Tell pygame how many sounds can play at the same time.
        # 16 channels means up to 16 overlapping key sounds.
        pygame.mixer.set_num_channels(config.NUM_AUDIO_CHANNELS)

        # Log that the mixer started successfully.
        logger.info("Pygame mixer initialized (buffer=512, channels=%d)", config.NUM_AUDIO_CHANNELS)

    except Exception as e:
        # If the mixer fails (e.g., no audio device), log the error and stop.
        logger.error("Failed to initialize pygame mixer: %s", e)
        raise  # Re-raise the error so main.py knows something went wrong

    # === PRE-LOAD ALL SOUND FILES INTO RAM ===
    # Loop through each sound defined in config.py (e.g., "mechanical", "soft").
    for name, path in config.SOUNDS.items():

        # Check if the sound file actually exists on disk.
        if not os.path.exists(path):
            # If the file is missing, log an error and skip it.
            logger.error("Sound file not found: %s (expected at %s)", name, path)
            continue  # Skip to the next sound

        try:
            # Load the WAV file into a pygame Sound object.
            # This reads the entire file into RAM — no more disk access after this.
            sound = pygame.mixer.Sound(path)

            # Set the volume for this sound using the level from config.py.
            sound.set_volume(config.VOLUME)

            # Store the loaded sound in our dictionary.
            _sounds[name] = sound

            # Log success for this sound.
            logger.info("Loaded sound '%s' from %s", name, path)

        except Exception as e:
            # If loading fails (e.g., corrupted WAV file), log it and continue.
            logger.error("Failed to load sound '%s': %s", name, e)

    # Make sure at least one sound was loaded successfully.
    if not _sounds:
        logger.error("No sounds were loaded! Check your sounds/ folder.")
        raise FileNotFoundError("No sound files could be loaded.")

    # Set the default active sound from config.py.
    # If the default sound wasn't loaded, fall back to the first available sound.
    if config.DEFAULT_SOUND in _sounds:
        _current_sound_name = config.DEFAULT_SOUND
    else:
        # Use the first sound that was successfully loaded.
        _current_sound_name = list(_sounds.keys())[0]
        logger.warning("Default sound '%s' not available, using '%s'",
                        config.DEFAULT_SOUND, _current_sound_name)

    # Set the active Sound object.
    _current_sound = _sounds[_current_sound_name]

    # Mark the player as initialized.
    _initialized = True

    # Log the final status.
    logger.info("Player ready. Active sound: '%s'. Total sounds loaded: %d",
                _current_sound_name, len(_sounds))


def play():
    """
    Play the currently active sound once, non-blocking.
    If all audio channels are busy, silently skip (no error, no queue).
    If the audio device disconnects, attempt to reinitialize once.
    """
    global _reinit_attempted

    # Don't try to play if the player hasn't been initialized yet.
    if not _initialized or _current_sound is None:
        return

    try:
        # Play the sound on any available channel.
        # play() returns a Channel object if successful, or None if all channels are busy.
        channel = _current_sound.play()

        # If channel is None, all 16 channels are busy — just skip silently.
        # This only happens during extremely fast typing.
        if channel is None:
            logger.debug("All audio channels busy — skipping this keypress sound")

        # Reset the reinit flag on successful play.
        _reinit_attempted = False

    except Exception as e:
        # If playback fails (e.g., audio device disconnected), try to recover.
        logger.warning("Playback failed: %s", e)

        # Only attempt reinit once to avoid infinite loops.
        if not _reinit_attempted:
            _reinit_attempted = True  # Set flag so we don't try again
            logger.info("Attempting to reinitialize audio mixer...")
            _attempt_reinit()  # Try to restart the mixer


def _attempt_reinit():
    """
    Try to restart the pygame mixer after an audio failure.
    This handles cases like headphones being unplugged/plugged in.
    """
    global _current_sound, _sounds

    try:
        # Shut down the current mixer (it's broken anyway).
        pygame.mixer.quit()

        # Reinitialize with the same low-latency settings.
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        # Restore the channel count.
        pygame.mixer.set_num_channels(config.NUM_AUDIO_CHANNELS)

        # Reload all sounds (they were lost when mixer was quit).
        for name, path in config.SOUNDS.items():
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(config.VOLUME)
                _sounds[name] = sound

        # Restore the currently active sound.
        if _current_sound_name in _sounds:
            _current_sound = _sounds[_current_sound_name]

        logger.info("Audio mixer reinitialized successfully")

    except Exception as e:
        # If reinit also fails, log it. User will need to restart FlowKeys.
        logger.error("Failed to reinitialize audio mixer: %s", e)


def set_sound(name):
    """
    Switch to a different sound by name (e.g., "mechanical" or "soft").
    Returns True if the switch was successful, False if the sound doesn't exist.
    """
    global _current_sound_name, _current_sound

    # Check if the requested sound was loaded.
    if name not in _sounds:
        logger.warning("Cannot switch to sound '%s' — not loaded", name)
        return False

    # Update the active sound name and object.
    _current_sound_name = name
    _current_sound = _sounds[name]

    # Log the switch.
    logger.info("Switched to sound: '%s'", name)
    return True


def get_current_sound_name():
    """
    Return the name of the currently active sound (e.g., "mechanical").
    """
    return _current_sound_name


def get_available_sounds():
    """
    Return a list of all loaded sound names (e.g., ["mechanical", "soft"]).
    """
    return list(_sounds.keys())


def cleanup():
    """
    Shut down the audio system cleanly.
    Call this when FlowKeys is exiting.
    """
    global _initialized

    try:
        # Quit the pygame mixer, releasing all audio resources.
        pygame.mixer.quit()
        _initialized = False
        logger.info("Player cleaned up — pygame mixer shut down")

    except Exception as e:
        # If cleanup fails, just log it — we're shutting down anyway.
        logger.error("Error during player cleanup: %s", e)
