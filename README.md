# Spatial Multimodal Analysis of Transcriptomes and Metabolomes in Tissues

This repository contains all the scripts needed to reproduce the images presented in the article [Spatial 
Multimodal Analysis of Transcriptomes and Metabolomes in 
Tissues](https://www.biorxiv.org/content/10.1101/2023.01.26.525195v1). 

## Set up
In order to reproduce the figures of the article go through the following steps.

### 1. Clone the repo
Pick a folder of your choice, clone this repository and navigate inside of it.
```
git clone https://github.com/marcovito/sma.git
cd sma
```

### 2. Download the data
Now download the data inside the repo.

We published on the following platforms:
- MALDI-MSI raw data (imzML files) are available on Figshare at the following URL: 
https://figshare.scilifelab.se/articles/dataset/Spatial_Multimodal_analysis_SMA_-_Mass_Spectrometry_Imaging_MSI_/22770161
- In situ sequencing data are available on Zenodo at the following URL: https://zenodo.org/record/7861508
- Raw and processed Spatial Transcriptomics (ST) data are available on Figshare at the following URL 
https://figshare.scilifelab.se/articles/dataset/Spatial_Multimodal_Analysis_SMA_-_Spatial_Transcriptomics/22778920 
-  Raw and processed ST data are available also on GEO at the following URL: 
https://figshare.scilifelab.se/articles/dataset/Spatial_Multimodal_Analysis_SMA_-_Spatial_Transcriptomics/22778920
- MALDI-MSI and ST processed data are available on Mendeley Data at the following URL https://data.mendeley.com/datasets/w7nw4km7xd/1

The code contained in this repo is set-up to work with the Mendeley dataset. You can download it clicking on the **Download All 5867 MB** button present on the website. If you do it this way then move the zip file to the `sma` folder and unpack this file and all the zip files inside of it by double-clicking on them. This will create a folder named `Spatial Multimodal Analysis of Transcriptomes and Metabolomes in Tissues` containing all the data. Rename this folder `data`.

You can also do it using the command line. However this downloads a zip file that for some reason is detected by the unzip command as a zip bomb. However the zip file is just fine. 
You just need to export the variable xx and then it gets correctly unzipped. Run the following commands to download and unzip, rename the repo and unzip all the files it contains:

```
wget https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/w7nw4km7xd-1.zip
unzip w7nw4km7xd-1.zip 
mv Spatial\ Multimodal\ Analysis\ of\ Transcriptomes\ and\ Metabolomes\ in\ Tissues/ data
cd data/
unzip \*.zip
```

Doing it from the command line it might happen that the unzip command gives you an error saying that this file might be a zip bomb. However the zip file is just fine. Just run the following command and then try again with the commands listed in the previous block (from `unzip w7nw4km7xd-1.zip ` on)
```
export UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE
```

### 3. Install packages
We don't provide conda environments for the scripts contained in this repo, except for the `WGCNA_20230428.Rmd` script, whose environment can be installed using the `WGCNA_environment_R2023.yml` file. All the libraries needed to run the scripts are called at the beginning of each script: check the needed libraries there, and install them as recommended on their websites if needed.

### 4. Run scripts
The scripts are contained in the `scripts` folder. The first scripts that you need to run are the three numbered scripts:
- `1_preprocessing.Rmd`: uploads all the data from the data folder and saves them as R objects in a folder named `R_objects`
- `2_analysis.Rmd`: runs all the analysis and saves the results as csv files in a folder named `results/tables`
- `3_main.Rmd`: reproduces most of the figures that you can find in the paper and saves them in a folder named `results/plots`

Run them in their numeric order (1>2>3). To run them you can open them in RStudio and then click on the button `knit`. This will also produce an html report. However, of the three reports, only the main.html report will show some figures, the other two will be useful just to check the code that has been run.

The rest of the scripts can be run in any order. They perform the following functions:
- `fdr_log_plots_msi.ipynb`: performs the analysis presented in the **Extended Data Fig. 3. Performance analysis of SMA-SRT data.** of the paper;
- `fdr_log_plots.ipynb`: performs the analysis presented in the **Extended Data Fig. 4. Performance analysis of SMA-MSI data.** of the paper;
- `ito_visium_correlations.py`: script used to calculate the correlation between SMA-MSI and standard MSI data;
- `making_csv_files.py`: script used to download the MSI data as csv files using SCiLS Lab software API;
- `MSI_SRT_hPDStr_LLMV.Rmd` and `MSI_SRT_mPD_LL.Rmd`: script used to manually align the MSI and Visium data coming from the same tissue sections. The first script was used for the human sample data and the second for the murine samples;
- `stereoscope_Kamath_MV.Rmd`: this script documents how the stereoscope analysis of the human data was performed;
- `stereoscope_Zeisel_JF.Rmd`: this script documents how the stereoscope analysis of the murine data was performed;
- `WGCNA_20230428.Rmd`: performs the analysis presented in the **Extended Data Fig. 9. Mirror plots showing MALDI-MS/MS identification of FMP-10 derivatized metabolites.** of the paper.
