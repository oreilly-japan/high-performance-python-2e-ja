import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

outfile = "generated_ols_data.pickle"
NBR_DAYS = 14
NBR_PEOPLE = 100_000
# NBR_PEOPLE = 5_000

lam = 60  # 100
np.random.seed(0)  # fix the seed
hours_per_day_per_person = np.random.poisson(lam=lam, size=(NBR_DAYS, NBR_PEOPLE)).T
hours_per_day_per_person = hours_per_day_per_person / 60

df = pd.DataFrame(hours_per_day_per_person).astype(np.float_)
print(f"Writing {df.shape} to {outfile}")
print(df.head())

df.to_pickle(outfile)

ax = plt.subplot()
df[:3].T.plot(ax=ax, marker="o")
ax.set_title("Random hours of mobile phone usage for 3 people")
ax.set_xlabel("Days")
ax.set_ylabel("Hours of usage")
ax.set_ylim(0, 1.5)
ax.legend()
plt.savefig("random_hours_mobile_phone_usage_3_people.png")
