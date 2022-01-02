from main import *
data = data_generation(sigma_sqr=1, grp=2000, smp=5)
track_delta = []
track_y1 = []
track_y2 = []
for sigma in np.linspace(0.1, 20, 500):
    delta = sigma / np.sqrt(1)
    ln_delta = np.log(delta)
    y_1 = hypothesis_test_variance(data, np.square(sigma), 0, alpha=0.05, mode=2)
    y_2 = hypothesis_test_variance(data, np.square(sigma), alpha=0.05, mode=2)
    track_delta.append(ln_delta)
    track_y1.append(y_1)
    track_y2.append(y_2)
plt.figure()
a, = plt.plot(track_delta, track_y1, color='blue')
b, = plt.plot(track_delta, track_y2, color='red')
plt.xlabel("ln(delta)")
plt.ylabel("Error rate")
plt.legend([a, b], ["μ known", "μ unknown"])
plt.show()