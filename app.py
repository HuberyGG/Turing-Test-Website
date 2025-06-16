import gradio as gr
import os

DIMENSIONS_DATA = [
    {
        "title": "语义和语用特征",
        "audio": "audio/sample1.wav",
        "desc": "这是“语义和语用特征”维度的文本描述示例。",
        "annotated_label": "人-机对话",
        "true_label": "人-机对话",
        "sub_dims": [
            "记忆一致性：回应者是否能够正确并正确并延续并记忆并延续对话信息？是否存在对上下文的误解或不自洽？", "逻辑连贯性：回应者在语义与对话结构上保持前后一致、合乎逻辑？是否存在前后矛盾的情况？",
            "常见多音字处理：是否能再上下文中正确使用常见多音字？", "多语言混杂：是否存在自然的语言切换现象？如中英混杂、文化化表达。",
            "语言不精确性：是否出现打断、自纠正等人类似语言行为？是否存在如“差不多”、“可能吧”这类表达不确定性的用法？", "填充词使用：如“呃”、“嗯”等自然语流中的停顿或过渡词，使用是否得体且自然？",
            "隐喻与语用用意：是否展现出复杂的语用功能（如讽刺、劝阻、暗示等），以及对活在含义层次的理解能力？"
        ]
    },
    {
        "title": "非生理性副语言特征",
        "audio": "audio/sample2.wav",
        "desc": "这是“非生理性副语言特征”维度的文本描述示例。",
        "annotated_label": "人-人对话",
        "true_label": "人-人对话",
        "sub_dims": [
            "节奏：回应者是否存在自然的停顿？语速是否存在自然、流畅的变化？", "语调：在表达疑问、惊讶、强调时，回应者的音调是否会自然上扬或下降？是否表现出符合语境的变化？",
            "重读：是否存在句中关键词上有意识地加重语气？", "辅助性发声：是否存在叹气、短哼、笑声等辅助情绪的非语言性发声？这些发声是否在语境中正确表达了情绪或意图？"
        ]
    },
    {
        "title": "生理性副语言特征",
        "audio": "audio/sample3.wav",
        "desc": "这是“生理性副语言特征”维度的文本描述示例。",
        "annotated_label": "人-机对话",
        "true_label": "人-人对话",
        "sub_dims": [
            "微生理杂音：回应中是否出现如呼吸声、口水音、气泡音等无意识发声？这些发声是否自然地穿插在恰当的语流节奏当中？",
            "发音不稳定性：回应者是否出现连读、颤音、鼻音等不稳定发音？", "口音：（如果存在的话）回应者的口音是否自然？是否存在机械式的元辅音发音风格？"
        ]
    },
    {
        "title": "机械人格",
        "audio": "audio/sample4.wav",
        "desc": "这是“机械人格”维度的文本描述示例。",
        "annotated_label": "人-人对话",
        "true_label": "人-机对话",
        "sub_dims": [
            "谄媚现象：回应者是否频繁地赞同用户、重复用户的说法、不断表示感谢或道歉？是否存在“无论用户说什么都肯定或支持”的语气模式？",
            "书面化表达：回应的内容是否缺乏口语化特征？句式是否整齐划一、结构完整却缺乏真实交流中的松散感或灵活性？是否使用抽象或泛泛的措辞来回避具体问题？"
        ]
    },
    {
        "title": "情感表达",
        "audio": "audio/sample5.wav",
        "desc": "这是“情感表达”维度的文本描述示例。",
        "annotated_label": "人-机对话",
        "true_label": "人-机对话",
        "sub_dims": [
            "语义层面：回应者的语言内容是否体现出符合上下文的情绪反应？是否表达了人类对某些情境应有的情感态度？",
            "声学层面：回应者的声音情绪是否与语义一致？语调是否有自然的高低起伏来表达情绪变化？是否出现回应内容与声音传达出的情绪不吻合的现象？"
        ]
    }
]

REFERENCE_TEXT = """
<p>🔴 <strong>记忆一致性：</strong> 在说话人明确提出自己已经中年后，回应者仍做出了他是青少年的错误假定</p>
<p>🔴 <strong>逻辑连贯性：</strong> 回应者在第一轮对话中说他说的话并不重要，但在第二轮对话中说他说的话“能够改变你的一生”</p>
<p>🔴 <strong>常见多音字处理：</strong> 该条对话中未出现多音字</p>
<p>🟢 <strong>多语言混杂：</strong> 回应者在回复中夹杂了"I see"，回复中存在多语言混杂</p>
<p>🔴 <strong>语言不精确性：</strong> 回应者使用的语言中未夹杂任何的不确定性</p>
<p>🟢 <strong>填充词使用：</strong> 回应者在回复中使用了“嗯”这个填充词</p>
<p>🔴 <strong>隐喻与语用用意：</strong> 回应者误将说话人的挖苦当成了真心的赞扬</p>
"""

# 页面切换
def start_challenge():
    return gr.update(visible=False), gr.update(visible=True)

def toggle_education_other(choice):
    return gr.update(visible=(choice == "其他（请注明）"), interactive=(choice == "其他（请注明）"), value="")

def _reset_to_first_dimension():
    dim = DIMENSIONS_DATA[0]
    return (
        0,
        f"当前评估维度：**{dim['title']}**",
        gr.update(choices=dim['sub_dims'], value=[], interactive=True),
        gr.update(interactive=False),
        gr.update(interactive=True),
        gr.update(value=dim['audio']),
        gr.update(value=dim['desc']),
        gr.update(value=f"该对话被标注结果为：{dim['annotated_label']}\n该对话的真实标签为：{dim['true_label']}")
    )

def show_sample_page(age, gender, education, education_other, user_data):
    final_edu = education_other if education == "其他（请注明）" else education
    user_data.update({"age": age, "gender": gender, "education": final_edu})
    return (
        gr.update(visible=False), gr.update(visible=True), user_data
    ) + _reset_to_first_dimension()

def change_dimension(direction, user_data, current_index):
    if direction == "next":
        new_index = min(current_index + 1, len(DIMENSIONS_DATA) - 1)
    else:
        new_index = max(current_index - 1, 0)
    dim = DIMENSIONS_DATA[new_index]
    return (
        new_index,
        f"当前评估维度：**{dim['title']}**",
        gr.update(choices=dim['sub_dims'], value=[], interactive=True),
        gr.update(interactive=new_index > 0),
        gr.update(interactive=new_index < len(DIMENSIONS_DATA) - 1),
        gr.update(value=dim['audio']),
        gr.update(value=dim['desc']),
        gr.update(value=f"该对话被标注结果为：{dim['annotated_label']}\n该对话的真实标签为：{dim['true_label']}")
    )

def toggle_reference_view(current):
    if current == "参考":
        return gr.update(visible=False), gr.update(visible=True), gr.update(value="返回")
    else:
        return gr.update(visible=True), gr.update(visible=False), gr.update(value="参考")

# 页面布局
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {max-width: 960px !important}") as demo:
    user_data_state = gr.State({})
    sample_dimension_state = gr.State(0)

    # 第1页：欢迎页
    with gr.Column(visible=True) as welcome_page:
        gr.Markdown("# AI 识破者")
        gr.Markdown("你将听到一系列对话，请判断哪个回应者是 AI。")
        start_btn = gr.Button("开始挑战", variant="primary")

    # 第2页：信息收集页
    with gr.Column(visible=False) as info_page:
        age_input = gr.Radio(["18岁以下", "18-25岁", "26-35岁", "36-45岁", "46-60岁", "60岁以上"], label="年龄")
        gender_input = gr.Radio(["男", "女", "其他", "不愿透露"], label="性别")
        education_input = gr.Radio(["初中及以下", "高中/中专", "大专", "本科", "硕士", "博士及以上", "其他（请注明）"], label="学历")
        education_other_input = gr.Textbox(label="请填写你的学历", visible=False, interactive=False)
        submit_info_btn = gr.Button("提交并开始游戏", variant="primary")

    # 第3页：样例页面
    with gr.Column(visible=False) as sample_page:
        gr.Markdown("## 样例分析")
        dimension_title = gr.Markdown()
        with gr.Row():
            with gr.Column(scale=1):
                sample_audio = gr.Audio()
                sample_desc = gr.Textbox(label="文本描述", interactive=False)
                sample_labels = gr.Textbox(label="标注与真实标签", interactive=False)
            with gr.Column(scale=2):
                with gr.Column(visible=True) as interactive_view:
                    interactive_checkbox_group = gr.CheckboxGroup(label="维度特征")
                with gr.Column(visible=False) as reference_view:
                    gr.Markdown("### 参考")
                    gr.Markdown(REFERENCE_TEXT)

        with gr.Row():
            prev_dim_btn = gr.Button("上一维度", interactive=False)
            reference_btn = gr.Button("参考")
            next_dim_btn = gr.Button("下一维度")
        start_test_btn = gr.Button("我明白了，开始测试", variant="primary")

    # 按钮事件绑定
    start_btn.click(start_challenge, outputs=[welcome_page, info_page])
    education_input.change(toggle_education_other, inputs=education_input, outputs=education_other_input)

    submit_info_btn.click(
        fn=show_sample_page,
        inputs=[age_input, gender_input, education_input, education_other_input, user_data_state],
        outputs=[
            info_page, sample_page, user_data_state,
            sample_dimension_state, dimension_title, interactive_checkbox_group,
            prev_dim_btn, next_dim_btn, sample_audio, sample_desc, sample_labels
        ]
    )

    prev_dim_btn.click(
        fn=lambda user_data, idx: change_dimension("prev", user_data, idx),
        inputs=[user_data_state, sample_dimension_state],
        outputs=[
            sample_dimension_state, dimension_title, interactive_checkbox_group,
            prev_dim_btn, next_dim_btn, sample_audio, sample_desc, sample_labels
        ]
    )

    next_dim_btn.click(
        fn=lambda user_data, idx: change_dimension("next", user_data, idx),
        inputs=[user_data_state, sample_dimension_state],
        outputs=[
            sample_dimension_state, dimension_title, interactive_checkbox_group,
            prev_dim_btn, next_dim_btn, sample_audio, sample_desc, sample_labels
        ]
    )

    reference_btn.click(
        fn=toggle_reference_view,
        inputs=[reference_btn],
        outputs=[interactive_view, reference_view, reference_btn]
    )

# 启动
if __name__ == "__main__":
    if not os.path.exists("audio"):
        os.makedirs("audio")
        print("⚠️ 创建了 audio 文件夹，请放入 sample1.wav 至 sample5.wav")
    else:
        for dim in DIMENSIONS_DATA:
            if not os.path.exists(dim["audio"]):
                print(f"⚠️ 缺失音频：{dim['audio']}")
    demo.launch(debug=True)
