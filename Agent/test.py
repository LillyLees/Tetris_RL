from Train import rewards, losses
import matplotlib
import matplotlib.pyplot as plt

plt.ioff()
plt.scatter(rewards, losses)
plt.xlabel("Reward")
plt.ylabel("Loss")
plt.show()
