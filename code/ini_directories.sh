#!/bin/bash
echo "--------------------------------"
echo "Pacific Ocean Portal - Installer"
echo "--------------------------------"

#SETUP BASE DIRECTORIES - CHANGE
baseURL="/home/pop"
rootPath="${baseURL}/ocean_portal"

#SUB DIRECTORIES
sub_dir1=(bom nasa noaa csiro copernicus spc)
sub_dir2=(historical hindcast forecast nrt outlook)
sub_dir3=(hourly daily monthly yearly)

#DATASETS - DO NOT CHANGE
echo "Creating dataset directories."
dataRoot="${rootPath}/datasets"
dataModelRegionalDir="${rootPath}/datasets/model/regional"
dataModelCountryDir="${rootPath}/datasets/model/country"
dataObsRegionalDir="${rootPath}/datasets/observations/regional"
dataObsCountryDir="${rootPath}/datasets/observations/country"
mkdir -p ${dataModelRegionalDir} ${dataModelCountryDir} \
    ${dataObsRegionalDir} ${dataObsCountryDir}

for item in "${sub_dir1[@]}"; do
    for item2 in "${sub_dir2[@]}"; do
        for item3 in "${sub_dir3[@]}"; do
            mkdir -p "${rootPath}/datasets/model/regional/$item/$item2/$item3"
            mkdir -p "${rootPath}/datasets/model/country/$item/$item2/$item3"
            mkdir -p "${rootPath}/datasets/observations/regional/$item/$item2/$item3"
            mkdir -p "${rootPath}/datasets/observations/country/$item/$item2/$item3"
        done
    done
done


#OUTPUT FILES - DO NOT CHANGE
echo "Creating files directories."
outModelRegionalDir="${rootPath}/files/model/regional"
outModelCountryDir="${rootPath}/files/model/country"
outObsRegionalDir="${rootPath}/files/observations/regional"
outObsCountryDir="${rootPath}/files/observations/country"
mkdir -p ${outModelRegionalDir} ${outModelCountryDir} \
    ${outObsRegionalDir} ${outObsCountryDir}

for item in "${sub_dir1[@]}"; do
    for item2 in "${sub_dir2[@]}"; do
        for item3 in "${sub_dir3[@]}"; do
            mkdir -p "${rootPath}/files/model/regional/$item/$item2/$item3"
            mkdir -p "${rootPath}/files/model/country/$item/$item2/$item3"
            mkdir -p "${rootPath}/files/observations/regional/$item/$item2/$item3"
            mkdir -p "${rootPath}/files/observations/country/$item/$item2/$item3"
        done
    done
done

#CONFIG FILES - DO NOT CHANGE
echo "Creating configuration directories."
config="${rootPath}/config"
threddsConfig="${config}/thredds_config"
ncwmsConfig="${config}/ncwms_config"
erddapConfig="${config}/erddap_config"
cgiConfig="${config}/cgi_config"
oceanAPI="${config}/ocean_api"
dataDownloadConfig="${config}/data_download_config"
plotterConfig="${config}/plotter_config"
mkdir -p ${config} ${threddsConfig} ${ncwmsConfig} \
    ${erddapConfig} ${cgiConfig} ${oceanAPI} \
    ${dataDownloadConfig} ${plotterConfig} 