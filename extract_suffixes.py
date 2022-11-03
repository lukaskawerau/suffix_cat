import csv

file = open("data/raw/public_suffixes.txt", "r").readlines()
outfile = open("data/processed/parsed_suffixes.csv", "w")
writer = csv.writer(outfile, dialect='unix', delimiter = ",", quoting=csv.QUOTE_MINIMAL)
sources = []

# suffix elements for categorization
#   <suffix_element>: (<is_tld>, <category>, <exclusions>)
#   <is_tld> : True if suffix is a TLD (gov in whitehouse.gov)
#              False if not (.gouv.fr)
#              (used in case of conflicting suffixes, eg.
#               "ac" which is also a ccTLD)
suffix_category_elements = {
    ### government
    # .gov, .gov.uk, ...
    "gov": (True, "government", {}),
    # .gouv.fr, gouv.ht, ...
    "gouv": (False, "government", {}),
    # .gob.mx, .gob.es, ...
    "gob": (False, "government", {}),
    # .gv.at, .gv.ao
    "gv": (False, "government", {}),
    # .go.ci, .go.kr, go.jp, ... (but not .go.it, .go.dyndns.org)
    "go": (False, "government", {"go.it"}),
    # .gc.ca
    "gc": (False, "government", {}),
    # .govt.nz
    "govt": (False, "government", {}),
    # .gub.uy
    "gub": (False, "government", {}),
    # .state.mn.us
    "state": (False, "government", {}),
    # .dep.no
    "dep": (False, "government", {}),
    # .stat.no
    "stat": (False, "government", {}),
    # .go.leg.br (legislation)
    "leg": (False, "government", {}),
    # TODO: .police.uk
    ### education
    "edu": (True, "education", {}),
    # academic institution: .ac.ci,
    "ac": (False, "education", {}),
    # .ed.ci
    "ed": (False, "education", {}),
    "school": (False, "education", {}),
    # TODO: .res.in (Indian research institutes)
    ### military
    "mil": (True, "military", {}),
    ### etc.
    "museum": (True, "museum", {}),
}

categorized_suffixes = {
    "fed.us": "government",
}

def check_cat(suffix, elements):
    global suffix_category_elements
    categories = set()
    # look at the last and second last elements
    for i in [1, 2]:
        if i > len(elements):
            break
        suffix_element = elements[-i]
        if suffix_element in suffix_category_elements:
            category = suffix_category_elements[suffix_element]
            if (i > 1 or category[0]) and not suffix in category[2]:
                return category[1]
    return None

for line in file:
    if "// newGTLDs" in line:
        # do not parse newGTLDs, only interested in ccTLDs
        #break
        # (however, some government suffixes are listed after
        #  the ccTLDs in the private section)
        pass
    elif "//" in line:
        # get lines for information source
        source = line.strip()
        source = source.strip("// ")
        source = source.split(" : ")
        if len(source) == 1:
            pass
        else:
            sources.append([source[0].strip(), source[1].strip()])
    elif line in ['\n', '\r\n']:
        pass
    else:
        suffix = line.strip()
        if '*' in suffix:
            # do not need wild card suffixes
            continue
        elements = suffix.split(".")
        category = check_cat(suffix, elements)
        tld = elements[-1]

        # source is always the source last added to the source list
        writer.writerow([tld, suffix, category, sources[-1][1]])
