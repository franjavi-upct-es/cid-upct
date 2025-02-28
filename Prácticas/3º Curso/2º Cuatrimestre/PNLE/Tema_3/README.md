# SympTEMIST CORPUS - TRAIN SET README

## What is SympTEMIST

SympTEMIST stands for Symptoms TExt MIning Shared Task. It is a shared task and set of resources focused on the detection, normalization and indexing of symptoms, signs and findings in medical documents in Spanish. SympTEMIST is complementary to the DisTEMIST corpus (https://temu.bsc.es/distemist) and MedProcNER/ProcTEMIST (https://temu.bsc.es/medprocner) as they all use the same document collection.

This repository includes the Train Set of the task's Subtask 1, which includes a total of 750 documents. Training data for subtasks 2 and 3 will be released later on.

SympTEMIST was developed by the Barcelona Supercomputing Center's NLP for Biomedical Information Analysis and used as part of BioCREATIVE 2023. For more information on the corpus, annotation scheme and task in general, please visit: https://temu.bsc.es/symptemist.

## Folder Structure

The SympTEMIST corpus is offered in two different formats, each separated in a different folder. The text files are also offered individually. All in all, the folder structure is:

- `symptemist_train/`: Includes the corpus' training set.

  - `symptemist_train/subtask1-ner/`: Includes the data for subtask 1 (named entity recognition)

    - `symptemist_train/subtask1-ner/brat/`: Includes the brat .ann files together with the .txt files. For more information on brat's format please visit: https://brat.nlplab.org/standoff.html

    - `symptemist_train/subtask1-ner/tsv/`: This folder includes tab-separated files (tsv) where each line represents an annotation. The file `symptemist_tsv_train_subtask1.tsv` includes the data for Subtask 1 with the following columns: "filename", "ann_id", "label", "start_span", "end_span" and "text".

    - `symptemist_train/subtask1-ner/txt/`: These are the standalone text files.

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

## Contact

If you have any questions or suggestions, please contact us at:

- Salvador Lima-López (<salvador [dot] limalopez [at] gmail [dot] com>)
- Martin Krallinger (<krallinger [dot] martin [at] gmail [dot] com>)
