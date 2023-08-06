import re
from wiktionaryparser import WiktionaryParser
import json
from tqdm import tqdm
import os.path

from clippings2anki.flashcards import get_flashcard
from clippings2anki.anki import save_to_text
import clippings2anki.gui


def main_gui():
    clippings2anki.gui.main()


def main_cli(input_file, language, output_file, save_json=False, anki_separator="\t", qt_signal=None):
    #! read the clippings file
    with open(input_file, "r") as f:
        clippings = f.read()
    
    clip_re = re.compile(r"(.*)\n==========")
    
    # find all matches
    clips = clip_re.findall(clippings)
    
    clips_set = set()
    
    for clip in clips:
        if not clip:
            continue

        # remove punctuation from the clip
        clip = re.sub(r"[^\w\s]", "", clip)

        # print(clip)
        clips_set.add(clip)
        
    print(f"{len(clips_set)} clippings found")
    print()

    #! get the definitions of the words from wiktionary
    parser = WiktionaryParser()
    parser.set_default_language(language)
    
    flashcards = {}

    for i, clip in enumerate(tqdm(clips_set, desc="Getting definitions from wiktionary")):
        word, f = get_flashcard(clip, parser)
        
        if not word:
            continue
        
        flashcards[word] = f
        
        if qt_signal:
            qt_signal.emit(int(((i+1) / len(clips_set))*100))
    
    if qt_signal:
        qt_signal.emit(100)
    
    print(f"\n{len(flashcards)} flashcards created out of {len(clips_set)} clippings ({len(clips_set) - len(flashcards)} clippings discarded)")
    
    if save_json:
        # save the flashcards to json file
        json_file = os.path.splitext(output_file)[0] + ".json"
        with open(json_file, "w") as f:
            json.dump(flashcards, f, indent=4)
        print(f"Saved flashcards in JSON format to \"{json_file}\"")
    
    #! save the flashcards to anki-friendly text file
    save_to_text(flashcards, file_name=output_file, separator=anki_separator)
    print(f"Flashcards exported to anki-friendly text file to \"{output_file}\"")
