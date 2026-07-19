# Mingli Fortune 命理咨询插件

一条龙紫微斗数 + 八字命理咨询插件，适用于 **Claude Code** 和 **OpenAI Codex**。

- **排盘**：托管 MCP 服务（`https://mcp.lee.locker/mcp`）——真太阳时修正、农历/闰月、早晚子时、6 种语言输出，7 个专业工具
- **解读**：`mingli-fortune` skill 驱动的结构化咨询方法论——输入规范化、紫微+八字交叉验证、置信度标注、分领域解读
- **计费**：连接与工具发现免费；排盘调用需要 License Key（**[$6.99 一次买断，每日 200 次调用](https://lee.locker/mcp)**）

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

1. 前往 [lee.locker/mcp](https://lee.locker/mcp) 购买（$6.99 买断）
2. 把拿到的 `ML-XXXX-XXXX-XXXX-XXXX` 设为环境变量：

```bash
export MINGLI_LICENSE_KEY="ML-XXXX-XXXX-XXXX-XXXX"
```

3. 重启你的客户端。没有 key 也可以安装和浏览工具，只有排盘调用会提示购买。

## 使用

直接对 AI 说：

> 帮我算命，看看事业、财运和婚姻。1995 年 3 月 8 日早上 8 点生，男。

Skill 会自动规范化生辰、调用紫微/八字/五行工具、输出带置信度说明的结构化命理咨询。

## 目录结构

```
.claude-plugin/   Claude Code 插件清单 + marketplace
.codex-plugin/    Codex 插件清单 + MCP 配置
.mcp.json         Claude Code 的 MCP 服务配置（读 MINGLI_LICENSE_KEY）
skills/mingli-fortune/
  SKILL.md        咨询方法论主文件
  references/     输入规范化、解读框架等参考资料
  agents/         Codex skill 元数据（openai.yaml）
```

## 免责声明

输出内容仅供文化娱乐与个人参考，不构成医疗、法律、金融或其他专业建议。

## License

MIT（插件与 skill 内容）。托管排盘服务的使用受 [服务条款](https://lee.locker/terms) 约束。
