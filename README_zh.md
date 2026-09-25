<div align="center">

# OmniJev

**全模态 Jev · An omni-modal Jev**

*一次前向、零生成 token：对图片、视频、屏幕和机器人画面提出带类型的问题，得到校准过的概率。*

[![Website](https://img.shields.io/badge/website-omnijev.net-4F46E5)](https://omnijev.net/)
[![Weights](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-tinnel123%2FOmniJev-yellow)](https://huggingface.co/tinnel123/OmniJev)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**北京中关村学院 · 中国科学院自动化研究所 · 智进化**

[项目首页](https://omnijev.net/) · [在线试用](https://omnijev.net/try.html) · [权重](https://huggingface.co/tinnel123/OmniJev) · [English](README.md)

</div>

---

## 它能干什么

OmniJev 是我们自己从头训练的模型——不是套一层 Jev 接口、后面接别人的模型。训练用了 **约 27 万条决策记录、130 万道带类型的问题**，覆盖网页与手机操作、机器人任务（仿真与真机）、视频事件、实时游戏、手势、危险场景和声音。

一个 4B 的模型，**能看图、看视频**，并据此做决策：**操作手机和电脑**、**实时玩游戏**、**操控机器人**、**实时监控摄像头画面**（危险、手势、事件）。它把画面、你的问题和文本上下文一起读，回答是**校准过的概率**而不是生成的文字，并且可以回答"都不是"。

## 它是什么

OmniJev 是一个 *System One* 决策模型。你不是让它写字，而是给它一个"状态"（图片、视频帧、截图、摄像头画面，可附带文本上下文）和一组**带类型的问题**，它在**一次前向、0 个生成 token** 内给每个问题返回一个概率分布：

| 类型 | 问的是 | 返回 |
|---|---|---|
| `choice` | 在这些选项里选哪个（或都不是）？ | 每个选项的概率、`abstain`（都不是的概率）、所选的 key |
| `noul` | 这个陈述对当前状态成立吗？ | 一个校准过的概率 |
| `score` | 在一个有序量表上到哪一级？ | 等级及各级概率 |

同一张截图问十二个问题，代价和问一个差不多。选项还可以是**图中的区域**（`box: [x1, y1, x2, y2]`，坐标 0–1000），"点哪个元素 / 哪一格 / 危险在哪"都是普通的选择题；视频会取 16 帧带时间戳的画面，模型看到的就是这些。

## 已发布的模型

三个尺寸，同一套代码（`mso.infer`）、同一个接口，全部 Apache-2.0，底座都是 Qwen3.5：

| 模型 | 底座 | 权重 | 下载 |
|---|---|---|---|
| **OmniJev-4B** | Qwen3.5-4B | [tinnel123/OmniJev](https://huggingface.co/tinnel123/OmniJev) · 镜像 [tinnel123/OmniJev-4B](https://huggingface.co/tinnel123/OmniJev-4B) | `hf download tinnel123/OmniJev --local-dir ckpt` · `hf download Qwen/Qwen3.5-4B --local-dir base` |
| **OmniJev-2B** | Qwen3.5-2B | [tinnel123/OmniJev-2B](https://huggingface.co/tinnel123/OmniJev-2B) | `hf download tinnel123/OmniJev-2B --local-dir ckpt` · `hf download Qwen/Qwen3.5-2B --local-dir base` |
| **OmniJev-0.8B** | Qwen3.5-0.8B | [tinnel123/OmniJev-0.8B](https://huggingface.co/tinnel123/OmniJev-0.8B) | `hf download tinnel123/OmniJev-0.8B --local-dir ckpt` · `hf download Qwen/Qwen3.5-0.8B --local-dir base` |

下面的所有示例对三个模型都适用：`MSO1("ckpt", "base")` 会根据权重自动选择推理路径。`pip install fla-core` 可选，开启线性注意力快速内核。

## 它能做什么

下面每段动图都是模型没见过的留出样例，计时都是真实测得的延迟。

<table>
<tr>
<td width="50%"><img src="docs/media/web_task.gif" width="100%"><br><sub><b>二十一步网页任务，逐页决策</b> — 每一页模型都判断点哪个元素、做什么操作、是不是最后一步、任务进行到哪。</sub></td>
<td width="50%"><img src="docs/media/robots.gif" width="100%"><br><sub><b>四个机器人任务同时看</b> — 四段 LIBERO-10 任务以视频速度并行；每一帧判断子任务、夹爪下一步方向、是否该抓、是否拿住、第一阶段完成没有。</sub></td>
</tr>
<tr>
<td><img src="docs/media/game.gif" width="100%"><br><sub><b>实时玩游戏</b> — 挡板往哪动、下一个球落在哪格、炸弹要不要砸到、比分如何。每帧一次前向，没有搜索、没有规划器。</sub></td>
<td><img src="docs/media/cua_trace.gif" width="100%"><br><sub><b>一步步操作手机</b> — 下一步做什么动作、多不可逆、屏幕上有没有报错弹窗。</sub></td>
</tr>
<tr>
<td><img src="docs/media/robot_task.gif" width="100%"><br><sub><b>一段长程机器人任务</b> — 两阶段操作任务的 276 帧：指令、子任务、方向、抓取、是否拿住、第一阶段完成没有。</sub></td>
<td><img src="docs/media/robot_monitor.gif" width="100%"><br><sub><b>盯着机器人，逐帧判断</b> — 每帧五个判断；轨道上的琥珀色刻度是真实的抓取时刻。</sub></td>
</tr>
<tr>
<td><img src="docs/media/pointing.gif" width="100%"><br><sub><b>在网格上指点，不需要任何人画框</b> — 在截图和照片上铺一张 96 格的网格；模型先选格子，再放大，再选一次。</sub></td>
<td><img src="docs/media/navigation.gif" width="100%"><br><sub><b>沿着链接一步步走向目标页</b> — 每一跳选哪个链接、每个候选都有概率、到了就停。</sub></td>
</tr>
<tr>
<td><img src="docs/media/hazard.gif" width="100%"><br><sub><b>盯着摄像头看危险</b> — 有没有火或烟、哪种危险、多紧急、在哪个区域。报警条就是模型自己给的概率。</sub></td>
<td><img src="docs/media/gesture.gif" width="100%"><br><sub><b>手势控制</b> — 摄像头前的一个手势变成一条设备指令，只在模型足够有把握时才触发。</sub></td>
</tr>
<tr>
<td><img src="docs/media/events.gif" width="100%"><br><sub><b>判断视频里发生了什么</b> — 事情发生了没有、从哪一帧开始、人还在不在画面里、在做什么。</sub></td>
<td><img src="docs/media/stopwatch.gif" width="100%"><br><sub><b>十个留出样例，一个秒表</b> — 一张照片、一个手机屏幕、一盘棋、一个机器人视角、一整段视频；秒表走的就是模型实际用的时间。</sub></td>
</tr>
<tr>
<td colspan="2"><img src="docs/media/audio.gif" width="100%"><br><sub><b>用看的方式听</b> — 五秒声音画成频谱图和波形：这是什么声音、是不是人发出的、有没有突发的响声、有多响。仓库里另有<a href="docs/media/audio.mp4">带真实声音的那一版</a>。</sub></td>
</tr>
</table>

## 成绩

下表是 **OmniJev-4B**（Qwen3.5-4B）在线上服务路径上的留出准确率，旁边依次是它自己的底座零训练作答、已发布的 **OmniJev-2B** 与 **OmniJev-0.8B**，以及一个**普通微调基线**（同一个 0.8B 底座按常规方式微调成生成文字答案，由 LLM 裁判判分，只给出它训练过的五个题族）。ECE 是 OmniJev-4B 在线上温度下的校准误差。

| 基准（留出） | n | 0.8B 零训练 | 0.8B 普通微调 | OmniJev-0.8B | OmniJev-2B | 4B 零训练 | OmniJev-4B | ECE ↓ |
|---|---|---|---|---|---|---|---|---|
| LIBERO-10 机器人决策 | 1504 | 0.551 | 0.247 | 0.771 | 0.724 | 0.299 | **0.807** | 0.031 |
| Mind2Web 测试集（任务 / 网站 / 领域） | 1500 | 0.401 | 0.193 | 0.596 | 0.631 | 0.303 | **0.733** | 0.038 |
| 网格指点，96 格（网页） | 1500 | 0.384 | – | 0.474 | 0.625 | 0.421 | **0.737** | 0.021 |
| 自建事件时序题（视频源自 Charades-STA 训练集） | 1500 | 0.390 | 0.363 | 0.811 | 0.826 | 0.543 | **0.859** | 0.021 |
| 接物游戏 | 1504 | 0.409 | 0.383 | 0.661 | 0.728 | 0.151 | **0.870** | 0.016 |
| HaGRID 手势 + 火 / 烟 / 武器 | 1500 | 0.529 | 0.620 | 0.969 | 0.984 | 0.683 | **0.987** | 0.009 |
| OK-VQA 答案池 | 1500 | 0.793 | – | 0.656 | 0.765 | **0.860** | 0.809 | 0.021 |
| LongVideoBench 验证集 | 500 | 0.410 | – | 0.486 | 0.502 | **0.585** | 0.582 | 0.073 |
| 长视频 / 规划 / 空间 | 1511 | 0.390 | – | 0.494 | 0.529 | 0.486 | **0.602** | 0.072 |
| 混合决策集（自建）：区域、存在、手机、象棋、短视频 | 1491 | 0.545 | – | 0.604 | 0.623 | 0.582 | **0.661** | 0.079 |
| 维基导航 | 1500 | 0.414 | – | 0.659 | 0.667 | 0.336 | **0.706** | 0.030 |
| 真实机器人操作（MUTEX） | 1500 | 0.442 | – | 0.681 | 0.687 | 0.267 | **0.749** | 0.022 |
| Atari 人类对局 | 1500 | – | – | **0.707** | 0.691 | 0.332 | 0.703 | 0.040 |
| 贪吃蛇 | 1500 | – | – | 0.727 | 0.763 | 0.449 | **0.833** | 0.048 |
| 五子棋 | 1500 | – | – | 0.694 | 0.669 | 0.154 | **0.696** | 0.021 |
| 国际象棋（局部候选走法） | 1500 | – | – | 0.603 | 0.609 | 0.166 | **0.611** | 0.051 |
| AndroidControl 手机操作 | 1502 | – | – | 0.634 | 0.668 | 0.291 | **0.734** | 0.037 |
| ESC-50 声音（频谱图） | 795 | – | – | 0.473 | 0.514 | 0.347 | **0.525** | 0.051 |
| RoboArena 真实机器人回放 | 1503 | – | – | – | – | 0.336 | **0.628** | 0.019 |
| JAT 街机游戏（赛车 / 滑雪 / 乒乓） | 1500 | – | – | – | – | 0.259 | **0.589** | 0.061 |
| 超级马里奥 | 735 | – | – | – | – | **0.464** | 0.339 | 0.184 |
| POPE 物体幻觉（是非题） | 9000 | – | – | – | – | 0.867 | **0.902** | 0.007 |

**这两列该怎么读。** POPE 和 LongVideoBench 是完全留出的：两者的数据一行都没有进过训练，所以那两行的差距是泛化能力。Mind2Web 用该数据集自己的训练集训练、官方测试集评测。其余每一行都是我们自建的题池，按行号哈希留出 8%。底座那一列在所有族上都是零训练，所以除前两行之外，两列的差衡量的是在这一族上训练能带来多少，不是同条件对比。

**有三行是在残缺输入下测得的。** RoboArena、JAT 和超级马里奥这三族的每条记录带不止一张图，而此前线上路径只编码其中第一张，所以这些题实际上是看着一帧作答的。修复和重测后的数字会随下一个版本一起发布；在那之前上表保持测得时的原样，我们不会悄悄改数。

**ECE**（期望校准误差）衡量概率可不可信：它是模型自报的把握和实际答对率之间的平均差距。ECE 0.05 大致意味着模型说"90%"时实际有 85–95% 的概率答对；0 是完美，越低越好。只会输出答案的生成式模型没有这个数。上表的 ECE 用的是随 `head_meta.json` 发布的温度。

**延迟**（一张空闲 NVIDIA A800-SXM4-40GB、线上服务路径、768 token 图片预算、同一张图的多个问题合成一次请求；12 次取中位数，三个模型同一张卡、同一脚本、同条件：`bench/speed_bench.py`，同一张图上固定的 12 道题）：

| 模型 | 1 题 | 3 题 | 6 题 | 12 题 | 12 题时每题 |
|---|---|---|---|---|---|
| OmniJev-4B | 294 ms | 292 ms | 344 ms | 436 ms | 36.3 ms |
| OmniJev-2B | 217 ms | 220 ms | 243 ms | 277 ms | 23.1 ms |
| OmniJev-0.8B | 216 ms | 216 ms | 218 ms | 236 ms | 19.6 ms |

三个模型都是 Qwen3.5 底座、同一条前缀分支推理路径，所以延迟随参数量单调增长（单问 216 ms → 294 ms）。把多个问题合进同一次请求后，每题的开销从 294 ms 降到 36.3 ms——图片只编码一次。这三行是三个尺寸第一次在同一块卡上测得；此前本页的数字来自不同硬件，行与行之间并不可比。

## 快速开始

```bash
git clone https://github.com/tinnel123666888/OmniJev && cd OmniJev
python -m venv venv && ./venv/bin/pip install -r requirements.txt     # torch, transformers>=5, pillow

hf download tinnel123/OmniJev --local-dir ckpt                       # OmniJev 权重
hf download Qwen/Qwen3.5-4B --local-dir base               # 底座（或软链本地副本）
```

**图片。** questions 是 `id -> 问题` 的字典，答案按同样的 id 返回。

```python
from mso.infer import MSO1

m = MSO1("ckpt", "base")
answers = m.system_one(
    {"images": ["screen.png"]},
    {"op":   {"type": "choice", "instructions": "Which operation comes next?",
              "criteria": {"click": "tap an element", "type text": "", "scroll": ""}},
     "risk": {"type": "score",  "instructions": "How irreversible is the next action?",
              "levels": ["harmless", "needs care", "irreversible"]},
     "err":  {"type": "noul",   "instructions": "This screen shows an error dialog."}})
# answers["op"]   -> {"choice": "click", "probabilities": {"click": 0.81, ...}, "abstain": 0.02, "confidence": 0.81}
# answers["risk"] -> {"score": "needs care", "probabilities": {...}, "confidence": 0.7}
# answers["err"]  -> {"noul": 0.01}
```

**视频。** `video_state` 把 16 帧带时间戳的画面拼成一张图（需要 PATH 里有 ffmpeg 和 ffprobe），模型整体判断这段视频。

```python
from mso.video import video_state

answers = m.system_one(
    video_state("clip.mp4"),                                  # 在视频旁边写出 clip.mosaic.jpg
    {"happened": {"type": "noul",   "instructions": "The person opens the door."},
     "doing":    {"type": "choice", "instructions": "What is the person doing?",
                  "criteria": {"cooking": "", "cleaning": "", "reading": "", "eating": ""}},
     "progress": {"type": "score",  "instructions": "How much of the action is shown?",
                  "levels": ["none of it", "the beginning", "most of it", "all of it"]}})
```

**文本上下文。** 放在问题前面即可，模型会和画面一起读（线上 API 对 `state.text` 就是这么做的）。

```python
task = "Task: book a table for two at 7 pm on the restaurant's website."
answers = m.system_one(
    {"images": ["page.png"]},
    {"op":   {"type": "choice", "instructions": task + "\nWhich operation comes next?",
              "criteria": {"click": "tap an element", "type text": "", "select": "", "scroll down": ""}},
     "done": {"type": "noul",   "instructions": task + "\nThe task is finished."}})
```

**区域。** 选项可以是区域而不是名字：`"options": [{"key": "a", "region": {"box": [120, 40, 380, 90]}}, ...]`（坐标 0–1000）。`mso/templates.py` 里有浏览器、手机、机器人、游戏、网格等现成的问题模板（`templates.questions("libero", instruction=...)`），`mso/infer.py` 也可以当命令行用（`--ckpt --model --image --questions`）。问题用英文效果最好。

## 它是怎么训的

OmniJev 从一个开源的 4B 视觉语言模型（Qwen3.5-4B）出发，由我们自己端到端训练，教它"做判断"而不是"写字"：一个很小的决策层直接从模型的概率里读出每个问题的答案，不生成任何文字，也就不会答出格式外的东西。训练数据是 **约 27 万条决策记录、130 万道带类型的问题**，用公开数据集和我们自己渲染的画面构造——网页与手机操作、机器人任务与真机回放、实时游戏与棋类、日常动作与长视频、手势与危险场景、以及画成频谱图的声音——我们公布的每个数字都只在模型没见过的留出样本上测得。训练采用**严格评分规则**下的监督训练，这类规则奖励的是"既答对、又对自己的把握诚实"的概率；最后在留出数据上做一次校准，所以"把握超过 0.8 才行动"这样的阈值是有意义的。选项的呈现方式保证答案不依赖选项顺序。权重在 [Hugging Face](https://huggingface.co/tinnel123/OmniJev)（在底座之上约 290 MB）。

## 许可与引用

**Apache-2.0**（见 [LICENSE](LICENSE)），代码和权重均适用；底座沿用其自身许可。

```bibtex
@misc{omnijev2026,
  title  = {OmniJev: an omni-modal System One decision model},
  author = {Xu, Tianrun and Fan, Hongbang and Lin, Jiahao and Zhu, Zilin and Diao, Zhenxin and Guo, Longteng and Liu, Jing},
  note   = {Beijing Zhongguancun Academy; Institute of Automation, Chinese Academy of Sciences; Zevo},
  year   = {2026},
  url    = {https://github.com/tinnel123666888/OmniJev}
}
```

## 团队与联系

OmniJev 由 **北京中关村学院**、**中国科学院自动化研究所**、**智进化** 联合研发。

主要贡献者

- 徐添润 (Tianrun Xu) · Core Developer
- 范红榜 (Hongbang Fan)
- 林佳豪 (Jiahao Lin)
- 朱子林 (Zilin Zhu)
- 刁镇薪 (Zhenxin Diao)
- 郭龙腾 (Longteng Guo) · Project Lead
- 刘静 (Jing Liu) · Corresponding Author

联系我们——学术交流、项目合作：s-xtr24@bza.edu.cn

<div align="center"><sub>北京中关村学院 · 中国科学院自动化研究所 · 智进化 · <a href="https://omnijev.net/">omnijev.net</a></sub></div>
