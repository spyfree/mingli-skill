# Mingli Fortune 命理咨询插件

一条龙紫微斗数 + 八字命理咨询插件，适用于 **Claude Code** 和 **OpenAI Codex**。

- **排盘**：托管 MCP 服务（`https://mcp.lee.locker/mcp`）——真太阳时修正、农历/闰月、早晚子时、多语言输出
- **解读**：`mingli-fortune` skill 驱动的结构化咨询方法论——输入规范化、紫微+八字同口径交叉验证、置信度标注、分领域解读
- **计费**：连接与工具发现免费；排盘调用需要 License Key（**[前往购买](https://lee.locker/mcp)**，当前价格与每日配额以该页面为准）

## 安装

### Claude Code

```bash
/plugin marketplace add spyfree/mingli-skill
/plugin install mingli-fortune@mingli
```

### OpenAI Codex

```bash
codex plugin marketplace add spyfree/mingli-skill
# 然后在 /plugins 中安装 mingli-fortune
```

## 配置 License Key

1. 前往 [lee.locker/mcp](https://lee.locker/mcp) 购买
2. 把拿到的 `ML-XXXX-XXXX-XXXX-XXXX` 设为环境变量：

```bash
export MINGLI_LICENSE_KEY="ML-XXXX-XXXX-XXXX-XXXX"
```

3. 重启你的客户端。没有 key 也可以安装和浏览工具，只有排盘调用会提示购买。

## 使用

直接对 AI 说：

> 帮我算命，看看事业、财运和婚姻。1995 年 3 月 8 日早上 8 点生，男。

Skill 会自动规范化生辰、调用紫微/八字/五行工具、按内置的多流派方法论（紫微三合为骨架 + 飞星四化做应期，八字走格局→旺衰→调候）输出带置信度说明的结构化命理咨询。

**指定流派**：直接说「用盲派看」「走飞星四化」，会切换为该派主框架并标注视角。

**场景入口**（Claude Code）：

| 命令 | 场景 |
|------|------|
| `/mingli-timing` | 事件应期专精——"什么时候适合跳槽/置产/结婚"，飞星转忌串连 + 八字岁运互验 |
| `/mingli-depth` | 格局层次深读——"我能到什么高度"，子平格局派 + 盲派做功交叉验证 |

## 隐私说明

排盘在托管服务端完成，因此每次排盘会把**出生日期、出生时间、性别、经度**发送到 `mcp.lee.locker` 处理。Skill 会在首次排盘前向用户主动说明这一点。除排盘所需字段外，不会转发姓名、对话内容或其他个人信息。数据在服务端的留存与处理受 [服务条款](https://lee.locker/terms) 约束。

## 排障

**`/mcp` 里 mingli 显示连接失败，但我还没买 key**

未设置 `MINGLI_LICENSE_KEY` 时，`.mcp.json` 会发出一个空的 `Authorization: Bearer` 头。部分网关会对"存在但畸形"的凭证直接返回 401，从而连免费的 `initialize` / `tools/list` 也走不通。先确认这一点：

```bash
# 不带 Authorization 头
curl -sS -X POST https://mcp.lee.locker/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'

# 带空 Bearer（模拟未设置环境变量的实际情形）
curl -sS -X POST https://mcp.lee.locker/mcp \
  -H 'Authorization: Bearer ' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'
```

两者行为若不一致，说明服务端需要把空 Bearer 当匿名处理；在修好之前，未购买用户的"可安装可浏览"体验是不成立的。

**排盘结果的时辰/日柱看起来不对**

大概率是两个已知事故源之一，参见 `skills/mingli-fortune/references/input-normalization.md`：

- 真太阳时只修正了一个系统 → 紫微和八字算的不是同一个时刻（见 Chart Consistency Contract）
- 23:00–23:59 出生时日期被进位了两次 → 日柱差一天（见 Day Boundary）

## 目录结构

```
.claude-plugin/   Claude Code 插件清单 + marketplace
.codex-plugin/    Codex 插件清单 + MCP 配置
.mcp.json         Claude Code 的 MCP 服务配置（读 MINGLI_LICENSE_KEY）
commands/         Claude Code 场景入口（/mingli-timing、/mingli-depth）
scripts/          插件清单校验脚本
skills/mingli-fortune/
  SKILL.md        咨询方法论主文件
  references/     输入规范化、解读框架、流派手册、咨询规范
  agents/         Codex skill 元数据（openai.yaml）
```

## 开发

改动清单或 skill 后跑一次校验（无第三方依赖）：

```bash
python3 scripts/validate_plugin.py
```

会检查 JSON 语法、两个 `plugin.json` 的版本号一致、清单里声明的路径存在、SKILL.md frontmatter 合法且 description 未超长、以及文档中引用的 `references/*.md` 均存在。CI 在每次 push 与 PR 上跑同一个脚本。

## 免责声明

输出内容仅供文化娱乐与个人参考，不构成医疗、法律、金融或其他专业建议。

## License

MIT（插件与 skill 内容），见 [LICENSE](LICENSE)。托管排盘服务的使用受 [服务条款](https://lee.locker/terms) 约束。
