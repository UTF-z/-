from main import *

track = {0.2: ([], []),
         0.1: ([], []),
         0.05: ([], []),
         0.02: ([], []),
         0.01: ([], [])}
alpha_list = [0.2, 0.1, 0.05, 0.02, 0.01]
color_list = ['black', 'red', 'blue', 'green', 'purple']
e = "α = {}"
label = []
plt.figure()
for i in range(0, 5):
    alpha = alpha_list[i]
    color = color_list[i]
    points = track[alpha]
    for n in range(2, 30, 1):
        data = data_generation(grp=5000, smp=n)
        error = hypothesis_test_variance(data, np.exp(1), 0, alpha=alpha, mode=2)
        points[0].append(n)
        points[1].append(error)
    l, = plt.plot(points[0], points[1], color=color)
    label.append(l)
plt.legend(label, [e.format(alpha_list[0]), e.format(alpha_list[1]), e.format(alpha_list[2]), e.format(alpha_list[3]),
                   e.format(alpha_list[4])])
plt.grid(b=True, color='gray', alpha=0.5)
plt.xlabel("n")
plt.ylabel("Error rate")
plt.show()
