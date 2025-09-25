# Updating LMRv2.1 with PReSto2k and LinkedEarth Tools

## Authors

By [Tanaya Gondhalekar](https://orcid.org/0009-0004-2440-3266), [Deborah Khider](https://orcid.org/0000-0001-7501-8430) & [Julien Emile-Geay](https://orcid.org/0000-0001-5920-4751)

## Motivation

Climate field reconstruction is the task of estimating variations in one or more climate fields (e.g. surface temperature or precipitation) from a collection of paleoclimate observations (a.k.a "proxies"). Many statistical methods are available for doing so; a relatively new and impactful one has been offline data assimilation, as implemented in the Last Millennium Reanalysis [(Hakim et al., 2016)](http://dx.doi.org/10.1002/2016JD024751). Part of [PReSto](https://paleopresto.com)'s mission is to democratize these tools and enable a wider variety of actors, from seasoned researchers to students or citizen scientists, to generate their own reconstructions based on available code and data.  

The purpose of this repository is to showcase how to use tools from the [LinkedEarth](http://linked.earth) Python research ecosystem (and broader scientific Python stack) to expand on the Last Millennium Reanalysis, version 2.1 [(Tardif et al., 2019)](https://doi.org/10.5194/cp-15-1251-2019), which used the offline data assimilation method of [Hakim et al. (2016)](http://dx.doi.org/10.1002/2016JD024751) together with the PReSto2k Database ([PAGES 2kv2.0](http://dx.doi.org/10.1038/sdata.2017.88), [Iso2k](https://lipdverse.org/project/iso2k/), and [CoralHydro2k](https://lipdverse.org/project/coralhydro2k/))  

This PaleoBook is an update and continuation on [Assimilating PAGES2k Records with LinkedEarth Tools](https://linked.earth/reproduce_lmr_pb/README.html), and it may be referenced in the subsequent chapters. 

## Structure

The reconstruction workflow is broken down into 3 major steps, some of which have variants:
1. Data assembly: gathering, selection and cleaning
2. Data assimilation, which blends proxy observations with calibration data and the model prior
3. Validation and comparison to other relevant reconstructions

Here we offer two different ways to carry out Step 1, all of which result in a netCDF file that can be used in Step 2:

- [Step 1a](https://tanaya-g.github.io/pages2k_cfr_pb/notebooks/data_assembly/C01_c_db_assembly_cfr_PAGES2k.html) illustrates how to get the proxy database from the [LiPDVerse](https://lipdverse.org). 
- [Step 1b](https://tanaya-g.github.io/pages2k_cfr_pb/notebooks/data_assembly/C01_b_db_assembly_cfr_PAGES2k.html) illustrates how to get the proxy database from the [LiPD Graph](http://linkedearth.graphdb.mint.isi.edu).

Step 2 can be common to all workflows, depending on the provided metadata. In this PaleoBook we showcase one way, but another (using class-based seasonality) can be found in [here](https://linked.earth/reproduce_lmr_pb/notebooks/data_assimilation/C02_a_DA_with_class_based_seasonality.html
)
- [Step 2](https://linked.earth/presto2k_cfr_pb/README.html#./C02_b_DA_with_individual_seasonality.html)  runs the DA with metadata-based seasonality. Once again, only one instance is illustrated in this notebook. 

Step 3 focuses on validating both our results from Step 2, as well as comparing different proxy databases from Step 1 for forensics purposes. This is specific to PReSto2k, which are the newer reconstructions based on updates to PAGES2k, and validates the three reconstructions run with this proxy data, using very similar methodologies to earlier chapters. Further experiments on this data will be shown in future chapters. 
