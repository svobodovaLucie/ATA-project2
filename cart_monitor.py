#!/usr/bin/env python3
"""
Dynamic analyser of a cart controller.
"""

# pocet slotu voziku ze zadani
slots = 4
# nosnost voziku ze zadani
capacity = 150
# zatim jsou vsechny vlastnosti dodrzeny
all_properties_hold = True

# matice pokryti - zezacatku prazdna, nevime, jake budou stanice
coverage = {
  # slot:   0      1      2      3  
    'A': [False, False, False, False],
    'B': [False, False, False, False],
    'C': [False, False, False, False],
    'D': [False, False, False, False]
}

# sloty, ktere jsou obsazene
slots_occupied = [False, False, False, False]
# pole zatim neobslouzenych pozadavku
requests = []
# pocet nalozenych nakladu
contents_loaded = 0
# aktualni vaha na voziku
current_capacity = 0

def report_coverage():
    global coverage, all_properties_hold, slots
    if all_properties_hold:
        print('All properties hold.')
    "Coverage reporter"
    cases_covered = 0
    cases_all = 0
    for station in list(coverage.keys()):
        for i in range(0, slots):
            if coverage[station][i]:
                cases_covered += 1
            cases_all += 1

    print('CartCoverage %d%%' % ((cases_covered/cases_all)*100))

def onmoving(time, pos1, pos2):
    global all_properties_hold, requests, current_capacity, contents_loaded
    time = int(time)

    # Vlastnost 3
    for req in requests:
        # kontrola, ze naklad je loaded a ze jeho cilova stanice se rovna pos1
        if req[1] == pos1 and req[4]:
            print(f'{time}:error: unloaded content {req[2]} in station {pos1}')
            all_properties_hold = False


def onrequesting(time, src, dst, content, w):
    global requests

    # Ulozeni pozadavku
    requests.append((src, dst, content, w, False))


def onloading(time, pos, content, w, slot):
    global capacity, all_properties_hold, coverage, slots_occupied, requests, current_capacity, contents_loaded
    slot_num = int(slot)
    w_num = int(w)

    # Vlastnost 1
    if slots_occupied[slot_num]:
        print(f'{time}:error: loading into an occupied slot #{slot_num}')
        all_properties_hold = False

    # Vlastnost 5
    found = False
    for req in requests:
        if req[0] == pos:       # src == pos
            found = True
            requests.remove(req)
            updated_req = (req[0], req[1], req[2], req[3], True)
            requests.append(updated_req)
    if not found:
        print(f'{time}:error: loading unrequested content in station {pos}')
        all_properties_hold = False

    # Vlastnost 6
    if contents_loaded >= 4:
        print(f'{time}:error: loading content when 4 slots occupied')
        all_properties_hold = False
        
    # Vlastnost 7
    if current_capacity + w_num > capacity:
        print(f'{time}:error: capacity overloaded')
        all_properties_hold = False

    # 'load' the content
    slots_occupied[slot_num] = True     # clot is occupied
    contents_loaded += 1                # add new content
    current_capacity += w_num           # add weight to the current capacity
    coverage[pos][slot_num] = True      # case covered


def onunloading(time, pos, content, w, slot):
    global all_properties_hold, slots_occupied, requests, contents_loaded
    slot_num = int(slot)

    # Vlastnost 2
    if not slots_occupied[slot_num]:
        print(f'{time}:error: unloading from an empty slot #{slot_num}')
        all_properties_hold = False

    # Odstranit obslouzeny pozadavek z requests (src, dst, content, w, False)
    for req in requests:
        if req[1] == pos and req[2] == content and req[3] == w and req[4]:
            requests.remove(req)

    contents_loaded -= 1
    slots_occupied[slot_num] = False


def onevent(event):
    "Event handler. event = [TIME, EVENT_ID, ...]"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # ZDE IMPLEMENTUJTE MONITORY
    #print(event)

    # vyjmeme identifikaci udalosti z dane n-tice
    event_id = event[1]
    del(event[1])
    # priklad predani ke zpracovani udalosti moving
    if event_id == 'moving':
        # predame n-tici jako jednotlive parametry pri zachovani poradi
        onmoving(*event)
    elif event_id == 'loading':
        onloading(*event)
    elif event_id == 'unloading':
        onunloading(*event)
    elif event_id == 'requesting':
        onrequesting(*event)

###########################################################
# Nize netreba menit.

def monitor(reader):
    "Main function"
    for line in reader:
        line = line.strip()
        onevent(line.split())
    report_coverage()

if __name__ == "__main__":
    import sys
    monitor(sys.stdin)
