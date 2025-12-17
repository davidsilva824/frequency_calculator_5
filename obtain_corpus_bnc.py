# It generates the British National Corpus in a .txt file: https://www.english-corpora.org/bnc/   
# must have BNC_XML folder in the working folder. I downloaded it at: http://www.natcorp.ox.ac.uk/ 
# The link to download the corpus doesn't always work.  

import os
import xml.etree.ElementTree as ET

BNC_XML_ROOT = 'BNC_XML'
OUTPUT_FILE = "bnc_corpus.txt"

def xml_to_text(xml_path: str) -> str:
    try:
        tree = ET.parse(xml_path)
    except Exception as e:
        print(f"Skipping {xml_path} (parse error: {e})")
        return ""
    return "".join(tree.getroot().itertext())

def build_bnc_plain(root_folder: str, output_file: str) -> None:
    started = False   # <--- NEW

    with open(output_file, "w", encoding="utf-8", errors="ignore") as out_f:
        for dirpath, _, filenames in os.walk(root_folder):
            for fname in sorted(filenames):
                if not fname.lower().endswith(".xml"):
                    continue

                # Start writing only when we hit the first real corpus file
                if not started:
                    # BNC corpus files start with "A00", so detect that
                    if fname.startswith("A00"):
                        started = True
                    else:
                        # skip everything before A00
                        continue

                xml_path = os.path.join(dirpath, fname)
                print(f"Processing: {xml_path}")
                text = xml_to_text(xml_path)

                if not text.strip():
                    continue

                out_f.write(f"\n\n<<<DOC_START: {fname}>>>\n\n")
                out_f.write(text)

    print(f"\nDone. Plain-text corpus written to: {output_file}")

if __name__ == "__main__":
    build_bnc_plain(BNC_XML_ROOT, OUTPUT_FILE)
