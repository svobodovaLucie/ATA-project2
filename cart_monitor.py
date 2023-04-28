#!/usr/bin/env python3
"""
Dynamic analyser of a cart controller.
"""

# pocet slotu voziku ze zadani
slots = 4
# nosnost voziku ze zadani
capacity = 150

# matice pokryti - zezacatku prazdna, nevime, jake budou stanice
coverage = {}

def report_coverage():
    "Coverage reporter"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Zde nahradte vypocet/vypis aktualne dosazeneho pokryti
    cases_covered = 0
    cases_all = 0
    for station in list(coverage.keys()):
        print(station)
        for i in range(0, slots):
            print(coverage[station][i])
            if coverage[station][i]:
                cases_covered += 1
            cases_all += 1

    print('Cases covered: ', cases_covered)
    print('Cases all: ', cases_all)
    print('CartCoverage %d%%' % ((cases_covered/cases_all)*100))

def onmoving(time, pos1, pos2):
    "priklad event-handleru pro udalost moving"
    # Podobnou funkci muzete i nemusite vyuzit, viz onevent().
    # Vsechny parametry jsou typu str; nektere muze byt nutne pretypovat.
    time = int(time)
    print('%d:debug: got moving from %s to %s' % (time, pos1, pos2))

def onloading(time, pos, content, w, slot):
    print(time + ", " + pos + ", " + content + ", " + w + ", " + slot)
    print('ahojkyyyy')
    slot_num = int(slot)

    stations = list(coverage.keys())
    print(stations)

    print(slot_num)

    if not pos in coverage:
        print("loading - adding a station: ", pos)
        coverage[pos] = [False] * slots

    coverage[pos][slot_num] = True
    print("After: ", coverage[pos][slot_num])
    print(coverage)

def onunloading(time, pos, content, w, slot):
    print('unloading')
    if not pos in coverage:
        print("unloading - adding a station: ", pos)
        coverage[pos] = [False] * slots

def onevent(event):
    "Event handler. event = [TIME, EVENT_ID, ...]"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # ZDE IMPLEMENTUJTE MONITORY
    print(event)

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
    #    ...

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
