def impute(x):
    import pandas as pd
    import numpy as np
    def nump (x):
        nump_x=x.values
        return nump_x
    
    def pad(data):
        #interpole
        bad_indexes = np.isnan(data)
        good_indexes = np.logical_not(bad_indexes)
        good_data = data[good_indexes]
        interpolated = np.interp(bad_indexes.nonzero()[0], good_indexes.nonzero()[0], good_data ,left=np.nan, right=np.nan)
        data[bad_indexes] = interpolated

        # check
        bad_indexes = np.isnan(data)
        good_indexes = np.logical_not(bad_indexes)
        good_data = data[good_indexes]


        #extrapole set
        left_num=np.argwhere(~np.isnan(data))[0]
        good_data_l = data[good_indexes][0:2]
        len_good_data_l = np.arange(len(good_data_l))
        right_num=len(data)-np.argwhere(~np.isnan(data))[-1]-1
        good_data_r = data[good_indexes][-2:]
        len_good_data_r = np.arange(len(good_data_r))

        right_start_num=np.argwhere(~np.isnan(data))[-1]+1

        # Fit a polynomial to the data
        coeffs_l = np.polyfit(len_good_data_l, good_data_l, 1)
        coeffs_r = np.polyfit(len_good_data_r, good_data_r, 1)

        # Use the polynomial to extrapolate new data
        x_l = np.flip(np.arange(-1, -1 -left_num, -1))
        y_l = np.polyval(coeffs_l, x_l)
        x_r = np.arange(2, 2 + right_num)
        y_r = np.polyval(coeffs_r, x_r) 

        new_data=np.concatenate((y_l,good_data,y_r),axis=0)
    
        return new_data

    def calcul_axis(x):
        result=np.apply_along_axis(pad, 0, x)
        resultpd=pd.DataFrame(result)
        return resultpd
    
    new=calcul_axis(nump(x))
    
    def set_col(imputed,x):
        cols=list(x.columns)
        convert_dict=x.dtypes.astype(str).to_dict()
        imputed.columns = cols
        imputed = imputed.astype(convert_dict)
        return imputed
    
    new2=set_col(new,x)
    
    return new2