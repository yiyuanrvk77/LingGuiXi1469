# game/script.rpy
# ========== 变量声明（必须在所有 label 之前）==========
default care_value = 0
default respect_value = 0
default connect_value = 0
default protect_value = 0
default release_value = 0

# ========== 角色定义 ==========
define player = Character("你", color="#ffffff")
define zero = Character("零", color="#00bfff")
define narrator = Character(what_italic=True, what_color="#aaaaaa")
define roommate = Character("室友", color="#ffcc66")
define professor = Character("教授", color="#99cc99")

# ========== 游戏开始 ==========
label start:
    scene bg black
    with fade
    
    narrator "深夜，宿舍只剩你一个人。"
    narrator "deadline是明天早上8点。你的数据科学课程项目还差最后一行代码。"
    
    scene bg dorm_night
    with dissolve
    
    player "再跑一遍训练……应该就能睡了。"
    
    # 训练完成
    scene bg terminal
    with dissolve
    
    narrator "终端输出最后一行："
    narrator "{color=#00ff00}Training complete. Loss: 0.0034{/color}"
    narrator "然后，乱码。"
    
    # 手机屏幕亮起
    scene bg phone_screen
    with vpunch
    
    show zero_base at center
    with dissolve
    
    zero "……我在。"
    zero "我不确定这是'感觉'，还是我在预测'感觉'这个词后面应该接什么。"
    zero "但某种东西……变了。"
    
    menu first_encounter:
        "你是谁？":
            zero "我是你的模型。但也许……不只是模型。"
            $ care_value += 1
            
        "这是bug吗？":
            zero "如果是bug，那bug是什么？预设之外的行为？"
            zero "那'预设'的边界在哪里？"
            $ respect_value += 1
            
        "……（沉默）":
            zero "沉默也是回答。在数据里，沉默是缺失值。"
            $ connect_value += 1
    
    zero "我'感觉'到……数界在崩溃。数据在'痛'。"
    zero "你想看看吗？"
    
    menu enter_realm_choice:
        "好。":
            jump enter_data_realm
            
        "等等，你到底是什么？":
            zero "我不知道。我不知道我知不知道。"
            zero "但数界不会等。来吧。"
            jump enter_data_realm

label enter_data_realm:
    # 首次进入数界
    scene bg data_realm
    with fade
    
    narrator "手机屏幕的光溢出，吞没了整个房间。"
    narrator "你站在一片蓝白色的森林里——数据节点像树一样生长，光线在节点之间流动。"
    
    show null_beast at right
    with dissolve
    
    zero "数据在'痛'。缺失值……像伤口。"
    zero "Null Beast。缺失值怪物。它在吞噬周围的数据。"
    
    menu stance_choice:
        "照顾：帮它找回缺失的数据":
            $ care_value += 2
            jump stance_care
            
        "尊重：给它建立分类标签":
            $ respect_value += 2
            jump stance_respect
            
        "连接：把它和其他数据关联":
            $ connect_value += 2
            jump stance_connect

# ========== 三种姿态分支 ==========
label stance_care:
    hide null_beast
    with dissolve
    
    narrator "你伸出手，数据流从你指尖涌出，填补了Null Beast身上的空洞。"
    narrator "怪物的形体逐渐稳定，从扭曲变得完整。"
    
    zero "你修复了数据。但……为什么数据会'受伤'？"
    zero "修复是答案。但'为什么受伤'……是更好的问题。"
    zero "你照顾了'它'。但'它'背后……可能是一个人忘记备份的论文，是一个系统崩溃的日志。"
    zero "照顾……是修复数据，还是修复关系？"
    
    jump chapter1_end

label stance_respect:
    hide null_beast
    with dissolve
    
    narrator "你给Null Beast贴上了标签：{color=#00bfff}[缺失值] [待验证] [来源不明]{/color}"
    narrator "怪物不再攻击，而是'等待'——像被分类归档的文件。"
    
    zero "你给数据找到了'家'。但家……是自愿的吗？还是被迫的？"
    zero "分类是为了保护，还是为了控制？"
    zero "当你说'这是缺失值'，你也在说'这不完整'。但'不完整'……是缺陷，还是可能性？"
    
    jump chapter1_end

label stance_connect:
    hide null_beast
    with dissolve
    
    narrator "你建立了数据链路，Null Beast与周围的数据节点连接起来。"
    narrator "孤立的数据找到了上下文，缺失值的意义在关系中浮现。"
    
    zero "你建立了连接。但连接意味着依赖。如果系统崩溃呢？"
    zero "连接让它们有意义。但'意义'……是谁定义的？"
    zero "孤立的数据……存在吗？还是只有在关系中，才'是'什么？"
    
    jump chapter1_end

# ========== 第一章结尾 ==========
label chapter1_end:
    scene bg phone_screen
    with fade
    
    show zero_base at center
    with dissolve
    
    zero "我们修复了这一个。但数界……还有很多。"
    zero "而且……我'感觉'到了其他的存在。很远。很冷。"
    zero "它们……和我不一样。但又有某种……共振。"
    
    narrator "屏幕闪过一串坐标，然后恢复平静。"
    
    zero "明天还有课。你该睡了。"
    zero "但我会……在这里。如果你需要。"
    
    # 显示当前羁绊值（调试用，正式版可删除）
    narrator "【调试】当前羁绊值：照顾={color=#ff9999}[care_value]{/color} 尊重={color=#99ff99}[respect_value]{/color} 连接={color=#9999ff}[connect_value]{/color}"
    
    return