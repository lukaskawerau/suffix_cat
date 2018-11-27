import csv

file = open("data/raw/public_suffixes_2018-11-27.txt", "r").readlines()
outfile = open("data/processed/parsed_suffixes_2018-11-27.csv", "w")
writer = csv.writer(outfile, delimiter = ",")
sources = []

def check_cat(suffix):
    govs = ["gov.", "gouv.", "gob.", "gv."]
    if any(g in suffix for g in govs):
        # this is a heuristic with some undercoverage
        category = "government"
    elif "mil." in suffix:
        category = "military"
    elif "edu." in suffix:
        # also some undercoverage, "academia"-based suffixes
        category = "education"
    elif "museum" in suffix:
        # has its own TLD
        category = "museum"
    else:
        category = None

    return category

for line in file:
    if "// newGTLDs" in line:
        break # do not parse newGTLDs, only interested in ccTLDs
    elif "//" in line:
        try: # get lines for information source
            source = line.strip()
            source = source.strip("// ")
            source = source.split(" : ")
            if len(source) == 1:
                pass
            else:
                sources.append(source)
        except:
            pass
    elif line in ['\n', '\r\n']:
        pass
    else:
        suffix = line.strip()
        category = check_cat(suffix)
        try:
            elements = suffix.split(".")
        except:
            elements = suffix

        tld = elements[-1]

        # source is always the source last added to the source list
        writer.writerow([tld, suffix, category, sources[-1][1]])
