import matplotlib
import matplotlib.pyplot as plt
import numpy as np

normal_distribution_table = {0.95: 1.645,
                             0.975: 1.96,
                             0.99: 2.327,
                             0.995: 2.575}
t_distribution_table = np.loadtxt("t_distribution_table.txt")
t_index = {0.05: 1,
           0.025: 2,
           0.01: 3,
           0.005: 4,
           0.0025: 5,
           0.001: 6,
           0.0005: 7}
x_distribution_table = np.loadtxt("x_distribution_table.txt")
x_index = {0.995: 1,
           0.99: 2,
           0.975: 3,
           0.95: 4,
           0.9: 5,
           0.1: 6,
           0.05: 7,
           0.025: 8,
           0.01: 9,
           0.005: 10}


def data_generation(mean=0, sigma_sqr=1, grp=1000, smp=100):
    dataset = np.ndarray([grp, smp])
    for i in range(grp):
        dataset[i] = np.random.normal(mean, sigma_sqr, smp)
    # print(dataset, '\n')
    return dataset


def average(dataset):
    avg = np.ndarray([dataset.shape[0]])
    for i in range(dataset.shape[0]):
        avg[i] = np.mean(dataset[i])
    # print(avg, '\n')
    return avg


def variance(dataset):
    var = np.ndarray([dataset.shape[0]])
    for i in range(dataset.shape[0]):
        var[i] = np.var(dataset[i], ddof=1)
    # print(var, '\n')
    return var


def hypothesis_test_mean(dataset, mean, sigma_sqr=None, alpha=0.05, mode=1, to_draw=False):
    avg = average(dataset)
    if sigma_sqr is None:
        s = variance(dataset)
        distribution = 't'
    else:
        s = sigma_sqr
        distribution = 'n'
    test_statistic = abs(avg - mean) / np.sqrt(s / dataset.shape[1])
    test_result = np.ndarray(test_statistic.shape)
    rejection_region = None
    title = None
    if distribution == 't':
        title = "(avg-μ)/sqrt(S_sqr/n) 的分布, μ = {}, alpha = {}".format(mean, alpha)
        rejection_region = (t_distribution_table[dataset.shape[1] - 1][t_index[alpha / 2]],)
        for i in range(test_result.shape[0]):
            test_result[i] = test_statistic[i] > rejection_region
    if distribution == 'n':
        title = "(avg-μ)/sqrt(σ_sqr/n) 的分布, μ = {}, alpha = {}".format(mean, alpha)
        rejection_region = (normal_distribution_table[1 - alpha / 2],)
        for i in range(test_result.shape[0]):
            test_result[i] = (test_statistic[i] > rejection_region)

    # print(test_result, '\n')
    if to_draw:
        draw_hist(test_statistic, rejection_region, title=title)

    rejection_percent = np.sum(test_result, 0) / test_result.shape[0]
    if mode == 1:
        return rejection_percent
    else:
        return 1 - rejection_percent


def hypothesis_test_variance(dataset, sigma_sqr, mean=None, alpha=0.05, mode=1, to_draw=False):
    avg = average(dataset)
    avg = np.expand_dims(avg, axis=1)
    avg = np.repeat(avg, dataset.shape[1], axis=1)
    title = None
    if mean is not None:
        title = "Σ(xi-μ)_sqr/sigma_sqr 的分布"
        test_statistics = np.square(dataset - mean) / sigma_sqr
        n = dataset.shape[1]
    else:
        title = "Σ(xi-avg)_sqr/sigma_sqr 的分布"
        test_statistics = np.square(dataset - avg) / sigma_sqr
        n = dataset.shape[1] - 1
    test_statistics = np.sum(test_statistics, axis=1)
    rejection_region = (x_distribution_table[n][x_index[alpha / 2]],
                        x_distribution_table[n][x_index[1 - alpha / 2]])

    if to_draw:
        draw_hist(test_statistics, axvline=rejection_region, title=title)

    test_result = np.ndarray(test_statistics.shape)
    for i in range(test_result.shape[0]):
        test_result[i] = (test_statistics[i] < rejection_region[1] or test_statistics[i] > rejection_region[0])

    rejection_percent = (np.sum(test_result, axis=0) / test_result.shape[0])
    if mode == 1:
        return rejection_percent
    else:
        return 1 - rejection_percent


def draw_hist(data, axvline=None, bins=30, normed=0, facecolor='blue', edgecolor='black', xlabel="x", ylabel="y",
         title="title", alpha=0.8):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.hist(data, bins=bins, density=normed, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if axvline is not None:
        for x in axvline:
            plt.axvline(x, color='red')
    plt.show()


data = data_generation(smp=5)
print("**********对正态分布总体期望的假设检验***********")
print("H0: μ = mean；H1: μ ≠ mean\n")
print("σ²已知的情况, 第二类错误率：", hypothesis_test_mean(data, 2, 1, mode=2), '\n')
print("σ²未知的情况, 第二类错误率：", hypothesis_test_mean(data, 2, mode=2), '\n')
print("**********对正态分布总体方差的假设检验***********")
print("H0: σ² = sigma；H1: σ² ≠ sigma\n")
print("μ已知的情况, 第二类错误率：", hypothesis_test_variance(data, 16, 0, mode=2), '\n')
print("μ未知的情况, 第二类错误率：", hypothesis_test_variance(data, 16, mode=2), '\n')
