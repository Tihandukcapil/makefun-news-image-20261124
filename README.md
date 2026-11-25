# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Tihandukcapil/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Tihandukcapil/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image newspaper front page summing up Tuesday 24 November 2026 in four stories: Jensen Huang reinstated as Nvidia CEO 11 days after resigning; Iran vowing to fight the US naval blockade as Qatar's prime minister meets Vance and Rubio; the Gaza strike that killed Hamas security chief Naeem Abu Nahel; and the overnight Russian strike on Zaporizhzhia that killed 2 and wounded 40. Every headline was checked against live reporting (Reuters, CNN, TechCrunch, Just Security). The four scene panels were generated clean, with no baked-in text; all headlines are drawn crisply with PIL so nothing is garbled.

## Run it

```sh
python3 main.py
```

That writes the front page to `/output/entry.png` (1024x1024 PNG, deterministic — two runs write the same bytes). `compose.py` rebuilds `entry.png` from the panels in `panels/` if you want to regenerate it.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ks2r30ft&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
