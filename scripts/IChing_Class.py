from enum import Enum
import random
import json
from pprint import pprint
from pathlib import Path

class Polarity(Enum):
    yin = 0
    yang = 1

class Movement(Enum):
    same = 0
    change = 1

pprint_width = 100

trigram_dict = {
    '111': '1 - Heaven',
    '100': '2 - Thunder',
    '010': '3 - Water',
    '001': '4 - Mountain',
    '000': '5 - Earth',
    '011': '6 - Wind',
    '101': '7 - Fire',
    '110': '8 - Lake'
}

hexagram_dict = {
    '111111': [1, 'Creative'],
    '000000': [2, 'Receptive'],
    '100010': [3, 'Difficulty'],
    '010001': [4, 'Folly'],
    '111010': [5, 'Waiting'],
    '010111': [6, 'Conflict'],
    '010000': [7, 'Army'],
    '000010': [8, 'Union'],
    '111011': [9, 'Taming'],
    '110111': [10, 'Treading'],
    '111000': [11, 'Peace'],
    '000111': [12, 'Standstill'],
    '101111': [13, 'Fellowship'],
    '111101': [14, 'Possession'],
    '001000': [15, 'Modesty'],
    '000100': [16, 'Enthusiasm'],
    '100110': [17, 'Following'],
    '011001': [18, 'Decay'],
    '110000': [19, 'Approach'],
    '000011': [20, 'View'],
    '100101': [21, 'Biting'],
    '101001': [22, 'Grace'],
    '000001': [23, 'Splitting'],
    '100000': [24, 'Return'],
    '100111': [25, 'Innocence'],
    '111001': [26, 'Taming'],
    '100001': [27, 'Mouth'],
    '011110': [28, 'Preponderance'],
    '010010': [29, 'Abysmal'],
    '101101': [30, 'Clinging'],
    '001110': [31, 'Influence'],
    '011100': [32, 'Duration'],
    '001111': [33, 'Retreat'],
    '111100': [34, 'Power'],
    '000101': [35, 'Progress'],
    '101000': [36, 'Darkening'],
    '101011': [37, 'Family'],
    '110101': [38, 'Opposition'],
    '001010': [39, 'Obstruction'],
    '010100': [40, 'Deliverance'],
    '110001': [41, 'Decrease'],
    '100011': [42, 'Increase'],
    '111110': [43, 'Resoluteness'],
    '011111': [44, 'Coming'],
    '000110': [45, 'Gathering'],
    '011000': [46, 'Pushing'],
    '010110': [47, 'Oppression'],
    '011010': [48, 'Well'],
    '101110': [49, 'Revolution'],
    '011101': [50, 'Caldron'],
    '100100': [51, 'Arousing'],
    '001001': [52, 'Still'],
    '001011': [53, 'Development'],
    '110100': [54, 'Marrying'],
    '101100': [55, 'Abundance'],
    '001101': [56, 'Wanderer'],
    '011011': [57, 'Gentle'],
    '110110': [58, 'Joyous'],
    '010011': [59, 'Dispersion'],
    '110010': [60, 'Limitation'],
    '110011': [61, 'Truth'],
    '001100': [62, 'Small'],
    '101010': [63, 'After'],
    '010101': [64, 'Before']
}




class Cast_Single:
    def __init__(self):
        self.polarity = random.choice(list(Polarity))
        self.movement = random.choice(list(Movement))

    def icon(self):
        if self.polarity.name == "yin" and self.movement.name == "same":
            return "- -"
        elif self.polarity.name == "yin" and self.movement.name == "change":
            return "- -x"
        elif self.polarity.name == "yang" and self.movement.name == "same":
            return "---"
        else:
            return "---x"

    def __repr__(self):
        return f"Cast_Single(polarity={self.polarity.name}, movement={self.movement.name})"




class IChingCaster:
    def __init__(self, json_path=None):
        if json_path is None:
            json_path = Path(__file__).with_name("IChing_ChatGPT_A_001.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.iching_data = json.load(f)

    def cast_text(self) -> str:
        # --- same body as cast_text(...) above, but use self.iching_data ---
        iching_data = self.iching_data

        cast_full = [Cast_Single() for _ in range(6)]
        cast_full_binary = ''.join(str(line.polarity.value) for line in cast_full)
        cast_full_number = hexagram_dict[cast_full_binary][0] - 1
        cast_full_name   = hexagram_dict[cast_full_binary][1]

        cast_full_changed = []
        for line in cast_full:
            if line.movement.name == "change":
                new_polarity = Polarity.yang if line.polarity == Polarity.yin else Polarity.yin
            else:
                new_polarity = line.polarity
            changed_line = Cast_Single()
            changed_line.polarity = new_polarity
            changed_line.movement = line.movement
            cast_full_changed.append(changed_line)

        cast_full_changed_binary = ''.join(str(l.polarity.value) for l in cast_full_changed)
        cast_full_changed_number = hexagram_dict[cast_full_changed_binary][0] - 1
        cast_full_changed_name   = hexagram_dict[cast_full_changed_binary][1]

        def get_line_text(hex_dict, n):
            return hex_dict["lines"][n - 1][f"line {n}"]

        moving_lines = [i + 1 for i, ln in enumerate(cast_full) if ln.movement.name == "change"]
        hex_cast = iching_data[cast_full_number]

        out = []
        out.append(f"Original Hexagram: {cast_full_number + 1} - {cast_full_name} - {cast_full_binary}")
        out.append(f"Judgment: {iching_data[cast_full_number]['judgment']}")
        out.append(f"Image: {iching_data[cast_full_number]['image']}")
        out.append("")
        out.append(f"Changed Hexagram: {cast_full_changed_number + 1} - {cast_full_changed_name} - {cast_full_changed_binary}")
        out.append(f"Judgment: {iching_data[cast_full_changed_number]['judgment']}")
        out.append(f"Image: {iching_data[cast_full_changed_number]['image']}")
        out.append("")
        out.append(f"Moving lines: {moving_lines}")

        m = len(moving_lines)
        if m == 0:
            out.append("No changing lines -> Read only the original hexagram:")
        elif m == 1:
            n = moving_lines[0]
            out.append(f"One changing line -> consult line {n}")
            out.append(get_line_text(hex_cast, n))
        elif m == 2:
            l1, l2 = sorted(moving_lines)
            ln1, ln2 = cast_full[l1 - 1], cast_full[l2 - 1]
            is1_yin = (ln1.polarity.name == "yin")
            is2_yin = (ln2.polarity.name == "yin")
            if is1_yin and is2_yin:
                chosen, note = l2, "both change yin -> upper line"
            elif (not is1_yin) and (not is2_yin):
                chosen, note = l2, "both change yang -> upper line"
            else:
                chosen, note = (l1 if is1_yin else l2), "mixed -> change yin prevails"
            out.append(f"Two changing lines -> {note}; consult line {chosen}")
            out.append(get_line_text(hex_cast, chosen))
        elif m == 3:
            middle = sorted(moving_lines)[1]
            out.append(f"Three changing lines -> consult middle line {middle}")
            out.append(get_line_text(hex_cast, middle))
        elif m == 4:
            non_moving = [i + 1 for i, ln in enumerate(cast_full) if ln.movement.name == "same"]
            upper = max(non_moving)
            out.append(f"Four changing lines -> consult upper non-changing line {upper}")
            out.append(get_line_text(hex_cast, upper))
        elif m == 5:
            non_moving = [i + 1 for i, ln in enumerate(cast_full) if ln.movement.name == "same"]
            only_line = non_moving[0]
            out.append(f"Five changing lines -> consult only non-changing line {only_line}")
            out.append(get_line_text(hex_cast, only_line))
        else:
            out.append("All changing lines -> Read only the changed hexagram:")

        return "\n".join(out)


if __name__ == "__main__":
    # Example: class usage
    caster = IChingCaster()
    print(caster.cast_text())



