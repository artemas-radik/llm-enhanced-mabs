### Project File Structure Description

`aggressive_dedup.json` needs to be downloaded from the Amazon product review dataset

`asin_B0051VVOB2.json` is the dataset of all reviews with asin B0051VVOB2

`filter.py` takes `asin_B0051VVOB2.json` and filters it down to 1000 entries

`filtered.txt` is the resulting filtered 1000 entries

`gen.py` calls the LM Studio inference server to add the LLM-enhancing

`main.py` takes `aggressive_dedup.json` and finds the product with most non-[0,0] reviews

`plot.py` generates plots for the runtimes of `main.py`

`results.txt` contains the LLM-enhanced 1000 entries from `gen.py`