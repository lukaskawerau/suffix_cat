# suffix_cat

A project to categorize publicly known domain suffixes of ccTLDs.  

## TODO:
1. [x] create data model
2. [ ] manually code remaining categories
3. [ ] insert correct source URL for all definitions
4. [ ] save source URLs for definitions using webarchive

## Data Model

| TLD | suffix  | country | category   | source/reference |
| --- | ------  | ------- | --------   | ---------------- |
| fr  | gouv.fr | FR      | government | http://www.afnic.fr/obtenir/chartes/nommage-fr/annexe-descriptifs |

Categories:

- government
- military
- education
- library
- museum

(to be done)
- ngo_unspecified
- ngo_local
- ngo_international
- individual
- network_infrastructure
- media
- other

## Updating

The list is updated by executing the following steps:
- upgrade to the latest version of the public suffix list in `data/raw/`
- run `python3 extract_suffixes.py`
- look for categorized suffixed which have disappeared and add them to `data/manual/legacy_public_suffixes.csv` in order to be able to process older data
- if necessary update and extend `data/manual/manual_additions_not_public_suffix.csv`
- if necessary also update the mapping of TLD to country (`data/manual/tld_country.csv`)
- run `python3 merge_suffixes.py`
- verify the final, merged list: [data/manual/parsed_suffixes_manual.csv](./data/manual/parsed_suffixes_manual.csv)
