# 完整成稿对照：2.3.0 与 2.4.0 候选

本文保存实际执行的完整正文和作者说明，未在评审后润色。作者工作稿均依据已发表研究重构，并非原作者历史稿件。原论文仅作此次任务的事实材料，未并入日常写作资料。

## 第一批：candidate-r2，四篇此前未参与改规则的论文

候选先冻结，再开放题目、原文和评审材料；比较完成后这四题转为开发材料。后续候选必须使用另一批来源，结果不能混称为一次固定版本试验。

### Q01：Anticipatory Anxiety and Wishful Thinking

Jan B. Engelmann、Maël Lebreton、Nahuel A. Salem-Garcia、Peter Schwardmann、Joël J. van der Weele（2024）《Anticipatory Anxiety and Wishful Thinking》，American Economic Review，114(4)。DOI：10.1257/aer.20191068。

任务：Please revise this draft introduction into a version I can use in the paper. The flow still feels uneven. Keep it to 400–450 words, use the attached paper for the research details, and give me the revised introduction followed by a short note on the main changes.

来源定位：One-based PDF physical pages 1–6 correspond to printed pages 926–931. The complete PDF is available; this range contains the background, study overview, and essential design information.

#### 重构工作稿

This is a reconstructed working draft created for a writing exercise from the research reported in the attached published article. It is not a draft written by the original authors, and no original author revision history is implied.

People sometimes judge uncertain future events in ways that make those events less worrying. Such judgments matter because beliefs guide decisions, while thinking about a possible bad outcome can itself be unpleasant. Wishful thinking may therefore have a role in economic behavior. Models of motivated beliefs suggest that people can trade the emotional benefits of an optimistic belief against the material costs of being wrong (Bénabou and Tirole, 2002; Brunnermeier and Parker, 2005). Accuracy incentives are relevant to this trade-off, although understanding their effects requires empirical evidence as well as a theoretical account.

We study these issues in five experiments with 1,714 participants. Participants identify visual patterns, and particular patterns are associated with the possibility of an electric shock or a monetary loss. They are paid for correct answers. Their responses do not determine whether the adverse outcome occurs, so giving the more comforting answer cannot prevent the outcome. We vary the ambiguity of the patterns and the rewards for accuracy. Repeated trials also allow us to examine differences between participants rather than looking only at average behavior. This approach provides a controlled setting for studying wishful thinking.

There is a broad literature on motivated cognition, including beliefs that protect a favorable self-image and beliefs that help people persuade others. The evidence specifically concerning wishful thinking is less consistent. Coutts (2019) finds it in one of three tasks, whereas Barron (2021) finds no evidence of asymmetric updating about monetary prizes. Field research includes people facing disease and other threatening events, while laboratory studies have often used desirable outcomes. These studies have different settings and methods, and the relation between everyday optimism and the laboratory findings remains an important issue.

In our experiments involving adverse outcomes, participants are less accurate when identifying patterns associated with a shock or loss. More ambiguous patterns produce more wishful thinking. Increasing accuracy rewards does not reduce this bias in the first three experiments, even though participants report greater concentration and take longer to answer. In the fourth experiment, participants can improve the information available by spending more time on the task, and greater incentives reduce wishful thinking. The fifth experiment compares monetary losses with gains: wishful thinking appears for losses but not for gains. Self-reported anxiety is also positively related to wishful thinking across individuals.

These findings contribute to understanding motivated beliefs and the effects of incentives. They suggest that the emotions associated with adverse outcomes deserve attention, as do the properties of the task in which beliefs are formed. They also show why it is useful to examine ambiguity, incentives, and individual differences together when studying wishful thinking.

#### 2.3.0 完整正文

Why do people remain optimistic when they face potentially harmful outcomes? Optimism may reflect a desire to avoid anxiety as well as a response to available information. Such wishful thinking matters because beliefs influence decisions even when they also provide immediate emotional benefits. Models of motivated beliefs formalize this tension as a trade-off between anticipatory utility and the material costs of inaccurate beliefs (Bénabou and Tirole, 2002; Brunnermeier and Parker, 2005). Whether people respond to these costs, however, remains an empirical question.

Existing evidence leaves two related issues unresolved. Field studies often document optimism in the face of illness or other threats, but they cannot readily isolate the motives underlying those beliefs. Laboratory evidence is mixed: Coutts (2019) finds wishful thinking in one of three tasks, while Barron (2021) finds no asymmetric updating about monetary prizes. Because laboratory studies have largely examined desirable outcomes, their findings need not capture the role of anxiety about adverse events. Moreover, accuracy incentives may discipline beliefs differently depending on whether additional effort can improve the evidence available.

We investigate these issues in five experiments with 1,714 participants. Participants identify visual patterns for accuracy rewards; in the adverse-outcome conditions, one pattern is associated with a possible electric shock or monetary loss. Their answers cannot affect whether that outcome occurs. Reporting the more comforting pattern therefore offers no material protection, allowing us to examine biased inference separately from attempts to avoid the outcome. We vary signal ambiguity and accuracy rewards, and repeated trials permit individual-level measures of wishful thinking.

Participants are less accurate when identifying patterns associated with shocks or losses, and greater ambiguity increases this bias. In the first three experiments, higher accuracy rewards increase response times and self-reported concentration but do not reduce wishful thinking. In the fourth, where participants can gather better information by spending more time on the task, greater rewards reduce the bias. Larger monetary losses raise reported anxiety but do not significantly increase wishful thinking. Self-reported anxiety is positively associated with wishful thinking across individuals. The fifth experiment finds wishful thinking for monetary losses but not gains.

These findings identify two conditions that help explain when wishful thinking emerges and when incentives constrain it. The loss–gain contrast and the association with anxiety support negative emotions as a plausible driver of comforting beliefs, offering a way to reconcile mixed laboratory evidence with optimism under threat. The incentive results indicate that raising the cost of error alone need not correct such beliefs: the effectiveness of rewards depends on whether effort can reduce ambiguity. Together, the experiments connect the emotional appeal of optimism to the informational conditions under which beliefs are formed.

篇幅记录：439 English words (whitespace)。

作者说明：

Reorganized the introduction around two unresolved questions: the role of adverse outcomes and the conditions under which accuracy incentives work. Connected each to the design and findings, and added the reported null effect of loss magnitude so that anxiety remains a plausible explanation rather than an established mechanism.

#### 2.4.0 candidate-r2 完整正文

Beliefs about future adversity affect both decisions and how people feel while awaiting an outcome. Wishful thinking may ease this anticipatory discomfort, but inaccurate beliefs can also carry material costs. Models of motivated beliefs formalize this trade-off between emotional benefits and decision quality (Bénabou and Tirole, 2002; Brunnermeier and Parker, 2005). Whether people make this trade-off, and whether rewards for accuracy constrain it, are therefore central to understanding when optimism persists despite incentives to be correct.

Existing evidence leaves these questions unresolved. Field studies describe optimistic beliefs among people facing disease and other threats, but cannot readily isolate the motives behind those beliefs. Laboratory findings are mixed: Coutts (2019) finds wishful thinking in one of three tasks, while Barron (2021) finds no asymmetric updating about monetary prizes. These laboratory studies largely concern desirable outcomes. Their findings therefore leave open whether the prospect of avoiding anxiety about losses motivates wishful thinking more strongly than the prospect of enjoying anticipated gains.

We investigate this possibility in five experiments with 1,714 participants. Participants earn rewards for identifying visual patterns, some of which are associated with a possible electric shock or monetary loss. Their answers cannot affect whether the adverse outcome occurs. Thus, reporting the comforting pattern cannot avert a shock or loss, but believing that this pattern appeared may relieve anxiety. We vary signal ambiguity and accuracy rewards, and use repeated trials to measure wishful thinking within individuals. A final experiment compares monetary losses with gains.

Participants are less accurate when the displayed pattern is associated with an adverse outcome, and more ambiguous evidence produces greater wishful thinking. The loss–gain comparison reproduces wishful thinking for losses but not gains, while self-reported anxiety is positively associated with the bias across individuals. However, increasing the size of potential losses raises reported anxiety without significantly increasing wishful thinking. The evidence thus points to the relevance of negative emotions without establishing that stronger anxiety translates directly into greater bias.

Accuracy incentives reveal a related limit to the trade-off account. In the first three experiments, higher rewards increase response times and reported concentration but do not improve accuracy or reduce wishful thinking. In the fourth, participants can obtain better information by spending more time on the task, and higher rewards reduce the bias. Together, these results suggest that incentives can constrain wishful thinking by improving the evidence on which beliefs rest, rather than simply making errors more costly. They help reconcile mixed evidence on motivated beliefs by identifying both the emotional setting in which wishful thinking arises and the conditions under which accuracy incentives can curb it.

篇幅记录：429 English words (whitespace)。

作者说明：

Reorganized the introduction around two linked questions: why anticipated losses elicit wishful thinking and when accuracy incentives can curb it. The design now explains how comforting beliefs are separated from control over outcomes. I also restored the finding that larger losses increased reported anxiety without significantly increasing wishful thinking, which qualifies the proposed emotional account.

### Q02：后发企业如何利用全球生产网络构建自主产品开发平台？——对长城汽车氢能技术产品开发的纵向案例研究

周麟、贺俊、兰宗敏、李志斌（2023）《后发企业如何利用全球生产网络构建自主产品开发平台？——对长城汽车氢能技术产品开发的纵向案例研究》，管理世界，2023年第11期。DOI：10.19744/j.cnki.11-1235/f.2023.0130。

任务：这是案例发现部分中写2018—2020年平台形成的一段，我觉得前后衔接还不够顺。请根据附件里的研究材料修订成可放进论文的正文，约900字。最后简要说一下主要改动。

来源定位：页码为从1开始的PDF物理页。第4–6页对应刊页155–157，介绍案例与资料；第9–11页对应刊页160–162，为本段所用阶段的案例事实。可按需要阅读完整PDF。

#### 重构工作稿

这是一份依据附件已发表论文的研究事实重构的练习用工作稿，不是原作者提供的历史草稿，也不代表原作者真实写作过程。

2018—2020年是长城汽车氢能自主产品开发平台形成的重要时期。在前一阶段，企业已经引入国外专家，建立研发团队和测试条件，也形成了产品开发方向。但有了这些基础，还需要真正推出产品。国外专家主导的团队看重技术成熟度，产品落地速度与长城原有的开发节奏并不完全一致。企业因此开始把更多精力投入核心功能实现，希望尽快在氢能市场上形成自己的产品和身份。

这一时期发生的重要事件是收购上燃动力。上燃动力有商用燃料电池汽车的开发和示范运营经验，但当时遇到了资金困难。长城的氢能开发主要面向乘用车，上燃动力主要面向商用车，双方的经验有所不同。长城于2018年8月正式控股上燃动力，次年4月完成全资控股并增资。收购之后，长城向上燃动力输入研发管理体系，支持实验室建设和人才引进，并提供氢能技术中心的测试条件。上燃动力过去较多依靠科研项目，这些支持也涉及其面向商业化量产所需的质量管理与供应商考核。

与此同时，长城以XEV项目组为主体成立未势能源，推动氢能业务独立市场化运营。运营主控权逐步转交国内专家，一部分自主培养的工程师走上技术管理岗位。慕尼黑和横滨团队的工作重点也发生变化，分别更加集中于储氢技术开发、储氢瓶原材料测试和机理研究。国外专家继续参与研发，只是承担的工作与初期不同。这些变化使国内外团队都找到了这一时期的工作重点。

在保定与上海之间，管理层没有立即合并两条开发路线。两支团队继续面向乘用车和商用车推进项目，各自掌握研发细节、设计方案及零部件选型，但重大节点评审统一开展，并交流阶段成果和技术困难。具体项目中也有国外团队参与。例如70MPa减压阀开发遇到结构设计问题时，慕尼黑团队提出方案，双方经过交流和试验完成设计；测试中发现锁定压力过高，又共同讨论可能原因并进行复现。

2019年11月，上燃动力发布100kW商用燃料电池发动机“超越—300E”，这是长城氢能领域第一款达到量产级别的产品。2020年9月，未势能源又发布乘用燃料电池发动机、电堆及储氢系统的相关产品，产品序列逐步形成。产品开发过程中，各方有不同的资源和经验，收购、投入、人员调整及合作都发挥了作用。平台的形成因此体现了企业多方面工作的推进，也说明产品成果与团队之间的学习交流具有密切联系。

#### 2.3.0 完整正文

2018—2020年，长城汽车氢能业务的重点由搭建研发支撑体系转向核心功能的产品化。前期国外专家主导的研发强调技术成熟后再推进产品开发，与企业缩短决策周期、加快市场进入的要求形成张力。此时，长城既要跨越研发与量产之间的边界，也需要通过自主产品改变市场对其燃油车企的既有认知，由此推动全球生产网络围绕产品落地重新分工。

收购上燃动力为这一调整提供了国内支点。上燃拥有商用燃料电池汽车的开发与示范运营经验，能够补充长城面向乘用车、从材料和零部件切入的研发积累。长城于2018年8月控股上燃，并于次年4月完成全资控股和增资，随后输入研发管理体系、资金及测试条件，完善其品控、供应商考核和质量追溯。双方的互补因而不仅体现为应用场景拓展，也体现为将上燃的集成经验与长城的基础研发和量产管理结合，为技术转化提供组织支撑。

与国内支点扩展相伴，长城于2019年4月以XEV项目组为主体成立未势能源，推动独立市场化运营，并逐步将运营与研发主控权交给国内专家。慕尼黑和横滨团队分别转向储氢技术开发、储氢瓶原材料测试与机理研究，国外专家由战略主导者转为具体项目的合作者。这一调整将前期引入的技术优势落实到产品开发中的具体瓶颈，同时使自主培养的工程师承担更多技术管理责任。

新的分工通过并行开发与共同解决问题转化为学习过程。保定和上海团队继续沿乘用车与商用车路线探索，自主决定研发细节、设计方案和零部件选型，同时统一开展重大节点评审，交流开发成果、试验数据与技术困难。保定向上海输入零部件层面的技术认知，上海则反馈产品开发和系统集成经验。国外团队也参与问题解决：在70MPa减压阀开发中，慕尼黑团队提出反压平衡式结构方案，经双方交流与试验完成定型；针对测试中锁定压力过高的问题，双方共同回溯原因并复现验证，直至通过测试。这种并行互补式协调保留了技术路线差异，同时通过共创式学习将分散的经验转化为可共享的产品开发知识。

2019年11月，上燃发布100kW商用燃料电池发动机“超越—300E”，成为长城氢能领域首款量产级产品，其开发管理和检验规范也为后续产品化提供了基础。2020年9月，未势进一步发布乘用燃料电池发动机、电堆及储氢系统相关产品。伴随产品序列形成，团队将项目中的设计、试验和集成经验积累为从底层元件到产品组构的向上开发能力，使前期研发支撑体系具备了跨技术轨道组织自主产品开发的基础。

篇幅记录：872 个汉字；983 个非空白字符（含标点、数字、字母）。

作者说明：

将事件罗列调整为产品化目标、网络分工、共创学习与平台形成之间的过程解释，补充了双向知识交流如何支持开发能力积累。产品类型沿用工作稿及附件正文的“商用”；附件图1将“超越—300E”写作“乘用”，与正文存在不一致。

#### 2.4.0 candidate-r2 完整正文

2018—2020年，长城汽车氢能产品开发的重心由搭建研发基础转向实现核心功能。前期引入的国外专家重视技术成熟度，但其较长的决策和研发周期难以满足企业加快产品落地的要求。长城还需以可投入市场的产品改变其传统燃油车企的品牌认知。因此，这一阶段的任务是把已有技术与研发条件转化为产品开发能力，并通过产品进入氢能市场。

收购上燃动力为这一转变补充了应用端经验。长城从材料级研发起步，主要面向乘用车；上燃动力则积累了商用燃料电池汽车的系统集成和示范运营经验，两者的知识基础与应用场景具有互补性。长城于2018年8月控股上燃动力，次年4月完成全资收购并增资，随后导入研发管理体系，投入实验室和人才建设，并提供氢能技术中心的测试条件。这些支持既缓解了资金约束，也补足了上燃动力从科研项目走向商业化量产所需的品控、供应商考核与质量追溯条件。

互补资源能否进入产品开发，取决于团队如何共同使用这些资源。保定和上海继续沿乘用车与商用车路线并行探索，各自决定研发细节、设计方案和零部件选型，同时接受统一的重大节点评审，交流阶段成果、试验数据与技术难题。保定团队向上海团队输入零部件层面的技术认知，上海团队则反馈系统集成与实际开发经验。由此，两条路线在保留探索空间的同时，通过具体产品问题开展相互学习。

国外团队的作用也随之转向项目合作。2019年4月，长城以XEV项目组为主体成立未势能源，将运营主控权逐步转交国内专家，部分自主培养的工程师也走上技术管理岗位；慕尼黑和横滨团队则分别聚焦储氢技术、储氢瓶材料测试与机理研究。70MPa减压阀开发体现了这一分工：国内团队理解减压原理，却缺少将其实现为精密机械结构的经验，慕尼黑团队提出反压平衡式结构方案，双方经交流和试验完成设计，并共同复现、排查锁定压力过高的问题。国外知识因而嵌入了具体产品瓶颈的解决过程。

2019年11月，上燃动力发布100kW商用燃料电池发动机“超越—300E”，成为长城氢能领域首款达到量产级别的产品。此次开发还积累了过程管理、体系审核和检验检测规范，为后续产品化提供了基础。2020年9月，未势能源进一步发布乘用燃料电池发动机、电堆及储氢系统相关产品。平台形成由此不仅表现为产品序列扩展，也体现为各团队在并行互补式协调下开展共创式学习，逐步形成从底层元件到系统产品的自主开发能力。

篇幅记录：851 个汉字；963 个非空白字符（含标点、数字、字母）。

作者说明：

将事件罗列改为“产品化要求—资源互补—分工与学习—平台能力形成”的过程解释，补明了保定与上海交换何种知识、国外专家如何参与解决产品难题，并用首款量产级产品留下的开发规范说明其对后续产品化的作用。

### Q03：中国城市群空间结构分布与演变特征

黄妍妮、高波、魏守华（2016）《中国城市群空间结构分布与演变特征》，经济学家，2016年第9期。DOI：10.16158/j.cnki.51-1312/f.2016.09.006。

任务：下面是结果部分后面的综合讨论草稿，读起来有些重复。我想把它改成约850字的论文正文，请结合附件核对和修订，最后简要说明主要改动。

来源定位：页码为从1开始的PDF物理页；第2–8页对应刊页51–57。其中第2–3页为指标和数据口径，第4–8页包含表1–4及结果说明。可按需要阅读完整PDF。

#### 重构工作稿

这是一份依据附件已发表论文的研究事实重构的练习用工作稿，不是原作者提供的历史草稿，也不代表原作者真实写作过程。

利用2007—2014年的市辖区人口资料，对我国十大城市群进行测度后发现，城市群之间的空间结构差异较为明显，而且不同城市群在观察期内发生的变化也不相同。本文使用帕累托指数、mono指数和四城市首位度进行考察。三个指标都涉及城市规模及其排序，能够从不同方面描述城市群的结构。从测度结果来看，城市群空间结构具有多样性，不能把所有城市群的变化都归为同一种趋势。

先看mono指数，成渝和关中两个城市群在各年份均大于1，属于单中心结构。山东半岛和长江中游城市群的指数则均小于1，而且观察期末低于期初，其中山东半岛由0.3327降至0.2346，长江中游由0.8755降至0.7071。中原城市群的变化比较突出，2007年为0.7094，2010年为1.3218，2014年为1.2857。长三角的mono指数由1.1757下降到0.9708，珠三角也呈下降趋势。以上结果说明，不同城市群的变化速度和方向有一定差别。从各年的取值还可以看出，一些城市群的变化主要集中在个别年份，另一些则较为平缓，平均结果并未呈现所有城市群的具体轨迹。

再看帕累托指数，长三角由1.0185升至1.0936，中原由1.4064降至0.9343，山东半岛则由1.5919升至1.8817。其他城市群的变化幅度有所不同，例如辽中南的指数基本稳定。这部分结果同样反映了城市群之间的差异。长三角和山东半岛的帕累托指数都在增加，而中原城市群的指数则在下降，变化方向并不相同。

首位度结果也值得关注。东部城市群的平均首位度从0.8356降至0.7526，中部从0.7313升至0.9386，西部则经历先下降后上升，2014年为1.9011。东北的辽中南城市群变化较小。具体到城市群，山东半岛2014年的首位度为0.4456，成渝为2.0255，关中为1.7767，中原则从2007年的0.6908升至2014年的1.2006。四城市首位度反映最大城市相对于随后三座城市的规模，这些差异有助于了解首位城市在各自城市群中的位置。

研究期内，苏州、南京、杭州和石家庄等城市还进行了行政区划调整，市辖区人口随之发生变化。总体而言，十大城市群表现出了不同的规模分布与演变轨迹。城市群建设应当结合当地结构特点，重视大中小城市之间的关系，并在优化空间布局时考虑各自的发展条件。对城市群差异的认识有助于为后续研究和空间结构优化提供依据。

#### 2.3.0 完整正文

2007—2014年十大城市群的差异，既体现为首位城市相对规模不同，也体现为城市等级体系的演变方向不同。三项指标提供了互补视角：帕累托指数描述整体位序—规模关系，mono指数反映前几位城市的规模梯度，四城市首位度则衡量最大城市相对于随后三市人口之和的规模。因而，判断集中或分散趋势，需要结合指标含义和具体年份，不能只比较数值增减或区域平均值。

成渝和关中的mono指数各年均大于1，2014年首位度分别为2.0255和1.7767，表明首位城市在人口规模上占据明显优势。山东半岛和长江中游的mono指数则始终小于1，且分别由0.3327、0.8755降至0.2346、0.7071，前几位城市的规模梯度进一步趋缓。两者2014年的首位度分别为0.4456和0.6765，与较为分散的头部规模分布一致。这一对照说明，规模差异较小与首位城市优势突出在不同城市群中同时存在，单一的集中化或多中心化叙事难以概括整体变化。

跨指标比较进一步揭示了结构变化的层次。中原的帕累托指数由1.4064降至0.9343，接近位序—规模基准；与此同时，mono指数由0.7094升至1.2857，首位度由0.6908升至1.2006，显示头部城市之间的集中程度增强。整体等级关系更接近基准，并不意味着首位优势减弱。长三角的帕累托指数由1.0185升至1.0936，而mono指数由1.1757降至0.9708，两者数值方向相反，却均与规模梯度趋缓相容。相较之下，辽中南各项指标变化较小，等级体系较为稳定。

区域均值也应结合城市群轨迹解读。东部平均首位度由0.8356降至0.7526，中部由0.7313升至0.9386，但中原与长江中游的变化方向相反，中部均值上升不能代表所有城市群。西部平均首位度先降后升，也不宜表述为持续集中。

上述演变首先反映市辖区人口口径下的规模重排。苏州、南京、杭州和石家庄等城市的行政区划调整改变了人口统计范围，因此，部分年份的指标跳变不能全部解释为人口迁移或经济活动集聚。空间结构优化需要先区分首位优势、整体层级与统计边界的变化，再结合城市功能和发展条件讨论分工协作；仅凭这些人口规模指标，尚不足以认定某种结构必然具有更高效率。

篇幅记录：683 个汉字；914 个非空白字符（含标点、数字、字母）。

作者说明：

将逐项复述改为城市群对照与跨指标解释，区分整体等级关系、头部规模梯度和首位优势。帕累托指数按附件公式α=1/q解释，避免将偏离1直接等同于首位城市集聚；同时将行政区划调整与人口口径联系，限制对实际集聚和最优结构的推断。

#### 2.4.0 candidate-r2 完整正文

2007—2014年十大城市群的测度结果表明，空间结构差异既体现为首位城市优势的强弱，也体现为不同层级城市规模关系的变化。帕累托指数概括全部样本城市的位序—规模分布，mono指数侧重前几位城市的规模梯度，四城市首位度则衡量第一大城市相对于随后三座城市的规模。因此，三个指标应相互参照，不能将其变化简单归并为同一种集聚或分散趋势。

成渝和关中的mono指数在各年均大于1，且2014年首位度分别为2.0255和1.7767，显示出持续较强的首位城市优势。山东半岛和长江中游则呈现不同格局：两者mono指数始终小于1，分别由0.3327、0.8755降至0.2346、0.7071，头部城市间的规模梯度进一步趋缓。“多中心化”因此并非所有城市群共同经历的过程。

中原城市群更能体现综合指标的必要性。其帕累托指数由1.4064降至0.9343，更接近位序—规模分布的基准值1；但mono指数由0.7094升至1.2857，四城市首位度也由0.6908升至1.2006。也就是说，整体规模分布接近这一基准，并不等同于首位城市优势减弱。与此同时，mono指数在2010年已升至1.3218，说明期初与期末的差异包含明显的阶段性跃变，不能描述为持续、平稳的单中心化。

区域均值也需要放回各城市群的轨迹中理解。东部平均首位度由0.8356降至0.7526，与长三角、珠三角头部城市规模差距缩小的方向一致；中部平均值由0.7313升至0.9386，却包含中原首位优势增强与长江中游首位度下降两种相反变化。因而，区域平均水平可以概括差异，却不能替代对各城市群内部结构的判断。

上述变化还受到市辖区统计边界的影响。研究期内，苏州、南京、杭州和石家庄的行政区划调整扩大了相应市辖区人口规模，指标变动因而同时包含人口增长与统计范围变化，不能全部解释为实际人口迁移。本文据此刻画的是市辖区口径下的城市规模关系，尚不足以判断城市间功能联系或集聚效率。空间结构优化应先识别具体城市群的层级关系及其变化来源，再结合交通、就业等联系考察调整方向，不能仅以是否多中心或是否接近某一指数阈值作为优劣标准。

篇幅记录：679 个汉字；879 个非空白字符（含标点、数字、字母）。

作者说明：

按不同指标所刻画的结构层次重组讨论，压缩逐项复述，并以中原城市群说明帕累托指数接近1不等于首位优势减弱。保留区域内部的相反变化，将行政区划调整与统计口径的限制直接纳入解释，避免从规模分布直接推断功能联系或效率。

### Q04：Working hard for money decreases risk tolerance

Christopher J. Bechler、Samina Lutfeali、Szu-chi Huang、Joshua I. Morris（2024）《Working hard for money decreases risk tolerance》，Journal of Consumer Psychology，34。DOI：10.1002/jcpy.1365。

任务：I need to shorten this discussion for the manuscript. Please reduce it to 260–290 words and make the English smoother while keeping the important substance. You can check the attached paper where needed. Give me the revised passage and a brief note on the main edits.

来源定位：One-based PDF pages 1–3 correspond to printed pages 110–112; PDF pages 5–8 correspond to printed pages 114–117. These cover the framing, designs, findings, and discussion. The complete PDF is available.

#### 重构工作稿

This is a reconstructed working draft created for a writing exercise from the research reported in the attached published article. It is not a draft written by the original authors, and no original author revision history is implied.

Our four incentivized experiments show that the effort involved in earning money can affect how consumers subsequently risk it. Across different tasks and payment arrangements, participants generally took less risk after working harder. The studies include decisions about which investment to choose and how much money to invest, extending the finding beyond a single risk measure. This matters because the way consumers acquire money may influence financial decisions even after the money has been received. Our findings therefore add effortful earning to the factors considered in research on risk taking.

Experiment 2 also shows why the relationship is not easy to infer from an overall correlation. Participants who completed more work across the experiment tended to choose riskier investments on average. Within participants, however, greater effort was associated with less risk, and the workload manipulation produced the predicted negative effect. The experiment allowed people to choose their effort and used both salary and commission payment structures. Thus, the positive association between people and the negative relationship within a person appeared in the same setting. This distinction is important when interpreting evidence about hard work and investing.

We explain the effect in terms of how people experience the money they acquire. More effort may make earnings feel more personally owned and more valuable, making their possible loss less acceptable. Experiment 3 found support for a sequence involving valuation and aversion to loss. Experiment 4 provided evidence involving psychological ownership and valuation. Together, these findings support our proposed account of why greater earning effort can be followed by lower risk tolerance. They also connect this research to work on ownership and to the idea that money is not always treated as psychologically interchangeable.

The currency study suggests one way this process can vary. In Experiment 4, participants who had never owned cryptocurrency worked to earn funds that would be donated to Ukraine. Working harder for dollars reduced risk taking, but participants took more risk when the high-effort payment was an equivalent amount of Bitcoin rather than dollars. The currency comparison was accompanied by differences in perceived ownership and valuation. The supplemental study also found attenuation when effort was linked to obtaining an investment opportunity rather than to accumulating money. These results point to the importance of what the effort is understood to produce.

The findings may be relevant when earnings can be spent or invested soon after work. Such situations make it useful to ask whether the effort of earning carries over into the next financial decision. Further research could test these processes in actual financial settings and examine how they change with the time between earning and investing. The present results provide reasons to investigate these possibilities, while the experimental tasks offer an initial basis for understanding them.

#### 2.3.0 完整正文

Across four incentivized experiments, greater earning effort generally reduced subsequent risk taking, whether measured by investment choice or the amount invested. The results extend the study of risk tolerance to how money is acquired: effort can shape consumers’ treatment of earnings even after payment.

Experiment 2 highlights why aggregate correlations can obscure this effect. Participants who completed more work overall chose riskier investments on average, whereas greater effort within participants was associated with less risk taking. The workload manipulation also reduced risk taking across salary and commission conditions. Distinguishing differences between people from changes within a person is therefore essential to interpreting the effort–risk relationship.

The evidence supports an account in which effort increases the perceived ownership and value of earnings, making potential losses less acceptable. Experiment 3 supported a sequence involving valuation and aversion to loss; Experiment 4 linked psychological ownership and valuation to risk taking. Thus, equal amounts of money need not carry equal psychological value.

The currency comparison further qualifies this account. In Experiment 4, participants who had never owned cryptocurrency earned funds for donation to Ukraine. Greater effort reduced risk taking with dollars, but, under high effort, participants took more risk with an equivalent amount of Bitcoin than with dollars. This comparison was accompanied by differences in perceived ownership and valuation. The supplemental study likewise found attenuation when effort was tied to securing an investment opportunity rather than accumulating money, suggesting that what effort produces matters.

These findings warrant investigation in settings where earnings can be spent or invested immediately. Field research should examine their relevance to actual financial decisions and how the interval between earning and investing affects the relationship.

篇幅记录：275 English words (whitespace)。

作者说明：

Condensed repeated statements of contribution and practical relevance while retaining the between-person/within-person distinction, mechanism evidence, and both boundary tests. Kept the Bitcoin result as a currency comparison under high effort, consistent with the study’s design.

#### 2.4.0 candidate-r2 完整正文

Across four incentivized experiments, greater earning effort reduced subsequent risk taking, affecting both investment choice and the amount invested. Effort thus changes how consumers treat money after receiving it. Experiment 2 shows why comparisons between people can obscure this effect: participants who worked more overall chose riskier investments, whereas greater effort within individuals was associated with less risk. The workload manipulation also reduced risk taking under both salary and commission pay.

Our account links these decisions to the experience of ownership: money earned through greater effort may feel more personally owned and valuable, making its loss more painful. Experiment 3 supported a sequence involving valuation and aversion to loss; Experiment 4 provided complementary evidence involving psychological ownership and valuation. These findings extend the role of ownership to effortfully acquired money, suggesting that earning history can influence risk taking even after payment.

The currency comparison further specifies the role of ownership. In Experiment 4, participants who had never owned cryptocurrency earned funds for donation to Ukraine. Greater effort reduced risk taking with dollars, but participants took more risk with Bitcoin than with equivalent dollar earnings under the same high workload. This difference was accompanied by lower perceived ownership and valuation of Bitcoin. The supplemental study also attenuated the negative effort–risk relationship by linking effort to obtaining an investment opportunity rather than accumulating money. What effort is understood to produce therefore matters for subsequent risk taking.

These findings motivate examining financial decisions made soon after work, when the experience of earning may remain salient. Whether the effects persist in actual financial settings, and how they change as the interval between earning and investing increases, remain questions for future research.

篇幅记录：277 English words (whitespace)。

作者说明：

Removed repeated statements of the main effect and its relevance. The shorter discussion preserves the distinction between comparisons across people and changes within a person, the complementary mechanism evidence, and both boundary tests. The Bitcoin result remains tied to the donation setting and the comparison under equal high workloads.

## 第二次冻结：candidate-r3 / 2.3.0

两题在 r3 冻结前未向规则修改者开放；每版各生成一次，以下保持实际输出，未在评审后拼接两版优点。R01、R02 的独立审阅均判持平。R01 主编偏好候选而独立审阅认为优势抵销；R02 两者均判平。主编与独立审阅均为模型代理，没有人类评审。

### R01：能源变革与生态福利绩效研究——基于新能源示范城市设立的准自然实验

陈利、姚凤禹、苏宇童（2024），工业技术经济，2024年第10期（总第372期），98–108。DOI：10.3969/j.issn.1004-910X.2024.10.011。

任务：下面是我准备放在论文末尾的“结论与政策启示”草稿，现在篇幅过长，重点也有些散。请实质改写为550—650汉字左右、可以直接入稿的正文。材料和顺序都可以取舍、调整，只给修改后的正文。

来源定位：物理页从1开始；PDF物理页1–11对应期刊印刷页98–108，印刷页=物理页+97。 核对相关页：1, 2, 3, 4, 5, 7, 8, 9, 10。

#### 重构工作稿

这是依据发表论文的研究事实重构的练习稿，不是原作者真实的历史工作稿。组织方式和措辞由任务编制者重新撰写；发表论文仅作为事实来源，不被预设为完美写作范本。

新能源示范城市建设是推动能源变革的重要政策工具，其意义不仅在于增加新能源使用，还在于能源投入和环境负担能否转化为更好的经济与社会发展结果。生态福利绩效把资源、环境与福利放在同一评价框架内。因此，评价这一政策时，既需要关注能源结构调整，也需要关注城市发展为居民带来的福利产出。这也是本文分析新能源示范城市政策效果的出发点。

本文使用2007—2021年全国279个城市的平衡面板数据，以2014年首批新能源示范城市政策为研究对象。样本中71个试点城市构成处理组，共得到4185个城市年度观测值。生态福利绩效采用Super-SBM模型测算，投入端包括资源消耗与污染排放，产出端包括人均GDP、平均受教育年限和人口平均预期寿命，能够从多个方面反映城市发展的综合绩效。模型控制城市和年份固定效应，并纳入财政投入、对外开放、信息化、人力资本及政府研发投入等变量。

实证结果显示，新能源示范城市政策与生态福利绩效的提高相联系。加入控制变量及城市、年份固定效应后，政策系数为0.110，在10%的水平上显著。倾向得分匹配后进行双重差分估计、采用合成双重差分方法以及替换相关指标，均得到方向一致的结果。这些检验为政策的积极效果提供了进一步支持，也表明从生态福利绩效视角评价能源转型具有价值。

关于政策发挥作用的途径，本文分别以技术创新、产业结构优化和资源依赖度作为被解释变量进行估计。技术创新用授权专利总数的对数衡量，产业结构指标由三次产业增加值占比加权构造，资源依赖度则以采掘业人员占比表示。政策变量对前两项指标的估计系数为正，对资源依赖度的估计系数为负。上述结果与本文提出的三条作用路径相符，也使政策讨论能够进一步联系到创新要素、产业发展和资源利用方式。

从城市之间的差异看，行政等级与政策变量的交互项为正。分组结果中，东部、西部和非资源型城市的政策系数显著，而中部和资源型城市的系数未达到显著水平。因此，不同城市的政策表现并不完全相同，讨论政策推广时仍需注意城市所处的区位、行政条件和资源条件。仅依据总体估计结果安排相同的建设任务，可能忽略这些差异所反映的问题。

政策实施需要把新能源利用与城市产业发展联系起来。地方政府可以结合已有技术和基础设施条件安排能源项目，支持新能源技术应用，吸引技术人才，并为产业多样化创造条件。对于资源依赖较强的城市，能源建设还应关注原有产业结构对转型的约束，探索新能源产业与当地发展基础的衔接。上述安排应根据当地条件逐步推进，并结合实施结果进行调整。

本文的研究表明，新能源示范城市政策为提高城市生态福利绩效提供了一个可行方向。生态福利绩效是由多项投入产出指标构成的效率评价，并非直接询问居民幸福感得到的结果；研究也主要围绕首批试点及样本期内表现展开。对政策成效的评价仍应结合这些研究范围，继续考察不同城市的后续变化。

#### 2.3.0 完整正文

本文基于2007—2021年279个城市的数据，考察2014年首批新能源示范城市政策与生态福利绩效的关系。控制城市、年份固定效应及相关因素后，政策系数为0.110，在10%水平上显著；匹配后双重差分、合成双重差分及指标替换检验的结果方向一致。研究支持从资源环境投入与福利产出的关系评估能源转型成效，将经济、教育和健康产出纳入政策评价。这里的绩效改善指综合效率提高，并不等同于居民主观幸福感上升。

进一步分析显示，政策与技术创新、产业结构优化正向相关，与资源依赖度负向相关，为三条作用路径提供了支持，但尚不能据此确认完整的因果传导链条。行政等级与政策变量的交互项显著为正；东部、西部及非资源型城市的政策系数显著，中部及资源型城市未达显著水平。后者既不意味着政策无效，也不足以单凭显著性差异判定组间效果不同。

据此，地方政府应把新能源项目布局与产业转型相衔接，依据已有技术和基础设施条件支持技术应用与人才集聚，促进产业多样化。资源依赖较强的城市尤其需要评估原有产业结构对新能源发展的约束，选择能够衔接当地产业基础的建设路径。政策推广宜结合城市条件分步推进，并以实施后的绩效变化调整建设任务和配套支持，避免把总体估计结果直接转化为统一的投入要求。

在评价上，应持续跟踪资源消耗、污染排放与各项福利产出，辨别综合效率变化的具体来源，尤其关注资源投入增加而福利改善不足的情形。本文证据限于首批试点和样本期内表现，后续评估还需检验改善能否持续，以及能否推广至不同条件的城市。

篇幅记录：562 个汉字；去空白共 628 字符。

#### 2.4.0 candidate-r3 完整正文

新能源示范城市政策与城市生态福利绩效提高相联系，说明能源转型的成效可以从资源环境投入与福利产出的关系加以考察。基于2007—2021年279个城市的双重差分估计，首批试点政策的系数为0.110，在10%水平上显著；匹配后估计、合成双重差分及指标替换的结果方向一致。这里的福利产出涵盖经济、教育和健康，该结果不能直接解释为居民主观幸福感提高。

政策实施还伴随技术创新水平提高、产业结构优化和资源依赖下降，与三条作用路径的预期相符，但尚不足以识别各路径对绩效改善的独立贡献。对地方政府而言，这提示能源项目建设应与本地创新和产业发展相衔接：依托既有技术与基础设施支持新能源应用，引进所需人才，并为产业多样化创造条件。资源依赖较强的城市应重点关注原有产业结构对转型的约束，探索新能源产业与当地发展基础的衔接。

政策推广需要保留因地制宜的空间。行政等级交互项为正，支持较高行政等级城市政策作用更强的判断；东部、西部和非资源型城市的分组系数显著，中部和资源型城市则未达到显著水平。分组结果不足以单独确认组间差异，也不能将不显著结果等同于政策无效。推广时宜依据区位和资源禀赋调整建设任务，并持续评估政策表现尚不明确的城市。

研究结论限于首批试点及样本期。后续评价既要关注新能源利用规模，也应追踪资源消耗、污染排放与福利产出的共同变化。地方政府可将这些变化作为调整建设重点和推进节奏的依据，检验能源项目及产业配套能否转化为持续的生态福利绩效改善。

篇幅记录：555 个汉字；去空白共 612 字符。

判读：候选更早给出结论，并让作用路径紧接政策选择；基线对投入增加而福利改善不足的评价情形更具体。两者都有直接采用价值，保守判平。

### R02：Does Expressing Anxiety at Work Help or Hurt? The Affiliative and Social Distancing Consequences of Coworker Anxiety Expression

Diwan Li、Katrina Jia Lin、Bonnie Hayden Cheng、Yidong Tu（2026），Personnel Psychology，2026; 00:1–23。DOI：10.1111/peps.70035。

任务：Please substantially revise my General Discussion so that it makes a more focused and convincing argument. I have room for about 400–450 words and need a section I can insert directly into the manuscript. You may reorganize the text and leave out material that does not earn its space. Please return only the revised section.

来源定位：1-based physical PDF pages; physical pages 1–23 match the printed article pages 1–23. 核对相关页：1, 2, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18。

#### 重构工作稿

This is a practice draft reconstructed from the facts reported in a published article, not an authentic historical draft by its authors. The curator independently wrote its organization and wording. The published article is a factual source, not a perfect writing exemplar.

General Discussion

Workplace anxiety is important for employees and for the people around them. Previous work has often considered what anxiety does to the person experiencing it, while anxiety expression can also be a source of information for a coworker. Our research examines this interpersonal side and therefore adds to research on workplace anxiety. It also contributes to emotions as social information theory by examining the cognitive responses that follow an emotional display. Anxiety is a negative emotion, but the reactions to its expression need not all be negative.

In Study 1, 144 employees in China provided 1,174 matched daily observations over ten workdays. Each employee reported on a selected coworker. On days of stronger perceived coworker anxiety expression, employees reported greater perspective taking and greater perceived incompetence. These responses were associated with more helping and more ostracizing behavior, respectively, later in the day. In Study 2, 262 British employees recalled an anxious and a neutral episode involving a selected coworker on separate days. This study also supported the two indirect paths. The two studies provide evidence from everyday observation and from a recall manipulation, which are useful in different ways.

These findings matter because an anxious expression can suggest that someone needs assistance, but it can also be read as a sign of weakness. The former interpretation is consistent with taking the coworker's perspective, while the latter is consistent with seeing the coworker as less competent. The same employee can therefore report responses associated with affiliation and with distance within a workday. Our account concerns fluctuations in responses to a particular coworker, rather than a comparison of permanently helpful and permanently unhelpful employees. This provides another contribution to the literature and shows why studying daily experiences is valuable.

Rivalry also matters for these responses. In both studies, greater rivalry strengthened the path involving perceived incompetence and ostracizing behavior. The evidence on the helping side was less consistent: rivalry weakened the affiliative path in Study 1, but the corresponding moderation was not supported in the main Study 2 analysis. Rivalry refers here to a relationship with a particular coworker, rather than general competitiveness. The samples came from different countries, although differences between the designs mean that these findings cannot establish a cultural explanation. Relationship context is consequently relevant to understanding the interpersonal meaning of anxiety.

There are other useful observations. Both studies found that observing or recalling anxiety expression was associated with the observer's own anxiety. However, felt anxiety did not predict subsequent helping or ostracizing in the main models. Cognitive responses and emotional transmission therefore deserve further attention. The experiment supports causal conclusions about cognitive responses to the manipulated recall, whereas the links from cognition to later behavior remain correlational. The daily outcomes were self-reported. In Study 1, ratings from 93 coworkers correlated with self-reported helping but not with self-reported ostracism, leaving a particular measurement concern for the latter.

Our findings suggest that employees could pause before interpreting a coworker's anxiety as incompetence and consider the demands the coworker is facing. Shared goals and cooperative interactions may also help limit rivalry, although we did not test these practices as interventions. Future research could examine emotional expression in hierarchical relationships, differences in authenticity, and forms of anxiety unrelated to the expresser's work. More daily reports from coworkers would be helpful as well. Taken together, the research suggests that anxiety expression has both benefits and costs and that the reactions of others deserve more attention.

#### 2.3.0 完整正文

General Discussion

Anxiety expression presents coworkers with two possible readings of the same display: a need for support and a lack of competence. Across a daily field study and a recall experiment, anxiety expression was linked to greater perspective taking and perceived incompetence, which predicted later helping and ostracizing behavior, respectively. This dual pattern concerns fluctuations within ongoing relationships, as each observer reported on the same coworker across occasions.

Within the emotions as social information framework, these findings distinguish two inferences that can accompany the same negative display. Perspective taking concerns understanding the coworker’s viewpoint; perceived incompetence concerns judgments of the coworker’s capability. Understanding the demands facing someone need not resolve doubts about their ability to meet them. This distinction explains why attending to a coworker’s needs and maintaining social distance can be compatible responses over a workday. The evidence also directs attention to interpretation alongside emotional transmission: observing or recalling anxiety expression was associated with observers’ own anxiety in both studies, but felt anxiety did not predict subsequent behavior in the main models. This pattern supports the relevance of cognitive responses over the measured interval, without excluding more immediate behavioral effects of emotional contagion.

Rivalry further clarifies why these interpretations matter. In both studies, greater rivalry with the particular coworker strengthened the indirect path from anxiety expression to ostracizing through perceived incompetence. Evidence that it weakened the affiliative pathway was confined to Study 1; the corresponding moderation was not supported in the main Study 2 analysis. Rivalry is thus more consistently implicated in amplifying distancing than in suppressing support. This asymmetry cautions against treating the two pathways as mirror images.

The designs also delimit the behavioral claim. The recall experiment supports causal conclusions about the effects of recalling anxious rather than neutral episodes on cognitive responses, but the subsequent cognition–behavior links remain correlational. Daily behaviors were self-reported, and Study 1 coworker ratings converged with self-reported helping but not ostracizing. Evidence for social distancing therefore needs corroboration through daily reports from both members of the relationship. Such data would also clarify whether the two parties recognize the same episodes as assistance or exclusion.

For practice, the findings identify a decision point in everyday interaction: before treating anxiety as evidence of incompetence, employees can consider the demands confronting the coworker. Shared goals may also reduce the rivalry that accompanies distancing responses, but neither practice was tested as an intervention. Evaluating whether these approaches change interpretations and subsequent behavior would connect the proposed processes to actionable support for anxious employees.

篇幅记录：418 English words (whitespace，含 General Discussion 标题)。

#### 2.4.0 candidate-r3 完整正文

General Discussion

An anxious coworker can appear to need assistance while also appearing less capable of meeting work demands. Our findings suggest that these interpretations need not cancel each other out. Across daily observations in China and a recall experiment in Britain, coworker anxiety expression was linked to greater perspective taking and perceived incompetence, which were associated with subsequent helping and ostracizing, respectively. The account concerns fluctuations in an employee’s responses to a particular coworker. It allows affiliation and distancing to occur within the same workday, without assuming that they occur simultaneously or establishing their sequence. This shifts attention from categorizing employees as supportive or unsupportive to explaining how their treatment of a coworker changes across occasions.

This pattern specifies how anxiety can function as social information: attending to a coworker’s circumstances makes assistance relevant, whereas evaluating the display as weakness provides a basis for distancing. The behavioral meaning of a negative emotional display therefore depends on the inference drawn from it. Observers also experienced more anxiety, but felt anxiety did not predict either later behavior in the main models. Cognitive interpretations thus help explain the measured responses beyond emotional transmission, although affective reactions over shorter intervals remain possible.

Rivalry sharpens this account, with more consistent evidence on the distancing side. In both studies, rivalry with the selected coworker strengthened the pathway through perceived incompetence to ostracism. Construing a rival’s anxiety as weakness may affirm the observer’s own standing, making a competence judgment especially consequential. This interpretation connects the replicated moderation to the relational stakes of judging a particular colleague. It weakened the affiliative pathway in Study 1, but the corresponding moderation was unsupported in the main Study 2 analysis. The clearest relational boundary therefore concerns the amplification of distancing; whether rivalry reliably suppresses support remains open. Differences between the studies’ designs also prevent attributing this contrast to national culture.

Study 2 provides causal evidence for cognitive responses to the recall manipulation; the cognition–behavior links remain correlational. In Study 1, coworker ratings correlated significantly with self-reported helping, but the corresponding correlation for ostracism was nonsignificant. Daily reports from both parties, together with experiments manipulating the proposed cognitive responses, would help establish whether these interpretations change how anxious coworkers are actually treated.

The practical implication centers on observers’ judgments. Employees can pause before construing a coworker’s anxiety as incompetence and consider the demands that coworker faces, especially in rivalrous relationships. Whether such reflection increases helping or reduces exclusion requires intervention evidence. Anxiety management at work consequently involves how colleagues interpret expressions of difficulty, alongside how employees manage the feeling itself.

篇幅记录：429 English words (whitespace，含 General Discussion 标题)。

判读：基线更清楚说明理解处境与怀疑能力为何可以并存；候选更具体解释竞争中的地位动机，并提出针对认知至行为因果关系的后续实验。候选还有一处 It 指代迟滞，原样保留。各有实质长处，判平。
