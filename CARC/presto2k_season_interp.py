
# %%
%load_ext autoreload
%autoreload 2

import cfr
import numpy as np
print(cfr.__version__)
import pickle

def main():
    with open('./prev_data/pdb_w_seasonality_annual_interp.pkl', 'rb') as f:
        pickle_db = pickle.load(f)

    print(f"Loaded {pickle_db.nrec} records from pickle")

    # %%
    # new

    job = cfr.ReconJob()
    job.proxydb = pickle_db

    fig, ax = job.proxydb.plot(plot_count=False)

    # %%
    job.load_clim(
        tag='prior',
        
        path_dict= {
        'tas': './prev_data/ccsm4_last_millenium/tas_sfc_Amon_CCSM4_past1000_085001-185012.nc',
        'pr': './prev_data/ccsm4_last_millenium/pr_sfc_Amon_CCSM4_past1000_085001-185012.nc'
        },
        anom_period=[850,1850],  # Tardif 2019 uses entire interval
        load=True,  
        verbose=True,
    )


    # %%
    job.load_clim(
        tag='obs',
        path_dict={
            'pr': './prev_data/GPCC_precip.mon.flux.1x1.v6.nc',
            'tas': 'gistemp1200_ERSSTv4'
        },
        rename_dict={'pr': 'precip','tas': 'tempanomaly'},
        anom_period=[1951, 1980], 
        load=True,
        verbose = True
    )


    import cfr.psm as psm
    from tqdm import tqdm

    def calib_psms_seasonality(job, ptype_psm_dict, ptype_clim_dict, 
                                            calib_period=[1850, 2015], verbose=True):
        """Custom PSM calibration that uses individual proxy seasonality metadata"""
        
        for pid, pobj in tqdm(job.proxydb.records.items(), total=job.proxydb.nrec, 
                            desc='Calibrating PSMs with metadata seasonality'):
            
            psm_name = ptype_psm_dict[pobj.ptype]
            
            # Get climate data for this proxy
            for vn in ptype_clim_dict[pobj.ptype]:
                if 'clim' not in pobj.__dict__ or f'obs.{vn}' not in pobj.clim:
                    pobj.get_clim(job.obs[vn], tag='obs')
            
            # Create PSM object
            pobj.psm = psm.__dict__[psm_name](pobj, climate_required=ptype_clim_dict[pobj.ptype])
            
            # Use individual proxy seasonality from metadata
            proxy_seasonality = pobj.seasonality
            
            # Calibrate based on PSM type
            if psm_name == 'Bilinear':
                try:
                    pobj.psm.calibrate(
                        season_list1=[proxy_seasonality],  # Use proxy's own seasonality
                        season_list2=[proxy_seasonality],  # Use proxy's own seasonality  
                        calib_period=calib_period
                    )
                except:  
                    pobj.psm.calibrate(
                    season_list1=[list(range(1,13))],
                    season_list2=[list(range(1,13))],
                    calib_period=calib_period
            )

            else:
                try:
                    pobj.psm.calibrate(
                        season_list=[proxy_seasonality],   # Use proxy's own seasonality
                        calib_period=calib_period
                    )
                except:
                    pobj.psm.calibrate(
                    season_list=[list(range(1,13))],
                    calib_period=calib_period
                    )

        
        # Tag calibrated records
        for pid, pobj in job.proxydb.records.items():
            if pobj.psm.calib_details is None:
                if verbose: print(f'>>> PSM for {pid} failed to be calibrated.')
            else:
                job.proxydb.records[pid].tags.add('calibrated')
                job.proxydb.records[pid].R = pobj.psm.calib_details['PSMmse']
        
        if verbose:
            calibrated_count = job.proxydb.nrec_tags("calibrated")
            print(f'>>> {calibrated_count} records tagged "calibrated" with ProxyRecord.psm created')

    # %%
    # PSM to be used
    ptype_psm_dict = {
        'tree.TRW': 'Bilinear',
        'tree.MXD': 'Linear',
        'coral.d18O': 'Linear',
        'coral.SrCa': 'Linear',
        'coral.calc': 'Linear',
        'ice.d18O': 'Linear',
        'ice.melt': 'Linear',
        'lake.other': 'Linear',
        'lake.reflectance': 'Linear',
        'speleothem.d18O' : 'Linear',
        'sclerosponge.d18O': 'Linear',
        'marine.other': 'Linear',
        'borehole': 'Linear',
        'hybrid': 'Linear',
        'documents': 'Linear',
    }


    ptype_clim_dict = {
        'tree.TRW': ['tas', 'pr'],
        'tree.MXD': ['tas'],
        'coral.d18O': ['tas'],
        'coral.SrCa': ['tas'],
        'coral.calc': ['tas'],
        'ice.d18O': ['tas'],
        'ice.melt': ['tas'],
        'lake.other': ['tas'],
        'lake.reflectance': ['tas'],
        'speleothem.d18O' : ['tas'],
        'sclerosponge.d18O': ['tas'],
        'marine.other': ['tas'],
        'borehole': ['tas'],
        'hybrid': ['tas'],
        'documents': ['tas'],
    }

    # %%
    # Use the custom function
    calib_psms_seasonality(
        job, 
        ptype_psm_dict=ptype_psm_dict,
        ptype_clim_dict=ptype_clim_dict,
        verbose=True
    )

    # %%
    job.forward_psms(verbose=True)


    # %%

    job.annualize_clim(tag='prior', verbose=True, months=list(range(1, 13)))
    job.regrid_clim(tag='prior', nlat=42, nlon=63, verbose=True)


    # %%
    job.save('./cases/presto2k_season_interp', verbose=True)

    # %%
    job.run_da_mc(
        save_dirpath='./recons/presto2k_season_interp',
        recon_seeds=list(range(1, 2)),  # as an example here
        recon_vars=['tas','pr'],  # running tas and pr even though paper mainly focuses on tas
        recon_period=[1, 2000],
        verbose=True,
    )

if __name__ == '__main__':
    main()


