---
title: "云原生与 Web3 学习资料"
weight: 5
type: docs
bookToC: true
---

# 云原生与 Web3 学习资料

这里整理 Kubernetes、CNCF、DevOps 和 Web3 方向的系统学习入口，适合从容器编排入门，逐步过渡到云原生工程实践和新技术方向扩展。

资料来源为技术书栈公开页面；本站整理学习路径、主题说明和原文入口，完整正文以原站链接为准。

## 建议学习顺序

1. 先看 Kubernetes 入门实战类资料，建立 Pod、Deployment、Service、Ingress、ConfigMap、Secret 等核心对象的直觉。
2. 再看 Kubernetes 实践指南，把部署、扩缩容、滚动更新、健康检查、存储和网络串起来。
3. 接着看 CNCF 与阿里巴巴云原生公开课，理解云原生生态、微服务、可观测性、服务网格和平台工程。
4. 然后补 DevOps 实战，把 CI/CD、环境管理、自动化发布、监控告警和团队协作流程连成工程链路。
5. 最后把 Web3 入门资料作为扩展方向，理解区块链、智能合约、钱包、DApp 和链上应用的基本概念。

## Kubernetes 从上手到实践

这份资料适合作为 Kubernetes 第一阶段学习入口，重点放在核心概念和动手实践之间的衔接。学习时建议边看边搭建本地集群，用 `kubectl` 反复操作资源对象。

- 适合阶段：Kubernetes 入门、容器编排初学
- 学习重点：集群基础、工作负载、服务暴露、配置管理、基础运维
- 原文地址：[Kubernetes 从上手到实践](https://study.disign.me/document/Kubernetes%20%E4%BB%8E%E4%B8%8A%E6%89%8B%E5%88%B0%E5%AE%9E%E8%B7%B5/)

## Kubernetes 实践入门指南

这份资料更适合在已经理解 Kubernetes 基础对象后继续学习，用来把日常部署、服务访问、配置注入、状态管理和排障流程串成完整实践。

- 适合阶段：Kubernetes 基础巩固、项目部署练习
- 学习重点：应用部署、服务发现、滚动更新、资源管理、常见排障
- 原文地址：[Kubernetes 实践入门指南](https://study.disign.me/document/Kubernetes%20%E5%AE%9E%E8%B7%B5%E5%85%A5%E9%97%A8%E6%8C%87%E5%8D%97/)

## Kubernetes 入门实战课

这份课程型资料适合跟着章节做练习，把容器镜像、编排对象、服务访问和应用发布放在同一条学习线上。建议配合真实 Demo 项目练习 YAML 编写。

- 适合阶段：实战练习、课程跟学
- 学习重点：资源清单、应用编排、服务发布、基础运维动作
- 原文地址：[Kubernetes 入门实战课](https://study.disign.me/document/Kubernetes%E5%85%A5%E9%97%A8%E5%AE%9E%E6%88%98%E8%AF%BE/)

## CNCF X 阿里巴巴云原生技术公开课

这门公开课适合用来建立云原生全局视角。除了 Kubernetes 本身，还可以顺带理解 CNCF 生态、容器、微服务、服务网格、可观测性和云原生应用治理。

- 适合阶段：云原生体系化学习、技术全景建立
- 学习重点：CNCF 生态、Kubernetes、微服务、可观测性、服务治理
- 原文地址：[CNCF X 阿里巴巴云原生技术公开课](https://study.disign.me/document/CNCF%20X%20%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%BA%91%E5%8E%9F%E7%94%9F%E6%8A%80%E6%9C%AF%E5%85%AC%E5%BC%80%E8%AF%BE/)

## DevOps 实战笔记

DevOps 实战笔记适合放在 Kubernetes 学习之后阅读。它能帮助你把代码提交、构建、测试、镜像制作、部署、监控和回滚理解成一条持续交付链路。

- 适合阶段：工程实践、发布流程建设、运维协作
- 学习重点：CI/CD、自动化发布、环境管理、监控告警、交付效率
- 原文地址：[DevOps 实战笔记](https://study.disign.me/document/DevOps%E5%AE%9E%E6%88%98%E7%AC%94%E8%AE%B0/)

## Web 3.0 入局攻略

这份资料适合作为 Web3 方向的入门索引，适合在后端、云原生和工程基础之外扩展区块链应用视角。阅读时可以重点关注钱包、智能合约、DApp 和链上数据交互。

- 适合阶段：Web3 概念入门、方向扩展
- 学习重点：区块链基础、智能合约、钱包、DApp、链上生态
- 原文地址：[Web 3.0 入局攻略](https://study.disign.me/document/Web%203.0%E5%85%A5%E5%B1%80%E6%94%BB%E7%95%A5/)

## 搭配练习

建议用一个最小 Go Web 服务串联这些资料：

1. 用 Docker 打包 Go 服务镜像。
2. 写 Kubernetes Deployment 和 Service 部署到本地集群。
3. 添加 ConfigMap、Secret 和健康检查。
4. 用 GitHub Actions 构建镜像并触发部署。
5. 接入 Prometheus 或 Grafana 做基础观测。

这条练习线能把 Kubernetes、云原生和 DevOps 的知识点落到一个真实项目上。
