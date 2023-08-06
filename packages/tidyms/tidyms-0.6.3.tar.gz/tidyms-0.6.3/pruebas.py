import tidyms as ms
import numpy as np
import pandas as pd
import os
from pathlib import Path
import json

# f1 = ms.chem.Formula("[C20H40SO5]2-")
# M, p = f1.get_isotopic_envelope(4)

assay_path = "../fgnotebooks/untargeted-nist.tidyms-assay"
data_path = Path("../data/NIST-SRM/")
mzml_path = data_path.joinpath("cent-full")
sample_list_path = data_path.joinpath("sample-list-cent-full.csv")
sample_list = pd.read_csv(sample_list_path)
assay = ms.Assay(assay_path, mzml_path, sample_list)
assay.build_feature_table()
assay.match_features(
    include_classes=["QC", "1", "2", "3", "4"],
    mz_tolerance=0.010,
    rt_tolerance=5,
    min_fraction=0.25,
    max_deviation=3,
    verbose=True,
    n_jobs=-1)
assay.make_data_matrix(mz_merge=0.01, rt_merge=3.0, merge_threshold=0.9)
data = assay.data_matrix
data.preprocess.group_isotopologues()

# TODO: update feature table for votation
#    create annotation module
#    add annotation information into the feature metadata
#    add function to group isotopologues in the data matrix.
#    