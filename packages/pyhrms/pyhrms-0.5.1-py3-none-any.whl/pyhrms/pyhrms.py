import pandas as pd
from pandas.core import frame
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import time
import pymzml
import scipy.signal
from numpy import where, argmin, zeros
from glob import glob
import numpy as np
import scipy.interpolate as interpolate
from molmass import Formula
import os
import json
import shutil
from tqdm import tqdm
import re
import copy
import networkx as nx
from multiprocessing import Pool
from scipy.stats import ttest_ind_from_stats
from sklearn.decomposition import PCA
from sklearn import preprocessing
import scipy.stats as st
from scipy import integrate
import itertools

atom_mass_table = pd.Series(
    data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
          'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
          'Cliso': 36.965903, 'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770,
          'Si': 27.976928, 'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
          'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
          })


def peak_picking(df1, threshold=15, i_threshold=500, SN_threshold=3,
                 profile_info=None, isotope_analysis=True, rt_error_alignment=0.05, mz_error_alignment=0.015):
    """
    :param df1: dataframe generated frm function: gen_df/gen_df_to_centroid
    :param threshold: peak_finding threshold
    :param i_threshold: minimum intensity
    :param SN_threshold: signal to noise threshold
    :param profile_info: profile information, a dict with all mass info
    :param isotope_analysis: Analyze isotope distribution
    :param rt_error_alignment: default: 0.05
    :param mz_error_alignment: default:0.015
    :return:
    """
    # 更新df1
    df1 = df1.sort_index(ascending=True)

    target_list = np.arange(50, max(df1.index.values), 0.02)
    index = find_locators(df1.index.values, target_list)

    RT = np.array(df1.columns)

    data = []
    num = len(index)
    for i in tqdm(range(num - 1), desc='Finding peaks'):
        df2 = df1.iloc[index[i]:index[i + 1]]
        a = df2.values.T  # 将dataframe转换成np.array
        if len(a[0]) != 0:
            extract_c = a.max(axis=1)
            if max(extract_c) < i_threshold:
                pass
            else:
                peak_index, left, right = peak_finding(extract_c, threshold)  # 关键函数，峰提取
                if len(peak_index) != 0:  # 判断是否找到峰
                    peak_height = extract_c[peak_index]
                    bg = cal_bg(extract_c)
                    SN = (peak_height / bg).round(2)
                    df3 = df2[df2.columns[peak_index]]
                    intensity = np.round(np.array(df3.max().values), 0)
                    rt = np.round(RT[peak_index], 2)
                    mz = np.round(np.array(df3.idxmax().values), 4)
                    # 计算峰面积
                    left_indice = abs(np.array([argmin(abs(RT - (rt_ - 0.2))) for rt_ in rt]) - 1)
                    right_indice = np.array([argmin(abs(RT - (rt_ + 0.2))) for rt_ in rt])

                    left_right_indice = np.array([left_indice, right_indice]).T
                    rt_t = [RT[index[0]:index[1]] for index in left_right_indice]
                    eic_t = [extract_c[index[0]:index[1]] for index in left_right_indice]
                    area = [round(scipy.integrate.simps(eic_t[i], rt_t[i]), 0) * 4 for i in range(len(rt_t))]
                    df_array = np.array([rt, mz, intensity, area, SN]).T
                    data.append(df_array)
    if len(data) == 0:
        return pd.DataFrame()
    else:
        peak_info = np.concatenate(data)
        peak_info_df = pd.DataFrame(data=peak_info, columns=['rt', 'mz', 'intensity', 'area', 'S/N'])
        peak_all = peak_info_df[(peak_info_df['intensity'] > i_threshold) & (peak_info_df['S/N'] > SN_threshold)]
        peak_all = peak_all.sort_values(by='intensity').reset_index(drop=True)

        # 对找到的峰进行alignment
        t0 = time.time()
        print('\r Single file alignment...                   ', end='')

        peak_p = np.array([peak_all.rt.values, peak_all.mz.values]).T
        indice = [
            peak_all[
                (peak_all.mz > peak_p[i][1] - mz_error_alignment) & (peak_all.mz < peak_p[i][1] + mz_error_alignment) &
                (peak_all.rt > peak_p[i][0] - rt_error_alignment) & (
                        peak_all.rt < peak_p[i][0] + rt_error_alignment)].index[-1] for
            i in range(len(peak_p))]
        indice1 = np.array(list(set(indice)))
        peak_all = peak_all.loc[indice1, :].sort_values(by='intensity', ascending=False).reset_index(drop=True)
        t1 = time.time()
        print(f'\r Alignment time: {round(t1 - t0, 0)} s          ', end='')

        # 对同位素丰度进行记录
        if isotope_analysis is True:
            rts = peak_all.rt.values
            mzs = peak_all.mz.values
            iso_info = [str(isotope_distribution(spec_at_rt(df1, rts[i]), mzs[i])) for i in range(len(rts))]
            peak_all['iso_distribution'] = iso_info

        # 分析profile数据，对spec进行优化
        if profile_info is None:
            return peak_all
        else:
            print('\r Optimizing ms1 based on profile data...    ', end='')
            rts = peak_all.rt.values
            mzs = peak_all.mz.values
            indice1 = np.array([i for i in profile_info.keys()])
            rt_keys = [indice1[argmin(abs(indice1 - i))] for i in rts]  # 基于上述rt找到ms的时间索引
            spec1 = [profile_info[i] for i in rt_keys]  # 获得ms的spec
            mz_result = np.array([list(evaluate_ms3(target_spec(spec1[i], mzs[i], width=0.04).copy(), mzs[i]))
                                  for i in range(len(mzs))]).T
            mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
            # mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else mzs[i] for i in range(len(mzs))]  # 去掉偏差大的矫正结果

            peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
            t2 = time.time()
            print(f'\r Optimized time: {round(t2 - t1, 0)} s     ', end='')
            return peak_all


def find_locators(df_mz_list, target_list):
    # 防止target_list最大值大于df_mz_list
    if (len(df_mz_list) != 0) & (len(target_list) != 0):
        if target_list[-1] < df_mz_list[-1]:
            pass
        else:
            target_list[target_list > df_mz_list[-1]] = df_mz_list[-1]

        if target_list[0] > df_mz_list[0]:
            pass
        else:
            target_list[target_list < df_mz_list[0]] = df_mz_list[0]
    else:
        pass
    locators = []
    j = 0  # j是df的，为了存储
    for i in range(len(target_list)):
        locator = df_mz_list[j]
        compare = target_list[i]
        while compare > locator:
            j += 1
            locator = df_mz_list[j]
            compare = target_list[i]
        locators.append(j)
    return np.array(locators)


def sep_scans(path, company):
    """
    To separate scans for MS1, MS2.
    :param company: Waters,Agilent,Thermo or AB
    :param path: The path for mzML files
    :return: ms1, ms2 and locker mass
    """
    if company == 'Waters':
        run = pymzml.run.Reader(path)
        ms1, ms2 = [], []
        for scan in tqdm(run, desc='Separating ms1 and ms2'):
            if scan.id_dict['function'] == 1:
                ms1.append(scan)
            if scan.ms_level == 2:
                ms2.append(scan)
        return ms1, ms2
    else:
        run = pymzml.run.Reader(path)
        ms1, ms2 = [], []
        for scan in tqdm(run, desc='Separating ms1 and ms2'):
            if scan.ms_level == 1:
                ms1.append(scan)
            else:
                ms2.append(scan)
        return ms1, ms2


def peak_finding(eic, threshold=15, width=2):
    """
    finding peaks in a single extracted chromatogram,and return peak index, left valley index, right valley index.
    :param width: width for a peak
    :param eic: extracted ion chromatogram data; e.g., [1,2,3,2,3,1...]
    :param threshold: define the noise level for a peak, 6 is recommend
    :return:peak index, left valley index, right valley index.
    """
    peaks, _ = scipy.signal.find_peaks(eic, width=width)
    prominence = scipy.signal.peak_prominences(eic, peaks)
    peak_prominence = prominence[0]
    left = prominence[1]
    right = prominence[2]
    # peak_picking condition 1: value of peak_prominence must be higher than
    if len(peak_prominence) == 0:
        peak_index, left, right = np.array([]), np.array([]), np.array([])

    elif len(peaks) <= 5:
        peak_index = peaks
    else:
        median_1 = np.median(peak_prominence)  # 获得中位数的值
        index_pos2 = where(prominence[0] > threshold * median_1)[0]
        peak_index = peaks[index_pos2]
        left = left[index_pos2]
        right = right[index_pos2]
    return peak_index, left, right


def extract(df1, mz, error=50):
    """
    Extracting chromatogram based on mz and error.
    :param df1: LC-MS dataframe, generated by the function gen_df()
    :param mz: Targeted mass for extraction.
    :param error: mass error for extraction
    :return: rt,eic
    """
    low = mz * (1 - error * 1e-6)
    high = mz * (1 + error * 1e-6)
    low_index = argmin(abs(df1.index.values - low))
    high_index = argmin(abs(df1.index.values - high))
    df2 = df1.iloc[low_index:high_index]
    rt = df1.columns.values
    if len(np.array(df2)) == 0:
        intensity = np.zeros(len(df1.columns))
    else:
        intensity = np.array(df2).T.max(axis=1)
    return rt, intensity  # 只返回RT和EIC


def extract2(df1, mz, error=50):
    """
    Extracting chromatogram based on mz and error.
    :param df1: LC-MS dataframe, generated by the function gen_df(),or ms1 scans can be imported.
    :param mz: Targeted mass for extraction.
    :param error: mass error for extraction
    :return: rt,eic
    """
    if type(df1) == pd.core.frame.DataFrame:
        low = mz * (1 - error * 1e-6)
        high = mz * (1 + error * 1e-6)
        low_index = argmin(abs(df1.index.values - low))
        high_index = argmin(abs(df1.index.values - high))
        df2 = df1.iloc[low_index:high_index]
        rt = df1.columns.values
        if len(np.array(df2)) == 0:
            intensity = np.zeros(len(df1.columns))
        else:
            intensity = np.array(df2).T.max(axis=1)
    elif type(df1) == list:
        rt = []
        intensity = []
        low = mz * (1 - error * 1e-6)
        high = mz * (1 + error * 1e-6)
        for scan in df1:
            mz_all = scan.mz
            i_all = scan.i
            rt1 = scan.scan_time[0]
            rt.append(rt1)
            index_e = np.where((mz_all <= high) & (mz_all >= low))
            eic1 = 0 if len(index_e[0]) == 0 else i_all[index_e[0]].sum()
            intensity.append(eic1)
    else:
        rt, intensity = None, None
    return rt, intensity  # 只返回RT和EIC


def gen_df_to_centroid(ms1, ms_round=4, profile_info=True, noise_threshold=None):
    """
    Convert mzml data to a dataframe in centroid mode.
    :param noise_threshold: noise threshold
    :param profile_info: True or False
    :param ms_round: ms round
    :param ms1: ms scan list generated by the function of sep_scans(), or directed from pymzml.run.Reader(path).
    :return: A Dataframe and a dict
    """
    t1 = time.time()
    peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]] for i in range(len(ms1))]
    if noise_threshold is None:
        data = [pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(ms_round),
                          name=round(ms1[i].scan_time[0], 3)) for i, peaks in peaks_index]
    else:
        data = [pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(ms_round),
                          name=round(ms1[i].scan_time[0], 3)) for i, peaks in peaks_index]
        data = [s1[s1 > noise_threshold] for s1 in data]

    t2 = time.time()
    # 开始级联所有数据
    print('\r Concatenating all the data...                   ', end='')
    df1 = pd.concat(data, axis=1)
    df2 = df1.fillna(0)
    t3 = time.time()
    t_1 = round(t2 - t1, 0)
    t_2 = round(t3 - t2, 0)
    print(f'\r Concat finished, 1st_stage:{t_1} s, 2nd_stage:{t_2} s            ', end='')
    if profile_info is True:
        raw_info = {round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round))
                    for i in range(len(ms1))}
        return df2, raw_info
    else:
        return df2


def gen_df_raw(ms1, ms_round=3, raw_info=True, noise_threshold=None):
    """
    Convert mzml data to a dataframe in profile mode.
    :param noise_threshold: noise threshold
    :param raw_info: raw info
    :param ms_round: ms round
    :param ms1: ms scan list generated by the function of sep_scans(), or directed from pymzml.run.Reader(path).
    :return: A Dataframe
    """
    t1 = time.time()

    # 将每个scan存在一个独立的变量scan(n)中
    if noise_threshold is None:
        data = [pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round),
                          name=round(ms1[i].scan_time[0], 3)) for i in range(len(ms1))]
    else:
        data = [pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round),
                          name=round(ms1[i].scan_time[0], 3)) for i in range(len(ms1))]
        data = [s1[s1 > noise_threshold] for s1 in data]
    t2 = time.time()

    # 开始级联所有数据
    print('\r Concatenating all the data...                             ', end='')
    df1 = pd.concat(data, axis=1)
    df2 = df1.fillna(0)
    t3 = time.time()
    t_1 = round(t2 - t1, 0)
    t_2 = round(t3 - t2, 0)
    print(f'\r Concat finished, 1st_stage:{t_1} s, 2nd_stage:{t_2} s            ', end='')
    if raw_info is True:
        raw_info = {round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i, index=ms1[i].mz.round(4))
                    for i in range(len(ms1))}
        return df2, raw_info
    else:
        return df2


def B_spline(x, y):
    """
    Generating more data points for a mass peak using beta-spline based on x,y
    :param x: mass coordinates
    :param y: intensity
    :return: new mass coordinates, new intensity
    """
    t, c, k = interpolate.splrep(x, y, s=0, k=4)
    n = 300
    xmin, xmax = x.min(), x.max()
    new_x = np.linspace(xmin, xmax, n)
    spline = interpolate.BSpline(t, c, k, extrapolate=False)
    return new_x, spline(new_x)


def cal_bg(eic):
    """
    :param eic: data need to calculate the background
    :return: background value
    """
    peaks, _ = scipy.signal.find_peaks(eic, width=0)
    if len(peaks) == 0:
        bg = max(eic) + 1
    else:
        peak_heights = eic[peaks]
        peak_heights1 = peak_heights[peak_heights < np.median(peak_heights) * 5]
        bg = max(peak_heights1) + 1
    return bg


def peak_checking_plot(df1, mz, rt1, Type='profile', path=None):
    """
    Evaluating/visualizing the extracted mz
    :param path: whether export to path
    :param Type: profile or centroid
    :param df1: LC-MS dataframe, generated by the function gen_df()
    :param mz: Targeted mass for extraction
    :param rt1: expected rt for peaks
    :return:
    """

    fig = plt.figure(figsize=(12, 4))
    # 检查色谱图ax
    ax = fig.add_subplot(121)
    rt, eic = extract(df1, mz, 50)
    rt2 = rt[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    eic2 = eic[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    ax.plot(rt, eic)
    ax.set_xlabel('Retention Time(min)', fontsize=12)
    ax.set_ylabel('Intensity', fontsize=12)
    peak_index = np.argmin(abs(rt - rt1))
    peak_height = max(eic[peak_index - 2:peak_index + 2])
    ax.scatter(rt1, peak_height * 1.05, c='r', marker='*', s=50)
    # 计算背景
    bg = cal_bg(eic)
    bg1 = zeros(len(eic)) + bg
    ax.plot(rt, bg1)
    SN = round(peak_height / bg, 1)
    ax.set_title(f'SN:{SN}')
    ax.set_ylim(top=peak_height * 1.1, bottom=-peak_height * 0.05)

    if path is None:
        pass
    else:
        plt.savefig(path, dpi=1000)
        plt.close('all')


def peak_alignment(files_excel, rt_error=0.1, mz_error=0.015):
    """
    Generating peaks information with reference mz/rt pair
    :param files_excel: files for excels of peak picking and peak checking;
    :param rt_error: rt error for merge
    :param mz_error: mz error for merge
    :return: Export to excel files
    """
    print('\r Generating peak reference...        ', end='')
    peak_ref = gen_ref(files_excel, rt_error=rt_error, mz_error=mz_error)
    pd.DataFrame(peak_ref, columns=['rt', 'mz']).to_excel(
        os.path.join(os.path.split(files_excel[0])[0], 'peak_ref.xlsx'))
    for file in tqdm(files_excel, desc='Reading each excel files'):
        peak_p = pd.read_excel(file, index_col='Unnamed: 0').loc[:, ['rt', 'mz']].values
        peak_df = pd.read_excel(file, index_col='Unnamed: 0')
        new_all_index = []
        for i in range(len(peak_p)):
            rt1, mz1 = peak_p[i]
            index = np.where((peak_ref[:, 0] <= rt1 + rt_error) & (peak_ref[:, 0] >= rt1 - rt_error)
                             & (peak_ref[:, 1] <= mz1 + mz_error) & (peak_ref[:, 1] >= mz1 - mz_error))
            new_index = str(peak_ref[index][0][0]) + '_' + str(peak_ref[index][0][1])
            new_all_index.append(new_index)
        peak_df['new_index'] = new_all_index
        peak_df = peak_df.set_index('new_index')
        peak_df = peak_df[~peak_df.index.duplicated(keep='first')]
        peak_df.to_excel(file.replace('.xlsx', '_alignment.xlsx'))


def spec_at_rt(df1, rt):
    """
    :param df1: LC-MS dataframe, generated by the function gen_df(),or ms1 list
    :param rt:  retention time for certain ms spec
    :return: ms spec
    """
    spec = None
    if type(df1) == pd.core.frame.DataFrame:
        index = argmin(abs(df1.columns.values - rt))
        spec = df1.iloc[:, index]
    elif type(df1) is list:
        for scan in df1:
            if scan.scan_time[0] > rt:
                spec = pd.Series(data=scan.i, index=scan.mz)
                break
    return spec


def concat_alignment(files_excel):
    """
    Concatenate all data and return
    :param files_excel: excel files
    :return: dataframe
    """
    align = []
    data_to_concat = []
    for i in range(len(files_excel)):
        if 'area' in files_excel[i]:
            align.append(files_excel[i])
    for i in tqdm(range(len(align)), desc='Concatenating all areas'):
        name = 'data' + str(i)
        locals()[name] = pd.read_excel(align[i], index_col='Unnamed: 0')
        data_to_concat.append(locals()[name])
    final_data = pd.concat(data_to_concat, axis=1)
    return final_data


def formula_to_distribution(formula, adducts='+H', num=3):
    """
    :param num: numbers for mass distribution
    :param formula: molecular formula, e.g., ‘C13H13N3’
    :param adducts: ion adducts, '+H', '-H'
    :return: mz_iso, i_iso (np.array)
    """
    f = Formula(formula)
    a = f.spectrum()
    mz_iso, i_iso = np.array([a for a in a.values()]).T
    i_iso = i_iso / i_iso[0] * 100
    if adducts == '+H':
        mz_iso += 1.00727647
    elif adducts == '-H':
        mz_iso -= 1.00727647
    mz_iso = mz_iso.round(4)
    i_iso = i_iso.round(1)
    s1 = pd.Series(data=i_iso, index=mz_iso).sort_values(ascending=False)
    return s1.index.values[:num], s1.values[:num]


def KMD_cal(mz_set, group='Br/H'):
    if '/' in group:
        g1, g2 = group.split('/')
        f1, f2 = Formula(g1), Formula(g2)
        f1, f2 = f1.spectrum(), f2.spectrum()
        f1_value, f2_value = [x for x in f1.values()][0][0], [x for x in f2.values()][0][0]
        values = [abs(f1_value - f2_value), round(abs(f1_value - f2_value), 0)]
        KM = mz_set * (max(values) / min(values))
        KMD_set = KM - np.floor(KM)

        print(f1_value, f2_value)
        print(min(values), max(values))
        print(values)
    else:
        g1 = Formula(group)
        f1 = g1.spectrum()
        f1_value = [x for x in f1.values()][0][0]
        KM = mz_set * (int(f1_value) / f1_value)
        KMD_set = KM - np.floor(mz_set)
    return KMD_set


def peak_checking_area(ref_all, df1, name):
    """
    Obtain the area for each rt&mz pair in df1
    :param ref_all:  peak_reference
    :param df1: dataframe df1
    :param name: name
    :return: new_dataframe
    """
    # 1. 给ref_all排序，获得需要计算的rts和mzs
    ref_all1 = ref_all.sort_values(by='mz')
    peak_index = np.array(
        ref_all1['rt'].map(lambda x: str(round(x, 2))).str.cat(ref_all1['mz'].map(lambda x: str(round(x, 4))), sep='_'))
    rts, mzs = ref_all1.rt.values, ref_all1.mz.values
    # 2. 获得mz的locators
    df_mz_list = df1.index.values
    left_locator = find_locators(df_mz_list, mzs - 0.01)
    right_locator = find_locators(df_mz_list, mzs + 0.01)
    mz_locators = np.array([left_locator, right_locator]).T
    # 3. 获得rt的locators
    df_rt = df1.columns.values
    rt_locators = [[argmin(abs(df_rt - (rt - 0.2))), argmin(abs(df_rt - (rt + 0.2)))] for rt in rts]
    # 4. 获得峰面积
    area_all = [round(scipy.integrate.simps(
        df1.iloc[mz_locators[i][0]:mz_locators[i][1], rt_locators[i][0]:rt_locators[i][1]].values.sum(axis=0) - min(
            df1.iloc[mz_locators[i][0]:mz_locators[i][1], rt_locators[i][0]:rt_locators[i][1]].values.sum(axis=0)),
        df_rt[rt_locators[i][0]:rt_locators[i][1]]), 0) * 4 for i in range(len(mz_locators))]
    sample_area = pd.DataFrame(area_all, index=peak_index, columns=[name])
    return sample_area + 1



def JsonToExcel(path, i_threshold = 10):
    """
    This function extract the information from json data and return a dataframe
    :param path: path for json file
    :return: DataFrame
    """
    with open(path, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    num = len(json_data)
    Inchikey, precursors, frags, formulas, smiles, ion_modes, instrument_types, collision_energies = [], [], [], [], [], [], [], []
    for i in tqdm(range(num)):
        # 信息1:包括分子信息
        info1 = json_data[i]['compound'][0]['metaData']
        ik_info = [x['value'] for x in info1 if x['name'] == 'InChIKey']
        formula_info = [x['value'] for x in info1 if x['name'] == 'molecular formula']
        precursor_info = [x['value'] for x in info1 if x['name'] == 'total exact mass']
        smile_info =[x['value'] for x in info1 if x['name'] == 'SMILES']
         # 获得数据
        ik = None if len(ik_info) ==0 else ik_info[0]
        formula = None if len(formula_info) ==0 else formula_info[0]
        precursor = None if len(precursor_info) ==0 else precursor_info[0]
        smile = None if len(smile_info) ==0 else smile_info[0]
        # 信息2:包括测试条件
        info2 = json_data[i]['metaData']
        ion_mode_info = [x['value'] for x in info2 if x['name'] == 'ionization mode']
        instrument_type_info = [x['value'] for x in info2 if x['name'] == 'instrument type']
        ce_info = [i for i in info2 if i['name'] == 'collision energy']



        ion_mode = None if len(ion_mode_info) ==0 else ion_mode_info[0]
        instrument_type = None if len(instrument_type_info) ==0 else instrument_type_info[0]
        ce = None if len(ce_info) ==0 else ce_info[0]['value']

        spec1 = r'{' + json_data[i]['spectrum'].replace(' ', ',') + r'}'
        spec2 = pd.Series(eval(spec1))
        spec3 = str(spec2[spec2>i_threshold].to_dict())
        # 搜集数据
        Inchikey.append(ik)
        precursors.append(precursor)
        formulas.append(formula)
        smiles.append(smile)
        ion_modes.append(ion_mode)
        instrument_types.append(instrument_type)
        frags.append(spec3)
        collision_energies.append(ce)
    database = pd.DataFrame(np.array([Inchikey, precursors, frags, formulas, smiles, ion_modes,collision_energies, instrument_types]).T,
                                    columns=['Inchikey', 'Precursor', 'Frag', 'Formula', 'Smiles', 'ion_modes', 'collision_energies',
                                             'instrument_types'])
    return database




def target_spec(spec, target_mz, width=0.04):
    """
    :param spec: spec generated from function spec_at_rt()
    :param target_mz: target mz for inspection
    :param width: width for data points
    :return: new spec and observed mz
    """
    index_left = argmin(abs(spec.index.values - (target_mz - width)))
    index_right = argmin(abs(spec.index.values - (target_mz + width)))
    new_spec = spec.iloc[index_left:index_right].copy()
    new_spec[target_mz - width] = 0
    new_spec[target_mz + width] = 0
    new_spec = new_spec.sort_index()
    return new_spec


def gen_ref(files_excel, mz_error=0.015, rt_error=0.1):
    """
    For alignment, generating a reference mz/rt pair
    :param rt_error: retention time error
    :param mz_error: mass error
    :param files_excel: excel files path for extracted peaks
    :return: mz/rt pair reference
    """
    data = []
    for i in tqdm(range(len(files_excel)), desc='Reading each excel files(gen_ref)'):
        peak1 = pd.read_excel(files_excel[i]).loc[:, ['rt', 'mz']].values
        data.append(peak1)
    print(f'\r Concatenating all peaks...                 ', end='')
    pair = np.concatenate(data, axis=0)
    peak_all_check = pair

    def align_ref(pair1):
        peak_ref1 = []
        while len(pair1) > 0:
            rt1_, mz1_ = pair1[0]
            rt1_ = round(rt1_, 2)
            mz1_ = round(mz1_, 4)
            index1 = np.where((pair1[:, 0] <= rt1_ + rt_error) & (pair1[:, 0] >= rt1_ - rt_error)
                              & (pair1[:, 1] <= mz1_ + mz_error) & (pair1[:, 1] >= mz1_ - mz_error))
            peak = [rt1_, mz1_]
            pair1 = np.delete(pair1, index1, axis=0)
            peak_ref1.append(peak)
            print(f'\r  {len(pair1)}                        ', end='')
        return peak_ref1

    peak_ref = align_ref(pair)
    peak_ref0 = np.array(peak_ref)
    # 检查漏网之鱼
    pair2 = []
    for pair in tqdm(peak_all_check, desc='Second Check for gen_ref'):
        rt1, mz1 = pair
        index = np.where((peak_ref0[:, 0] <= rt1 + rt_error) & (peak_ref0[:, 0] >= rt1 - rt_error)
                         & (peak_ref0[:, 1] <= mz1 + mz_error) & (peak_ref0[:, 1] >= mz1 - mz_error))
        if len(index[0]) == 0:
            pair2.append([rt1, mz1])
    peak_ref2 = align_ref(np.array(pair2))
    final_peak_ref = peak_ref + peak_ref2
    return np.array(final_peak_ref)


def ms_bg_removal(background, target_spec1, i_threshold=500, mz_error=0.01):
    """
    Only support for centroid data, please convert profile data to centroid
    :param i_threshold: intensity threshold
    :param background:  background spec
    :param target_spec1:  target spec
    :param mz_error: ms widow
    :return: spec after bg removal
    """
    target_spec1 = target_spec1[target_spec1 > i_threshold]
    bg = []
    if len(target_spec1) == 0:
        return None
    else:
        for i in target_spec1.index.values:
            index = argmin(abs(background.index.values - i))
            if background.index.values[index] - i < mz_error:
                bg.append([i, background.values[index]])
            else:
                bg.append([i, 0])
        bg_spec = pd.Series(np.array(bg).T[1], np.array(bg).T[0], name=target_spec1.name)
        spec_bg_removal = target_spec1 - bg_spec
        return spec_bg_removal[spec_bg_removal > i_threshold].sort_values()


def ms_to_centroid(spec):
    """
    :param spec: profile spec ready to convert into centroid data
    :return: converted centroid data
    """
    peaks, _ = scipy.signal.find_peaks(spec.values.copy())
    new_index = spec.index.values[peaks]
    new_values = spec.values[peaks]
    new_spec = pd.Series(new_values, new_index, name=spec.name)
    return new_spec


def spec_similarity(spec_obs, suspect_frag, error=0.005):
    """
    :param spec_obs: observed spec
    :param suspect_frag: frag in database
    :param error: mz window
    :return:
    """
    fragments = suspect_frag.index.values[-10:]
    score = 0
    for i in fragments:
        if min(abs(spec_obs.index.values - i)) < error:
            score += 1
    return score / len(fragments)


def evaluate_ms(new_spec, mz_exp):
    """
    :param new_spec: target ms spec with width ± 0.04
    :param mz_exp:  expected mz
    :return: mz_obs, error1, final_mz_opt, error2, resolution
    """

    peaks, _ = scipy.signal.find_peaks(new_spec.values)
    if (len(peaks) == 0) or (max(new_spec.values) < 100):
        mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    else:
        try:
            mz_obs = new_spec.index.values[peaks][argmin(abs(new_spec.index.values[peaks] - mz_exp))]
            x, y = B_spline(new_spec.index.values, new_spec.values)
            peaks, _ = scipy.signal.find_peaks(y)
            max_index = peaks[argmin(abs(x[peaks] - mz_exp))]
            half_height = y[max_index] / 2
            mz_left = x[:max_index][argmin(abs(y[:max_index] - half_height))]
            mz_right = x[max_index:][argmin(abs(y[max_index:] - half_height))]
            resolution = int(mz_obs / (mz_right - mz_left))
            mz_opt = round(mz_left + (mz_right - mz_left) / 2, 4)
            error1 = round((mz_obs - mz_exp) / mz_exp * 1000000, 1)
            error2 = round((mz_opt - mz_exp) / mz_exp * 1000000, 1)
        except TypeError:
            mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    return mz_obs, error1, mz_opt, error2, resolution

def evaluate_ms2(new_spec, mz_exp):
    """
    :param new_spec: target ms spec with width ± 0.04
    :param mz_exp:  expected mz
    :return: mz_obs, error1, final_mz_opt, error2, resolution
    """

    peaks, _ = scipy.signal.find_peaks(new_spec.values)
    if (len(peaks) == 0) or (max(new_spec.values) < 100):
        mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    else:
        try:
            mz_obs = new_spec.index.values[peaks][argmin(abs(new_spec.index.values[peaks] - mz_exp))]
            x, y = B_spline(new_spec.index.values, new_spec.values)
            peaks1, left,right = peak_finding(y)
            max_index_index = argmin(abs(x[peaks1] - mz_exp))
            max_index = peaks1[max_index_index]
            left_index = left[max_index_index] # 获得峰的左边边界
            right_index = right[max_index_index] # 获得峰的右边边界
            half_height = y[max_index]/2 # 获得峰的半峰高
            half_mz_left=x[left_index:max_index][argmin(abs(y[left_index:max_index]-half_height))]
            half_mz_right= x[max_index:right_index][argmin(abs(y[max_index:right_index]-half_height))]
            resolution = int(mz_obs / (half_mz_right - half_mz_left))
            mz_opt = round(half_mz_left + (half_mz_right - half_mz_left) / 2, 4)
            error1 = round((mz_obs - mz_exp) / mz_exp * 1000000, 1)
            error2 = round((mz_opt - mz_exp) / mz_exp * 1000000, 1)
        except:
            mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    return round(mz_obs,4), error1, mz_opt, error2, resolution

def evaluate_ms3(new_spec, mz_exp):
    """
    :param new_spec: target ms spec with width ± 0.04
    :param mz_exp:  expected mz
    :return: mz_obs, error1, final_mz_opt, error2, resolution
    """

    peaks, _ = scipy.signal.find_peaks(new_spec.values)
    if (len(peaks) == 0) or (max(new_spec.values) < 100):
        mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    else:
        try:
            mz_obs = new_spec.index.values[peaks][argmin(abs(new_spec.index.values[peaks] - mz_exp))]
            x, y = B_spline(new_spec.index.values, new_spec.values)
            peaks1, left,right = peak_finding(y)
            max_index_index = argmin(abs(x[peaks1] - mz_exp))
            max_index = peaks1[max_index_index]
            half_height = y[max_index]/2 # 获得峰的半峰高
            # 找到交叉点
            intersect_index = [i for i in range(len(y)-1) if ((y[i]<half_height)&
                                                              (y[i+1]>half_height))|((y[i]>half_height)&(y[i+1]<half_height))]
            
            target_list = x[intersect_index]
            half_mz_left = target_list[np.argwhere(target_list<mz_exp)[-1]][0]
            half_mz_right = target_list[np.argwhere(target_list>mz_exp)[0]][0]
            
            resolution = int(mz_obs / (half_mz_right - half_mz_left))
            mz_opt = round(half_mz_left + (half_mz_right - half_mz_left) / 2, 4)
            error1 = round((mz_obs - mz_exp) / mz_exp * 1000000, 1)
            error2 = round((mz_opt - mz_exp) / mz_exp * 1000000, 1)
        except:
            mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    return round(mz_obs,4), error1, mz_opt, error2, resolution

def first_process(file, company, i_threshold=200, SN_threshold=3,
                  profile=True, ms2_analysis=True, frag_rt_error=0.02):
    """
    For processing HRMS data, this process will do peak picking and peak checking
    :param SN_threshold: signal to noise threshold
    :param frag_rt_error:  for fragments,MS2 analysis retention time error
    :param i_threshold: intensity threshold
    :param ms2_analysis: True or False
    :param profile: True or False
    :param file: single file to process
    :param company: e.g., 'Waters', 'Agilent',etc,
    """
    mz_round = 4
    ms1, ms2 = sep_scans(file, company)

    if profile is True:
        if company.lower() == 'waters':
            df1, raw_info = gen_df_to_centroid(ms1, mz_round)
            peak_all = peak_picking(df1, profile_info=raw_info, i_threshold=i_threshold)
        else:
            peak_all = split_peak_picking(ms1, i_threshold=i_threshold)
    else:
        if company.lower() == 'waters':
            df1 = gen_df_raw(ms1, mz_round)
            peak_all = peak_picking(df1)
        else:
            peak_all = split_peak_picking(ms1, profile=False, i_threshold=i_threshold)

    # 根据intensity和SN筛选
    peak_all = peak_all[(peak_all['intensity'] > i_threshold) & (peak_all['S/N'] > SN_threshold)]

    if len(ms2) == 0:
        pass
    else:
        if ms2_analysis is True:
            if ('control' in file.lower()) | ('blank' in file.lower()) | ('methanol' in file.lower()) | (
                    'qaqc' in file.lower()):
                pass
            else:
                print('\r Starting DIA ms2 analysis...          ', end='')
                if profile is True:
                    if company.lower() == 'waters':
                        df2 = gen_df_to_centroid(ms2, mz_round, profile_info=False)  # 不分析二级碎片
                        peak_all2 = peak_picking(df2, isotope_analysis=False)
                    else:
                        peak_all2 = split_peak_picking(ms2, profile=True, i_threshold=i_threshold)
                else:
                    if company.lower() == 'waters':
                        df2 = gen_df_raw(ms2, mz_round)
                        peak_all2 = peak_picking(df2, isotope_analysis=False)
                    else:
                        peak_all2 = split_peak_picking(ms2, profile=False, i_threshold=i_threshold)

                frag_all = []
                for i in range(len(peak_all)):
                    rt = peak_all.loc[i, 'rt']
                    frag = str(list(peak_all2[(peak_all2['rt'] > rt - frag_rt_error)
                                              & (peak_all2['rt'] < rt + frag_rt_error)].sort_values(
                        by='intensity', ascending=False)['mz'].values))
                    frag_all.append(frag)
                peak_all.loc[:, 'frag_DIA'] = frag_all

        else:
            pass
    file_name = os.path.basename(file)
    print(f'\r Success!  #################  file name:{file_name}   ', end='')
    peak_selected = identify_isotopes(peak_all)
    peak_selected.to_excel(file.replace('.mzML', '.xlsx'))


def second_process(file, ref_all, company, profile=True):
    """
    This process will reintegrate peak area
    :param profile: True or False
    :param file: single file to process
    :param ref_all: all reference peaks
    :param company: e.g., 'Waters', 'Agilent',etc,
    :return: export to files
    """
    ms_round = 4
    ms1, ms2 = sep_scans(file, company)
    if company.lower() == 'waters':
        if profile is True:
            df1 = gen_df_to_centroid(ms1, ms_round=4, profile_info=False)
        else:
            df1 = gen_df_raw(ms1, ms_round=4, raw_info=False)
        final_result = peak_checking_area(ref_all, df1, name=os.path.basename(file).split('.')[0])
        final_result.to_excel(file.replace('.mzML', '_final_area.xlsx'))
    else:
        name1 = os.path.basename(file).split('.')[0]
        final_result = peak_checking_area_split(ref_all, ms1, company,
                                                name1, profile=profile)
        final_result.to_excel(file.replace('.mzML', '_final_area.xlsx'))


def extract_tic(ms1):
    """
    For extracting TIC data
    :param ms1: ms1
    :return: rt,tic
    """
    rt = [scan.scan_time[0] for scan in ms1]
    tic = [scan.TIC for scan in ms1]
    return rt, tic


def fold_change_filter(path, fold_change=5, area_threshold=500):
    """
    :param path: path for all excels
    :param fold_change:  minimum fold change
    :param area_threshold: minimum area
    :return: generate unique cmps
    """
    # 整合blank数据，获的最大值
    print('\r Organizing blank data...         ', end='')
    excel_path = os.path.join(path, '*.xlsx')
    files_excel = glob(excel_path)
    alignment = [file for file in files_excel if 'alignment' in file]
    area_files = [file for file in files_excel if 'final_area' in file]
    blk_files = [file for file in area_files if 'blank' in file.lower() or
                 'control' in file.lower() or 'qaqc' in file.lower() or 'methanol' in file.lower()]
    blk_df = concat_alignment(blk_files)  # 生成所有blank的dataframe表
    blk_s = blk_df.max(axis=1)  # 找到blanks中每个峰的最大值
    final_blk = blk_s.to_frame(name='blk')
    print('\r Start to process fold change         ', end='')
    # 整合每个area_file与blank的对比结果，输出fold change 大于fold_change倍的值
    area_files_sample = [file for file in area_files if 'blank' not in file.lower() and
                         'control' not in file.lower() and 'qaqc' not in file.lower()
                         and 'methanol' not in file.lower()]
    for i in tqdm(range(len(area_files_sample)), desc='Fold change processing'):
        # 基于峰面积的对比拿到比较数据
        sample = pd.read_excel(area_files_sample[i], index_col='Unnamed: 0')
        compare = pd.concat((sample, final_blk), axis=1)
        compare['fold_change'] = (compare.iloc[:, 0] / compare.iloc[:, 1]).round(2)
        compare_result1 = compare[compare['fold_change']
                                  > fold_change].sort_values(by=compare.columns[0], ascending=False)
        compare_result = compare_result1[compare_result1[compare_result1.columns[0]] > area_threshold]
        # 开始处理alignment文件
        name = os.path.basename(area_files_sample[i]).replace('_final_area.xlsx', '')  # 拿到名字
        alignment_path = [file for file in alignment if name in file][0]
        alignment_df = pd.read_excel(alignment_path, index_col='new_index').sort_values(by='intensity')
        alignment_df1 = alignment_df[~alignment_df.index.duplicated(keep='last')]  # 去掉重复索引

        final_index = np.intersect1d(alignment_df1.index.values, compare_result.index.values)
        final_alignment = alignment_df1.loc[final_index, :].sort_values(by='intensity', ascending=False)
        final_alignment['fold_change'] = compare_result.loc[final_index, ['fold_change']]
        new_name = area_files_sample[i].replace('_final_area', '_unique_cmps')  # 文件输出名称
        final_alignment.to_excel(new_name)


def classify_files(path):
    """
    Classify the generated excel files.
    :param path: path for excel files
    :return:
    """
    files_excel = glob(os.path.join(path, '*.xlsx'))
    step1 = os.path.join(path, 'step1_peak_picking_result')
    step2 = os.path.join(path, 'step2_peak_alignment_result')
    step3 = os.path.join(path, 'step3_all_peak_areas')
    step4 = os.path.join(path, 'step4_fold_change_filter')
    try:
        os.mkdir(step1)
    except:
        pass
    try:
        os.mkdir(step2)
    except:
        pass
    try:
        os.mkdir(step3)
    except:
        pass
    try:
        os.mkdir(step4)
    except:
        pass
    for file in files_excel:
        if 'alignment' in file:
            try:
                shutil.move(file, step2)
            except:
                pass
        elif 'final_area' in file:
            try:
                shutil.move(file, step3)
            except:
                pass
        elif 'unique_cmps' in file:
            try:
                shutil.move(file, step4)
            except:
                pass
        else:
            try:
                shutil.move(file, step1)
            except:
                pass
    files_excel = glob(os.path.join(step3, '*.xlsx'))
    all_peak_areas = concat_alignment(files_excel)
    all_peak_areas.to_excel(os.path.join(step3, 'final_result.xlsx'))


def gen_frag_DIA(ms1, ms2, rt, profile=True, i_threshold=200):
    """
    :param i_threshold: Intensity threshold
    :param ms1: ms1 list
    :param ms2: ms2 list
    :param rt: peak retention time
    :param profile: True or False
    :return: frag_spec_after_bg_removal
    """
    target_ms1 = ms1[0]
    target_ms2 = ms1[0]
    for ms in ms1:
        if ms.scan_time[0] > rt:
            target_ms1 = ms
            break
    for ms in ms2:
        if ms.scan_time[0] > rt:
            target_ms2 = ms
            break
    if profile is True:
        spec1 = pd.Series(data=target_ms1.i, index=target_ms1.mz)
        spec2 = pd.Series(data=target_ms2.i, index=target_ms2.mz)
        spec1 = ms_to_centroid(spec1)
        spec2 = ms_to_centroid(spec2)
        spec_bg_removal = ms_bg_removal(spec1, spec2, i_threshold=i_threshold)
    else:
        spec1 = pd.Series(data=target_ms1.i, index=target_ms1.mz)
        spec2 = pd.Series(data=target_ms2.i, index=target_ms2.mz)
        spec_bg_removal = ms_bg_removal(spec1, spec2, i_threshold=i_threshold)
    return spec_bg_removal


def identify_isotopes(cmp, iso_error=0.005):
    """
    :param iso_error: isotope mass error
    :param cmp: unique compounds dataframe
    :return: unique compounds dataframe with isotope peak labeled
    """
    # 元素周期表
    atom_mass_table1 = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853, 'Cliso': 36.965903,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Briso': 80.916290, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })

    # 计算不同同位素和adducts之间的差值
    Ciso = atom_mass_table1['Ciso'] - atom_mass_table1['C']
    Cliso = atom_mass_table1['Cliso'] - atom_mass_table1['Cl']
    Na = atom_mass_table1['Na'] - atom_mass_table1['H']
    K = atom_mass_table1['K'] - atom_mass_table1['H']
    NH3 = 3 * atom_mass_table1['H'] + atom_mass_table1['N']

    all_rts = list(set(cmp['rt'].values))
    for i in tqdm(range(len(all_rts)), desc='Finding Isotopes and adducts:'):
        cmp_rt = cmp[(cmp['rt'] >= all_rts[i] - 0.015) & (cmp['rt'] <= all_rts[i] + 0.015)].sort_values(by='mz')
        mzs = cmp_rt['mz'].values
        for mz in mzs:
            C_fold = 1
            differ = mzs - mz
            # 拿到此mz的intensity
            mz_i = cmp_rt[cmp_rt['mz'] == mz]['intensity'].values[0]  # 数值

            # 搜索C13同位素
            i_C13_1 = np.where((differ < Ciso + iso_error) & (differ > Ciso - iso_error))[0]
            if len(i_C13_1) == 0:
                pass
            elif len(i_C13_1) == 1:
                index_ = cmp_rt.index[i_C13_1]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if mz_i * C_fold > compare_i:
                    cmp.loc[index_, 'Ciso'] = f'C13:{all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_C13_1]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if mz_i * C_fold > compare_i:
                        cmp.loc[index, 'Ciso'] = f'C13: {all_rts[i]} _{mz}'

            # 搜索Cl同位素
            i_Cl = np.where((differ < Cliso + iso_error) & (differ > Cliso - iso_error))[0]
            if len(i_Cl) == 0:
                pass
            elif len(i_Cl) == 1:
                index_ = cmp_rt.index[i_Cl]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if (mz_i * 0.45 > compare_i) & (mz_i * 0.2 < compare_i):
                    cmp.loc[index_, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                elif (mz_i * 0.5 < compare_i) & (mz_i * 0.8 > compare_i):
                    cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                elif (mz_i * 0.8 < compare_i) & (mz_i * 1.2 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                elif (mz_i * 1.5 < compare_i) & (mz_i * 2.5 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'

            else:
                index_ = cmp_rt.index[i_Cl]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if (mz_i * 0.45 > compare_i) & (mz_i * 0.2 < compare_i):
                        cmp.loc[index, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                    elif (mz_i * 0.5 < compare_i) & (mz_i * 0.8 < compare_i):
                        cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                    elif (mz_i * 0.8 < compare_i) & (mz_i * 1.2 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                    elif (mz_i * 1.5 < compare_i) & (mz_i * 2.5 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'

            # 搜索+Na+峰
            i_Na = np.where((differ < Na + iso_error) & (differ > Na - iso_error))[0]  # Na+:22.9892, Na+-H: 21.9814
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'

            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'

            # 搜索+K+峰
            i_Na = np.where((differ < K + iso_error) & (differ > K - iso_error))[0]
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'

            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'

            # 搜索+NH4+峰
            i_NH4 = np.where((differ < NH3 + iso_error) & (differ > NH3 - iso_error))[0]  # NH3:17.0266
            if len(i_NH4) == 0:
                pass
            elif len(i_NH4) == 1:
                index_ = cmp_rt.index[i_NH4]
                cmp.loc[index_, 'NH4 adducts'] = f'NH4 adducts:  {all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_NH4]
                for index in index_:
                    cmp.loc[index, 'NH4 adducts'] = f'NH4 adducts: {all_rts[i]} _{mz}'
        columns = cmp.columns.values
        new_columns = sort_columns_name(columns)
        cmp = cmp.loc[:, new_columns]

    return cmp


def database_quantification(mzml_files, local_database):
    """
    To integrate peaks and return areas for quantification based on local_database
    :param mzml_files: mzml files
    :param local_database: local database dataframe
    :return: dataframe
    """
    for file in mzml_files:
        name = os.path.basename(file).replace('.mzML', '')
        ms1, ms2 = sep_scans(file, 'Waters')
        df1 = gen_df_raw(ms1)
        for i in range(len(local_database)):
            mz, rt = local_database.loc[i, ['mz_exp', 'rt']]
            rt1, eic1 = extract(df1, mz, 50)
            left = argmin(abs(rt1 - (rt - 0.2)))
            right = argmin(abs(rt1 - (rt + 0.2)))
            rt_t, eic_t = rt1[left:right], eic1[left:right]
            area = round(scipy.integrate.simps(eic_t, rt_t), 0)
            local_database.loc[i, f'{name}'] = area
    return local_database


def append_list(mz, loop_num, atoms, atom_n):
    """
    For formula prediction function
    :param mz: target mz for prediction
    :param loop_num: number of atoms
    :param atoms: atoms
    :param atom_n: atom numbers
    :return:
    """
    pattern = []
    if loop_num == 2:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            for j in range(atom_n[1][0], atom_n[1][1] + 2):
                pattern.append([i, j])
    if loop_num == 3:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            for j in range(atom_n[1][0], atom_n[1][1] + 2):
                for k in range(atom_n[2][0], atom_n[2][1] + 2):
                    pattern.append([i, j, k])
    if loop_num == 4:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]] * i  # i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table[atoms[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table[atoms[1]])) < atom_n[1][1] else atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                for k in range(atom_n[2][0], atom_n[2][1] + 2):
                    for l in range(atom_n[3][0], atom_n[3][1] + 2):
                        pattern.append([i, j, k, l])
    # 五个原子
    if loop_num == 5:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]] * i  # i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table[atoms[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table[atoms[1]])) < atom_n[1][1] else atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j  # j还剩多少质量
                k1 = int(np.floor(j_mz_remain / atom_mass_table[atoms[2]])) if int(
                    np.floor(j_mz_remain / atom_mass_table[atoms[2]])) < atom_n[2][1] else atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    for l in range(atom_n[3][0], atom_n[3][1] + 2):
                        for m in range(atom_n[4][0], atom_n[4][1] + 2):
                            pattern.append([i, j, k, l, m])
    # 六个原子
    if loop_num == 6:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]] * i  # i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table[atoms[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table[atoms[1]])) < atom_n[1][1] else atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j  # j还剩多少质量
                k1 = int(np.floor(j_mz_remain / atom_mass_table[atoms[2]])) if int(
                    np.floor(j_mz_remain / atom_mass_table[atoms[2]])) < atom_n[2][1] else atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    k_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j - atom_mass_table[
                        atoms[2]] * k  # k还剩多少质量
                    l1 = int(np.floor(k_mz_remain / atom_mass_table[atoms[3]])) if int(
                        np.floor(k_mz_remain / atom_mass_table[atoms[3]])) < atom_n[3][1] else atom_n[3][1]
                    for l in range(atom_n[3][0], l1 + 2):
                        for m in range(atom_n[4][0], atom_n[4][1] + 2):
                            for n in range(atom_n[5][0], atom_n[5][1] + 2):
                                pattern.append([i, j, k, l, m, n])
    # 七个原子
    if loop_num == 7:
        for i in range(atom_n[0][0], atom_n[0][1] + 2):
            i_mz_remain = mz - atom_mass_table[atoms[0]] * i  # i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table[atoms[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table[atoms[1]])) < atom_n[1][1] else atom_n[1][1]
            for j in range(atom_n[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j  # j还剩多少质量
                k1 = int(np.floor(j_mz_remain / atom_mass_table[atoms[2]])) if int(
                    np.floor(j_mz_remain / atom_mass_table[atoms[2]])) < atom_n[2][1] else atom_n[2][1]
                for k in range(atom_n[2][0], k1 + 2):
                    k_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j - atom_mass_table[
                        atoms[2]] * k  # k还剩多少质量
                    l1 = int(np.floor(k_mz_remain / atom_mass_table[atoms[3]])) if int(
                        np.floor(k_mz_remain / atom_mass_table[atoms[3]])) < atom_n[3][1] else atom_n[3][1]
                    for l in range(atom_n[3][0], l1 + 2):
                        l_mz_remain = mz - atom_mass_table[atoms[0]] * i - atom_mass_table[atoms[1]] * j - \
                                      atom_mass_table[atoms[2]] * k - atom_mass_table[atoms[3]] * l  # l还剩多少质量
                        m1 = int(np.floor(l_mz_remain / atom_mass_table[atoms[4]])) if int(
                            np.floor(l_mz_remain / atom_mass_table[atoms[4]])) < atom_n[4][1] else atom_n[4][1]
                        for m in range(atom_n[4][0], m1 + 2):
                            for n in range(atom_n[5][0], atom_n[5][1] + 2):
                                for o in range(atom_n[6][0], atom_n[6][1] + 2):
                                    pattern.append([i, j, k, l, m, n, o])

    return pattern


def formula_prediction(mz, error=500, atoms1=None, atom_n1=None, mode='pos'):
    """
    To predict the possible formula based on mass and possible atoms,support 7 atoms max.
    :param mz: mz to predict
    :param error: mass error tolerance
    :param atoms1:  atoms for prediction, e.g.,['C','H','O','N']
    :param atom_n1: atoms number range, e.g., [[0,15],[0,20],[0,10],[0,10]]
    :param mode: 'pos' or 'neg'
    :return: prediction result
    """
    if atom_n1 is None:
        atom_n1 = [[0, 15], [0, 20], [0, 10], [0, 10]]
    if atoms1 is None:
        atoms1 = ['C', 'H', 'O', 'N']
    atoms = copy.deepcopy(atoms1)
    atom_n = copy.deepcopy(atom_n1)
    atom_mass_table1 = pd.Series(data={'C': 12.000000, 'N': 14.003074, 'O': 15.994915, 'H': 1.007825,
                                       'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
                                       'S': 31.972072, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
                                       'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477,
                                       'D': 2.014102,
                                       'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305,
                                       })

    # 纠错机制,把明显不可能的删除掉，提高效率
    for i in range(len(atoms)):
        num = int(np.floor(mz / atom_mass_table1[atoms[i]])) if int(np.floor(mz / atom_mass_table1[atoms[i]])) < \
                                                                atom_n[i][1] else atom_n[i][1]
        atom_n[i][1] = num

    # 矫正formula
    def process_formula(formula):
        b1 = re.findall('[A-Z][a-z]*|\\d+', formula)
        c = ''
        for n in range(len(b1)):
            if b1[n].isdigit():
                if eval(b1[n]) == 1:
                    c += b1[n - 1]
                elif eval(b1[n]) > 1:
                    c += b1[n - 1]
                    c += b1[n]
        return c

    mz_h = mz * (1 + error * 1e-6)
    mz_l = mz * (1 - error * 1e-6)
    a = len(atoms)
    b = len(atom_n)
    pattern = []

    if (a > 0) & (a == b):
        pattern = append_list(mz, a, atoms, atom_n)

    else:
        if a <= 0:
            print('Atoms number is 0')
        else:
            print(f'There are {a} atoms,but numbers only have {b}')

    p_df = pd.DataFrame(pattern, columns=atoms)

    data_all = []
    for atom in p_df.columns:
        data_all.append(p_df[atom] * atom_mass_table1[atom])
    df_ = pd.concat(data_all, axis=1)
    if mode == 'pos':
        p_df['mass'] = df_.sum(axis=1).values - 0.000549
    else:
        p_df['mass'] = df_.sum(axis=1).values + 0.000549

    p_df['error'] = ((p_df['mass'].values - mz) / mz * 1e6).round(1)
    p_df['error_abs'] = abs(((p_df['mass'].values - mz) / mz * 1e6).round(1))

    p_df = p_df[(p_df['mass'] >= mz_l) & (p_df['mass'] <= mz_h)].sort_values(by='error_abs').reset_index(drop=True)

    # 转成formula

    formula1 = p_df.columns[0] + p_df.iloc[:, 0].astype(str)
    for i in range(1, a):
        formula1 += p_df.columns[i] + p_df.iloc[:, i].astype(str)
    p_df['formula'] = formula1.apply(process_formula)

    return p_df.loc[:, ['formula', 'mass', 'error']]


def formula_sep(formula):
    """
    Transform formula to atoms list and atoms number list.
    :param formula: e.g., 'C13H13N3'
    """
    a = re.findall('[A-Z][a-z]*|\\d+', formula)
    b = {}
    for i in range(len(a)):
        try:
            eval(a[i])
        except NameError:
            try:
                b[a[i]] = eval(a[i + 1])
            except NameError:
                b[a[i]] = 1
    c = pd.Series(b)
    atoms = list(c.index)
    atom_n1 = list(c.values)
    atom_n = []
    for num in atom_n1:
        atom_n.append([0, num])
    return atoms, atom_n


def frag_correction(mz, formula, mode):
    """
    Correct the observed mz to theoretical mz.
    :param mz: observed mz
    :param formula: precursor formula or atom range
    :param mode: 'pos' or 'neg'
    :return: frag_formula, mz_opt, error
    """
    atoms, atom_n = formula_sep(formula)
    result = formula_prediction(mz, 50, atoms, atom_n, mode=mode)
    if len(result) == 0:
        frag_formula, mass, error = None, None, None
    else:
        frag_formula, mass, error = result.loc[0, ['formula', 'mass', 'error']]
    return frag_formula, mass, error


def FT_ICRMS(path, formula='C50H60O50N1S1', mz_range=None, peak_threshold=6, error=1, iso_error=0.0003,
             iso_fold_change=2, mode='neg'):
    """
    :param mode: pos or neg
    :param path: file path, support for profile raw data, format: .xy, .csv, .xlsx
    :param formula: formula range for prediction
    :param mz_range: mz range for prediction
    :param peak_threshold: Similar to signal to noise.
    :param error: mz error for formula prediction, unit: part per million(ppm)
    :param iso_error: mz error for isotope assignment, unit: Dalton
    :param iso_fold_change: the peak intensity/isotope intensity
    :return: A dataframe with formula prediction
    """
    if mz_range is None:
        mz_range = [200, 800]
    atom_mass_table1 = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })

    # 查找同位素的函数
    def find_isotopes(data1, atom_mass_table2, error1=0.0003, iso_fold_change1=5):

        Ciso = atom_mass_table2['Ciso'] - atom_mass_table2['C']
        Niso = atom_mass_table2['Niso'] - atom_mass_table2['N']
        Oiso = atom_mass_table2['Oiso'] - atom_mass_table2['O']
        Siso = atom_mass_table2['Siso'] - atom_mass_table2['S']
        Ciso_all = []
        Niso_all = []
        Oiso_all = []
        Siso_all = []

        for mz1 in tqdm(data1['m/z'].values, desc='Finding isotopes'):
            mz_i = data1[data1['m/z'] == mz1]['i'].values[0]
            mz_s = data1['m/z'] - mz1
            C = np.where((mz_s < Ciso + error1) & (mz_s > Ciso - error1))
            C_i = data1.loc[C[0]]['i']
            N = np.where((mz_s < Niso + error1) & (mz_s > Niso - error1))
            N_i = data1.loc[N[0]]['i']
            O = np.where((mz_s < Oiso + error1) & (mz_s > Oiso - error1))
            O_i = data1.loc[O[0]]['i']
            S = np.where((mz_s < Siso + error1) & (mz_s > Siso - error1))
            S_i = data1.loc[S[0]]['i']

            if len(C[0]) > 0:
                if mz_i > iso_fold_change1 * C_i.values[0]:
                    Ciso_all.append(int(C[0]))
            if len(N[0]) > 0:
                if mz_i > iso_fold_change1 * N_i.values[0]:
                    Niso_all.append(int(N[0]))
            if len(O[0]) > 0:
                if mz_i > iso_fold_change1 * O_i.values[0]:
                    Oiso_all.append(int(O[0]))
            if len(S[0]) > 0:
                if mz_i > iso_fold_change1 * S_i.values[0]:
                    Siso_all.append(int(S[0]))
        return np.array(Ciso_all), np.array(Niso_all), np.array(Oiso_all), np.array(Siso_all)

    # 生成所有可能的formula
    def generate_formula_df(mz_range1, atoms1, atom_n1, mode1=mode):
        """
        generate possible formula set for mz range
        """
        if mode1 == 'pos':
            e = atom_mass_table1['e'] * -1
        elif mode1 == 'neg':
            e = atom_mass_table1['e']
        else:
            print('mode set as positive')
            e = atom_mass_table1['e'] * -1
        pattern = []
        for n in range(atom_n1[0][0], atom_n1[0][1] + 2):
            i_mz_remain = mz - atom_mass_table1[atoms1[0]] * n  # i还剩多少质量
            j1 = int(np.floor(i_mz_remain / atom_mass_table1[atoms1[1]])) if int(
                np.floor(i_mz_remain / atom_mass_table1[atoms1[1]])) < atom_n1[1][1] else atom_n1[1][1]
            for j in range(atom_n1[1][0], j1 + 2):
                j_mz_remain = mz - atom_mass_table1[atoms1[0]] * n - atom_mass_table1[atoms1[1]] * j  # j还剩多少质量
                k1 = int(np.floor(j_mz_remain / atom_mass_table1[atoms1[2]])) if int(
                    np.floor(j_mz_remain / atom_mass_table1[atoms1[2]])) < atom_n1[2][1] else atom_n1[2][1]
                for k in range(atom_n1[2][0], k1 + 2):
                    for l in range(atom_n1[3][0], atom_n1[3][1] + 2):
                        for m in range(atom_n1[4][0], atom_n1[4][1] + 2):
                            pattern.append([n, j, k, l, m])
        pattern_df1 = pd.DataFrame(pattern, columns=atoms1)
        pattern_df1['m/z_exp'] = (pattern_df1[atoms1[0]] * atom_mass_table1[atoms1[0]] +
                                  pattern_df1[atoms1[1]] * atom_mass_table1[atoms1[1]] +
                                  pattern_df1[atoms1[2]] * atom_mass_table1[atoms1[2]] +
                                  pattern_df1[atoms1[3]] * atom_mass_table1[atoms1[3]] +
                                  pattern_df1[atoms1[4]] * atom_mass_table1[atoms1[4]] + e)
        pattern_df1 = pattern_df1.sort_values(by='m/z_exp')
        pattern_df1 = pattern_df1[
            (pattern_df1['m/z_exp'] > mz_range1[0]) & (pattern_df1['m/z_exp'] < mz_range1[1]) & (pattern_df1['C'] >= 3)
            & (pattern_df1['H'] >= 1) & (pattern_df1['O'] >= 1)].reset_index(drop=True)
        return pattern_df1

    # 开始匹配
    def formula_match(data1, pattern_df1, error1=1.05, iso_error1=0.0003, iso_fold_change1=5):
        # 匹配同位素
        def iso_match(data2, Ciso_index2, pattern_df2, marker, error2=1.05):
            final_data = []
            for n in tqdm(range(len(data2.loc[Ciso_index2])), desc=f'matching {marker} isotope'):
                iso = marker[0] + 'iso'
                mz1 = data2.loc[Ciso_index2].iloc[n, 0] - atom_mass_table1[iso]
                df2 = pattern_df2[(pattern_df2['m/z_exp'] < mz1 * (1 + error2 * 1e-6)) & (
                        pattern_df2['m/z_exp'] > mz1 * (1 - error2 * 1e-6))].copy()
                df2 = df2[(df2['C'] >= df2['O'] / 1.2) & (df2['C'] >= df2['H'] / 2.5)]  # 筛选条件
                if len(df2) == 0:
                    pass
                else:
                    df2['m/z_obs'] = data2.loc[Ciso_index2].iloc[n, 0]
                    df2['intensity'] = data2.loc[Ciso_index2].iloc[n, 1]
                    df2['error(ppm)'] = ((df2['m/z_exp'] - mz1) / mz1 * 1 * 1e6).round(4)
                    df2['error_abs'] = df2['error(ppm)'].abs()
                    df2['hetero'] = df2['N'] + df2['S']
                    df2['isotope'] = marker
                    s1 = df2.sort_values(by='hetero').iloc[0]
                    s1.loc[marker[0]] += 1
                    s1.loc['m/z_exp'] += atom_mass_table1[iso]
                    final_data.append(s1)
            if len(final_data) == 0:
                return None
            else:
                return pd.concat(final_data, axis=1).T

        # 匹配普通峰
        def normal_match(data3, Ciso_index3, pattern_df3, marker, error3=1.05):
            final_data = []
            for i1 in tqdm(range(len(data3.loc[Ciso_index3])), desc='matching normal peaks'):
                mz1 = data3.loc[Ciso_index3].iloc[i1, 0]
                df2 = pattern_df3[(pattern_df3['m/z_exp'] < mz1 * (1 + error3 * 1e-6)) & (
                        pattern_df3['m/z_exp'] > mz1 * (1 - error3 * 1e-6))].copy()
                df2 = df2[(df2['C'] >= df2['O'] / 1.2) & (df2['C'] >= df2['H'] / 2.5)]  # 筛选条件
                if len(df2) == 0:
                    pass
                else:
                    df2['m/z_obs'] = mz1
                    df2['intensity'] = data3.loc[Ciso_index3].iloc[i1, 1]
                    df2['error(ppm)'] = ((df2['m/z_exp'] - mz1) / mz1 * 1 * 1e6).round(4)
                    df2['error_abs'] = df2['error(ppm)'].abs()
                    df2['hetero'] = df2['N'] + df2['S']
                    df2['isotope'] = marker
                    s1 = df2.sort_values(by='hetero').iloc[0]
                    final_data.append(s1)
            if len(final_data) == 0:
                return None
            else:
                return pd.concat(final_data, axis=1).T

        # 开始处理
        Ciso_index, Niso_index, Oiso_index, Siso_index = find_isotopes(data1, atom_mass_table1, iso_error1,
                                                                       iso_fold_change1)

        all_iso_index = np.concatenate([Ciso_index, Niso_index, Oiso_index, Siso_index])
        peak_no_iso = np.delete(data1.index.values, all_iso_index.astype(int))
        # 处理同位素
        data_to_concat = []
        if len(Ciso_index) != 0:
            Ciso_df = iso_match(data1, Ciso_index, pattern_df1, 'C13', error2=error1)
            data_to_concat.append(Ciso_df)
        if len(Niso_index) != 0:
            Niso_df = iso_match(data1, Niso_index, pattern_df1, 'N15', error2=error1)
            data_to_concat.append(Niso_df)
        if len(Oiso_index) != 0:
            Oiso_df = iso_match(data1, Oiso_index, pattern_df1, 'O18', error2=error1)
            data_to_concat.append(Oiso_df)
        if len(Siso_index) != 0:
            Siso_df = iso_match(data1, Siso_index, pattern_df1, 'S34', error2=error1)
            data_to_concat.append(Siso_df)
        # 处理其他
        peak_no_iso_df = normal_match(data1, peak_no_iso, pattern_df1, '', error3=error1)
        data_to_concat.append(peak_no_iso_df)

        return pd.concat(data_to_concat)

    # 读取数据
    raw_data = pd.read_csv(path, delimiter=' ', names=['m/z', 'i'])

    # 分割分子式
    atoms, atom_n = formula_sep(formula)
    mz = mz_range[1]
    for i in range(len(atoms)):
        num = int(np.floor(mz / atom_mass_table1[atoms[i]])) if int(np.floor(mz / atom_mass_table1[atoms[i]])) < \
                                                                atom_n[i][1] else atom_n[i][1]
        atom_n[i][1] = num

    # 找到峰
    eic = raw_data.loc[:, 'i']
    index, index_left, index_right = peak_finding(eic, threshold=peak_threshold)
    data = raw_data.loc[index, :].reset_index(drop=True)
    background = np.mean(eic) * 2.5
    # 生成所有可能的formula
    pattern_df = generate_formula_df(mz_range, atoms, atom_n)

    # 开始匹配
    final_result = formula_match(data, pattern_df, error1=error, iso_error1=iso_error, iso_fold_change1=iso_fold_change)
    final_result = final_result.sort_values(by='m/z_obs').reset_index(drop=True)

    # 矫正formula,把C13H13O3N0S0转成C13H13N3
    def process_formula(formula4, mode4):
        b = re.findall('[A-Z][a-z]*|\\d+', formula4)
        for j in range(len(b)):
            if (b[j] == 'H') & (mode4 == 'pos'):
                b[j + 1] = str(eval(b[j + 1]) - 1)
            elif (b[j] == 'H') & (mode4 == 'neg'):
                b[j + 1] = str(eval(b[j + 1]) + 1)
        c = ''
        for j in range(len(b)):
            if b[j].isdigit():
                if eval(b[j]) == 1:
                    c += b[j - 1]
                elif eval(b[j]) > 1:
                    c += b[j - 1]
                    c += b[j]
        return c

    # 把所有formula整合
    formula1 = final_result.columns[0] + final_result.iloc[:, 0].astype(str)
    for i in range(1, 5):
        formula1 += final_result.columns[i] + final_result.iloc[:, i].astype(str)
    final_result['formula'] = formula1.apply(process_formula, mode=mode)

    # 计算其他参数
    final_result['S/N'] = (final_result['intensity'] / background).astype(float).round(2)
    final_result['O/C'] = (final_result['O'] / final_result['C']).astype(float).round(3)

    if mode == 'pos':
        x = 1
    elif mode == 'neg':
        x = -1
    else:
        x = 1
        print('mode set as positive')
    final_result['H/C'] = ((final_result['H'] - x) / final_result['C']).astype(float).round(3)
    final_result['DBE'] = 1 + 0.5 * (2 * final_result['C'] - (final_result['H'] - x) + final_result['N'])
    final_result['NOSC'] = 4 - (4 * final_result['C'] + (final_result['H'] - x)
                                - 3 * final_result['N'] - 2 * final_result['O'] - 2 * final_result['S']) / final_result[
                               'C']
    final_result['NOSC'] = final_result['NOSC'].astype(float).round(3)
    AI_denominator = final_result['C'] - 0.5 * final_result['O'] - final_result['S'] - final_result['N']
    AI_numerator = 1 + final_result['C'] - 0.5 * final_result['O'] - final_result['S'] - 0.5 * (final_result['H'] - x)
    AI = AI_numerator / (AI_denominator.sort_values() + 1 * 1e-6)
    final_result['AI'] = AI
    return final_result


def concat_list(l):
    """
    Finding list with same elements and concat them into one list
    :param l: list to concat
    :return: final list
    """
    G = nx.Graph()
    # 将节点添加到Graph
    G.add_nodes_from(sum(l, []))
    # 从节点列表创建边
    q = [[(s[i], s[i + 1]) for i in range(len(s) - 1)] for s in l]
    for i in q:
        # 向Graph添加边
        G.add_edges_from(i)
    # 查找每个组件的图形和列表节点中的所有连接组件
    final_list = [list(i) for i in nx.connected_components(G)]
    return final_list


def gen_possible_formula(formula, mz_range=None, mode='pos'):
    if mz_range is None:
        mz_range = [50, 1000]
    mz = mz_range[1]
    atoms, atom_n = formula_sep(formula)
    # 删除不可能的组合
    for i in range(len(atoms)):
        num = int(np.floor(mz / atom_mass_table[atoms[i]])) if int(np.floor(mz / atom_mass_table[atoms[i]])) < \
                                                               atom_n[i][1] else atom_n[i][1]
        atom_n[i][1] = num
    #  开始匹配
    pattern_df = pd.DataFrame(append_list(mz, len(atoms), atoms, atom_n), columns=atoms)
    pattern_df = pattern_df[
        (pattern_df['C'] > 2) & (pattern_df['H'] > 2) & (pattern_df['C'] >= pattern_df['O'] / 1.2) & (
                pattern_df['C'] >= pattern_df['H'] / 2.5)]

    a = pattern_df[atoms[0]] * atom_mass_table[atoms[0]]
    for i in range(len(atoms) - 1):
        a += pattern_df[atoms[i + 1]] * atom_mass_table[atoms[i + 1]]
    if mode == 'pos':
        pattern_df['m/z_exp'] = a - 0.0005
    elif mode == 'neg':
        pattern_df['m/z_exp'] = a + 0.0005
    return pattern_df[pattern_df['m/z_exp'] < mz_range[1]].reset_index(drop=True)


def one_step_process(path, company, profile=True, i_threshold=200,
                     SN_threshold=3, ms2_analysis=True, frag_rt_error=0.02, filter_type=3,
                     fold_change=5, area_threshold=500):
    """
    For beginners, one step process will greatly simplify this process.
    :param filter_type: 1 for only peak area change filter (> maximum of control area);
                        2 for p_value and fold change filter (treat all controls as a whole);
                        3 for  p_value and fold change filter (treat each set of solvent_blank, filed blank,lab blank)
    :param frag_rt_error: fragment retention error
    :param ms2_analysis: True or False
    :param SN_threshold: signal to noise threshold
    :param i_threshold: intensity threshold
    :param path: path for mzml files
    :param company: company for LC-HRMS data
    :param profile: False or True
    :param fold_change: False or a number
    :param area_threshold: area threshold
    """

    # 第一个过程
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    for file in files_mzml:
        first_process(file, company, i_threshold=i_threshold, SN_threshold=SN_threshold,
                      profile=profile, ms2_analysis=ms2_analysis, frag_rt_error=frag_rt_error)

    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')

    # 第二个过程
    for file in files_mzml:
        second_process(file, ref_all, company, profile)

    # 第三个过程


def compare_frag(frag_obs, frag_exp, error=0.015):
    """
    Compare similarity of fragments.
    :param frag_obs: fragments observed;
    :param frag_exp: fragments expected;
    :param error: mass error, Da
    :return: a series.
    """
    frag_obs = np.sort(frag_obs)
    frag_exp = np.sort(frag_exp)
    compare_result = {}
    if len(frag_obs) < len(frag_exp):
        for mz in frag_obs:
            index = argmin(abs(frag_exp - mz))
            matched_mz = frag_exp[index]
            compare_result[mz] = matched_mz - mz
    else:
        for mz in frag_exp:
            index = argmin(abs(frag_obs - mz))
            matched_mz = frag_obs[index]
            compare_result[matched_mz] = mz - matched_mz
    if len(compare_result) == 0:
        s2 = []
    else:
        s1 = pd.Series(compare_result)
        s2 = s1[s1.abs() < error]
        s2 = s2.sort_values()
        s3 = s2.copy()
        s3.index = s3.index.values.round(1)
        s2 = s2[~s3.index.duplicated()].sort_index()
    return s2


def ms2_matching(unique, database, ms1_error=50, ms2_error=0.015, mode='pos'):
    """
    :param mode: pos or neg
    :param unique: unique cmp dataframe
    :param database: database dataframe
    :param ms1_error: precursor error
    :param ms2_error: fragment mz error
    :return:
    """

    columns = list(unique.columns.values)

    DIA = [column for column in columns if 'DIA' in column]
    DDA = [column for column in columns if 'DDA' in column]
    print(' ')
    print('DIA columns:', DIA)
    print('DIA columns:', DDA)
    database1 = database[database['mode'] == mode]  # 匹配mode模式
    if len(DIA) != 0:
        for i in tqdm(range(len(unique)), desc='Starting DIA ms2 matching:'):
            mz = unique.loc[i]['mz']
            mz_opt = unique.loc[i]['mz_opt'] if 'mz_opt' in unique.columns.values else None  # 如果有mz_opt则读入
            if mode == 'pos':
                precursor = mz - 1.0073
                precursor_opt = mz_opt - 1.0073 if mz_opt is not None else None
            else:
                precursor = mz + 1.0073
                precursor_opt = mz_opt + 1.0073 if mz_opt is not None else None
            frag_obs = np.array(eval(unique.loc[i][DIA[0]]))
            # 根据 precursor在数据库database里做ms1匹配
            if precursor_opt is None:
                match_result = database1[(database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))]
            else:
                match_result = database1[((database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))) |
                                         ((database1['Precursor'] < precursor_opt * (1 + ms1_error * 1e-6)) & (
                                                 database1['Precursor'] > precursor_opt * (1 - ms1_error * 1e-6)))]

            match_result_dict = []  # 定义一个列表接收数据
            # 对匹配结果依次分析
            if len(match_result) == 0:  # 匹配失败
                pass
            else:
                for j in range(len(match_result)):
                    ik_match = match_result['Inchikey'].iloc[j]  # 匹配的ik
                    source_info = match_result.iloc[j]['Source info']
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match - precursor) / precursor * 1e6, 1)  # 计算ms1 error
                    ms1_error_opt = round((precursor_match - precursor_opt) / precursor_opt * 1e6,
                                          1) if precursor_opt is not None else None  # 计算ms1_opt error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                    except:
                        frag_exp = []
                    try:
                        compare_result = compare_frag(frag_obs, frag_exp, error=ms2_error)
                    except:
                        print(frag_exp)
                        compare_result = []

                    if len(compare_result) == 0:
                        pass
                    else:
                        single_result_dict = {}  # 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  # 匹配的具体数据
                        match_num = len(compare_frag_dict)  # 匹配的个数

                        match_percent = round(len(compare_frag_dict) / len(set(frag_exp.round())), 2)  # 匹配的百分比

                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['ms1_opt_error'] = ms1_error_opt
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        single_result_dict['source'] = source_info
                        match_result_dict.append(single_result_dict)
            # 输出结果
            unique.loc[i, 'match_result_DIA'] = str(match_result_dict)
            if len(match_result_dict) == 0:
                unique.loc[i, 'best_results_DIA'] = str([])
            else:
                optimized_result = pd.concat([pd.Series(a) for a in match_result_dict], axis=1).T.sort_values(
                    by=['match_num', 'ms1_error', 'match_percent'], ascending=[False, True, False])
                unique.loc[i, 'best_results_DIA'] = str(optimized_result.iloc[0].to_dict())

    if len(DDA) != 0:
        for i in tqdm(range(len(unique)), desc='Starting DDA ms2 matching:'):
            mz = unique.loc[i]['mz']
            mz_opt = unique.loc[i]['mz_opt'] if 'mz_opt' in unique.columns.values else None  # 如果有mz_opt则读入
            if mode == 'pos':
                precursor = mz - 1.0078
                precursor_opt = mz_opt - 1.0073 if mz_opt is not None else None
            else:
                precursor = mz + 1.0078
                precursor_opt = mz_opt + 1.0073 if mz_opt is not None else None

            frag_obs = np.array(eval(unique.loc[i][DDA[0]]))
            # 根据 precursor在数据库database里做ms1匹配
            if precursor_opt is None:
                match_result = database1[(database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))]
            else:
                match_result = database1[((database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))) |
                                         ((database1['Precursor'] < precursor_opt * (1 + ms1_error * 1e-6)) & (
                                                 database1['Precursor'] > precursor_opt * (1 - ms1_error * 1e-6)))]

            match_result_dict = []  # 定义一个列表接收数据
            # 对匹配结果依次分析
            if len(match_result) == 0:  # 匹配失败
                pass
            else:
                for j in range(len(match_result)):
                    ik_match = match_result['Inchikey'].iloc[j]  # 匹配的ik
                    source_info = match_result.iloc[j]['Source info']
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match - precursor) / precursor * 1e6, 1)  # 计算ms1 error
                    ms1_error_opt = round((precursor_match - precursor_opt) / precursor_opt * 1e6,
                                          1) if precursor_opt is not None else None  # 计算ms1_opt error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                    except:
                        frag_exp = []
                    compare_result = compare_frag(frag_obs, frag_exp, error=ms2_error)
                    if len(compare_result) == 0:
                        pass
                    else:
                        single_result_dict = {}  # 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  # 匹配的具体数据
                        match_num = len(compare_frag_dict)  # 匹配的个数

                        match_percent = round(len(compare_frag_dict) / len(set(frag_exp.round())), 2)  # 匹配的百分比

                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['ms1_opt_error'] = ms1_error_opt
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        single_result_dict['source'] = source_info
                        match_result_dict.append(single_result_dict)
            # 输出结果
            unique.loc[i, 'match_result_DDA'] = str(match_result_dict)

            if len(match_result_dict) == 0:
                unique.loc[i, 'best_results_DDA'] = '[]'
            else:
                optimized_result = pd.concat([pd.Series(a) for a in match_result_dict], axis=1).T.sort_values(
                    by=['match_num', 'ms1_error', 'match_percent'], ascending=[False, True, False])
                unique.loc[i, 'best_results_DDA'] = str(optimized_result.iloc[0].to_dict())

    return unique


def multi_process(path, company, profile=True, processors=5, p_value=0.05, ms2_analysis=True, fold_change=5,
                  area_threshold=200, filter_type=3):
    """
    :param path: path for mzml files
    :param company: 'Waters','Agilent','AB','Thermo',etc
    :param profile:  True if profile, False if centroid;
    :param processors: shared processors number. Warning: If memory use > 90%, some excel files may not be generated.
    :param p_value: max p_values
    :param ms2_analysis: True if you want DIA frag analysis.
    :param fold_change: fold change for peak areas
    :param area_threshold: minimum area
    :param filter_type: 1 for only peak area change filter (> maximum of control area);
                        2 for p_value and fold change filter (treat all controls as a whole);
                        3 for  p_value and fold change filter (treat each set of solvent_blank, filed blank,lab blank)
    :return: None
    """
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml_DDA = [file for file in files_mzml if 'DDA' in os.path.basename(file)]
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    # 第一个过程
    pool = Pool(processes=processors)
    for file in files_mzml:
        print(file)
        pool.apply_async(first_process, args=(file, company, profile, ms2_analysis))
    print('==========================')
    print('First process started...')
    print('==========================')
    pool.close()
    pool.join()

    # 检查是否有遗漏的
    files_excel_temp = glob(os.path.join(path, '*.xlsx'))
    files_excel_names = [os.path.basename(i)[:-5] for i in files_excel_temp]
    path_omitted = []
    if len(files_mzml) > len(files_excel_names):
        # 检查是哪个文件漏掉了
        for path1 in files_mzml:
            if os.path.basename(path1)[:-5] in files_excel_names:
                pass
            else:
                path_omitted.append(path1)
    if len(path_omitted) == 0:
        pass
    else:
        pool = Pool(processes=processors)
        for file in path_omitted:
            print('Omitted files')
            print(file)
            pool.apply_async(first_process, args=(file, company, profile, ms2_analysis))
        pool.close()
        pool.join()

    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')

    # 第二个过程
    pool = Pool(processes=processors)
    for file in files_mzml:
        print(file)
        pool.apply_async(second_process, args=(file, ref_all, company, profile))
    print('==========================')
    print('Second process started...')
    print('==========================')
    pool.close()
    pool.join()

    # 第三个过程, 做fold change filter
    print('\r ==========================', end='')
    print('Third process started...')
    print('==========================')
    if filter_type == 1:
        fold_change_filter(path, fold_change=fold_change, area_threshold=area_threshold)
    elif filter_type == 2:
        fold_change_filter2(path, fold_change=fold_change, p_value=p_value, area_threshold=area_threshold)
    elif filter_type == 3:
        fold_change_filter3(path, fold_change=fold_change, p_value=p_value, area_threshold=area_threshold)

    # 如果有DDA，将DDA数据加入到excel里
    files_excel = glob(os.path.join(path, '*.xlsx'))
    unique_cmps = [file for file in files_excel if 'unique_cmps' in os.path.basename(file)]
    for file in files_mzml_DDA:
        df2 = gen_DDA_ms2_df(file, company, profile=profile, opt=False)
        name = os.path.basename(file).replace('-DDA', '').replace('_DDA', '').replace('.mzML', '')  # 获得DDA文件的特征名称
        for file_excel in unique_cmps:
            if name in os.path.basename(file_excel):
                df1 = pd.read_excel(file_excel)
                for i in range(len(df1)):
                    rt, mz = df1.loc[i, ['rt', 'mz']]
                    df_frag = df2[(df2['precursor'] >= mz - 0.015) & (df2['precursor'] <= mz + 0.015)
                                  & (df2['rt'] >= rt - 0.1) & (df2['rt'] <= rt + 0.1)]
                    if len(df_frag) == 0:
                        df1.loc[i, 'frag_DDA'] = str([])
                    else:
                        frag_all = []
                        for j in range(len(df_frag)):
                            mz1, intensity1 = df_frag['frag'].iloc[j], df_frag['intensity'].iloc[j]
                            frag_s = pd.Series(data=intensity1, index=mz1, dtype='float64')
                            frag_all.append(frag_s)
                        frag_s_all = pd.concat(frag_all).sort_values(ascending=False)
                        frag_s_all1 = frag_s_all[frag_s_all > 200]
                        frag_s_all2 = frag_s_all1[~frag_s_all1.index.duplicated(keep='first')]
                        frag_final = str(list(frag_s_all2.iloc[:20].index.values))
                        df1.loc[i, 'frag_DDA'] = frag_final
                        df1.loc[i, 'MS2_spectra'] = str(frag_s_all2.iloc[:20])
                df1.to_excel(file_excel)


def fold_change_filter2(path, fold_change=5, p_value=0.05, area_threshold=500):
    """
    New fold change filter, to calculate the fold change based on mean value, and calculate the p_values.
    :param path: excel path
    :param fold_change: fold change threshold
    :param p_value: p value threshold
    :param area_threshold: area threshold
    :return: Export new excel files.
    """

    def get_p_value(mean1, std1, nobs1, mean2, std2, nobs2):
        result = ttest_ind_from_stats(mean1, std1, nobs1, mean2, std2, nobs2)
        return result.pvalue

    # 把 excel files分类
    excel_path = os.path.join(path, '*.xlsx')
    files_excel = glob(excel_path)
    alignment = [file for file in files_excel if 'alignment' in file]
    area_files = [file for file in files_excel if 'final_area' in file]
    blk_files = [file for file in area_files if 'blank' in file.lower() or
                 'control' in file.lower() or 'qaqc' in file.lower() or 'methanol' in file.lower()]

    # 开始处理blank 统计数据
    blk_df = concat_alignment(blk_files)  # 生成所有blank的dataframe表

    area_files_sample = [file for file in area_files if 'blank' not in file and
                         'control' not in file.lower() and 'qaqc' not in file.lower() and
                         'methanol' not in file.lower()]
    all_names = list(
        set([os.path.basename(x).replace('_final_area.xlsx', '')[:-1] for x in area_files_sample]))  # 拿到所有样品名称
    # 获得blank的统计信息
    blk_df_info = pd.concat([blk_df.mean(axis=1), blk_df.std(axis=1), blk_df.apply(len, axis=1)], axis=1)
    blk_df_info.columns = ['mean1', 'std1', 'nobs1']

    # 开始处理sample
    for name in all_names:
        print(name)
        samples1 = [x for x in area_files_sample if name in x]
        sample_df = concat_alignment(samples1)
        sample_df_info = pd.concat([sample_df.mean(axis=1), sample_df.std(axis=1), sample_df.apply(len, axis=1)],
                                   axis=1)
        sample_df_info.columns = ['mean2', 'std2', 'nobs2']
        all_info = pd.concat([blk_df_info, sample_df_info], axis=1)
        pvalues_s = all_info.apply(
            lambda row: get_p_value(row['mean1'], row['std1'], row['nobs1'], row['mean2'], row['std2'], row['nobs2']),
            axis=1)
        fold_change_s = (all_info['mean2'] / all_info['mean1']).round(2)
        area_sample_mean = all_info['mean2'].round(0)
        area_sample_std = all_info['std2'].round(0)
        # 将数值付给每一个alignment变量

        samples1_alignment = [x for x in alignment if name in x]
        for alignment_path in samples1_alignment:
            alignment_file = pd.read_excel(alignment_path, index_col='new_index')
            alignment_file = alignment_file[~alignment_file.index.duplicated(keep='last')]  # 去掉重复索引
            alignment_file['area_mean'] = area_sample_mean.loc[alignment_file.index.values]
            alignment_file['area_std'] = area_sample_std.loc[alignment_file.index.values]
            alignment_file['fold_change'] = fold_change_s.loc[alignment_file.index.values]
            alignment_file['p_values'] = pvalues_s.loc[alignment_file.index.values]
            alignment_file['Control set number'] = len(blk_files)
            alignment_file['Sample set number'] = len(samples1_alignment)

            unique_cmp = alignment_file[(alignment_file['fold_change'] > fold_change)
                                        & (alignment_file['p_values'] < p_value)
                                        & (alignment_file['area'] > area_threshold)].sort_values(by='intensity',
                                                                                                 ascending=False)
            columns = unique_cmp.columns.values
            new_columns = sort_columns_name(columns)
            unique_cmp = unique_cmp.loc[:, new_columns]

            unique_cmp.to_excel(alignment_path.replace('_alignment', '_unique_cmps'))


def fold_change_filter3(path, fold_change=5, p_value=0.05, area_threshold=500):
    def get_p_value(mean1, std1, nobs1, mean2, std2, nobs2):
        result = ttest_ind_from_stats(mean1, std1, nobs1, mean2, std2, nobs2)
        return result.pvalue

    # 把 excel files分类
    excel_path = os.path.join(path, '*.xlsx')
    files_excel = glob(excel_path)
    alignment = [file for file in files_excel if 'alignment' in file]
    area_files = [file for file in files_excel if 'final_area' in file]
    methanol = [file for file in area_files if 'methanol' in file.lower()]  # blank1
    ISTD_blank = [file for file in area_files if 'istd_blank' in file.lower()]  # blank2
    field_blank = [file for file in area_files if 'field_blank' in file.lower()]  # blank3
    lab_blank = [file for file in area_files if 'lab_blank' in file.lower()]  # blank4
    sampler_blank = [file for file in area_files if 'sampler_blank' in file.lower()]  # blank5
    control = [file for file in area_files if 'control' in file.lower()]  # blank6
    # 开始处理blank 统计数据
    # 1.甲醇空白
    if len(methanol) != 0:
        methanol_df = concat_alignment(methanol)  # 生成所有blank的dataframe表
        methanol_df_info = pd.concat([methanol_df.mean(axis=1), methanol_df.std(axis=1),
                                      methanol_df.apply(len, axis=1)], axis=1).fillna(1)
        methanol_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        methanol_df_info = []
    # 2. 内标空白
    if len(ISTD_blank) != 0:
        ISTD_blank_df = concat_alignment(ISTD_blank)
        ISTD_blank_df_info = pd.concat([ISTD_blank_df.mean(axis=1), ISTD_blank_df.std(axis=1),
                                        ISTD_blank_df.apply(len, axis=1)], axis=1).fillna(1)
        ISTD_blank_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        ISTD_blank_df_info = []

    # 3. 现场空白
    if len(field_blank) != 0:
        field_blank_df = concat_alignment(field_blank)
        field_blank_df_info = pd.concat([field_blank_df.mean(axis=1), field_blank_df.std(axis=1),
                                         field_blank_df.apply(len, axis=1)], axis=1).fillna(1)
        field_blank_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        field_blank_df_info = []

    # 4. 实验室空白
    if len(lab_blank) != 0:
        lab_blank_df = concat_alignment(lab_blank)
        lab_blank_df_info = pd.concat([lab_blank_df.mean(axis=1), lab_blank_df.std(axis=1),
                                       lab_blank_df.apply(len, axis=1)], axis=1).fillna(1)
        lab_blank_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        lab_blank_df_info = []

    # 5. 采样器空白
    if len(sampler_blank) != 0:
        sampler_blank_df = concat_alignment(sampler_blank)
        sampler_blank_df_info = pd.concat([sampler_blank_df.mean(axis=1), sampler_blank_df.std(axis=1),
                                           sampler_blank_df.apply(len, axis=1)], axis=1).fillna(1)
        sampler_blank_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        sampler_blank_df_info = []

    # 其他对照
    if len(control) != 0:
        control_df = concat_alignment(control)
        control_df_info = pd.concat([control_df.mean(axis=1), control_df.std(axis=1),
                                     control_df.apply(len, axis=1)], axis=1).fillna(1)
        control_df_info.columns = ['mean1', 'std1', 'nobs1']
    else:
        control_df_info = []

    blank_all = [methanol_df_info, ISTD_blank_df_info, field_blank_df_info, lab_blank_df_info, sampler_blank_df_info,
                 control_df_info]
    blank_name = ['methanol', 'ISTD_blank', 'field_blank', 'lab_blank', 'sampler_blank', 'control']

    print('--------------------------------')
    print('Start processing samples...')
    print('--------------------------------')

    area_files_sample = [file for file in area_files if
                         'methanol' not in file.lower() and 'blank' not in file.lower()
                         and 'control' not in file.lower()]
    all_names = list(
        set([os.path.basename(x).replace('_final_area.xlsx', '')[:-1] for x in area_files_sample]))  # 拿到所有样品名称

    for name in all_names:
        print(name)
        samples1 = [x for x in area_files_sample if name in x]
        sample_df = concat_alignment(samples1)
        sample_df_info = pd.concat([sample_df.mean(axis=1), sample_df.std(axis=1), sample_df.apply(len, axis=1)],
                                   axis=1)
        sample_df_info.columns = ['mean2', 'std2', 'nobs2']

        # 计算每个样品组之间的p值
        all_p_mean_std = []
        all_p_mean_std_name = []

        area_sample_mean = sample_df_info['mean2'].round(0)
        all_p_mean_std.append(area_sample_mean)
        all_p_mean_std_name.append('Sample_area_mean')

        area_sample_std = sample_df_info['std2'].round(0)
        all_p_mean_std.append(area_sample_std)
        all_p_mean_std_name.append('Sample_area_std')

        for j in tqdm(range(len(blank_all)), desc='Calculating p values'):
            blk_df_info = blank_all[j]
            if len(blk_df_info) != 0:  # 必须不等于0才能进行合并
                all_info = pd.concat([blk_df_info, sample_df_info], axis=1)
                pvalues_s = all_info.apply(
                    lambda row: get_p_value(row['mean1'], row['std1'], row['nobs1'], row['mean2'], row['std2'],
                                            row['nobs2']),
                    axis=1)
                all_p_mean_std.append(pvalues_s)
                all_p_mean_std_name.append(blank_name[j] + '_p_value')

                fold_change_s = (all_info['mean2'] / all_info['mean1']).round(2)
                all_p_mean_std.append(fold_change_s)
                all_p_mean_std_name.append(blank_name[j] + '_fold_change')

        addition = pd.concat(all_p_mean_std, axis=1)
        addition.columns = all_p_mean_std_name

        # 开始生成样品
        samples1_alignment = [x for x in alignment if name in x]
        for alignment_path in samples1_alignment:
            alignment_file = pd.read_excel(alignment_path, index_col='new_index')
            alignment_file = alignment_file[~alignment_file.index.duplicated(keep='last')]  # 去掉重复索引
            unique_cmp = pd.concat([alignment_file, addition.loc[alignment_file.index]], axis=1)
            columns = unique_cmp.columns.values
            new_columns = sort_columns_name(columns)
            unique_cmp = unique_cmp.loc[:, new_columns]
            fold_change_columns = [column for column in unique_cmp.columns if 'fold_change' in column]
            p_values_columns = [column for column in unique_cmp.columns if 'p_value' in column]
            for column in fold_change_columns:
                unique_cmp = unique_cmp[unique_cmp[column] > fold_change]
            for column in p_values_columns:
                unique_cmp = unique_cmp[unique_cmp[column] < p_value]
            unique_cmp = unique_cmp[unique_cmp['area'] > area_threshold].sort_values(by='intensity', ascending=False)
            unique_cmp.to_excel(alignment_path.replace('_alignment', '_unique_cmps'))


def rt_matching(unique, database, ms1_error=50, rt_error=0.1, mode='pos'):
    """
    Matching compounds based on retention time & m/z in database
    :param unique: target unique compounds dataframe
    :param database: database
    :param ms1_error: ms1 error
    :param rt_error:  retention time error
    :param mode: 'pos' or 'neg'
    :return:  unique dataframe
    """
    db = database[(database['mode'] == mode) & (~database['rt'].isna())]
    for i in tqdm(range(len(unique)), desc='Starting rt & m/z matching:'):
        if 'mz_opt' in unique.columns.values:
            rt, mz, mz_opt = unique.loc[i, ['rt', 'mz', 'mz_opt']]
        else:
            rt, mz = unique.loc[i, ['rt', 'mz']]
            mz_opt = None

        if mode == 'pos':
            precursor = mz - 1.0073
            mz_opt1 = mz_opt - 1.0073 if mz_opt is not None else None
        else:
            precursor = mz + 1.0073
            mz_opt1 = mz_opt + 1.0073 if mz_opt is not None else None

        if mz_opt1 is None:
            result = db[(db['rt'] > rt - rt_error) & (db['rt'] < rt + rt_error) &
                        (db['Precursor'] > precursor * (1 - ms1_error * 1e-6)) & (
                                db['Precursor'] < precursor * (1 + ms1_error * 1e-6))]
        else:
            result = db[(db['rt'] > rt - rt_error) & (db['rt'] < rt + rt_error) &
                        ((db['Precursor'] > precursor * (1 - ms1_error * 1e-6)) &
                         (db['Precursor'] < precursor * (1 + ms1_error * 1e-6)) |
                         (db['Precursor'] > mz_opt1 * (1 - ms1_error * 1e-6))
                         & (db['Precursor'] < mz_opt1 * (1 + ms1_error * 1e-6))
                         )]

        if len(result) != 0:
            result1 = result.copy()
            result1['rt_error'] = (result1['rt'] - rt).round(3)
            result1['mz_error'] = ((result1['Precursor'] - precursor) / precursor * 1e6).round(1)
            result1['mz_opt_error'] = ((result1['Precursor'] - mz_opt1) / mz_opt1 * 1e6).round(
                1) if mz_opt1 is not None else None
            result1['ik'] = result1['Inchikey']
            result_str = str(result1.loc[:, ['ik', 'rt_error', 'mz_error',
                                             'mz_opt_error']].sort_values(by='mz_error',
                                                                          ascending=False).iloc[0, :].T.to_dict())
            unique.loc[i, 'rt_match_result'] = result_str
        else:
            unique.loc[i, 'rt_match_result'] = str([])
    return unique


def database_match(path, database, ms1_error=50, ms2_error=0.015, rt_error=0.1, mode='pos'):
    """
    Matching compounds in database, process all files in path by single core.
    :param path: path for excel
    :param database: database dataframe
    :param ms1_error: ms1 error, ppm
    :param ms2_error: ms2 error, Da
    :param rt_error: retention error
    :param mode: pos or neg
    :return: export to file
    """
    unique_files = [file for file in glob(os.path.join(path, '*.xlsx')) if 'unique_cmp' in file]
    a = 0
    for file in unique_files:
        a += 1
        print('=======================')
        print(f'正在处理第{a}个文件,info:', os.path.basename(file))
        print('=======================')
        unique = pd.read_excel(file)
        unique_ms2_match = ms2_matching(unique, database, ms1_error=ms1_error, ms2_error=ms2_error, mode=mode)
        unique_rt_ms2_match = rt_matching(unique_ms2_match, database, ms1_error=ms1_error, rt_error=rt_error,
                                          mode=mode)
        unique_rt_ms2_match.to_excel(file.replace('.xlsx', '_rt_ms2_match.xlsx'))


def database_match2(file, database, ms1_error=50, ms2_error=0.015, rt_error=0.1, mode='pos'):
    """
    Matching for single file
    :param file: single file path
    :param database: database dataframe
    :param ms1_error: ms1 error, ppm
    :param ms2_error: ms2 error, Da
    :param rt_error: retention time, min
    :param mode: pos or neg
    :return: export to file
    """
    unique = pd.read_excel(file)
    unique_ms2_match = ms2_matching(unique, database, ms1_error=ms1_error, ms2_error=ms2_error, mode=mode)
    unique_rt_ms2_match = rt_matching(unique_ms2_match, database, ms1_error=ms1_error, rt_error=rt_error,
                                      mode=mode)

    unique_rt_ms2_match.to_excel(file.replace('.xlsx', '_rt_ms2_match.xlsx'))


def multi_process_database_matching(path, database, processors=5, ms1_error=50, ms2_error=0.015, rt_error=0.1,
                                    mode='pos'):
    """
    Matching compounds in database by using multiprocessing method
    :param path: path for excel
    :param database: database dataframe
    :param processors: processors used
    :param ms1_error: ms1 error in ppm
    :param ms2_error: ms2 error in Da
    :param rt_error: rt error in min
    :param mode: 'pos' or 'neg'
    :return:
    """

    unique_files = [file for file in glob(os.path.join(path, '*.xlsx')) if 'unique_cmp' in file]
    pool = Pool(processes=processors)
    for file in unique_files:
        print(file)
        pool.apply_async(database_match2, args=(file, database, ms1_error, ms2_error, rt_error, mode,))
    print('==========================')
    print('Matching started...')
    print('==========================')
    pool.close()
    pool.join()


def sort_columns_name(columns):
    """
    :param columns: columns need to sort
    :return: new_columns
    """
    final_columns = []
    locators = ['rt', 'mz', 'intensity', 'S/N', 'area', 'area_mean', 'area_std', 'mz_opt',
                'frag_DIA', 'frag_DDA', 'iso_distribution', 'resolution', 'Ciso', 'Cliso', 'Na adducts', 'NH4 adducts',
                'Briso',
                'K adducts',
                'fold_change', 'p_values', 'Control set number', 'Sample set number']
    for name in locators:
        if name in columns:
            final_columns.append(name)
    for name in columns:
        if name not in final_columns:
            final_columns.append(name)
    return final_columns


def PCA_analysis(data):
    """
    :param data: final area data
    :return: PCA dataframe
    """
    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)
    per_var1 = np.round(pca.explained_variance_ratio_ * 100, 1)  # 看看PCA偏差大小
    labels1 = ['PC' + str(x) for x in range(1, len(per_var1) + 1)]
    pca_df = pd.DataFrame(pca_data, index=data.columns.values, columns=labels1)
    return pca_df


def calibration(path, mode='internal'):
    """
    Calibrate using internal or external standard method, must have 'all_area_df.xlsx', 'quan_info.xlsx',
    and 'alignment' files.
    :param path: path for excel files
    :param mode: external or internal
    :return: result dataframe
    """
    print('-----------------------')
    print('Reading files...')
    print('-----------------------')
    files_excel = glob(os.path.join(path, '*.xlsx'))  # 拿到所有excel文件
    area_file = [file for file in files_excel if 'all_area_df' in file][0]  # 拿到所有final_area
    area_df = pd.read_excel(area_file, index_col='Unnamed: 0')
    quan_info_file = [file for file in files_excel if 'quan_info' in file][0]  # 拿到定量信息
    cmp_info = pd.read_excel(quan_info_file)  # 污染物信息
    file_info = pd.read_excel(quan_info_file, sheet_name=1)  # 样品信息
    print('-----------------------')
    print('Processing data...')
    print('-----------------------')
    # 开始处理
    std_df = file_info[file_info['sample_type'] == 'STD']  # 标准品信息
    # 给std_df排序
    one_cmp = [cmp for cmp in std_df.columns.values if (cmp != 'file_name') &
               (cmp != 'ISTD_fold') & (cmp != 'unit') & (cmp != 'sample_type')][0]  # 随机选一个污染物名称
    std_df1 = std_df.sort_values(by=one_cmp, ascending=False)

    # 找到area df，拿到所有的new index,在这里面找new_index去更新标线里面的index
    index_df1 = pd.DataFrame(area_df.index, columns=['index'])
    index_df1['rt'] = index_df1['index'].apply(lambda x: eval(x.split('_')[0]))
    index_df1['mz'] = index_df1['index'].apply(lambda x: eval(x.split('_')[1]))

    # 更新cmp_info的new_index
    for i in range(len(cmp_info)):
        mz, rt = cmp_info.loc[i, ['mz', 'rt']]
        x = index_df1[(index_df1.mz > mz - 0.015) & (index_df1.mz < mz + 0.015) &
                      (index_df1.rt > rt - 0.1) & (index_df1.rt < rt + 0.1)].reset_index(drop=True)
        if len(x) == 0:
            x = index_df1[(index_df1.mz > mz - 0.03) & (index_df1.mz < mz + 0.03) &
                          (index_df1.rt > rt - 0.2) & (index_df1.rt < rt + 0.2)].reset_index(drop=True)
            if len(x) > 1:
                x['error'] = (x['mz'] - mz).abs()
                x1 = x.sort_values(by='error').reset_index(drop=True)
                match_index = x1.iloc[0]['index']
            else:
                match_index = x['index'].values[0]
        elif len(x) == 1:
            match_index = x['index'].values[0]
        elif len(x) > 1:
            x['error'] = (x['mz'] - mz).abs()
            x1 = x.sort_values(by='error').reset_index(drop=True)
            match_index = x.iloc[0]['index']
        cmp_info.loc[i, 'new_index'] = match_index

    # 获得standard的峰面积
    std_indice = cmp_info.new_index
    std_area_df = area_df.loc[std_indice, std_df.file_name]

    if mode.lower() == 'internal':
        for i in range(len(cmp_info)):
            istd_mz, istd_rt = cmp_info.loc[i, ['ISTD_mz', 'ISTD_rt']]
            istd_index = index_df1[(index_df1.mz > istd_mz - 0.05) & (index_df1.mz < istd_mz + 0.05) &
                                   (index_df1.rt > istd_rt - 0.1) & (index_df1.rt < istd_rt + 0.1)].reset_index(
                drop=True).loc[0, 'index']
            cmp_info.loc[i, 'new_index_istd'] = istd_index

        # 获得STD文件中istd的峰面积
        istd_indice = cmp_info.new_index_istd
        istd_area_df = area_df.loc[istd_indice, std_df.file_name]

        # 根据标准曲线求RF
        for i in range(len(cmp_info)):  # 先选择不同的污染物
            RFs = []
            raw_data = []
            istd_conc_raw = cmp_info.loc[i, 'ISTD_conc']
            std_cmp_name = cmp_info.loc[i, 'compound']
            for j in range(len(std_df)):  # 以std_file name 作为索引
                area_sample = std_area_df.iloc[i].loc[std_df.file_name.values[j]]
                area_istd = istd_area_df.iloc[i].loc[std_df.file_name.values[j]]
                std_conc = std_df[std_df['file_name'] == std_df.file_name.values[j]][std_cmp_name].values[0]
                istd_conc = std_df.ISTD_fold.iloc[j] * istd_conc_raw
                RF = (area_sample / area_istd) * (istd_conc / std_conc)
                raw_data.append([area_sample, area_istd, std_conc, istd_conc])
                RFs.append(round(RF, 2))
            RF_mean = round(np.mean(RFs), 2)
            RF_error = round(np.std(RFs) / np.mean(RFs) * 100, 1)
            cmp_info.loc[i, ['RF_mean', 'RF_std']] = RF_mean, RF_error

        # 获得sample文件中sample的area和istd的area
        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df.file_name]  # 样品峰面积
        istd_area_df = area_df.loc[istd_indice, sample_df.file_name]  # 样品峰面积

        # 计算样品
        for i in range(len(sample_area_df.columns)):
            column_name = sample_area_df.columns[i]
            # 开始计算浓度
            for j in range(len(cmp_info)):
                istd_conc = cmp_info.loc[j, 'ISTD_conc']
                area_sample = sample_area_df.iloc[j].loc[column_name]
                area_istd = istd_area_df.iloc[j].loc[column_name]
                RF = cmp_info.loc[j, 'RF_mean']
                cmp_info.loc[j, column_name] = round((area_sample / area_istd) * (istd_conc / RF), 2)
        final_result = cmp_info

    else:
        # 开始外标法
        external_std_df = pd.concat([cmp_info, std_area_df.reset_index(drop=True)], axis=1)  # 二者合并
        for i in range(len(external_std_df)):
            cmp_index = external_std_df.loc[i, 'compound']
            conc = std_df1.loc[:, cmp_index]  # 在这里改浓度
            area = external_std_df.loc[i, std_df1.file_name].values.astype(float)
            slope, intercept, r_value, p_value, std_err = st.linregress(area, conc)
            name = 'cmp' + str(i)
            locals()[name] = [slope, intercept, r_value ** 2]
            external_std_df.loc[i, ['slop', 'intercept', 'R2']] = [slope, intercept, r_value ** 2]

        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df.file_name]  # 样品峰面积
        # 计算标线斜率和截距
        for i in range(len(sample_area_df)):
            name = 'cmp' + str(i)
            area1 = sample_area_df.iloc[i, :].values
            c = locals()[name][0] * area1 + locals()[name][1]
            sample_area_df.iloc[i, :] = c
        final_result = pd.concat([external_std_df, sample_area_df.round(3).reset_index(drop=True)], axis=1)

    # 将unique_cmp没有筛查出来的数据移除
    unique_files = [file for file in files_excel if 'unique_cmp' in file]
    unique_file_names = [os.path.basename(i).split('_unique_cmps')[0] for i in unique_files]
    path_s1 = pd.Series(data=unique_files, index=unique_file_names)
    final_result.index = final_result['new_index']
    std_index = final_result['new_index'].values
    for name in tqdm(final_result.columns):
        if name in path_s1.index.values:
            df_unique = pd.read_excel(path_s1.loc[name])
            unique_info = pd.DataFrame(np.array([df_unique.rt.values, df_unique.mz.values]).T, columns=['rt', 'mz'])
            set_0_index = []
            for index in std_index:
                rt, mz = index.split('_')
                rt = eval(rt)
                mz = eval(mz)
                result1 = unique_info[(unique_info.rt < rt + 0.1)
                                      & (unique_info.rt > rt - 0.1)
                                      & (unique_info.mz < mz + 0.015)
                                      & (unique_info.mz > mz - 0.015)]
                if len(result1) == 0:
                    set_0_index.append(index)
                else:
                    pass
            final_result.loc[set_0_index, name] = np.nan
    return final_result


def calibration2(path, mode='internal'):
    """
    Calibrate using internal or external standard method, must have 'all_area_df.xlsx', 'quan_info.xlsx',
    and 'alignment' files.
    :param path: path for excel files
    :param mode: external or internal
    :return: result dataframe
    """
    print('-----------------------')
    print('Reading files...')
    print('-----------------------')
    files_excel = glob(os.path.join(path, '*.xlsx'))  # 拿到所有excel文件
    area_file = [file for file in files_excel if 'all_area_df' in file][0]  # 拿到所有final_area
    unique_files = [file for file in files_excel if 'unique_cmp' in file]  # 拿到所有final_area
    area_df = pd.read_excel(area_file, index_col='Unnamed: 0')
    quan_info_file = [file for file in files_excel if 'quan_info' in file][0]  # 拿到定量信息
    cmp_info = pd.read_excel(quan_info_file)  # 污染物信息
    file_info = pd.read_excel(quan_info_file, sheet_name=1)  # 样品信息
    print('-----------------------')
    print('Processing data...')
    print('-----------------------')
    # 开始处理
    std_df = file_info[file_info['sample_type'] == 'STD']  # 标准品信息
    # 给std_df排序
    one_cmp = [cmp for cmp in std_df.columns.values if (cmp != 'file_name') &
               (cmp != 'ISTD_fold') & (cmp != 'unit') & (cmp != 'sample_type')][0]  # 随机选一个污染物名称
    std_df1 = std_df.sort_values(by=one_cmp, ascending=False)

    # 找到area df，拿到所有的new index,在这里面找new_index去更新标线里面的index
    index_df1 = pd.DataFrame(area_df.index, columns=['index'])
    index_df1['rt'] = index_df1['index'].apply(lambda x: eval(x.split('_')[0]))
    index_df1['mz'] = index_df1['index'].apply(lambda x: eval(x.split('_')[1]))

    # 更新cmp_info的new_index
    for i in range(len(cmp_info)):
        mz, rt = cmp_info.loc[i, ['mz', 'rt']]
        x = index_df1[(index_df1.mz > mz - 0.015) & (index_df1.mz < mz + 0.015) &
                      (index_df1.rt > rt - 0.1) & (index_df1.rt < rt + 0.1)].reset_index(drop=True)
        if len(x) == 0:
            x = index_df1[(index_df1.mz > mz - 0.03) & (index_df1.mz < mz + 0.03) &
                          (index_df1.rt > rt - 0.2) & (index_df1.rt < rt + 0.2)].reset_index(drop=True)
            if len(x) > 1:
                x['error'] = (x['mz'] - mz).abs()
                x1 = x.sort_values(by='error').reset_index(drop=True)
                match_index = x1.iloc[0]['index']
            elif len(x) ==1:
                match_index = x['index'].values[0]
            else:
                match_index = np.nan
        elif len(x) == 1:
            match_index = x['index'].values[0]
        elif len(x) > 1:
            x['error'] = (x['mz'] - mz).abs()
            x1 = x.sort_values(by='error').reset_index(drop=True)
            match_index = x.iloc[0]['index']
        cmp_info.loc[i, 'new_index'] = match_index
    cmp_info = cmp_info[~cmp_info['new_index'].isna()].reset_index(drop=True)

    # 获得standard的峰面积
    std_indice = cmp_info.new_index
    std_area_df = area_df.loc[std_indice, std_df.file_name]

    if mode.lower() == 'internal':
        for i in range(len(cmp_info)):
            istd_mz, istd_rt = cmp_info.loc[i, ['ISTD_mz', 'ISTD_rt']]
            istd_index = index_df1[(index_df1.mz > istd_mz - 0.05) & (index_df1.mz < istd_mz + 0.05) &
                                   (index_df1.rt > istd_rt - 0.1) & (index_df1.rt < istd_rt + 0.1)].reset_index(
                drop=True).loc[0, 'index']
            cmp_info.loc[i, 'new_index_istd'] = istd_index

        # 获得STD文件中istd的峰面积
        istd_indice = cmp_info.new_index_istd
        istd_area_df = area_df.loc[istd_indice, std_df.file_name]

        # 根据标准曲线求RF
        for i in range(len(cmp_info)):  # 先选择不同的污染物
            RFs = []
            raw_data = []
            istd_conc_raw = cmp_info.loc[i, 'ISTD_conc']
            std_cmp_name = cmp_info.loc[i, 'compound']
            for j in range(len(std_df)):  # 以std_file name 作为索引
                area_sample = std_area_df.iloc[i].loc[std_df.file_name.values[j]]
                area_istd = istd_area_df.iloc[i].loc[std_df.file_name.values[j]]
                std_conc = std_df[std_df['file_name'] == std_df.file_name.values[j]][std_cmp_name].values[0]
                istd_conc = std_df.ISTD_fold.iloc[j] * istd_conc_raw
                RF = (area_sample / area_istd) * (istd_conc / std_conc)
                raw_data.append([area_sample, area_istd, std_conc, istd_conc])
                RFs.append(round(RF, 2))
            RF_mean = round(np.mean(RFs), 2)
            RF_error = round(np.std(RFs) / np.mean(RFs) * 100, 1)
            cmp_info.loc[i, ['RF_mean', 'RF_std']] = RF_mean, RF_error

        # 获得sample文件中sample的area和istd的area
        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积
        istd_area_df = area_df.loc[istd_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积

        # 计算样品
        for i in range(len(sample_area_df.columns)):
            column_name = sample_area_df.columns[i]
            # 开始计算浓度
            for j in range(len(cmp_info)):
                istd_conc = cmp_info.loc[j, 'ISTD_conc']
                area_sample = sample_area_df.iloc[j].loc[column_name]
                area_istd = istd_area_df.iloc[j].loc[column_name]
                RF = cmp_info.loc[j, 'RF_mean']
                cmp_info.loc[j, column_name] = round((area_sample / area_istd) * (istd_conc / RF), 2)
        final_result = cmp_info

    else:
        # 开始外标法
        external_std_df = pd.concat([cmp_info, std_area_df.reset_index(drop=True)], axis=1)  # 二者合并
        for i in range(len(external_std_df)):
            cmp_index = external_std_df.loc[i, 'compound']
            conc = std_df1.loc[:, cmp_index]  # 在这里改浓度
            area = external_std_df.loc[i, std_df1.file_name].values.astype(float)
            slope, intercept, r_value, p_value, std_err = st.linregress(area, conc)
            name = 'cmp' + str(i)
            locals()[name] = [slope, intercept, r_value ** 2]
            external_std_df.loc[i, ['slop', 'intercept', 'R2']] = [slope, intercept, r_value ** 2]

        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df.file_name]  # 样品峰面积
        # 计算标线斜率和截距
        for i in range(len(sample_area_df)):
            name = 'cmp' + str(i)
            area1 = sample_area_df.iloc[i, :].values
            c = locals()[name][0] * area1 + locals()[name][1]
            sample_area_df.iloc[i, :] = c
        final_result = pd.concat([external_std_df, sample_area_df.round(3).reset_index(drop=True)], axis=1)

    # 将unique_cmp没有筛查出来的数据移除
    unique_files = [file for file in files_excel if 'unique_cmp' in file]
    unique_file_names = [os.path.basename(i).split('_unique_cmps')[0] for i in unique_files]
    path_s1 = pd.Series(data=unique_files, index=unique_file_names)
    final_result.index = final_result['new_index']
    std_index = final_result['new_index'].values
    for name in tqdm(final_result.columns):
        if name in path_s1.index.values:
            df_unique = pd.read_excel(path_s1.loc[name])
            unique_info = pd.DataFrame(np.array([df_unique.rt.values, df_unique.mz.values]).T, columns=['rt', 'mz'])
            set_0_index = []
            for index in std_index:
                rt, mz = index.split('_')
                rt = eval(rt)
                mz = eval(mz)
                result1 = unique_info[(unique_info.rt < rt + 0.1)
                                      & (unique_info.rt > rt - 0.1)
                                      & (unique_info.mz < mz + 0.015)
                                      & (unique_info.mz > mz - 0.015)]
                if len(result1) == 0:
                    set_0_index.append(index)
                else:
                    pass
            final_result.loc[set_0_index, name] = np.nan
    return final_result

def calibration3(path, mode='internal'):
    """
    Calibrate using internal or external standard method, must have 'all_area_df.xlsx', 'quan_info.xlsx',
    and 'alignment' files.
    :param path: path for excel files
    :param mode: external or internal
    :return: result dataframe 
    """
    # 测试使用，2如果可以用就删除
    print('-----------------------')
    print('Reading files...')
    print('-----------------------')
    files_excel = glob(os.path.join(path, '*.xlsx'))  # 拿到所有excel文件
    area_file = [file for file in files_excel if 'all_area_df' in file][0]  # 拿到所有final_area
    unique_files = [file for file in files_excel if 'unique_cmp' in file]  # 拿到所有final_area
    area_df = pd.read_excel(area_file, index_col='Unnamed: 0')
    quan_info_file = [file for file in files_excel if 'quan_info' in file][0]  # 拿到定量信息
    cmp_info = pd.read_excel(quan_info_file)  # 污染物信息
    file_info = pd.read_excel(quan_info_file, sheet_name=1)  # 样品信息
    print('-----------------------')
    print('Processing data...')
    print('-----------------------')
    # 开始处理
    std_df = file_info[file_info['sample_type'] == 'STD']  # 标准品信息
    # 给std_df排序
    one_cmp = [cmp for cmp in std_df.columns.values if (cmp != 'file_name') &
               (cmp != 'ISTD_fold') & (cmp != 'unit') & (cmp != 'sample_type')][0]  # 随机选一个污染物名称
    std_df1 = std_df.sort_values(by=one_cmp, ascending=False)

    # 找到area df，拿到所有的new index,在这里面找new_index去更新标线里面的index
    index_df1 = pd.DataFrame(area_df.index, columns=['index'])
    index_df1['rt'] = index_df1['index'].apply(lambda x: eval(x.split('_')[0]))
    index_df1['mz'] = index_df1['index'].apply(lambda x: eval(x.split('_')[1]))

    # 更新cmp_info的new_index
    for i in range(len(cmp_info)):
        mz, rt = cmp_info.loc[i, ['mz', 'rt']]
        x = index_df1[(index_df1.mz > mz - 0.015) & (index_df1.mz < mz + 0.015) &
                      (index_df1.rt > rt - 0.1) & (index_df1.rt < rt + 0.1)].reset_index(drop=True)
        if len(x) == 0:
            x = index_df1[(index_df1.mz > mz - 0.03) & (index_df1.mz < mz + 0.03) &
                          (index_df1.rt > rt - 0.2) & (index_df1.rt < rt + 0.2)].reset_index(drop=True)
            if len(x) > 1:
                x['error'] = (x['mz'] - mz).abs()
                x1 = x.sort_values(by='error').reset_index(drop=True)
                match_index = x1.iloc[0]['index']
            elif len(x) ==1:
                match_index = x['index'].values[0]
            else:
                match_index = np.nan
        elif len(x) == 1:
            match_index = x['index'].values[0]
        elif len(x) > 1:
            x['error'] = (x['mz'] - mz).abs()
            x1 = x.sort_values(by='error').reset_index(drop=True)
            match_index = x.iloc[0]['index']
        cmp_info.loc[i, 'new_index'] = match_index
    cmp_info = cmp_info[~cmp_info['new_index'].isna()].reset_index(drop=True)

    # 获得standard的峰面积
    std_indice = cmp_info.new_index
    std_area_df = area_df.loc[std_indice, std_df.file_name]

    if mode.lower() == 'internal':
        for i in range(len(cmp_info)):
            istd_mz, istd_rt = cmp_info.loc[i, ['ISTD_mz', 'ISTD_rt']]
            istd_index = index_df1[(index_df1.mz > istd_mz - 0.05) & (index_df1.mz < istd_mz + 0.05) &
                                   (index_df1.rt > istd_rt - 0.1) & (index_df1.rt < istd_rt + 0.1)].reset_index(
                drop=True).loc[0, 'index']
            cmp_info.loc[i, 'new_index_istd'] = istd_index

        # 获得STD文件中istd的峰面积
        istd_indice = cmp_info.new_index_istd
        istd_area_df = area_df.loc[istd_indice, std_df.file_name]

        # 根据标准曲线求RF
        for i in range(len(cmp_info)):  # 先选择不同的污染物
            RFs = []
            raw_data = []
            istd_conc_raw = cmp_info.loc[i, 'ISTD_conc']
            std_cmp_name = cmp_info.loc[i, 'compound']
            for j in range(len(std_df)):  # 以std_file name 作为索引
                area_sample = std_area_df.iloc[i].loc[std_df.file_name.values[j]]
                area_istd = istd_area_df.iloc[i].loc[std_df.file_name.values[j]]
                std_conc = std_df[std_df['file_name'] == std_df.file_name.values[j]][std_cmp_name].values[0]
                istd_conc = std_df.ISTD_fold.iloc[j] * istd_conc_raw
                RF = (area_sample / area_istd) * (istd_conc / std_conc)
                raw_data.append([area_sample, area_istd, std_conc, istd_conc])
                RFs.append(round(RF, 2))
            RF_mean = round(np.mean(RFs), 2)
            RF_error = round(np.std(RFs) / np.mean(RFs) * 100, 1)
            cmp_info.loc[i, ['RF_mean', 'RF_std']] = RF_mean, RF_error

        # 获得sample文件中sample的area和istd的area
        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积
        istd_area_df = area_df.loc[istd_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积

        # 计算样品
        for i in range(len(sample_area_df.columns)):
            column_name = sample_area_df.columns[i]
            # 开始计算浓度
            for j in range(len(cmp_info)):
                istd_conc = cmp_info.loc[j, 'ISTD_conc']
                area_sample = sample_area_df.iloc[j].loc[column_name]
                area_istd = istd_area_df.iloc[j].loc[column_name]
                RF = cmp_info.loc[j, 'RF_mean']
                cmp_info.loc[j, column_name] = round((area_sample / area_istd) * (istd_conc / RF), 2)
        final_result = cmp_info

    else:
        # 开始外标法
        external_std_df = pd.concat([cmp_info, std_area_df.reset_index(drop=True)], axis=1)  # 二者合并
        for i in range(len(external_std_df)):
            cmp_index = external_std_df.loc[i, 'compound']
            conc = std_df1.loc[:, cmp_index]  # 在这里改浓度
            area = external_std_df.loc[i, std_df1.file_name].values.astype(float)
            slope, intercept, r_value, p_value, std_err = st.linregress(area, conc)
            name = 'cmp' + str(i)
            locals()[name] = [slope, intercept, r_value ** 2]
            external_std_df.loc[i, ['slop', 'intercept', 'R2']] = [slope, intercept, r_value ** 2]

        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df.file_name]  # 样品峰面积
        # 计算标线斜率和截距
        for i in range(len(sample_area_df)):
            name = 'cmp' + str(i)
            area1 = sample_area_df.iloc[i, :].values
            c = locals()[name][0] * area1 + locals()[name][1]
            sample_area_df.iloc[i, :] = c
        final_result = pd.concat([external_std_df, sample_area_df.round(3).reset_index(drop=True)], axis=1)

    # 将unique_cmp没有筛查出来的数据移除
    unique_files = [file for file in files_excel if 'unique_cmp' in file]
    unique_file_names = [os.path.basename(i).split('_unique_cmps')[0] for i in unique_files]
    path_s1 = pd.Series(data=unique_files, index=unique_file_names)
    final_result.index = final_result['new_index']
    std_index = final_result['new_index'].values
    for name in tqdm(final_result.columns):
        if name in path_s1.index.values:
            df_unique = pd.read_excel(path_s1.loc[name])
            unique_info = pd.DataFrame(np.array([df_unique.rt.values, df_unique.mz.values]).T, columns=['rt', 'mz'])
            set_0_index = []
            for index in std_index:
                rt, mz = index.split('_')
                rt = eval(rt)
                mz = eval(mz)
                result1 = unique_info[(unique_info.rt < rt + 0.1)
                                      & (unique_info.rt > rt - 0.1)
                                      & (unique_info.mz < mz + 0.015)
                                      & (unique_info.mz > mz - 0.015)]
                if len(result1) == 0:
                    set_0_index.append(index)
                else:
                    pass
            final_result.loc[set_0_index, name] = np.nan
    return final_result



def summarize_frag(db1, mode, source, source_info):
    """
    For massbank database, summarize all fragments and combine them together.
    :param db1: database1
    :param mode: pos or neg
    :param source: comment
    :param source_info:  comment
    :return: result dataframe
    """
    iks = list(set(db1['Inchikey'].values))  # 拿到所有的iks
    all_final_s = []
    massbank_pos = pd.DataFrame()
    for ik in tqdm(iks):
        db2 = db1[db1['Inchikey'] == ik]
        mz = db2['Precursor'].iloc[0]
        formula = db2['Formula'].iloc[0]
        smile = db2['Smiles'].iloc[0]
        all_series = []
        for dict1 in db2['Frag'].values:
            s1 = pd.Series(eval(dict1))
            all_series.append(s1)
        s_all = pd.concat(all_series)
        s_all1 = s_all[s_all.index < mz - 5]
        if len(s_all1) == 0:
            frag = []
        else:
            frag = list(set(s_all1[s_all1 > 50].index.values))
            if len(frag) < 3:
                frag = list(set(s_all1[s_all1 > 20].index.values))
        final_s = pd.Series({'Inchikey': ik, 'Precursor': mz, 'Frag': frag, 'Formula': formula, 'Smiles': smile})
        all_final_s.append(final_s)
        massbank_pos = pd.concat(all_final_s, axis=1).T
        massbank_pos['mode'] = mode
        massbank_pos['Source'] = source
        massbank_pos['Source info'] = source_info
    return massbank_pos


def parent_tp_analysis(file):
    cmp_result = pd.read_excel(file)
    if 'frag_DDA' in cmp_result.columns.values:
        DDA_result = [np.array(eval(i)) for i in cmp_result.frag_DDA]
        DDA_index = [n for n, i in enumerate(cmp_result.frag_DDA) if len(eval(i)) > 0]
        if len(DDA_index) == 0:
            pass
        else:
            a = itertools.combinations(DDA_index, 2)
            t = [list(i) for i in a]
            level1_2_index = cmp_result[(~(cmp_result['best_results_DDA']  # 只考虑有定性结果的，level1，level2，level3
                                           == '[]')) | (~(cmp_result['rt_match_result'] == '[]'))].index
            t = [i for i in t if (i[0] in level1_2_index) | (i[1] in level1_2_index)]
            compare_result = [compare_frag(DDA_result[t[i][0]], DDA_result[t[i][1]]) for i in
                              range(len(t))]  # 比较所有可能DDA
            nums = [len(s) for s in compare_result]  # 比较每种可能性
            # 开始建立dataframe
            result_df = pd.DataFrame(data=t)
            result_df.columns = ['cmp1', 'cmp2']
            result_df.cmp1 = cmp_result.new_index.loc[result_df.cmp1.values].values
            result_df.cmp2 = cmp_result.new_index.loc[result_df.cmp2.values].values
            result_df['same_frag_num'] = nums
            result_df['frag_info'] = [str(a.round(4).to_dict()) for a in compare_result]
            result_df = result_df[result_df.same_frag_num > 0]
            result_df = result_df.sort_values(by='same_frag_num', ascending=False).reset_index(drop=True)
            # 开始标注每一个化合物的分级
            index1 = list(set(np.hstack([result_df['cmp1'].values, result_df['cmp2'].values])))  # 将所有index合并
            level = []
            # 对index进行分级
            for index in index1:
                df_index = cmp_result[cmp_result['new_index'] == index]
                if (df_index['rt_match_result'].values != '[]') & (df_index['best_results_DDA'].values != '[]'):
                    level.append(1)
                elif (df_index['rt_match_result'].values != '[]') & (df_index['best_results_DDA'].values == '[]'):
                    level.append(3)
                elif (df_index['rt_match_result'].values == '[]') & (df_index['best_results_DDA'].values != '[]'):
                    level.append(2)
                else:
                    level.append(None)
            s2 = pd.Series(level, index1)
            for i in range(len(result_df)):
                cmp1_index, cmp2_index = result_df.loc[i, 'cmp1'], result_df.loc[i, 'cmp2']
                result_df.loc[i, 'cmp1_level'] = s2.loc[cmp1_index]
                result_df.loc[i, 'cmp2_level'] = s2.loc[cmp2_index]
            result_df = result_df.loc[:, ['cmp1', 'cmp1_level', 'cmp2', 'cmp2_level', 'same_frag_num', 'frag_info']]
            with ExcelWriter(file) as writer:
                cmp_result.to_excel(writer, sheet_name='Original Data')
                result_df.to_excel(writer, sheet_name='DDA_parent_products_analysis')


def isotope_distribution(spec1, mz, error=0.02):
    """
    :param df1:  centroid dataframe
    :param rt:  retention time
    :param mz: mass
    :param error: mass error
    :return: iso_info
    """
    spec2 = spec1[spec1 > 0]
    spec3 = spec2[(spec2.index > mz - 5) & (spec2.index < mz + 5)]
    mz_s = spec3[(spec3.index > mz - error) * (spec3.index < mz + error)].sort_values().iloc[-1:]
    mz__1 = spec3[(spec3.index > mz - 1 - error) * (spec3.index < mz - 1 + error)].sort_values().iloc[-1:]
    mz__2 = spec3[(spec3.index > mz - 2 - error) * (spec3.index < mz - 2 + error)].sort_values().iloc[-1:]
    mz__3 = spec3[(spec3.index > mz - 3 - error) * (spec3.index < mz - 3 + error)].sort_values().iloc[-1:]
    mz__4 = spec3[(spec3.index > mz - 4 - error) * (spec3.index < mz - 4 + error)].sort_values().iloc[-1:]
    mz_1 = spec3[(spec3.index > mz + 1 - error) * (spec3.index < mz + 1 + error)].sort_values().iloc[-1:]
    mz_2 = spec3[(spec3.index > mz + 2 - error) * (spec3.index < mz + 2 + error)].sort_values().iloc[-1:]
    mz_3 = spec3[(spec3.index > mz + 3 - error) * (spec3.index < mz + 3 + error)].sort_values().iloc[-1:]
    mz_4 = spec3[(spec3.index > mz + 4 - error) * (spec3.index < mz + 4 + error)].sort_values().iloc[-1:]
    x = [mz_s, mz__1, mz__2, mz__3, mz__4, mz_1, mz_2, mz_3, mz_4]
    iso_info_s = pd.concat([i for i in x if len(x) != 0])
    if len(iso_info_s) == 0:
        return {}
    else:
        iso_info_s1 = (iso_info_s / iso_info_s.values.max()).sort_index().round(3)
        iso_info_s2 = iso_info_s1[iso_info_s1 > 0.015].to_dict()
        return iso_info_s2


def isotope_matching(iso_info, formula):
    """
    :param iso_info: isotope distribution infor in a dict
    :param formula: formula
    :return: a dataframe
    """
    isotopes, distribution = formula_to_distribution(formula, num=5)
    s_obs = pd.Series(iso_info)
    a = sorted(np.hstack([isotopes, s_obs.index]))  # 所有的质量放一起
    if len(a) > 1:
        b = [a[0] if abs(a[1] - a[0]) > 0.015 else a[0]] + [a[i + 1] for i in range(len(a) - 1) if
                                                            abs(a[i] - a[i + 1]) > 0.015]
    else:
        b = a  # b为alignment之后的质量
    # expected isotope info
    df_exp = pd.DataFrame(index=[b[argmin(abs(b - x))] for x in isotopes],
                          data=np.vstack([isotopes, distribution / 100]).T,
                          columns=['mz_exp', 'exp_distribution'])
    # observed isotope info
    df_obs = pd.DataFrame(index=[b[argmin(abs(b - x))] for x in s_obs.index.values],
                          data=np.vstack([s_obs.index.values, s_obs.values]).T,
                          columns=['mz_obs', 'obs_distribution'])
    compare_result = pd.concat([df_exp, df_obs], axis=1)
    compare_result = compare_result[~compare_result.mz_exp.isna()].fillna(0)
    compare_result['dis_diff'] = abs(compare_result.exp_distribution - compare_result.obs_distribution)
    compare_result['mz_diff'] = abs(compare_result.mz_exp - compare_result.mz_obs)
    return compare_result


def split_peak_picking(ms1, profile=True, split_n=20, threshold=15, i_threshold=500,
                       SN_threshold=3, noise_threshold=0, rt_error_alignment=0.05,
                       mz_error_alignment=0.015):
    def target_spec1(spec, target_mz, width=0.04):
        """
        :param spec: spec generated from function spec_at_rt()
        :param target_mz: target mz for inspection
        :param width: width for data points
        :return: new spec and observed mz
        """
        index_left = argmin(abs(spec.index.values - (target_mz - width)))
        index_right = argmin(abs(spec.index.values - (target_mz + width)))
        new_spec = spec.iloc[index_left:index_right].copy()
        new_spec[target_mz - width] = 0
        new_spec[target_mz + width] = 0
        new_spec = new_spec.sort_index()
        return new_spec

    t1 = time.time()
    if profile is True:
        peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]] for i in range(len(ms1))]
        raw_info_centroid = {
            round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(4),
                                                     name=round(ms1[i].scan_time[0], 3)) for i, peaks in peaks_index}
        raw_info_profile = {round(ms1[i].scan_time[0], 3):
                                pd.Series(data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3))
                            for i in range(len(ms1))}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]
    else:
        raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
            data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3)) for i in
            range(len(ms1))}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]

    t2 = time.time()
    time1 = round(t2 - t1, 0)
    print(f'Reading data: {time1}')

    # 开始分割
    # 定义变量名称
    all_data = []
    for j in range(split_n):
        name = 'a' + str(j + 1)
        locals()[name] = []
    # 对series进行切割
    ms_increase = int(1000 / split_n)
    for i in tqdm(range(len(data)), desc='Split series:'):
        s1 = data[i]
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            name = 'a' + str(j + 1)
            locals()[name].append(s1[(s1.index < high) & (s1.index >= low) & (s1.index > noise_threshold)])
            low += ms_increase
            high += ms_increase
    for j in range(split_n):
        name = 'a' + str(j + 1)
        all_data.append(locals()[name])

    # 开始分段提取
    all_peak_all = []
    for i, data in enumerate(all_data):
        df1 = pd.concat(data, axis=1)
        df1 = df1.fillna(0)
        if len(df1) == 0:
            pass
        else:
            peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold,
                                    i_threshold=i_threshold, SN_threshold=SN_threshold,
                                    rt_error_alignment=rt_error_alignment,
                                    mz_error_alignment=mz_error_alignment)
            all_peak_all.append(peak_all)
        print(f'\r Processing {i + 1}/{20} df1                  ', end='')

    peak_all = pd.concat(all_peak_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)

    # 对同位素丰度进行记录
    raw_info_rts = [v.name for k, v in raw_info_centroid.items()]
    rts = peak_all.rt.values
    mzs = peak_all.mz.values
    rt_keys = [raw_info_rts[argmin(abs(np.array(raw_info_rts) - i))] for i in rts]  # 基于上述rt找到ms的时间索引

    iso_info = [str(isotope_distribution(raw_info_centroid[rt_keys[i]], mzs[i])) for i in range(len(mzs))]
    peak_all['iso_distribution'] = iso_info

    # 更新质量数据
    if profile is True:
        spec1 = [raw_info_profile[i] for i in rt_keys]  # 获得ms的spec
        mz_result = np.array(
            [list(evaluate_ms(target_spec1(spec1[i], mzs[i], width=0.04).copy(), mzs[i])) for i in range(len(mzs))]).T
        mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
        mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else mzs[i] for i in range(len(mzs))]  # 去掉偏差大的矫正结果

        peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
        t2 = time.time()
        print(f'\r Optimized time: {round(t2 - t1, 0)} s     ', end='')
    else:
        spec1 = [raw_info_centroid[i] for i in rt_keys]  # 获得ms的spec
        target_spec = [spec1[i][(spec1[i].index > mzs[i] - 0.015) & (spec1[i].index < mzs[i] + 0.015)] for i in
                       range(len(spec1))]
        mzs_obs = [target_spec[i].index.values[[np.argmax(target_spec[i].values)]][0] for i in range(len(target_spec))]
        peak_all['mz'] = mzs_obs
    return peak_all


def peak_checking_area_split(ref_all, ms1, company, name1, profile=True, split_n=20, noise_threshold=0):
    # 需要给ref_all排序
    ref_all1 = ref_all.sort_values(by='mz')

    if profile is True:
        peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]] for i in range(len(ms1))]
        raw_info_centroid = {
            round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(4),
                                                     name=round(ms1[i].scan_time[0], 3)) for i, peaks in peaks_index}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]
    else:
        raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
            data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3)) for i in
            range(len(ms1))}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]

    # 开始分割 series数据
    # 定义变量名称
    all_data = []
    for j in range(split_n):
        name = 'a' + str(j + 1)
        locals()[name] = []
    # 对series进行切割
    ms_increase = int(1000 / split_n)
    for i in tqdm(range(len(data)), desc='Split series:'):
        s1 = data[i]
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            name = 'a' + str(j + 1)
            locals()[name].append(s1[(s1.index < high + 0.1) & (s1.index >= low - 0.1) & (s1.index > noise_threshold)])
            low += ms_increase
            high += ms_increase
    for j in range(split_n):
        name = 'a' + str(j + 1)
        all_data.append(locals()[name])

    # 开始分割peak_ref
    all_peak_ref = []
    # 对peak_ref进行切割
    ms_increase = int(1000 / split_n)
    low, high = 50, 50 + ms_increase
    for j in range(split_n):
        name = 'b' + str(j + 1)
        locals()[name] = ref_all1[(ref_all1.mz < high) & (ref_all1.mz >= low)]
        low += ms_increase
        high += ms_increase
        all_peak_ref.append(locals()[name])

    # 获取所有area
    area_all = []
    for i in tqdm(range(split_n)):
        peak_ref1 = all_peak_ref[i]
        df1 = pd.concat(all_data[i], axis=1)
        df1 = df1.fillna(0)
        df_area = peak_checking_area(peak_ref1, df1, 'split')
        area_all.append(df_area)

    # 合成所有的area
    final_df = pd.concat(area_all)
    final_df.columns = [name1]
    return final_df


def gen_DDA_ms2_df(path, company, i_threhold=0, profile=True, opt=True):
    """
    :param path: path for single file
    :param profile: True or false
    :param path: DDA mzml file path
    :return: DataFrame with rt, precursor and fragments info
    """
    ms1, ms2 = sep_scans(path, company)
    precursors, rts, frags, intensities, collision_energies, modes, scan_indices = [], [], [], [], [], [], []
    for i, scan in enumerate(ms2):
        precursor = scan.selected_precursors[0]['mz']
        precursors.append(precursor)
        # append rt
        rt = round(scan.scan_time[0], 3)
        rts.append(rt)
        # append collision energy
        collision_energy = scan['collision energy']
        collision_energies.append(collision_energy)
        scan_indices.append(i)
        # append modes
        if scan['negative scan'] is True:
            modes.append('neg')
        elif scan['positive scan'] is True:
            modes.append('pos')
        else:
            modes.append('Unkonwn')
        mz = scan.mz
        intensity = scan.i
        if profile is True:
            spec = pd.Series(data=intensity, index=mz)
            new_spec = ms_to_centroid(spec)
            mz = new_spec.index.values
            intensity = new_spec.values
        else:
            pass

        s = pd.Series(data=intensity, index=mz).sort_values(ascending=False).iloc[:20]
        s = s[s > i_threhold]
        frag = list(s.index.values.round(4))
        frags.append(frag)
        intensities.append(list(s.values))

    DDA_df = pd.DataFrame([precursors, rts, collision_energies, frags, intensities, modes, scan_indices],
                          index=['precursor', 'rt', 'collision energy', 'frag', 'intensity', 'mode', 'scan_index']).T

    if profile == False:
        pass
    else:
        if opt == False:
            pass
        else:
            mz_opt_all = []
            for i in tqdm(range(len(DDA_df)), desc='Optimizing mass'):
                frag = DDA_df.loc[i].frag
                x = DDA_df.loc[i].scan_index
                s1 = pd.Series(ms2[x].i, ms2[x].mz.round(4))
                mz_opt = [evaluate_ms(target_spec(s1, mz), mz)[2] for mz in frag]
                mz_opt_all.append(mz_opt)

            DDA_df['frag_opt'] = mz_opt_all
    return DDA_df


def spectra_plot(DDA_df1, mz_num=3, name='', path=None, show=True, dpi=500):
    """
    :param DDA_df1: targeted DDA_df
    :param mz_num: number of shown mass
    :param name:  name for compound
    :param path:  path to save
    :param show: shown in jupyter notebook
    :param dpi: dot per inch
    :return:
    """
    if len(DDA_df1) == 0:
        pass
    elif (len(DDA_df1) <= 6) & (len(DDA_df1) > 0):
        precursor = DDA_df1.precursor.values[0]
        c1, c2, c3, *_ = DDA_df1['collision energy'].values
        mzs1 = DDA_df1[DDA_df1['collision energy'] == c1].frag_opt.values[0]
        intensity1 = DDA_df1[DDA_df1['collision energy'] == c1].intensity.values[0]
        rt1 = DDA_df1[DDA_df1['collision energy'] == c1].rt.values
        mzs2 = DDA_df1[DDA_df1['collision energy'] == c2].frag_opt.values[0]
        intensity2 = DDA_df1[DDA_df1['collision energy'] == c2].intensity.values[0]
        rt2 = DDA_df1[DDA_df1['collision energy'] == c2].rt.values
        mzs3 = DDA_df1[DDA_df1['collision energy'] == c3].frag_opt.values[0]
        intensity3 = DDA_df1[DDA_df1['collision energy'] == c3].intensity.values[0]
        rt3 = DDA_df1[DDA_df1['collision energy'] == c3].rt.values

        fig = plt.figure(figsize=(10, 10))
        plt.rc('font', family='Times New Roman')

        # 第一个图
        ax1 = fig.add_subplot(311)
        ax1.bar(mzs1, intensity1)
        ax1.set_title(f'Compound info: {name}', fontsize=15, loc='left')
        arr1 = np.array(mzs1)  # 转成array
        arr2 = np.array(intensity1)
        # 画出来precursor的点
        index_ = np.argwhere((arr1 > precursor - 0.015) & (arr1 < precursor + 0.015))  # 找到index
        if len(index_) != 0:
            index = index_[0][0]
            ax1.scatter(precursor, intensity1[index] * 1.1, c='r', marker='D', s=10)
        else:
            ax1.scatter(precursor, 0, c='r', marker='D', s=10)
        # 标注出质量
        s1 = pd.Series(arr2, arr1).sort_values(ascending=False).head(mz_num)
        highest_3 = np.array([s1.index.values, s1.values]).T
        for i in range(mz_num):
            ax1.text(highest_3[i][0], highest_3[i][1], highest_3[i][0], size=11)
        ax1.set_ylabel('Intensity', fontsize=15)  # 设置y_label大小
        ax1.set_ylim(0, max(intensity1) * 1.2)
        ax1.set_xlim(50, precursor * 1.2)
        ax1.set_title(f'+ESI scan (rt: {rt1} min), Frag = 135.0 V, CID@{c1} V ({round(precursor, 4)}[z=1] -> **)',
                      loc='right', size=10)

        # 画第二个图
        ax2 = fig.add_subplot(312)
        ax2.bar(mzs2, intensity2)
        arr1 = np.array(mzs2)  # 转成array
        arr2 = np.array(intensity2)
        # 画出来precursor的点
        index_ = np.argwhere((arr1 > precursor - 0.015) & (arr1 < precursor + 0.015))  # 找到index
        if len(index_) != 0:
            index = index_[0][0]
            ax2.scatter(precursor, intensity2[index] * 1.1, c='r', marker='D', s=10)
        else:
            ax2.scatter(precursor, max(intensity2) / 20, c='r', marker='D', s=10)

        # 标注出质量
        s1 = pd.Series(arr2, arr1).sort_values(ascending=False).head(mz_num)
        highest_3 = np.array([s1.index.values, s1.values]).T
        for i in range(mz_num):
            ax2.text(highest_3[i][0], highest_3[i][1], highest_3[i][0], size=11)
        ax2.set_ylabel('Intensity', fontsize=15)  # 设置y_label大小
        ax2.set_ylim(0, max(intensity2) * 1.2)
        ax2.set_xlim(50, precursor * 1.2)
        ax2.set_title(f'+ESI scan (rt: {rt2} min), Frag = 135.0 V, CID@{c2} V', loc='right', size=10)

        # 画第三个图
        ax3 = fig.add_subplot(313)
        ax3.bar(mzs3, intensity3)
        arr1 = np.array(mzs3)  # 转成array
        arr2 = np.array(intensity3)
        # 画出来precursor的点
        index_ = np.argwhere((arr1 > precursor - 0.015) & (arr1 < precursor + 0.015))  # 找到index
        if len(index_) != 0:
            index = index_[0][0]
            ax3.scatter(precursor, intensity3[index] * 1.1, c='r', marker='D', s=10)
        else:
            ax3.scatter(precursor, max(intensity3) / 20, c='r', marker='D', s=10)

        # 标注出质量
        s1 = pd.Series(arr2, arr1).sort_values(ascending=False).head(mz_num)
        highest_3 = np.array([s1.index.values, s1.values]).T
        for i in range(mz_num):
            ax3.text(highest_3[i][0], highest_3[i][1], highest_3[i][0], size=11)
        ax3.set_ylabel('Intensity', fontsize=15)  # 设置y_label大小
        ax3.set_ylim(0, max(intensity3) * 1.2)
        ax3.set_xlim(50, precursor * 1.2)
        ax3.set_title(f'+ESI scan (rt: {rt3} min), Frag = 135.0 V, CID@{c3} V', loc='right', size=10)
        ax3.set_xlabel('Counters vs. m/z', fontsize=14)
        if path == None:
            pass
        else:
            fig.savefig(path, dpi=dpi)
        if show is True:
            pass
        else:
            plt.close('all')
    else:
        new_path = path[:-4] + '.xlsx'
        DDA_df1.to_excel(new_path)


def spectrum_plot(mzs, intensity, mz_num, rt, precursor, collision_energy, path=None, show=True):
    """
    :param mzs: all mzs
    :param intensity: intensities
    :param mz_num: number of shown mass
    :param rt: target rt
    :param collision_energy: collision energy
    :param precursor: precursor
    :param path: path to store
    :param show: show or not
    :return:
    """
    fig = plt.figure(figsize=(10, 3))
    plt.rc('font', family='Times New Roman')

    # 第一个图
    ax1 = fig.add_subplot(111)
    ax1.bar(mzs, intensity)
    arr1 = np.array(mzs)  # 转成array
    arr2 = np.array(intensity)
    # 画出来precursor的点
    index = np.argwhere((arr1 > precursor - 0.015) & (arr1 < precursor + 0.015))[0][0]  # 找到index
    ax1.scatter(precursor, intensity[index] * 1.3, c='r', marker='D', s=10)
    # 标注出质量
    s1 = pd.Series(arr2, arr1).sort_values(ascending=False).head(mz_num)
    highest_3 = np.array([s1.index.values, s1.values]).T
    for i in range(mz_num):
        ax1.text(highest_3[i][0], highest_3[i][1], highest_3[i][0], size=11)
    ax1.set_ylabel('Intensity', fontsize=15)  # 设置y_label大小
    ax1.set_ylim(0, max(intensity) * 1.2)
    ax1.set_xlim(50, precursor * 1.2)
    ax1.set_title(f'+ESI scan (rt: {rt} min), Frag = 135.0 V, CID@{collision_energy} V', loc='right', size=10)
    ax1.set_xlabel('Counters vs. m/z')

    if path == None:
        pass
    else:
        fig.savefig(path)
    if show is True:
        pass
    else:
        plt.close('all')


def chromatogram_plot(rt, eic, extract_mz='', name='', path=None, show=True, dpi=500):
    """
    :param rt: retention time
    :param eic: extracted signal
    :param extract_mz:  extracted m/z
    :param name: compound name
    :param path: path to save
    :param show: shown or not
    :param dpi: dot per inch
    :return:
    """
    fig = plt.figure(figsize=(15, 5))
    plt.rc('font', family='Times New Roman')  # 设置全局字体

    # 第一个图
    ax1 = fig.add_subplot(111)
    ax1.plot(rt, eic, linewidth=2, c='C0', )
    # 设置坐标轴名称
    ax1.set_xlabel('Retention time (min)', fontsize=15)
    ax1.set_ylabel('Height', fontsize=15)

    # 添加标题
    ax1.set_title(f'Compound info: {name}', fontsize=15, loc='left')
    ax1.set_title(f'Extracted m/z: {round(extract_mz, 4)}', fontsize=15, loc='right')
    # 标注峰的rt
    y = max(eic)
    x = rt[np.argmax(eic)]
    ax1.scatter(x, y * 1.05, c='r', marker='D')
    ax1.text(x + 0.5, y, f'{round(x, 3)} min', fontdict=dict(fontsize=16, weight='light'))

    # 设置坐标轴刻度
    ax1.set_xticks(np.arange(0, 25, 5), minor=False)
    ax1.set_xticks(np.arange(0, 25, 2.5), minor=True)

    # 设置坐标轴刻度参数
    ax1.tick_params(axis='x', which='major', direction='in', labelsize=15)
    ax1.tick_params(axis='y', which='major', direction='in', labelsize=15)

    if path is None:
        pass
    else:
        fig.savefig(path, dpi=dpi)

    if show is True:
        pass
    else:
        plt.close('all')


def get_ms2_from_DDA(ms2, rt, mz, DDA_rt_error=0.1, DDA_mz_error=0.015):
    target_scans = []
    for scan in ms2:
        if (scan.scan_time[0] > rt - DDA_rt_error
        ) & (scan.scan_time[0] < rt + DDA_rt_error
        ) & (scan.selected_precursors[0]['mz'] < mz + DDA_mz_error
        ) & (scan.selected_precursors[0]['mz'] > mz - DDA_mz_error):
            target_scans.append(scan)
    return target_scans


def remove_adducts(df):
    '''
    :param df: df need to remove isototope and adducts peaks
    :return: new df
    '''
    names = ['Ciso', 'Cliso', 'Na adducts', 'NH4 adducts', 'Briso', 'K adducts']
    for name in names:
        df = df[df[name].isna()]
    names2 = [name for name in df.columns.values if 'Unnamed:' in name]
    df = df.drop(columns=names2)

    return df.reset_index(drop=True)


def suspect_list_matching(df, suspect_list, error=5, mode='pos'):
    '''
    :param df: df that need to match with suspect list
    :param suspect_list: S0-Merged NORMAN Suspect List SusDat
    :param error: ms1 error, ppm
    :param mode: 'pos' or 'neg'
    :return: new df
    '''
    df1 = remove_adducts(df)
    for i in tqdm(range(len(df1))):
        mz, iso_distribution = df1.loc[i, ['mz', 'iso_distribution']]
        if mode == 'pos':
            a = suspect_list[(suspect_list['M+H+'] > mz * (1 - error * 1e-6)) &
                             (suspect_list['M+H+'] < mz * (1 + error * 1e-6))].reset_index(drop=True)
        elif mode == 'neg':
            a = suspect_list[(suspect_list['M-H-'] > mz * (1 - error * 1e-6)) &
                             (suspect_list['M-H-'] < mz * (1 + error * 1e-6))].reset_index(drop=True)

        if len(a) == 0:
            df1.loc[i, 'suspect_match_result'] = '[]'
        else:
            score_dict = {}
            for formula in list(set(a.Molecular_Formula.values)):
                iso_score_info = isotope_matching(eval(iso_distribution), formula)
                if mode == 'pos':
                    iso, distribution = formula_to_distribution(formula)
                else:
                    iso, distribution = formula_to_distribution(formula, adducts='-H')
                mz_error = round((mz - iso[0]) / mz * 1e6, 1)

                score = round(1 - sum(iso_score_info.dis_diff.values), 2)
                score_dict[formula] = [score, mz_error]
            # 制作列表
            b = a.loc[:, ['StdInChIKey', 'Molecular_Formula']]
            final_score_list = []
            for k, v in score_dict.items():
                c = b[b['Molecular_Formula'] == k].copy()
                c['iso_Score'] = v[0]
                c['mz_error'] = v[1]
                final_score_list.append(c)
            d = pd.concat(final_score_list).reset_index(drop=True)
            e = d[d['iso_Score'] > 0.85]
            if len(e) == 0:
                f = '[]'
            else:
                f = str([e.iloc[i].to_dict() for i in range(len(e))])
            df1.loc[i, 'suspect_match_result'] = f
    return df1


def summarize_results(df, db_category, suspect_list, db_toxicity):
    '''
    :param df: dataframe
    :param db_category: category database
    :param suspect_list: suspect_list
    :param db_toxicity: toxicity database
    :return: new_dataframe
    '''
    # 检查这些元素在不在列表名里
    if 'rt_match_result' not in df.columns.values:
        df['rt_match_result'] = '[]'
    if 'best_results_DDA' not in df.columns.values:
        df['best_results_DDA'] = '[]'
    if 'best_results_DIA' not in df.columns.values:
        df['best_results_DIA'] = '[]'
    if 'match_result_DDA' not in df.columns.values:
        df['match_result_DDA'] = '[]'
    if 'match_result_DIA' not in df.columns.values:
        df['match_result_DIA'] = '[]'

    sorted_columns = ['new_index', 'name', 'formula', 'CAS', 'rt', 'mz', 'intensity', 'iso_distribution',
                      'MS2_spectra', 'ik', 'Smile',
                      'rt_error', 'ms1_error', 'ms1_opt_error', 'match_num', 'match_percent',
                      'match_info', 'MS2 mode', 'source', 'Norman_SusDat_ID', 'category', 'Toxicity']

    # 第一步骤，生成最终level1和level2的表
    data_all = []
    for i in range(len(df)):
        # 1. 先生成level1的表
        if df.loc[i, 'rt_match_result'] != '[]':
            rt_match = eval(df.loc[i, 'rt_match_result'])
            rt, mz, index, intensity, iso_distribution = df.loc[
                i, ['rt', 'mz', 'new_index', 'intensity', 'iso_distribution']]
            MS2_spectra = df.loc[i, 'MS2_spectra'] if 'MS2_spectra' in df.columns.values else None
            rt_match['rt'] = rt
            rt_match['mz'] = mz
            rt_match['new_index'] = index
            rt_match['intensity'] = intensity
            rt_match['iso_distribution'] = iso_distribution
            rt_match['MS2_spectra'] = MS2_spectra
            rt_match['ms1_error'] = rt_match.pop('mz_error')
            rt_match['ms1_opt_error'] = rt_match.pop('mz_opt_error')

            if df.loc[i, 'best_results_DDA'] != '[]':  # 首先这个不能是0
                # 找到和rt 匹配的ik值
                if rt_match['ik'] in df.loc[i, 'match_result_DDA']:  # 因此这个也不可能是0
                    DDA_match = [dict1 for dict1 in
                                 eval(df.loc[i, 'match_result_DDA']) if rt_match['ik'] == rt_match['ik']][0]
                    rt_match['match_num'] = DDA_match['match_num']
                    rt_match['match_percent'] = DDA_match['match_percent']
                    rt_match['match_info'] = DDA_match['match_info']
                    rt_match['source'] = DDA_match['source']
                    rt_match['MS2 mode'] = 'DDA'
                    if df.loc[i, 'best_results_DIA'] != '[]':  # 首先这个不能是0
                        if rt_match['ik'] in df.loc[i, 'match_result_DIA']:  # 因此这个也不可能是0
                            rt_match['MS2 mode'] = 'DDA&DIA'
                else:
                    DDA_match = eval(df.loc[i, 'best_results_DDA'])
                    rt_match['match_num'] = DDA_match['match_num']
                    rt_match['match_percent'] = DDA_match['match_percent']
                    rt_match['match_info'] = DDA_match['match_info']
                    rt_match['source'] = DDA_match['source']
                    rt_match['MS2 mode'] = DDA_match['ik']

            elif df.loc[i, 'best_results_DIA'] != '[]':  # 首先这个不能是0
                if rt_match['ik'] in df.loc[i, 'match_result_DIA']:  # 因此这个也不可能是0
                    DIA_match = [dict1 for dict1 in
                                 eval(df.loc[i, 'match_result_DIA']) if rt_match['ik'] == rt_match['ik']][0]
                    rt_match['match_num'] = DIA_match['match_num']
                    rt_match['match_percent'] = DIA_match['match_percent']
                    rt_match['match_info'] = DIA_match['match_info']
                    rt_match['source'] = DIA_match['source']
                    rt_match['MS2 mode'] = 'DIA'
                else:
                    DIA_match = eval(df.loc[i, 'best_results_DIA'])
                    rt_match['match_num'] = DIA_match['match_num']
                    rt_match['match_percent'] = DIA_match['match_percent']
                    rt_match['match_info'] = DIA_match['match_info']
                    rt_match['source'] = DIA_match['source']
                    rt_match['MS2 mode'] = DIA_match['ik']
            s1 = pd.Series(rt_match)
            data_all.append(s1)

        # 2. 再生成level2 DDA的表
        elif df.loc[i, 'best_results_DDA'] != '[]':
            DDA_match = eval(df.loc[i, 'best_results_DDA'])
            rt, mz, index, intensity, iso_distribution = df.loc[
                i, ['rt', 'mz', 'new_index', 'intensity', 'iso_distribution']]
            MS2_spectra = df.loc[i, 'MS2_spectra'] if 'MS2_spectra' in df.columns.values else None
            DDA_match['rt'] = rt
            DDA_match['mz'] = mz
            DDA_match['new_index'] = index
            DDA_match['intensity'] = intensity
            DDA_match['iso_distribution'] = iso_distribution
            DDA_match['MS2_spectra'] = MS2_spectra
            DDA_match['MS2 mode'] = 'DDA'

            if df.loc[i, 'best_results_DIA'] != '[]':  # 首先这个不能是0
                if DDA_match['ik'] in df.loc[i, 'match_result_DIA']:  # 因此这个也不可能是0
                    DDA_match['MS2 mode'] = 'DDA&DIA'
            s1 = pd.Series(DDA_match)
            data_all.append(s1)

            # 3. 再生成level2 DIA的表
        elif df.loc[i, 'best_results_DIA'] != '[]':
            DIA_match = eval(df.loc[i, 'best_results_DIA'])
            rt, mz, index, intensity, iso_distribution = df.loc[
                i, ['rt', 'mz', 'new_index', 'intensity', 'iso_distribution']]
            DIA_match['rt'] = rt
            DIA_match['mz'] = mz
            DIA_match['new_index'] = index
            DIA_match['iso_distribution'] = iso_distribution
            DIA_match['intensity'] = intensity
            DIA_match['MS2 mode'] = 'DIA'
            s1 = pd.Series(DIA_match)
            data_all.append(s1)
    if len(data_all) == 0:
        return pd.DataFrame()
    else:
        result_df = pd.concat(data_all, axis=1).T

        # 第二步骤，从suspect_list 把相关信息读入
        for i in range(len(result_df)):
            x = suspect_list[suspect_list.StdInChIKey == result_df.loc[i, 'ik']]
            if len(x) != 0:
                smi, name, cas, formula, Norman_SusDat_ID = x.loc[:, ['SMILES', 'Name', 'CAS_RN',
                                                                      'Molecular_Formula', 'Norman_SusDat_ID']].iloc[0]
                result_df.loc[i, 'Smile'] = smi
                result_df.loc[i, 'CAS'] = cas
                result_df.loc[i, 'name'] = name
                result_df.loc[i, 'formula'] = formula
                result_df.loc[i, 'Norman_SusDat_ID'] = Norman_SusDat_ID
        # 第三步骤获得分类数据
        for j in range(len(result_df)):
            ik = result_df.loc[j, 'ik']
            categories = db_category[db_category['Inchikey'] == ik]
            b = [eval(a) for a in categories.category.values] if len(categories) != 0 else []
            category = [d for c in b for d in c]
            result_df.loc[j, 'category'] = str(category)

        # 第四部分将毒理数据导入
        if 'Norman_SusDat_ID' not in result_df.columns.values:
            pass
        else:
            for n in range(len(result_df)):
                Norman_SusDat_ID = result_df.loc[n, 'Norman_SusDat_ID']
                cmp_toxicity_df = db_toxicity[db_toxicity['Norman SusDat ID'] == Norman_SusDat_ID]
                if len(cmp_toxicity_df) != 0:
                    cmp_toxicity_dict = cmp_toxicity_df.loc[:, ['Lowest PNEC Freshwater [µg//l]',
                                                                'Lowest PNEC Marine water [µg//l]',
                                                                'Lowest PNEC Sediments [µg//kg dw]',
                                                                'Lowest PNEC Biota (fish) [µg//kg ww]',
                                                                ]].iloc[0].to_dict()
                    result_df.loc[n, 'Toxicity'] = str(cmp_toxicity_dict)

        # 给对level3和level4进行分类，level3在suspect匹配到，并且有二级碎片，level4，能在suspect匹配到，但是没有碎片，剩下level5   

        # 最后给其排序
        columns = [column for column in sorted_columns if column in result_df.columns.values]
        result_df1 = result_df.loc[:, columns]

        return result_df1


def rename_files(rename_info, files):
    """
    This function can rename the files,make sure you have columns 'old_name' and 'new_name', these are new_name index,
    make sure they are unique
    :param rename_info: a dataframe include 'new_name' and 'old_name' columns
    :param files: files that need to rename
    :return: 
    """
    for i in tqdm(range(len(rename_info))):
        old_name_index = rename_info.loc[i, 'old_name']
        new_name_index = rename_info.loc[i, 'new_name']
        target_files = [file for file in files if old_name_index in file]
        if len(target_files) == 0:
            pass
        else:
            for old_file_name in target_files:
                new_file_name = old_file_name.replace(old_name_index, new_name_index)
                os.rename(old_file_name, new_file_name)


# ------------------组学分析-------------------------------------------


def remove_unnamed(df):
    '''
    :param df: df need to remove 'Unnamed: 0'
    :return: new df
    '''
    names2 = [name for name in df.columns.values if 'Unnamed:' in name]
    df = df.drop(columns=names2)

    return df.reset_index(drop=True)


def remove_adducts2(df, mode='pos'):
    '''
    :param df: df need to remove isototope and adducts peaks,but remain the Matching results.
    :return: new df
    '''
    columns_names = ['match_result_DIA', 'best_results_DIA',
                     'match_result_DDA', 'best_results_DDA', 'rt_match_result']
    for columns_name in columns_names:
        if columns_name not in df.columns.values:
            df[columns_name] = str([])
    # 找到所有有二级匹配信息的
    df_info1 = df[(df['match_result_DIA'] != '[]') | (df['match_result_DDA'] != '[]') | (df['rt_match_result'] != '[]')]
    # 去掉所有同位素的
    if mode == 'pos':
        names = ['Ciso', 'Cliso', 'Na adducts', 'NH4 adducts', 'Briso', 'K adducts']
    else:
        names = ['Ciso', 'Cliso', 'Briso']
    for name in names:
        if name in df.columns.values:
            df = df[(df[name].isna())]

    # 合并上述所有信息
    final_info = pd.concat([df, df_info1]).sort_values(by='intensity')
    final_info = final_info.drop_duplicates(subset=['new_index'], keep='first')
    # 去除所有unnamed列
    names2 = [name for name in final_info.columns.values if 'Unnamed:' in name]
    final_info = final_info.drop(columns=names2)

    return final_info.reset_index(drop=True)


def remove_adducts3(path, mode):
    """
    Removing adducts using remove_adducts2
    :param path: path for excel files
    :param mode:  'pos' or 'neg'
    :return: 
    """
    files = glob(os.path.join(path, '*.xlsx'))
    for file in tqdm(files):
        df = pd.read_excel(file)
        df1 = remove_adducts2(df, mode=mode)
        df1.to_excel(file.replace('.xlsx', '_removing_adducts.xlsx'))


def post_filter(path, fold_change=5, p_value=0.05, i_threshold=500, area_threshold=500, drop=None):
    '''
    :param path: path for unique_cmps excel files
    :param fold_change: fold change threshold
    :param p_value: p value threshold
    :param drop: the columns need to drop
    :return: generate a new excel file
    '''
    files = glob(os.path.join(path, '*.xlsx'))
    for i in tqdm(range(len(files))):
        try:
            df = pd.read_excel(files[i], index_col='Unnamed: 0')
        except:
            df = pd.read_excel(files[i])
        if drop == None:
            pass
        else:
            for name1 in drop:
                if name1 in df.columns.values:
                    df = df.drop(name1, axis=1)
                else:
                    pass

        fold_change_columns = [i for i in df.columns if 'fold_change' in i]
        p_values_columns = [i for i in df.columns if 'p_value' in i]

        for fold_change in fold_change_columns:
            df = df[df[fold_change] > 5]
        for p_value in p_values_columns:
            df = df[df[p_value] < 0.05].reset_index(drop=True)
        # other parameters
        df = df[(df.intensity > i_threshold) & (df.area > area_threshold)].reset_index(drop=True)

        df.to_excel(files[i].replace('.xlsx', '_filter.xlsx'))


def data_for_numbers(files, names, mode='pos'):
    """
    :param files: files to count compounds' numbers
    :param names: files series name
    :return: dataframe with number and error
    """
    WWTP = {}
    WWTP_error = {}
    for name in names:
        print(f'Processing {name}')
        files1 = [file for file in files if name in file]
        triplicates = []
        for file in files1:
            file_name = os.path.basename(file)
            print(f'    * reading file: {file_name}')
            df = pd.read_excel(file)
            triplicates.append(len(df))
        average = np.average(np.array(triplicates))
        error = np.std(np.array(triplicates))
        WWTP[name] = int(average)
        WWTP_error[name] = int(error)

    WWTP_s = pd.Series(WWTP)
    WWTP_error_s = pd.Series(WWTP_error)
    num_info = pd.concat([WWTP_s, WWTP_error_s], axis=1)
    if mode == 'pos':
        num_info.columns = ['pos_num', 'pos_num_error']
    else:
        num_info.columns = ['neg_num', 'neg_num_error']
    return num_info


def data_for_intensity(files, names, mode='pos', i_error_threshold=False):
    """
    :param files: files to count compounds' numbers
    :param names: files series name
    :return: dataframe with number and error
    """
    WWTP = {}
    WWTP_error = {}
    for name in names:
        print(f'Processing {name}')
        files1 = [file for file in files if name in file]
        triplicates = []
        for file in files1:
            file_name = os.path.basename(file)
            print(f'    * reading file: {file_name}')
            df = pd.read_excel(file)
            total_i = df['area_corr'].sum()
            original_i = df['area'].sum()
            if i_error_threshold is False:
                triplicates.append(total_i)
            else:
                if (total_i / original_i > i_error_threshold) | (original_i / total_i > i_error_threshold):
                    triplicates.append(original_i)
                else:
                    triplicates.append(total_i)

        average = np.average(np.array(triplicates))
        error = np.std(np.array(triplicates))
        WWTP[name] = int(average)
        WWTP_error[name] = int(error)

    WWTP_s = pd.Series(WWTP)
    WWTP_error_s = pd.Series(WWTP_error)
    i_info = pd.concat([WWTP_s, WWTP_error_s], axis=1)
    if mode == 'pos':
        i_info.columns = ['pos_intensity', 'pos_intensity_error']
    else:
        i_info.columns = ['neg_intensity', 'neg_intensity_error']
    return i_info


def correcting_areas(path_for_final_area, path_for_files, istd_info, normalized_area):
    """
    To use this function, you have to provide the rt and mz of internal standard
    :param path_for_final_area: path for final area
    :param path_for_files: file's path
    :param istd_info: a list for rt and mz, e.g., [4.35, 212.1183]
    :param normalized_area: the area value for comparison
    :return:
    """
    # 获得所有文件路径
    final_area_files = glob(os.path.join(path_for_final_area, '*.xlsx'))
    files = glob(os.path.join(path_for_files, '*.xlsx'))
    rt, mz = istd_info
    # 首先找到istd_index
    final_area_df1 = pd.read_excel(final_area_files[0])
    columns_name = final_area_df1.columns
    final_area_df1 = final_area_df1.sort_values(by=columns_name[-1], ascending=False)
    final_area_df1['rt'] = final_area_df1['Unnamed: 0'].apply(lambda x: eval(x.split('_')[0]))
    final_area_df1['mz'] = final_area_df1['Unnamed: 0'].apply(lambda x: eval(x.split('_')[1]))
    istd_index = final_area_df1[(final_area_df1.rt > rt - 0.1) &
                                (final_area_df1.rt < rt + 0.1) &
                                (final_area_df1.mz < mz + 0.015) &
                                (final_area_df1.mz > mz - 0.015)]['Unnamed: 0'].values[0]
    print(f'The istd_index area: {istd_index}')

    # 第一步：处理final_area获得所有样品的峰面积
    istd_all = []
    for file in tqdm(final_area_files, desc='Reading final area files'):
        df = pd.read_excel(file, index_col='Unnamed: 0')
        s = df.loc[istd_index]
        istd_all.append(s)
    corr = pd.concat(istd_all)

    # 第二步：处理files
    for name in tqdm(corr.index):
        file = [file for file in files if name in file]
        if len(file) != 0:
            df = pd.read_excel(file[0])
            coeff = corr.loc[name] / normalized_area
            df['area_corr'] = (df['area'] / coeff).astype(int)
            df = df[df.intensity > 500]
            df = df[df.area > 500]
            df = df.sort_values(by='intensity', ascending=False).reset_index(drop=True)
            df = remove_unnamed(df)
            df.to_excel(file[0].replace('.xlsx', '_istd_corrected.xlsx'))


def data_for_clustermap_final_area_average(path, names):
    """
    This function summarize all the final area files, and calculate the average value; (data_for_clustermap_1)
    :param path: path for final area files
    :param names: names for sample set
    :return:
    """
    files = glob(os.path.join(path, '*.xlsx'))
    final_result = []
    for name in names:
        print(f'Processing name: {name}')
        name_files = [file for file in files if name in file]
        name_data = []
        for file in name_files:
            file_name1 = os.path.basename(file)
            print(f'     * reading file: {file_name1}')
            df = pd.read_excel(file, index_col='Unnamed: 0')
            name_data.append(df)
        name_s = pd.concat(name_data, axis=1).mean(axis=1)
        final_result.append(name_s)
    data = pd.concat(final_result, axis=1).astype(int)
    data.columns = names
    return data


def data_for_clustermap_index_dict(all_new_index, names, path):
    """
    This function can check all new_index in final area, and keep the ones that present in sample;(data_for_clustermap_2)
    :param all_new_index: all new_index)
    :param names: names for sample set
    :param files: files of original file
    :return: a dict with all new_index
    """
    files = glob(os.path.join(path, '*.xlsx'))
    # 把所有new_index转化成pair
    pair = [[eval(all_new_index[i].split('_')[0]), eval(all_new_index[i].split('_')[1])] for i in
            range(len(all_new_index))]
    pair_df = pd.DataFrame(np.array(pair))
    pair_df.columns = ['rt', 'mz']
    pair_df.index = all_new_index
    # 针对每一组样品进行处理
    final_dict = {}
    for name in names:
        print(f'Processing files name: {name}')
        name_files = [file for file in files if name in file]
        df_all = []
        for file in name_files:
            file_name1 = os.path.basename(file)
            print(f'   * reading {file_name1}')
            df = pd.read_excel(file)
            df_all.append(df)
        df_all_df = pd.concat(df_all, axis=0).reset_index(drop=True)
        index_check = []
        for i in tqdm(range(len(pair_df)), desc='Checking compounds for each new_index:'):
            rt, mz = pair_df.iloc[i, [0, 1]]
            new_index = pair_df.iloc[i].name
            check_result = df_all_df[(df_all_df.rt > rt - 0.1) & (df_all_df.rt < rt + 0.1) &
                                     (df_all_df.mz < mz + 0.015) & (df_all_df.mz > mz - 0.015)]
            if len(check_result) > 0:
                index_check.append(new_index)
        final_dict[name] = index_check
    return final_dict


def data_for_clustermap_filter(data, index_dict, mz_range=[100, 800], rt_range=[1, 18], area_threshold=5000):
    """
    This function can help you to reduce the datasize and so the clustermap can be generated;;(data_for_clustermap_3)
    :param data: dataframe for clustermap
    :param index_dict: index dict for each sample set
    :param mz_range: mz range
    :param rt_range: rt range
    :param area_threshold: area threshold
    :return: a new dataframe
    """
    final_list = []
    for key, values in index_dict.items():
        s1 = data[key]
        s2 = s1.loc[values]
        final_list.append(s2)
    final_df = pd.concat(final_list, axis=1)  # 获得原始的数据

    # 进行峰面积筛选
    final_df[final_df < area_threshold] = np.nan
    index1 = final_df.dropna(how='all', axis=0).index.values
    final_df = pd.concat(final_list, axis=1)  # 再次获得原始的数据
    final_df = final_df.loc[index1]

    # 进行mz,和rt的筛选
    final_df['index'] = final_df.index
    final_df['rt'] = final_df['index'].apply(lambda x: eval(x.split('_')[0]))
    final_df['mz'] = final_df['index'].apply(lambda x: eval(x.split('_')[1]))
    final_df = final_df[(final_df.mz > mz_range[0]) & (final_df.mz < mz_range[1]) & (final_df.rt > rt_range[0]) & (
            final_df.rt < rt_range[1])]  # 筛选条件
    final_df = final_df.drop(columns=['index', 'rt', 'mz']).fillna(1)
    return final_df


def check_istd_quality(istd_info, final_area_df):
    """
    This function can locate the internal standard new_index and return the final areas
    :param istd_info: information for internal standard, e.g., [4.3,212.1183]
    :param final_area_df: final area dataframe
    :return: a series with file names and areas
    """
    rt, mz = istd_info
    # 首先找到istd_index
    final_area_df['new_index'] = final_area_df.index.values
    final_area_df['rt'] = final_area_df['new_index'].apply(lambda x: eval(x.split('_')[0]))
    final_area_df['mz'] = final_area_df['new_index'].apply(lambda x: eval(x.split('_')[1]))
    istd_index_df = final_area_df[(final_area_df['rt'] > rt - 0.1) &
                                  (final_area_df['rt'] < rt + 0.1) &
                                  (final_area_df['mz'] < mz + 0.015) &
                                  (final_area_df['mz'] > mz - 0.015)]['new_index']
    if len(istd_index_df) == 0:
        print(r'Error: istd not found')
        return None
    else:
        istd_index = istd_index_df.values[0]
        print(f'The istd_index: {istd_index}')
        final_area_df = final_area_df.drop(columns=['new_index', 'rt', 'mz'])
        result = final_area_df.loc[istd_index]
        return result

def check_istd_quality2(istd_info,path):
    '''
    :param istd_info: ISTD information, e.g.,[14.13,221.1325]
    :param path:  path for unique_cmp files
    :return: 
    '''
    rt, mz = istd_info
    files = glob(os.path.join(path,'*.xlsx'))
    df_all = []
    for file in tqdm(files):
        df = pd.read_excel(file)
        df1 = df[(df['rt']>rt-0.1)&
          (df['rt']<rt+0.1)&
          (df['mz']>mz-0.015)&
          (df['mz']<mz+0.015)]
        df2 = df1.loc[:,['new_index','rt','mz','intensity','area']]
        df2['file'] = os.path.basename(file)
        df_all.append(df2)
    df_all_df = pd.concat(df_all,axis=0)
    return df_all_df    


def check_istd_concat(path_for_final_area):
    """
    This function can concat all the final area files, so it is easy to locate each internal standard new index
    :param path_for_final_area: path for final area
    :return: A dataframe
    """
    files = glob(os.path.join(path_for_final_area, '*.xlsx'))
    files = [file for file in files if 'final_area' in file]
    df_all = []
    for file in tqdm(files):
        df = pd.read_excel(file, index_col='Unnamed: 0')
        df_all.append(df)
    final_area_df = pd.concat(df_all, axis=1)
    return final_area_df


# -----identification result analysis-------------------------------------

def summarized_results_concat(path, all_name_index, mode):
    """
    This function can summarize all the summarized result files (generated from function summarized_result), and 
    return a dataframe without duplicates (same site and same compound)
    :param path: path for summarized result
    :param all_name_index: name index, must be unique to represent sample set
    :param mode: 'pos' or 'neg'
    :return: all result together, without duplicate with same site and compound
    """
    files = glob(os.path.join(path, '*.xlsx'))
    df_all = []
    for file in tqdm(files):
        df = pd.read_excel(file, index_col='Unnamed: 0')
        if len(df) == 0:
            pass
        else:
            name_index = [i for i in all_name_index if i in os.path.basename(file)][0]
            df['site'] = name_index
            # 确保索引的column都在里面
            if 'rt_error' not in df.columns.values:
                df['rt_error'] = np.nan
            if 'MS2 mode' not in df.columns.values:
                df['MS2 mode'] = np.nan
            # 每个数据进行分级
            # level1
            need_change_index1 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index1, 'Confidence level'] = 1
            # level2
            need_change_index2 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & df['rt_error'].isna()].index
            df.loc[need_change_index2, 'Confidence level'] = 2
            # level3
            need_change_index3 = df[~((df['MS2 mode'] == 'DDA')
                                      | (df['MS2 mode'] == 'DIA')
                                      | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index3, 'Confidence level'] = 3
            df_all.append(df)
    df_all_df = pd.concat(df_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
    drop_duplicate_index = df_all_df.loc[:, ['ik', 'site', 'Confidence level']].drop_duplicates().index
    df_all_df_no_duplicate = df_all_df.loc[drop_duplicate_index].reset_index(drop=True)
    df_all_df_no_duplicate['mode'] = mode
    # 第二步，整理结果：
    all_df = df_all_df_no_duplicate  # 先赋值，免得下面改了
    iks = all_df['ik'].value_counts().index
    data_all = []
    for i in range(len(iks)):
        df1 = all_df[all_df['ik'] == iks[i]]  # 所有有此ik的物质
        # 要先看是否有保留时间
        rt_check = df1[~df1['rt_error'].isna()]
        if len(rt_check) != 0:
            right_rt_list = df1[df1['Confidence level'] == 1].rt.values  # 选取一个锚定保留时间
            if len(right_rt_list) == 0:
                df1 = df1.sort_values(by=['Confidence level', 'intensity'], ascending=[True, False])
                df2 = df1.iloc[0]
                df3 = df2.to_dict()
                df3['site'] = str(list(set(df1['site'].values)))
                df3['sites_num'] = len(list(set(df1['site'].values)))
                df4 = pd.Series(df3)
            else:
                right_rt = right_rt_list[0]
                df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 这些都定义为level1
                df3 = df2.iloc[0].to_dict()
                mode_index = df2['MS2 mode'].value_counts().index.values
                if 'DDA&DIA' in mode_index:
                    df3['MS2 mode'] = 'DDA&DIA'
                elif 'DDA' in mode_index:
                    df3['MS2 mode'] = 'DDA'
                elif 'DIA' in mode_index:
                    df3['MS2 mode'] = 'DIA'
                # 更新最好的信息
                df3['site'] = str(list(set(df2['site'].values)))

                df3['rt_error'] = df2['rt_error'].value_counts().index[0]
                df_ = df2.sort_values(by='match_num', ascending=False).iloc[0]
                df3['match_num'] = df_.loc['match_num']
                df3['match_percent'] = df_.loc['match_percent']
                df3['match_info'] = df_.loc['match_info']
                df3['sites_num'] = len(list(set(df2['site'].values)))
                df3['Confidence level'] = 1
                df4 = pd.Series(df3)
        else:
            df1 = df1.sort_values(by=['match_num', 'intensity'], ascending=[False, False])
            right_rt = df1.rt.iloc[0]
            df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 如果保留时间偏差太大就不是一个物质
            df3 = df2.iloc[0].to_dict()
            mode_index = df2['MS2 mode'].value_counts().index.values
            if 'DDA&DIA' in mode_index:
                df3['MS2 mode'] = 'DDA&DIA'
            elif 'DDA' in mode_index:
                df3['MS2 mode'] = 'DDA'
            elif 'DIA' in mode_index:
                df3['MS2 mode'] = 'DIA'
            df3['site'] = str(list(set(df2['site'].values)))
            df3['sites_num'] = len(list(set(df2['site'].values)))
            df4 = pd.Series(df3)
        data_all.append(df4)
    dfx = pd.concat(data_all, axis=1).T

    return dfx

def summarized_results_concat2(path, all_name_index, mode):
    """
    This function can summarize all the summarized result files (generated from function summarized_result), and 
    return a dataframe without duplicates (same site and same compound)
    :param path: path for summarized result
    :param all_name_index: name index, must be unique to represent sample set
    :param mode: 'pos' or 'neg'
    :return: all result together, without duplicate with same site and compound
    """
    files = glob(os.path.join(path, '*.xlsx'))
    df_all = []
    for file in tqdm(files):
        df = pd.read_excel(file, index_col='Unnamed: 0')
        if len(df) == 0:
            pass
        else:
            name_index = [i for i in all_name_index if i in os.path.basename(file)][0]
            df['site'] = name_index
            # 确保索引的column都在里面
            if 'rt_error' not in df.columns.values:
                df['rt_error'] = np.nan
            if 'MS2 mode' not in df.columns.values:
                df['MS2 mode'] = np.nan
            # 每个数据进行分级
            # level1
            need_change_index1 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index1, 'Confidence level'] = 1
            # level2
            need_change_index2 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & df['rt_error'].isna()].index
            df.loc[need_change_index2, 'Confidence level'] = 2
            # level3
            need_change_index3 = df[~((df['MS2 mode'] == 'DDA')
                                      | (df['MS2 mode'] == 'DIA')
                                      | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index3, 'Confidence level'] = 3
            df_all.append(df)
    df_all_df = pd.concat(df_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
    drop_duplicate_index = df_all_df.loc[:, ['ik', 'site', 'Confidence level']].drop_duplicates().index
    df_all_df_no_duplicate = df_all_df.loc[drop_duplicate_index].reset_index(drop=True)
    df_all_df_no_duplicate['mode'] = mode
    # 第二步，整理结果：
    all_df = df_all_df_no_duplicate  # 先赋值，免得下面改了
    iks = all_df['ik'].value_counts().index
    data_all = []
    for i in range(len(iks)):
        df1 = all_df[all_df['ik'] == iks[i]]  # 所有有此ik的物质
        
        # 确定一下不同样品中的质量最准的
        df_temp = df1.copy()
        df_temp['error_obs_abs'] = df_temp['ms1_error'].abs()
        df_temp1 = df_temp.sort_values(by = 'error_obs_abs').iloc[0]
        best_mz_obs = df_temp1['mz']
        best_mz_error = df_temp1['ms1_error']
        best_ms1_opt_error = df_temp1['ms1_opt_error']
        # 记录一下详细的质量信息
        df_temp = df1.copy()
        df2_ = df_temp.loc[:,['ms1_error','ms1_opt_error','site']].sort_values(by = 'site')
        df2__ = df2_.set_index('site')
        ms_error_detail = df2__.to_dict()
        
        # 要先看是否有保留时间
        rt_check = df1[~df1['rt_error'].isna()]
        if len(rt_check) != 0:
            right_rt_list = df1[df1['Confidence level'] == 1].rt.values  # 选取一个锚定保留时间
            if len(right_rt_list) == 0:
                df1 = df1.sort_values(by=['Confidence level', 'intensity'], ascending=[True, False])
                df2 = df1.iloc[0]
                df3 = df2.to_dict()
                df3['site'] = str(list(set(df1['site'].values)))
                df3['sites_num'] = len(list(set(df1['site'].values)))
                df3['ms_error_detail'] = ms_error_detail
                df4 = pd.Series(df3)
            else:
                right_rt = right_rt_list[0]
                df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 这些都定义为level1
                df3 = df2.iloc[0].to_dict()
                mode_index = df2['MS2 mode'].value_counts().index.values
                if 'DDA&DIA' in mode_index:
                    df3['MS2 mode'] = 'DDA&DIA'
                elif 'DDA' in mode_index:
                    df3['MS2 mode'] = 'DDA'
                elif 'DIA' in mode_index:
                    df3['MS2 mode'] = 'DIA'
                # 更新最好的信息
                df3['site'] = str(list(set(df2['site'].values)))

                df3['rt_error'] = df2['rt_error'].value_counts().index[0]
                df_ = df2.sort_values(by='match_num', ascending=False).iloc[0]
                df3['match_num'] = df_.loc['match_num']
                df3['match_percent'] = df_.loc['match_percent']
                df3['match_info'] = df_.loc['match_info']
                df3['sites_num'] = len(list(set(df2['site'].values)))
                df3['ms_error_detail'] = ms_error_detail
                df3['Confidence level'] = 1
                df4 = pd.Series(df3)
        else:
            df1 = df1.sort_values(by=['match_num', 'intensity'], ascending=[False, False])
            right_rt = df1.rt.iloc[0]
            df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 如果保留时间偏差太大就不是一个物质
            df3 = df2.iloc[0].to_dict()
            mode_index = df2['MS2 mode'].value_counts().index.values
            if 'DDA&DIA' in mode_index:
                df3['MS2 mode'] = 'DDA&DIA'
            elif 'DDA' in mode_index:
                df3['MS2 mode'] = 'DDA'
            elif 'DIA' in mode_index:
                df3['MS2 mode'] = 'DIA'
            df3['site'] = str(list(set(df2['site'].values)))
            df3['sites_num'] = len(list(set(df2['site'].values)))
            df3['ms_error_detail'] = ms_error_detail
            df4 = pd.Series(df3)
        df4['best_mz_obs']=best_mz_obs
        df4['best_mz_error']=best_mz_error
        df4['best_ms1_opt_error']=best_ms1_opt_error
        data_all.append(df4)
    dfx = pd.concat(data_all, axis=1).T

    return dfx


def summarize_pos_neg_result(all_df_pos, all_df_neg):
    """
    This function can concat the df in pos and neg mode.
    :param all_df_pos: all_df_pos
    :param all_df_neg: all_df_neg
    :return: final result
    """
    df_pos_neg = pd.concat([all_df_pos, all_df_neg], axis=0)
    iks = df_pos_neg['ik'].value_counts().index
    df_all = []
    for ik in iks:
        df1 = df_pos_neg[df_pos_neg['ik'] == ik]
        df1 = df1.sort_values(by='Confidence level')
        df2 = df1.iloc[0]
        df3 = df2.to_dict()
        # 更新点位的名称，和点位的个数
        site = list(set([j for i in df1['site'].values for j in eval(i)]))
        df3['site'] = str(site)
        df3['sites_num'] = len(site)
        # 更新mode，如果pos和neg都有，要说明各有几个
        site_info = df1.loc[:, ['mode', 'sites_num']]
        site_info1 = site_info.set_index('mode').to_dict()['sites_num']
        df3['mode'] = str(site_info1)
        # 更新MS2 mode
        mode_index = df1['MS2 mode'].values
        if 'DDA&DIA' in mode_index:
            df3['MS2 mode'] = 'DDA&DIA'
        elif 'DDA' in mode_index:
            df3['MS2 mode'] = 'DDA'
        elif 'DIA' in mode_index:
            df3['MS2 mode'] = 'DIA'
        df4 = pd.Series(df3)
        df_all.append(df4)
    return pd.concat(df_all, axis=1).T.reset_index(drop=True)


def update_category(result, category_updates, good_category):
    """
    This function can transform old categories to new categories.
    :param level1: final summarized result with level1 or level2
    :param category_updates: category updates information 
    :param good_category: This category are doubtless，most of them are standards in our lab
    :return: new summarized results with new category
    """
    updates = category_updates[~category_updates['new category'].isna()].reset_index(drop=True)
    # 先做替换
    for i in range(len(result)):
        x = eval(result.loc[i, 'category'])
        if len(x) == 0:
            pass
        else:
            y = list(set([None if i not in updates['old category'].values else
                          updates[updates['old category'] == i]['new category'].values[0] for i in x]))
            if None in y:
                y.remove(None)
            result.loc[i, 'new_category'] = str(y)
    # 再将正确的替换
    ik_index = good_category['ik'].value_counts().index
    for ik in ik_index:
        ik_df = good_category[good_category.ik == ik]
        new_category = list(set(ik_df['category'].values))
        usage = list(set(ik_df['sub_category'].values))
        if np.nan in usage:
            usage.remove(np.nan)
        # 去找一下result里面是否有这个物质
        a = result[result['ik'] == ik]
        if len(a) != 0:
            index = a.index.values[0]
            if 'REACH' in str(result.loc[index, 'new_category']):  # 看一下原来的分类里，是否包含REACH
                new_category.append('REACH')
            result.loc[index, 'new_category'] = str(new_category)
            result.loc[index, 'usage'] = str(usage)
    return result


def final_result_filter(final_result, remove_list=None, match_num=2):
    if remove_list is None:
        pass
    else:
        for remove_item in remove_list:
            final_result1 = final_result[~final_result['source'].fillna('-').str.contains(remove_item)]
    a = final_result1[final_result1['Confidence level'] == 1]
    c = final_result1[final_result1['Confidence level'] == 3]
    b_ = final_result1[final_result1['Confidence level'] == 2]
    b = b_[b_['match_num'] >= match_num]
    final_result2 = pd.concat([a, b, c], axis=0).reset_index(drop=True)
    for i in range(len(final_result2)):
        if type(final_result2.loc[i, 'Toxicity']) == float:
            pass
        else:
            x = eval(final_result2.loc[i, 'Toxicity'])
            for k, v in x.items():
                if (type(v) is float) | (v == '-'):
                    final_result2.loc[i, k] = v
                else:
                    final_result2.loc[i, k] = eval(v)
    return final_result2


def draw_WWTP_fig(new_index, final_area_all, names, level1, path=None):
    """
    This function can draw the change of peak area, and export the fig with molecule information
    :param new_index:  new index for a single compound
    :param final_area_all: all final area dataframe
    :param names: name index for each sample set, a list, e.g., ['raw_water','A1_out'...]
    :param path: path to save the fig
    :return:
    """
    from rdkit.Chem import Draw
    from rdkit import Chem
    from matplotlib.offsetbox import DrawingArea, OffsetImage, AnnotationBbox, TextArea
    import matplotlib.image as mpimg

    # 1. 获取数据
    s1 = final_area_all.loc[new_index]
    data = []
    for name in names:
        index = [i for i in s1.index.values if name in i]
        x = round(np.average(s1.loc[index].values), 1)
        x_error = round(np.std(s1.loc[index].values), 1)
        data.append([x, x_error])
    # 2. 开始作图
    x = np.array(data).T[0]
    x_error = np.array(data).T[1]
    plt.rcParams['font.sans-serif'] = 'Times New Roman'  # 设置全局字体
    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(121)
    ax.errorbar(names, x, yerr=x_error, capsize=7, marker='o', markersize=20, alpha=0.7, fmt="-", ecolor='black',
                elinewidth=2, mec="b", mfc="g")
    ax.set_ylabel('Peak area', size=25)
    ax.tick_params(labelrotation=30, axis='x', labelsize=16)
    ax.tick_params(labelrotation=0, axis='y', labelsize=15)
    plt.ylim(0, max(x) * 1.1)
    # 3. 将分子信息画上去
    ax1 = fig.add_subplot(122)
    ax1.axis('off')
    try:
        smi = level1[level1['new_index'] == new_index]['Smile'].values[0]
        mol = Chem.MolFromSmiles(smi)
        img = Draw.MolToImage(mol, size=(300, 300), kekulize=True)
        imagebox = OffsetImage(img, zoom=0.8)  ## 将图片放在OffsetBox容器中
        imagebox2 = AnnotationBbox(imagebox, (0.9, 0.8), frameon=False)  ##使用AnnotationBbox添加到画布中
        ax1.add_artist(imagebox2)
    except:
        pass

    # 4. 将分子信息放上去
    info_index = ['name', 'rt', 'rt_error', 'mz', 'MS2 mode', 'CAS', 'formula', 'site', 'new_category',
                  'Lowest PNEC Freshwater [µg//l]']
    y1 = 0.6
    for index1 in info_index:
        m_info = level1[level1['new_index'] == new_index].T.loc[index1].values[0]
        ax1.text(-0.1, y1, f'{index1}:  {m_info}', zorder=0, size=20)
        y1 -= 0.07
    if path is None:
        pass
    else:
        plt.savefig(path, dpi=300)
        plt.close('all')


# ===============SWATH data processing method =====================

def swath_peak_picking(file, precursor_ion_start_mass=99.5, profile=True,
           threshold=15, i_threshold=500, SN_threshold=3, mz_overlap=1, rt_error=0.05):
    """
    Processing swath-ms data and return a dataframe with all informations
    :param file: file in mzml format
    :param precursor_ion_start_mass: for MS/MS spectra, precursor_ion_start_mass
    :param profile: if profile: True, Centroid: False
    :param threshold: peak picking threshold
    :param i_threshold: intensity threshold
    :param SN_threshold: singal to noise threshold
    :param mz_overlap: MS2 window overlap
    :param rt_error: rt_error
    :return: A dataframe with peak informations
    """
    ms1, ms2 = sep_scans(file, 'AB')  # 分离ms1和ms2
    print('=======================================')
    print('   ')
    print(f'First process: ms1 peak picking...')
    print('======================================')
    print('   ')
    peak_all_ms1 = split_peak_picking(ms1, profile=profile, threshold=threshold,
                                      i_threshold=i_threshold, SN_threshold=SN_threshold)

    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)

    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'], 1))
        locals()[name].append(scan)

    # 4. 开始分批提取峰
    all_peak_all = {}
    for k, v in all_data.items():
        print('-----------------------')
        print(f'Processing m/z: {k}')
        print('-----------------------')
        print('   ')
        x = locals()[v]
        peak_all = split_peak_picking_swath(x, k, profile=profile, i_threshold=i_threshold)
        all_peak_all[k] = peak_all

    print('=======================================')
    print('   ')
    print(f'Third process: ms2 spec assignment...')
    print('======================================')
    print('   ')

    # ======计算窗口大小=============

    precursor = precursors[0]
    # 第一个要手动
    ms_range = {}
    next_gap = precursors[0] - precursor_ion_start_mass
    ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
    end_mz = round(precursor + next_gap, 1)
    for precursor in precursors[1:]:
        next_start_mz = round(end_mz - mz_overlap, 1)
        next_gap = precursor - next_start_mz
        end_mz = round(precursor + next_gap, 1)
        ms_range[precursor] = [next_start_mz, end_mz]

    # ======将提取的峰赋值=============
    for i in tqdm(range(len(peak_all_ms1))):
        rt, mz = peak_all_ms1.loc[i, ['rt', 'mz']]
        for k, v in ms_range.items():
            if (mz <= v[1] - 0.5) & (mz > v[0] + 0.5):
                scan_index = k
                break
        target_s = all_peak_all[scan_index]
        if len(target_s) == 0:
            peak_all_ms1.loc[i, 'frag_swath'] = str([])
            peak_all_ms1.loc[i, 'MS2_spectra_swath'] = str([])
            peak_all_ms1.loc[i, 'MS2_spectra_swath_dict'] = str([])
        else:
            target_s_df = target_s[(target_s['rt'] > rt - rt_error) & (target_s['rt'] < rt + rt_error)]
            mz2, intensity2 = target_s_df['mz'].values, target_s_df['intensity'].values
            frag_s = pd.Series(data=intensity2, index=mz2)
            peak_all_ms1.loc[i, 'frag_swath'] = str(list(mz2))
            peak_all_ms1.loc[i, 'MS2_spectra_swath'] = str(frag_s)
            peak_all_ms1.loc[i, 'MS2_spectra_swath_dict'] = str(frag_s.to_dict())
    return peak_all_ms1


def split_peak_picking_swath(ms1, highest_mz, profile=True, split_n=20, threshold=15, i_threshold=1000,
                             SN_threshold=5, noise_threshold=0, rt_error_alignment=0.05, mz_error_alignment=0.015):
    def target_spec1(spec, target_mz, width=0.04):
        """
        :param spec: spec generated from function spec_at_rt()
        :param target_mz: target mz for inspection
        :param width: width for data points
        :return: new spec and observed mz
        """
        index_left = argmin(abs(spec.index.values - (target_mz - width)))
        index_right = argmin(abs(spec.index.values - (target_mz + width)))
        new_spec = spec.iloc[index_left:index_right].copy()
        new_spec[target_mz - width] = 0
        new_spec[target_mz + width] = 0
        new_spec = new_spec.sort_index()
        return new_spec

    if profile is True:
        peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]] for i in range(len(ms1))]
        raw_info_centroid = {
            round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(4),
                                                     name=round(ms1[i].scan_time[0], 3)) for i, peaks in peaks_index}
        raw_info_profile = {round(ms1[i].scan_time[0], 3):
                                pd.Series(data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3))
                            for i in range(len(ms1))}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]
    else:
        raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
            data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3)) for i in
            range(len(ms1))}
        data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
                raw_info_centroid.items()]

    # 开始分割
    # 定义变量名称
    all_data = []
    for j in range(split_n):
        name = 'a' + str(j + 1)
        locals()[name] = []
    # 对series进行切割
    ms_increase = int(1000 / split_n)
    for i in tqdm(range(len(data)), desc='Split series:'):
        s1 = data[i]
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            name = 'a' + str(j + 1)
            if low > highest_mz:
                break
            locals()[name].append(s1[(s1.index < high) & (s1.index >= low) & (s1.index > noise_threshold)])
            low += ms_increase
            high += ms_increase

    # 将所有数据合并到all_data里
    for j in range(split_n):
        name = 'a' + str(j + 1)
        all_data.append(locals()[name])

    # 开始分段提取
    all_peak_all = []
    for i, data1 in enumerate(all_data):
        if len(data1) == 0:
            pass
        else:
            df1 = pd.concat(data1, axis=1)

            df1 = df1.fillna(0)
            if len(df1) == 0:
                pass
            else:
                highest_mz = df1.index.values.max()
                print(f'highest_mz:   {highest_mz}')
                peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold,
                                        i_threshold=i_threshold, SN_threshold=SN_threshold,
                                        rt_error_alignment=rt_error_alignment,
                                        mz_error_alignment=mz_error_alignment)
                all_peak_all.append(peak_all)

    # 避免concat空列表
    if len(all_peak_all) == 0:
        peak_all = pd.DataFrame()
    else:
        peak_all = pd.concat(all_peak_all)

    if len(peak_all) == 0:
        pass
    else:
        peak_all = peak_all.sort_values(by='intensity', ascending=False).reset_index(drop=True)
        raw_info_rts = [v.name for k, v in raw_info_centroid.items()]
        rts = peak_all.rt.values
        mzs = peak_all.mz.values
        rt_keys = [raw_info_rts[argmin(abs(np.array(raw_info_rts) - i))] for i in rts]  # 基于上述rt找到ms的时间索引

        # 更新质量数据
        if profile is True:
            spec1 = [raw_info_profile[i] for i in rt_keys]  # 获得ms的spec
            mz_result = np.array(
                [list(evaluate_ms(target_spec1(spec1[i], mzs[i], width=0.04).copy(), mzs[i])) for i in
                 range(len(mzs))]).T
            mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
            mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else mzs[i] for i in range(len(mzs))]  # 去掉偏差大的矫正结果

            peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
            
        else:
            spec1 = [raw_info_centroid[i] for i in rt_keys]  # 获得ms的spec
            target_spec = [spec1[i][(spec1[i].index > mzs[i] - 0.015) & (spec1[i].index < mzs[i] + 0.015)] for i in
                           range(len(spec1))]
            mzs_obs = [target_spec[i].index.values[[np.argmax(target_spec[i].values)]][0] for i in
                       range(len(target_spec))]
            peak_all['mz'] = mzs_obs
    return peak_all

def JsonToExcel3(json_file):
    with open(json_file, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    Inchikey, precursors, frags, formulas, smiles, ion_modes, instrument_types, collision_energies = [], [], [], [], [], [], [], []
    cases, pubchem_cids, inchis, total_exact_masses = [], [], [], []
    columns, mass_accuracies, precursor_mzs, precursor_types, ionization_modes = [], [], [], [],[]
    kingdoms, superclasses, class1s, subclasses = [], [], [], []
    names = []
    frag_annotations =[]
    num = len(json_data)
    for i in tqdm(range(num)):
        # 信息1:包括分子信息
        info1 = json_data[i]['compound'][0]['metaData']
        ik_info = [x['value'] for x in info1 if x['name'] == 'InChIKey']
        formula_info = [x['value'] for x in info1 if x['name'] == 'molecular formula']
        precursor_info = [x['value'] for x in info1 if x['name'] == 'total exact mass']
        smile_info = [x['value'] for x in info1 if x['name'] == 'SMILES']
        cas_info = [x['value'] for x in info1 if x['name'] == 'cas']  # 新增cas
        pubchem_cid_info = [x['value'] for x in info1 if x['name'] == 'pubchem cid']  # 新增pubchem_cid
        inchi_info = [x['value'] for x in info1 if x['name'] == 'InChI']  # 新增 inchi
        total_exact_mass_info = [x['value'] for x in info1 if x['name'] == 'total exact mass'] # 新增 total_exact_mass
        # 获得数据
        ik = None if len(ik_info) == 0 else ik_info[0]
        formula = None if len(formula_info) == 0 else formula_info[0]
        precursor = None if len(precursor_info) == 0 else precursor_info[0]
        smile = None if len(smile_info) == 0 else smile_info[0]
        cas = None if len(cas_info) == 0 else cas_info[0]
        pubchem_cid = None if len(pubchem_cid_info) == 0 else pubchem_cid_info[0]
        inchi = None if len(inchi_info) == 0 else inchi_info[0]
        total_exact_mass = None if len(total_exact_mass_info) == 0 else total_exact_mass_info[0]

        # 信息2:包括测试条件
        info2 = json_data[i]['metaData']
        ion_mode_info = [x['value'] for x in info2 if x['name'] == 'ionization mode']
        instrument_type_info = [x['value'] for x in info2 if x['name'] == 'instrument type']
        ce_info = [i for i in info2 if i['name'] == 'collision energy']
        columns_info = [x['value'] for x in info2 if x['name'] == 'column'] # 新增columns
        mass_accuracy_info = [x['value'] for x in info2 if x['name'] == 'mass accuracy'] # 新增mass_accuracy
        precursor_mz_info = [x['value'] for x in info2 if x['name'] == 'precursor m/z'] # 新增precursor_mz
        precursor_type_info = [x['value'] for x in info2 if x['name'] == 'precursor type'] # 新增precursor_type
        ionization_mode_info = [x['value'] for x in info2 if x['name'] == 'ionization mode'] # 新增ionization_mode

        # 获得数据
        ion_mode = None if len(ion_mode_info) == 0 else ion_mode_info[0]
        instrument_type = None if len(instrument_type_info) == 0 else instrument_type_info[0]
        ce = None if len(ce_info) == 0 else ce_info[0]['value']
        column = None if len(columns_info) == 0 else columns_info[0]
        mass_accuracy = None if len(mass_accuracy_info) == 0 else mass_accuracy_info[0]
        precursor_mz = None if len(precursor_mz_info) == 0 else precursor_mz_info[0]
        precursor_type = None if len(precursor_type_info) == 0 else precursor_type_info[0]
        ionization_mode = None if len(ionization_mode_info) == 0 else ionization_mode_info[0]

        # 信息3：包括分类
        info3 = json_data[i]['compound'][0]['classification'] if 'classification' in [k for k,v in json_data[i]['compound'][0].items()] else []
        if len(info3) == 0:
            kingdom_info,superclass_info,class1_info,subclass_info = [],[],[],[]
        else:
            kingdom_info = [x['value'] for x in info3 if x['name'] == 'kingdom'] # 新增kingdom_info
            superclass_info = [x['value'] for x in info3 if x['name'] == 'superclass']# 新增superclass_info
            class1_info = [x['value'] for x in info3 if x['name'] == 'class']# 新增class1_info
            subclass_info = [x['value'] for x in info3 if x['name'] == 'subclass']# 新增subclass_info
        # 获得数据
        kingdom = None if len(kingdom_info) == 0 else kingdom_info[0]
        superclass = None if len(superclass_info) == 0 else superclass_info[0]
        class1 = None if len(class1_info) == 0 else class1_info[0]
        subclass = None if len(subclass_info) == 0 else subclass_info[0]

        # 信息4： 名字
        name = json_data[i]['compound'][0]['names'][0]['name'] if len(json_data[i]['compound'][0]['names'])!=0 else np.nan

        # 信息5： spectrum
        spec1 = r'{' + json_data[i]['spectrum'].replace(' ', ',') + r'}'
        spec2 = pd.Series(eval(spec1))
        s1 = spec2.sort_values(ascending=False).iloc[:10]
        # 生成碎片的annotation
        frag = [i['name'] for i in json_data[i]['annotations']] if 'annotations' in [k for k,v in json_data[i].items()] else []
        frag_mz = [i['value'] for i in json_data[i]['annotations']] if 'annotations' in [k for k,v in json_data[i].items()] else []
        s2 = pd.Series(frag, frag_mz)
        s2 = s2[~s2.index.duplicated(keep='first')]
        # 合并成dataframe
        df1 = pd.concat([s1, s2], axis=1)
        df1.columns = ['ratio', 'frag']
        df2 = df1[~df1['ratio'].isna()].sort_values(by = 'ratio',ascending = False)
        spec3 = str(df2.loc[:,'ratio'].to_dict())
        spec3_annotation = str(df2.loc[:,'frag'].to_dict())  # 新增spec3——annotation

        # 搜集数据
        Inchikey.append(ik)
        precursors.append(precursor)
        formulas.append(formula)
        smiles.append(smile)
        ion_modes.append(ion_mode)
        instrument_types.append(instrument_type)
        frags.append(spec3)
        collision_energies.append(ce)
        # 新增信息
        cases.append(cas)
        pubchem_cids.append(pubchem_cid)
        inchis.append(inchi)
        total_exact_masses.append(total_exact_mass)
        columns.append(column)
        mass_accuracies.append(mass_accuracy)
        precursor_mzs.append(precursor_mz)
        precursor_types.append(precursor_type)
        ionization_modes.append(ionization_mode)
        kingdoms.append(kingdom)
        superclasses.append(superclass)
        class1s.append(class1)
        subclasses.append(subclass)
        names.append(name)
        frag_annotations.append(spec3_annotation)
    database = pd.DataFrame(
        np.array([Inchikey, precursors, frags,frag_annotations, formulas, smiles, ion_modes, collision_energies, instrument_types,
                  cases,pubchem_cids,inchis,total_exact_masses,columns,mass_accuracies,precursor_mzs,precursor_types,
                  ionization_modes,kingdoms,superclasses,class1s,subclasses,names]).T,
        columns=['Inchikey', 'Precursor', 'Frag','frag annotations', 'Formula', 'Smiles', 'ion_modes', 'collision_energies', 'instrument type',
                 'cas','pubchem_cid','Inchi','total_exact_mass','chromatogram column info','mass_accuracy (ppm)',
                 'precursor mz','precursor_types','ionization_mode','kingdom','superclass','class1s','subclasses','names'
                 ])
    return database

def swath_frag_extract(ms2,mz,frag,error = 50, precursor_ion_start_mass = 99.5):
    '''
    Chromatogram extract based on precusor and fragment.
    :param ms2: ms2 from sep_scans
    :param mz: precursor
    :param frag: fragment to extract
    :param error: mass error window
    :param precursor_ion_start_mass: precursor_ion_start_mass
    :return: rts, eic
    '''
    def swath_window(ms2,precursors = [],precursor_ion_start_mass = precursor_ion_start_mass):
        precursor_ion_start_mass = 99.5
        mz_overlap = 1
        ms_range = {}
        precursor = precursors[0]
        # 第一个要手动
        ms_range = {}
        next_gap = precursors[0] - precursor_ion_start_mass
        ms_range[precursor] = [precursor-next_gap,precursor+next_gap]
        end_mz = round(precursor+next_gap,1)
        for precursor in precursors[1:]:
            next_start_mz = round(end_mz -mz_overlap,1)
            next_gap = precursor - next_start_mz
            end_mz = round(precursor+next_gap,1)
            ms_range[precursor] = [next_start_mz,end_mz]
        return ms_range


    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'],1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)

    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'],1))
        locals()[name].append(scan)

    # 4. 存储变量
    all_data1 = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        all_data1[precursor] = locals()[name]

    ms_range = swath_window(ms2,precursors = precursors,precursor_ion_start_mass = precursor_ion_start_mass)
    for k,v in ms_range.items():
        if (mz<=v[1]-0.5)&(mz>v[0]+0.5):
            scan_index = k
            break
    new_ms2 = all_data1[scan_index]
    rts,eic = extract2(new_ms2,frag,error = error)
    return rts,eic

def swath_frag_raw(ms2,mz,rt, precursor_ion_start_mass = 99.5):
    '''
    Chromatogram extract based on precusor and fragment.
    :param ms2: ms2 from sep_scans
    :param mz: precursor
    :param rt: retention time
    :param precursor_ion_start_mass: precursor_ion_start_mass
    :return: mzs,intensities
    '''
    def swath_window(ms2,precursors = [],precursor_ion_start_mass = precursor_ion_start_mass):
        precursor_ion_start_mass = 99.5
        mz_overlap = 1
        ms_range = {}
        precursor = precursors[0]
        # 第一个要手动
        ms_range = {}
        next_gap = precursors[0] - precursor_ion_start_mass
        ms_range[precursor] = [precursor-next_gap,precursor+next_gap]
        end_mz = round(precursor+next_gap,1)
        for precursor in precursors[1:]:
            next_start_mz = round(end_mz -mz_overlap,1)
            next_gap = precursor - next_start_mz
            end_mz = round(precursor+next_gap,1)
            ms_range[precursor] = [next_start_mz,end_mz]
        return ms_range


    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'],1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)

    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'],1))
        locals()[name].append(scan)

    # 4. 存储变量
    all_data1 = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        all_data1[precursor] = locals()[name]

    ms_range = swath_window(ms2,precursors = precursors,precursor_ion_start_mass = precursor_ion_start_mass)
    for k,v in ms_range.items():
        if (mz<=v[1]-0.5)&(mz>v[0]+0.5):
            scan_index = k
            break
    new_ms2 = all_data1[scan_index]
    for scan in new_ms2:
        if scan.scan_time[0]>rt:
            break
    mzs = scan.mz
    intensities = scan.i
    return mzs,intensities





if __name__ == '__main__':
    pass
# %config InlineBackendlineBackend.figure_format ='retina'
#  plt.rcParams['font.sans-serif'] = 'Times New Roman'  # 设置全局字体
