from __future__ import print_function
from typing import Any, List
from threading import Thread
from .chalk import chalk
from .context import Context
import cursor
from spinners import Spinners
import os
import sys
import time
import codecs

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CLEAR_LINE = '\033[K'

def decode_utf_8_text(text):
    """Decodes the text from utf-8 format.
    
    Parameters
    ----------
    text : str
        Text to be decoded
    
    Returns
    -------
    str
        Decoded text
    """
    try:
        return codecs.decode(text, 'utf-8')
    except:
        return text


def encode_utf_8_text(text):
    """Encodes the text to utf-8 format
    
    Parameters
    ----------
    text : str
        Text to be encoded
    
    Returns
    -------
    str
        Encoded text
    """
    try:
        return codecs.encode(text, 'utf-8')
    except:
        return text

if sys.version_info.major == 2:
    get_coded_text = encode_utf_8_text
else:
    get_coded_text = decode_utf_8_text

def animate(frames, interval, name, iterations=2):
    """Animate given frame for set number of iterations.

    Parameters
    ----------
    frames : list
        Frames for animating
    interval : float
        Interval between two frames
    name : str
        Name of animation
    iterations : int, optional
        Number of loops for animations
    """
    while Context.args['c_process']:
        for i in range(iterations):
            for frame in frames:
                frame = get_coded_text(frame)
                output = "\r{0} {1}\n".format(frame, name)
                sys.stdout.write(f"\033[95m{output}\033[0m")
                sys.stdout.write("\n")
                sys.stdout.write("\033[F") # Cursor up one line
                sys.stdout.write("\033[F") # Cursor up one line
                #sys.stdout.write(CLEAR_LINE)
                
                sys.stdout.flush()
                time.sleep(0.001 * interval)

def _loading(cmd: str):
    cursor.hide()
    spinner = [spinner for spinner in Spinners][0]
    frames = spinner.value['frames']
    interval = spinner.value['interval']
    animate(frames, interval, cmd)
    cursor.show()

def loading_process(
    log: str,
    f,
    args: List[str],
):
    Context.args['c_process'] = True
    p_log = Thread(target=_loading, args=[log])
    p_install = Thread(target=f, args=args)
    p_log.start()
    p_install.start()
    p_install.join()
    Context.args['c_process'] = False
    p_log.join()




def completed_process(cmd):
    chalk.green(cmd)

def failed_process(cmd):
    chalk.red(cmd)

def show_help(
    command: str,
    description: str,
    usage: List[Any]
):
    def pretty_print_usage(usage: Any):
        print(
            f"""
            \033[95mpyclk\033[1m {usage['command']}\033[0m | \033[92m{usage['description']}\033[0m"""
        )

    print(
        f"""
        Command: 
            \033[94m{command}\033[0m
        Description: 
            \033[92m{description}\033[0m
        
        Usage:"""
    )
    [pretty_print_usage(u) for u in usage]
    print()
    