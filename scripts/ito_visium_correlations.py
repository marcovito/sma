import pandas as pd
import numpy as np
from scilslab import LocalSession
import time
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import seaborn as sns
from scipy.stats import pearsonr

fn = ""

with LocalSession(filename=fn, timeout=30) as session:
    start_time = time.time()
    dataset = session.dataset_proxy
    rms_norm_id = [unique_id for unique_id, name in dataset.get_normalizations().items() if name == "Root Mean Square" ][0]
    region_tree = dataset.get_region_tree()

    feature_table = dataset.feature_table
    peaklist = feature_table.get_features(feature_list_name="masslist_from_ITO_lesioned_mice")
    names = [x for x in peaklist.keys()]
    for i in region_tree.subregions[0].subregions[0].subregions:
        if "/Mouse_03" in i.name:
            region3 = i.id
        if "/Mouse_04" in i.name:
            region4 = i.id
        if "/Mouse_01" in i.name:
            region5 = i.id
    for i in region_tree.subregions[1].subregions[0].subregions:
        if "/03" in i.name:
            region1 = i.id
        if "/04" in i.name:
            region2 = i.id
        if "/01" in i.name:
            region6 = i.id



    mz, diff, visium_mean, ito_mean, ito_mean2, visium_mean2, ito_mean3, visium_mean3 = [], [], [], [], [], [], [], []
    for j in range(1, len(peaklist["mz_low"].values)):
        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region1, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        ito_mean.append(img.mean())

        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region2, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        ito_mean2.append(img.mean())
        
        mz.append(peaklist["mz_low"].values[j])

        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region6, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        ito_mean3.append(img.mean())


        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region3, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        visium_mean.append(img.mean())

        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region4, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        visium_mean2.append(img.mean())

        ion_images = dataset.get_ion_images(peaklist["mz_low"].values[j], peaklist["mz_high"].values[j], region_id=region5, mode='max')#, normalization_id=rms_norm_id)
        img = ion_images[0].values
        img = img.flatten()
        img = np.nan_to_num(img, nan=0)
        img = img[img > 0]
        img = np.log10(img.flatten()+1)
        visium_mean3.append(img.mean())

    df = pd.DataFrame(index=mz)
    #df["diff"] = diff
    df["Mouse 1 visium"] = visium_mean3
    df["Mouse 3 visium"] = visium_mean
    df["Mouse 4 visium"] = visium_mean2
    df["Mouse 1 ITO"] = ito_mean3
    df["Mouse 3 ITO"] = ito_mean
    df["Mouse 4 ITO"] = ito_mean2
    

    
    plt.figure(figsize = (7,5))
    plt.title("Spearman correlation of FMP10 mPD tissues for log transformed picked peaks")
    sns.heatmap(df.corr(method="spearman"), annot=True,cmap="Greys", vmin=0, vmax=1)
    plt.tight_layout()
    plt.show()
    



def reg_coef(x,y, **kwargs):
    ax = plt.gca()
    r, p = pearsonr(x,y)
    ax.annotate('r = {:.2f}'.format(r), xy=(0.5,0.5), xycoords='axes fraction', ha='center')
    ax.set_axis_off()

def violin_plot(x1, y1, **kwargs):
    sns.violinplot(y=np.array([x1.values.tolist(), y1.values.tolist()], **kwargs))


print(df)
g = sns.PairGrid(df)
g.map_diag(sns.histplot)
g.map_upper(violin_plot, kwargs={"split":True, "hue":["green", "blue"]})
g.map_lower(sns.regplot, line_kws={"color": "red"})
#g.map_upper(sns.violinplot)

plt.show()

#pd.plotting.scatter_matrix(df, alpha=0.2)   
#plt.show()

