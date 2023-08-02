import pandas as pd
import numpy as np
from scilslab import LocalSession
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from scipy.optimize import fmin
import matplotlib.pyplot as plt

# set the paths and folders for where the files are
path = "" # destination of all the files
peaklist_name = "" # name of the peaklist to be used
fmp10_ref = "" # name of the reference file
dest_path = "" # path to put the resulting csv files

# dictionaries of information needed for each of the files
scils_filepaths = {"filename": "filepath"}

known_peaks = {"filename": "list of a couple of known peaks" }

name_conv = {"filename": "Visium identifier"}

regions = {"filename": "dict of brain sections as named in SCiLS"}

type_of_data = {"filename": "type of data"}



#functions for calibration of the spectras
def lq(parameters, x):
    return (parameters[0]*(x**2)) + parameters[1]*x + parameters[2]

def objective(parameters, x, y, w):
    err = y - lq(parameters, x)
    return np.sum(w*err**2)

def RANSACcalibration(ref, peaks):
    estimators = [("RANSAC", RANSACRegressor(random_state=0))]
    x = np.array(ref)
    y = np.array(peaks)
    x = np.reshape(x, (-1, 1))

    for _, estimator in estimators:
        model = make_pipeline(PolynomialFeatures(2), estimator).fit(x, y)

        x_plot = np.linspace(x.min(), x.max())
        y_plot = model.predict(x_plot[:, np.newaxis])

        x0 = [0, 0, 0]
        w = [1 for i in list(x_plot)]
        plsq = fmin(objective, x0, args=(x_plot, y_plot, w), ftol=1e-20, maxiter=100000, disp=False)

    return  plsq

def get_adj_mass(mz, plsq):
    return plsq[0]*(mz**2) + plsq[1]*mz + plsq[2]




for file in scils_filepaths:
    for region in regions[file].keys():
        with LocalSession(filename=scils_filepaths[file], timeout=300) as session:
            dataset = session.dataset_proxy
            rms_norm_id = [unique_id for unique_id, name in dataset.get_normalizations().items() if name == "Root Mean Square" ][0]
            region_tree = dataset.get_region_tree()

            feature_table = dataset.feature_table
            if file == fmp10_ref:
                peaklist = feature_table.get_features(feature_list_name=peaklist_name)

            names = [x for x in peaklist.keys()]
            for i in region_tree.subregions[0].subregions:
                if regions[file][region] in i.name:
                    region1 = i.id

            x_list, y_list = [], []
            plsq = RANSACcalibration(known_peaks[fmp10_ref], known_peaks[file])

            #for j in range(len(peaklist["mz_low"].values)):
            mz_low = get_adj_mass(peaklist["mz_low"].values[0], plsq)
            mz_high = get_adj_mass(peaklist["mz_high"].values[0], plsq)
            
            ion_images = dataset.get_ion_images(mz_low, mz_high, region_id=region1, mode='max', normalization_id=rms_norm_id)
            img = ion_images[0].values
            df = pd.DataFrame()

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    x_list.append(x)
                    y_list.append(y)
            df["x"] = x_list
            df["y"] = y_list

            for j in range(len(peaklist["mz_low"].values)):
                try:
                    mz_low = get_adj_mass(peaklist["mz_low"].values[j], plsq)
                    mz_high = get_adj_mass(peaklist["mz_high"].values[j], plsq)
                    ion_images = dataset.get_ion_images(mz_low, mz_high, region_id=region1, mode='max', normalization_id=rms_norm_id)
                    img = ion_images[0].values
                    img = np.nan_to_num(img, nan=0)
                except:
                    continue

                intensity = []
                for x in range(img.shape[1]):
                    for y in range(img.shape[0]):
                        intensity.append(img[y][x])
            
            
                df[(peaklist["mz_low"].values[j] + peaklist["mz_high"].values[j])/2] = intensity

            csv_name = dest_path + name_conv[file] + region + type_of_data[file] + ".csv"
            print("produced:", csv_name)
            df.to_csv(csv_name, index=False)
