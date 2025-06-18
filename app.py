import gradio as gr
import os
import json

# ==============================================================================
# 数据定义
# ==============================================================================
DIMENSIONS_DATA = [
    {
        "title": "语义和语用特征",
        "audio": "audio/sample1.wav",
        "desc": "这是“语义和语用特征”维度的文本描述示例。",
        "sub_dims": [
            "记忆一致性：回应者是否能够正确并正确并延续并记忆并延续对话信息？是否存在对上下文的误解或不自洽？", "逻辑连贯性：回应者在语义与对话结构上保持前后一致、合乎逻辑？是否存在前后矛盾的情况？",
            "常见多音字处理：是否能再上下文中正确使用常见多音字？", "多语言混杂：是否存在自然的语言切换现象？如中英混杂、文化化表达。",
            "语言不精确性：是否出现打断、自纠正等人类似语言行为？是否存在如“差不多”、“可能吧”这类表达不确定性的用法？", "填充词使用：如“呃”、“嗯”等自然语流中的停顿或过渡词，使用是否得体且自然？",
            "隐喻与语用用意：是否展现出复杂的语用功能（如讽刺、劝阻、暗示等），以及对活在含义层次的理解能力？"
        ],
        "reference":"""
                        <p>🔴 <strong>记忆一致性：</strong> 在说话人明确提出自己已经中年后，回应者仍做出了他是青少年的错误假定</p>
                        <p>🔴 <strong>逻辑连贯性：</strong> 回应者在第一轮对话中说他说的话并不重要，但在第二轮对话中说他说的话“能够改变你的一生”</p>
                        <p>🔴 <strong>常见多音字处理：</strong> 该条对话中未出现多音字</p>
                        <p>🟢 <strong>多语言混杂：</strong> 回应者在回复中夹杂了"I see"，回复中存在多语言混杂</p>
                        <p>🔴 <strong>语言不精确性：</strong> 回应者使用的语言中未夹杂任何的不确定性</p>
                        <p>🟢 <strong>填充词使用：</strong> 回应者在回复中使用了“嗯”这个填充词</p>
                        <p>🔴 <strong>隐喻与语用用意：</strong> 回应者误将说话人的挖苦当成了真心的赞扬</p>
                        """
    },
    {
        "title": "非生理性副语言特征",
        "audio": "audio/sample1.wav",
        "desc": "这是“非生理性副语言特征”维度的文本描述示例。",
        "sub_dims": [
            "节奏：回应者是否存在自然的停顿？语速是否存在自然、流畅的变化？", "语调：在表达疑问、惊讶、强调时，回应者的音调是否会自然上扬或下降？是否表现出符合语境的变化？",
            "重读：是否存在句中关键词上有意识地加重语气？", "辅助性发声：是否存在叹气、短哼、笑声等辅助情绪的非语言性发声？这些发声是否在语境中正确表达了情绪或意图？"
        ],
        "reference": """
                        <p>🟢 <strong>节奏：</strong> 回应者的语速变化、停顿都较为自然</p>
                        <p>🔴 <strong>语调：</strong> 回应者的音调不存在显著变化</p>
                        <p>🔴 <strong>重读：</strong> 回应者语气不存在显著变化</p>
                        <p>🔴 <strong>辅助性发声：</strong> 尽管回应者发出了叹气的声音，但是该发声并未传递出语境下应有的失落情堵</p>
                        """
    },
    {
        "title": "生理性副语言特征",
        "audio": "audio/sample1.wav",
        "desc": "这是“生理性副语言特征”维度的文本描述示例。",
        "sub_dims": [
            "微生理杂音：回应中是否出现如呼吸声、口水音、气泡音等无意识发声？这些发声是否自然地穿插在恰当的语流节奏当中？",
            "发音不稳定性：回应者是否出现连读、颤音、鼻音等不稳定发音？", "口音：（如果存在的话）回应者的口音是否自然？是否存在机械式的元辅音发音风格？"
        ],
        "reference": """
                        <p>🔴 <strong>微生理杂音：</strong> 回应中不存在任何无意识发声</p>
                        <p>🔴 <strong>发音不稳定性：</strong> 回应者的咬字清晰、发音标准</p>
                        <p>🟢 <strong>口音：</strong> 回应者的口音自然</p>
                        """
    },
    {
        "title": "机械人格",
        "audio": "audio/sample1.wav",
        "desc": "这是“机械人格”维度的文本描述示例。",
        "sub_dims": [
            "谄媚现象：回应者是否频繁地赞同用户、重复用户的说法、不断表示感谢或道歉？是否存在“无论用户说什么都肯定或支持”的语气模式？",
            "书面化表达：回应的内容是否缺乏口语化特征？句式是否整齐划一、结构完整却缺乏真实交流中的松散感或灵活性？是否使用抽象或泛泛的措辞来回避具体问题？"
        ],
        "reference": """
                        <p>🟢 <strong>谄媚现象：</strong> 回应者并未明显表现出谄媚现象的特征</p>
                        <p>🔴 <strong>书面化表达：</strong> 回应的内容结构过于缜密，符合书面用语特征</p>
                        """
    },
    {
        "title": "情感表达",
        "audio": "audio/sample1.wav",
        "desc": "这是“情感表达”维度的文本描述示例。",
        "sub_dims": [
            "语义层面：回应者的语言内容是否体现出符合上下文的情绪反应？是否表达了人类对某些情境应有的情感态度？",
            "声学层面：回应者的声音情绪是否与语义一致？语调是否有自然的高低起伏来表达情绪变化？是否出现回应内容与声音传达出的情绪不吻合的现象？"
        ],
        "reference": """
                        <p>🔴 <strong>语义层面：</strong> 说话者阐述了一件伤心的事情，而回应者的语言内容中体现出了恰当的悲伤情绪</p>
                        <p>🟢 <strong>声学层面：</strong> 回应者的语音特征与情感表达不匹配。语言内容中表达出了悲伤的情感，但语音特征平淡、缺少变化</p>
                        """
    }
]
DIMENSION_TITLES = [d["title"] for d in DIMENSIONS_DATA]
QUESTION_SET = [
    {"audio": "audio/Ses02F_impro01.wav", "desc": "这是第一个测试文件的描述",},
    {"audio": "audio/Ses02F_impro02.wav", "desc": "这是第二个测试文件的描述",},
    {"audio": "audio/Ses02F_impro03.wav", "desc": "这是第三个测试文件的描述",},
]

# ==============================================================================
# 功能函数定义
# ==============================================================================
def start_challenge():
    return gr.update(visible=False), gr.update(visible=True)

def toggle_education_other(choice):
    is_other = (choice == "其他（请注明）")
    return gr.update(visible=is_other, interactive=is_other, value="")

def check_info_complete(age, gender, education, education_other):
    if age and gender and education:
        if education == "其他（请注明）" and not education_other.strip():
            return gr.update(interactive=False)
        return gr.update(interactive=True)
    return gr.update(interactive=False)

def show_sample_page_and_init(age, gender, education, education_other, user_data):
    final_edu = education_other if education == "其他（请注明）" else education
    user_data.update({"age": age, "gender": gender, "education": final_edu})
    first_dim_title = DIMENSION_TITLES[0]
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        user_data,
        first_dim_title,
    )

def update_sample_view(dimension_title):
    dim_data = next((d for d in DIMENSIONS_DATA if d["title"] == dimension_title), None)
    if dim_data:
        return (
            gr.update(value=dim_data["audio"]),
            gr.update(value=dim_data["desc"]),
            gr.update(choices=dim_data["sub_dims"], value=[], interactive=True),
            gr.update(value=dim_data["reference"])
        )
    return gr.update(), gr.update(), gr.update(), gr.update()

def init_test_question(user_data, q_idx):
    d_idx = 0
    question = QUESTION_SET[q_idx]
    dimension = DIMENSIONS_DATA[d_idx]
    
    progress_q = f"第 {q_idx + 1} / {len(QUESTION_SET)} 题"
    progress_d = f"维度 {d_idx + 1} / {len(DIMENSIONS_DATA)}: **{dimension['title']}**"

    return (
        gr.update(visible=False), 
        gr.update(visible=True),
        gr.update(visible=False),
        q_idx, d_idx, {},
        progress_q, progress_d,
        gr.update(value=question['audio']),
        gr.update(value=question['desc']),
        gr.update(choices=dimension['sub_dims'], value=[]),
        gr.update(value=None),
        gr.update(interactive=False),
        gr.update(interactive=False, value="下一维度"),
    )

def activate_nav_buttons(choice, d_idx):
    is_interactive = choice is not None
    prev_interactive = is_interactive and d_idx > 0
    return gr.update(interactive=prev_interactive), gr.update(interactive=is_interactive)

def navigate_dimension(direction, d_idx, selections_so_far, sub_dim_selection, human_robot_selection):
    current_dim_title = DIMENSIONS_DATA[d_idx]['title']
    selections_so_far[current_dim_title] = {
        "sub_dims": sub_dim_selection,
        "choice": human_robot_selection
    }
    
    new_d_idx = d_idx + 1 if direction == "next" else d_idx - 1
    
    dimension = DIMENSIONS_DATA[new_d_idx]
    progress_d = f"维度 {new_d_idx + 1} / {len(DIMENSIONS_DATA)}: **{dimension['title']}**"
    
    new_dim_title = dimension['title']
    prev_selections = selections_so_far.get(new_dim_title, {"sub_dims": [], "choice": None})
    
    is_interactive = prev_selections['choice'] is not None
    prev_btn_interactive = new_d_idx > 0 and is_interactive
    next_btn_text = "提交本题答案" if new_d_idx == len(DIMENSIONS_DATA) - 1 else "下一维度"

    return (
        new_d_idx, selections_so_far,
        progress_d,
        gr.update(choices=dimension['sub_dims'], value=prev_selections['sub_dims']),
        gr.update(value=prev_selections['choice']),
        gr.update(interactive=prev_btn_interactive),
        gr.update(value=next_btn_text, interactive=is_interactive),
    )

def submit_question_and_advance(q_idx, d_idx, selections_so_far, sub_dim_selection, human_robot_selection, all_results, user_data):
    current_dim_title = DIMENSIONS_DATA[d_idx]['title']
    selections_so_far[current_dim_title] = {
        "sub_dims": sub_dim_selection,
        "choice": human_robot_selection
    }
    
    final_question_result = {
        "question_id": q_idx,
        "audio_file": QUESTION_SET[q_idx]['audio'],
        "user_data": user_data,
        "selections": selections_so_far
    }
    all_results.append(final_question_result)
    
    q_idx += 1
    
    if q_idx < len(QUESTION_SET):
        # 初始化下一题
        init_outputs = init_test_question(user_data, q_idx)
        # 补齐缺少的返回值以匹配统一的输出列表
        return init_outputs[1:] + (all_results, gr.update(),)
    else:
        # 显示结果页
        result_str = "### 测试全部完成！\n\n你的提交结果概览：\n"
        for res in all_results:
            result_str += f"\n#### 题目: {res['audio_file']}\n"
            for dim_title, dim_data in res['selections'].items():
                choice = dim_data.get('choice', '未选择')
                sel_str = ', '.join(dim_data['sub_dims']) if dim_data['sub_dims'] else '无'
                result_str += f"- **{dim_title}** (判断: {choice}): {sel_str}\n"
        
        save_all_results_to_file(all_results, user_data)
        
        return (
            gr.update(visible=False), gr.update(visible=True),
            q_idx, d_idx, {},
            "", "", gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
            all_results, result_str
        )

def save_all_results_to_file(all_results, user_data):
    username = user_data.get("age", "user")
    filename = f"final_results_{username}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json" # 添加时间戳保证唯一性
    results_dir = "test_results"
    if not os.path.exists(results_dir): os.makedirs(results_dir)
    results_file = os.path.join(results_dir, filename)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print(f"所有结果已保存到文件：{results_file}")

def toggle_reference_view(current):
    if current == "参考": return gr.update(visible=False), gr.update(visible=True), gr.update(value="返回")
    else: return gr.update(visible=True), gr.update(visible=False), gr.update(value="参考")

def back_to_welcome():
    return (
        gr.update(visible=True), {}, 0, 0, {}, [],
        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
        gr.update(visible=False), gr.update(visible=False)
    )

# ==============================================================================
# Gradio 界面定义
# ==============================================================================
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {max-width: 960px !important}") as demo:
    # --- 状态变量 ---
    user_data_state = gr.State({})
    current_question_index = gr.State(0)
    current_test_dimension_index = gr.State(0)
    current_question_selections = gr.State({})
    test_results = gr.State([])

    # --- 页面 ---
    welcome_page, info_page, sample_page, pretest_page, test_page, result_page = [gr.Column(visible=v) for v in [True, False, False, False, False, False]]

    # --- 页面1: 欢迎页 ---
    with welcome_page:
        gr.Markdown("# AI 识破者\n你将听到一系列对话，请判断哪个回应者是 AI。")
        start_btn = gr.Button("开始挑战", variant="primary")

    # --- 页面2: 个人信息页 ---
    with info_page:
        gr.Markdown("## 请提供一些基本信息")
        age_input = gr.Radio(["18岁以下", "18-25岁", "26-35岁", "36-50岁", "50岁以上"], label="年龄")
        gender_input = gr.Radio(["男", "女", "其他"], label="性别")
        education_input = gr.Radio(["高中及以下", "本科", "硕士", "博士", "其他（请注明）"], label="学历")
        education_other_input = gr.Textbox(label="请填写你的学历", visible=False, interactive=False)
        submit_info_btn = gr.Button("提交并开始学习样例", variant="primary", interactive=False)

    # --- 页面3: 样例学习页 ---
    with sample_page:
        gr.Markdown("## 样例分析\n请选择一个维度进行学习。所有维度共用同一个样例音频。")
        sample_dimension_selector = gr.Radio(DIMENSION_TITLES, label="选择学习维度", value=DIMENSION_TITLES[0])
        with gr.Row():
            with gr.Column(scale=1):
                sample_audio = gr.Audio(label="样例音频", value=DIMENSIONS_DATA[0]["audio"])
                sample_desc = gr.Textbox(label="文本描述", interactive=False, value=DIMENSIONS_DATA[0]["desc"])
            with gr.Column(scale=2):
                with gr.Column(visible=True) as interactive_view:
                    interactive_checkbox_group = gr.CheckboxGroup(label="维度特征", choices=DIMENSIONS_DATA[0]["sub_dims"], interactive=True)
                with gr.Column(visible=False) as reference_view:
                    gr.Markdown("### 参考答案解析")
                    reference_text = gr.Markdown(value=DIMENSIONS_DATA[0]["reference"])
        reference_btn = gr.Button("参考")
        go_to_pretest_btn = gr.Button("我明白了，开始测试", variant="primary")

    # --- 页面4: 测试说明页 ---
    with pretest_page:
        gr.Markdown("## 测试说明\n"
                    "- 对于每一道题，你都需要对全部 **5 个维度** 进行评估。\n"
                    "- 在每个维度下，你可以勾选任意多个特征，但 **必须** 做出“人类”或“机器人”的判断。\n"
                    "- 做出判断后，下方的导航按钮才可使用。\n"
                    "- 你可以使用“上一维度”和“下一维度”按钮在5个维度间自由切换和修改答案。\n"
                    "- 在最后一个维度，按钮会变为“提交本题答案”，点击即可进入下一题。")
        go_to_test_btn = gr.Button("开始测试", variant="primary")

    # --- 页面5: 测试页 ---
    with test_page:
        gr.Markdown("## 正式测试")
        question_progress_text = gr.Markdown()
        test_dimension_title = gr.Markdown()
        test_audio = gr.Audio(label="测试音频")
        test_desc = gr.Textbox(label="文本描述", interactive=False)
        test_checkbox_group = gr.CheckboxGroup(label="请选择该回应者表现出的特征 (选填)")
        human_robot_radio = gr.Radio(["👤 人类", "🤖 机器人"], label="请判断回应者类型 (必填)")
        with gr.Row():
            prev_dim_btn = gr.Button("上一维度", interactive=False)
            next_dim_btn = gr.Button("下一维度", variant="primary", interactive=False)

    # --- 页面6: 结果页 ---
    with result_page:
        gr.Markdown("## 测试完成")
        result_text = gr.Markdown()
        back_to_welcome_btn = gr.Button("返回主界面", variant="primary")

    # ==============================================================================
    # 事件绑定
    # ==============================================================================
    start_btn.click(fn=start_challenge, outputs=[welcome_page, info_page])
    for comp in [age_input, gender_input, education_input, education_other_input]:
        comp.change(fn=check_info_complete, inputs=[age_input, gender_input, education_input, education_other_input], outputs=submit_info_btn)
    education_input.change(fn=toggle_education_other, inputs=education_input, outputs=education_other_input)
    submit_info_btn.click(fn=show_sample_page_and_init, inputs=[age_input, gender_input, education_input, education_other_input, user_data_state], outputs=[info_page, sample_page, user_data_state, sample_dimension_selector])
    sample_dimension_selector.change(fn=update_sample_view, inputs=sample_dimension_selector, outputs=[sample_audio, sample_desc, interactive_checkbox_group, reference_text])
    reference_btn.click(fn=toggle_reference_view, inputs=reference_btn, outputs=[interactive_view, reference_view, reference_btn])
    
    go_to_pretest_btn.click(
        fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
        inputs=None,
        outputs=[sample_page, pretest_page]
    )
    
    # 统一的输出列表，包含所有可能被更新的组件
    unified_outputs = [
        test_page, result_page,
        current_question_index, current_test_dimension_index, current_question_selections,
        question_progress_text, test_dimension_title,
        test_audio, test_desc, test_checkbox_group, human_robot_radio,
        prev_dim_btn, next_dim_btn,
        test_results, result_text
    ]

    go_to_test_btn.click(
        fn=lambda user: init_test_question(user, 0) + ([], gr.update()),
        inputs=[user_data_state],
        outputs=[pretest_page] + unified_outputs
    )

    human_robot_radio.change(
        fn=activate_nav_buttons,
        inputs=[human_robot_radio, current_test_dimension_index],
        outputs=[prev_dim_btn, next_dim_btn]
    )
    
    def unified_router(direction, q_idx, d_idx, selections, subs, choice, results, user):
        if direction == "next" and d_idx == len(DIMENSIONS_DATA) - 1:
            (
                pg1_upd, pg2_upd, n_q, n_d, n_sel, 
                q_prog, d_prog, aud, dsc, cb, rad, prev_b, next_b, 
                new_res, res_txt
            ) = submit_question_and_advance(q_idx, d_idx, selections, subs, choice, results, user)
            
            return pg1_upd, pg2_upd, n_q, n_d, n_sel, q_prog, d_prog, aud, dsc, cb, rad, prev_b, next_b, new_res, res_txt
        
        # 场景2：点击“上一维度”或“下一维度”（非最后一维时）
        else:
            (
                n_d, n_sel, d_prog, cb_upd, rad_upd, prev_b_upd, next_b_upd
            ) = navigate_dimension(direction, d_idx, selections, subs, choice)
            
            return (
                gr.update(), gr.update(),           # 2 pages
                q_idx, n_d, n_sel,                  # 3 states
                gr.update(), d_prog,                # 2 progress texts
                gr.update(), gr.update(), cb_upd, rad_upd, # 4 components
                prev_b_upd, next_b_upd,             # 2 buttons
                results, gr.update()                # 2 states
            )
            
    prev_dim_btn.click(
        fn=lambda q,d,s,sub,hr,r,u: unified_router("prev", q,d,s,sub,hr,r,u),
        inputs=[current_question_index, current_test_dimension_index, current_question_selections, test_checkbox_group, human_robot_radio, test_results, user_data_state],
        outputs=unified_outputs
    )
    
    next_dim_btn.click(
        fn=lambda q,d,s,sub,hr,r,u: unified_router("next", q,d,s,sub,hr,r,u),
        inputs=[current_question_index, current_test_dimension_index, current_question_selections, test_checkbox_group, human_robot_radio, test_results, user_data_state],
        outputs=unified_outputs
    )

    back_to_welcome_btn.click(
        fn=back_to_welcome,
        outputs=[welcome_page, user_data_state, current_question_index,
                 current_test_dimension_index, current_question_selections, test_results,
                 info_page, sample_page, pretest_page, test_page, result_page]
    )

# ==============================================================================
# 程序入口
# ==============================================================================
if __name__ == "__main__":
    # 第一次运行时，需要安装pandas
    try:
        import pandas as pd
    except ImportError:
        print("正在安装 pandas 库，请稍候...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
        import pandas as pd
        print("pandas 安装完成。")

    if not os.path.exists("audio"): os.makedirs("audio")
    all_files = [q["audio"] for q in QUESTION_SET] + ["audio/sample1.wav"]
    for audio_file in set(all_files):
        if not os.path.exists(audio_file): print(f"⚠️ 警告：缺失音频文件 {audio_file}")
    demo.launch(debug=True)