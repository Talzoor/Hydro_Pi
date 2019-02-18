import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15,5))

# plt.subplot(2, 2, 1)
# this "A" is clipped in the plot
# plt.annotate("A",
#              xy = (-0.25, 1.1),
#              xytext = (-0.25, 1.1),
#              xycoords = 'axes fraction',
#              textcoords = 'axes fraction',
#              fontsize=30)
plt.annotate("A",
             xy = (0, 0),
             xytext = (0, 1.2),
             xycoords = 'axes fraction',
             textcoords = 'axes fraction',
             fontsize=30)
# ax = plt.subplot(1, 1, 1)
# plt.subplot(2, 2, 3)
# plt.subplot(2, 2, 4)
plt.tight_layout()
plt.subplots_adjust(top=0.9)
ax = plt.gca()
ax.axis('equal')
plt.show()
