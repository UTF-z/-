from main import *
data = data_generation(sigma_sqr=1, grp=5000, smp=5)
print("**********对正态分布总体期望的假设检验***********")
print("H0: μ = mean；H1: μ ≠ mean")
print("μ0 from 0 to 3, step = 0.1")
to_draw = False
track_x = []
track_ny = []
track_ty = []
for miu in np.linspace(-2, 2, 401):
    if miu == 0.5 or miu == 1 or miu == 1.5 or miu == 2:
        to_draw = True
    else:
        to_draw = False
    # print("******* μ0 = {} *******".format(miu))
    a = hypothesis_test_mean(data, miu, 1, mode=2, alpha=0.05)
    # print("σ²已知的情况, 第二类错误率：", a)
    b = hypothesis_test_mean(data, miu, mode=2, alpha=0.05)
    # print("σ²未知的情况, 第二类错误率：", b)
    track_x.append(miu)
    track_ny.append(a)
    track_ty.append(b)
plt.figure()
n1, = plt.plot(track_x, track_ny, color='red')
t1, = plt.plot(track_x, track_ty, color='blue')
plt.xlabel("μ0")
plt.ylabel("Error rate")
plt.grid(b=True, color='gray', alpha=0.5)
plt.legend([n1, t1], ["σ^2 known", "σ^2 unknown"])
plt.show()

