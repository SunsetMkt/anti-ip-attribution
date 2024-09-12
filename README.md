# anti-ip-attribution

针对部分网站显示 IP 归属地的流量分流规则

项目作者无法保证配置文件一定能起到作用，有可能会触发账号风控。

## 使用之前

请在使用前详细阅读`rules.yaml`内容，内部注释包含部分可选规则，请酌情参考。

强烈建议 Fork 自己的一份配置文件，不要直接使用最新的。

## 自动生成的配置文件

|                                     文件                                     |                                                              用途                                                               |
| :--------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: |
|                   ~~[parser.yaml](generated/parser.yaml)~~                   |             ~~适用于 Clash for Windows 的配置文件预处理功能，详见https://docs.cfw.lbyczf.com/contents/parser.html~~             |
|              [rule-provider.yaml](generated/rule-provider.yaml)              |            适用于 Clash 的 Rule Provider 功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider            |
|       [rule-provider-direct.yaml](generated/rule-provider-direct.yaml)       |  仅包含 DIRECT 规则，适用于 Clash 的 Rule Provider 功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider  |
|        [rule-provider-proxy.yaml](generated/rule-provider-proxy.yaml)        | 仅包含需要代理的规则，适用于 Clash 的 Rule Provider 功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider |
|       [rule-provider-reject.yaml](generated/rule-provider-reject.yaml)       |  仅包含 REJECT 规则，适用于 Clash 的 Rule Provider 功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider  |
|                      [surge.list](generated/surge.list)                      |                                                         Surge 分流规则                                                          |
|                [quantumultx.list](generated/quantumultx.list)                |                                                      QuantumultX 分流规则                                                       |
| [quantumultx-domesticsocial.list](generated/quantumultx-domesticsocial.list) |                                        QuantumultX 分流规则，策略组名称为 DomesticSocial                                        |

## 关于 Clash for Windows

Clash for Windows 已于 2023.11.2 (UTC+8) 删库，将不再积极支持`parser.yaml`（适用于 Clash for Windows 的配置文件预处理功能）。

如有需要，您仍可通过 [Internet Archive 的镜像](https://web.archive.org/web/20231030023222/https://github.com/Fndroid/clash_for_windows_pkg/releases)下载 Clash for Windows。若无此类特殊需求，您也可将使用的 Clash GUI 替换为[clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev)。

## 关于自动生成

本仓库使用 GitHub Actions 从`rules.yaml`中生成配置文件，详见`generate.py`。

## PR & 贡献

仓库所有者和开发者的能力不能保证持续、高效维护地此仓库。如若发现改进或更好的方案，欢迎 PR。

只需要修改`rules.yaml`，其余配置文件会自动生成。

如果您对项目改进有兴趣，欢迎 Email 联系我获取 Collaborator 权限。

## 使用提示

不建议使用手机客户端访问这些网站，应用可能会包含难以寻找的 API 地址获取信息。

## 免责声明

本项目仅用于学习交流，请在遵守所在地法律法规的前提下使用。

本项目记录的 API 域名地址信息可以被任何人通过开发人员工具获取，没有经过逆向工程或网络攻击，不构成入侵计算机系统。

请不要在中华人民共和国境内使用此项目。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SunsetMkt/anti-ip-attribution&type=Date)](https://star-history.com/#SunsetMkt/anti-ip-attribution&Date)
