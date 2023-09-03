import streamlit as st
import streamlit_mermaid as stmd
import uuid
from src.model.models import EnglishWord
from src.common import app_logger

from service import WordQuestionBuilder, OpenAISSEClient

USER_NAME = "user"
ASSISTANT_NAME = "assistant"


def init_page():
    st.set_page_config(
        page_title="Utilizer: Boost your English active vocabulary 📚",
        page_icon="📚"
    )
    st.header("Utilizer: Boost your English active vocabulary")


def generate_session_id():
    return str(uuid.uuid4())


def convart_to_url_part(sentence):
    return sentence.replace(" ", "%20")

def convart_to_under_score(sentence):
    converted =  sentence.replace(" ", "_")
    # del the fisrt, last char if it is "_"
    if converted[0] == "_":
        converted = converted[1:]
    if converted[-1] == "_":
        converted = converted[:-1]
    return converted

def build_elsa_link(user_msg):
    return f"\n - [Go To ELSA：{user_msg}](https://elsaspeak.com/en/learn-english/how-to-pronounce/{convart_to_url_part(user_msg)})"


def build_youglish_link(user_msg):
    return f"\n\n - [Go To Youglish：{user_msg}](https://youglish.com/pronounce/{convart_to_url_part(user_msg)}/english?)"


def build_mermaid_graph_str(user_msg, result_str):

    li = map(convart_to_under_score, result_str.split("|"))
    # skip the first element
    next(li)

    code = f"""
    graph TD
        {user_msg} --> {next(li)}
        {user_msg} --> {next(li)}
        {user_msg} --> {next(li)}
        {user_msg} --> {next(li)}
    """
    return code


def ask_llm_sse(key, user_msg, assistant_msg, message_placeholder, is_collocation=False):
    question = WordQuestionBuilder.call(key=key, word=EnglishWord(value=user_msg))
    answers = OpenAISSEClient.call(question)

    result_str = ""
    for answer in answers:

        if answer.value == '[END]':
            message_placeholder.write(assistant_msg)
            break

        if not is_collocation:
            assistant_msg += answer.value
            message_placeholder.write(assistant_msg + "▌")

        result_str += answer.value

    return assistant_msg, result_str


def ask_several_questions_in_order(user_msg, assistant_msg, message_placeholder):
    # Meaning
    assistant_msg += f"\n\n #### Meaning \n\n"
    assistant_msg, _ = ask_llm_sse(key="meaning", user_msg=user_msg, assistant_msg=assistant_msg,
                                   message_placeholder=message_placeholder)
    # Pronunciation
    assistant_msg += f"\n\n #### Pronunciation \n\n"
    assistant_msg += "\n - IPA: "
    assistant_msg, _ = ask_llm_sse(key="pronunciation", user_msg=user_msg, assistant_msg=assistant_msg,
                                   message_placeholder=message_placeholder)
    # pronunciation_tip
    assistant_msg += "\n - Pronunciation Tip: "
    assistant_msg, _ = ask_llm_sse(key="pronunciation_tip", user_msg=user_msg, assistant_msg=assistant_msg,
                                   message_placeholder=message_placeholder)
    # st.write(build_youglish_link(user_msg)
    assistant_msg += build_youglish_link(user_msg)
    assistant_msg += build_elsa_link(user_msg)
    message_placeholder.write(assistant_msg)

    # Origin
    assistant_msg += f"\n\n #### Origin \n\n"
    assistant_msg, _ = ask_llm_sse(key="origin", user_msg=user_msg, assistant_msg=assistant_msg,
                                   message_placeholder=message_placeholder)
    # Synonym
    assistant_msg += f"\n\n #### Synonym \n\n"
    assistant_msg, _ = ask_llm_sse(key="synonym", user_msg=user_msg, assistant_msg=assistant_msg,
                                   message_placeholder=message_placeholder)
    # Example Sentence
    assistant_msg += f"\n\n #### Example Sentence \n\n"
    assistant_msg, result_str = ask_llm_sse(key="example_sentence", user_msg=user_msg, assistant_msg=assistant_msg,
                                            message_placeholder=message_placeholder)
    assistant_msg += build_elsa_link(result_str)

    # Collocation
    assistant_msg += f"\n\n #### Collocation MindMap \n\n"
    assistant_msg, result_str = ask_llm_sse(key="collocation", user_msg=user_msg, assistant_msg=assistant_msg,
                                             message_placeholder=message_placeholder, is_collocation=True)
    app_logger.info(f"result_str: {result_str}")
    code = build_mermaid_graph_str(user_msg, result_str)
    assistant_msg += code
    app_logger.info(f"code: {code}")
    stmd.st_mermaid(code)
    return assistant_msg

def ask():
    current_session = st.session_state.current_session
    chat_log = st.session_state.chat_sessions[current_session]
    # 現在のセッションのチャット履歴を表示
    for chat in chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    user_msg = st.chat_input("Enter english word or phrase you want to learn")
    if user_msg:
        # 最新のメッセージを表示
        with st.chat_message(USER_NAME):
            st.write(f"### {user_msg}")

        with st.chat_message(ASSISTANT_NAME):
            message_placeholder = st.empty()
            assistant_msg = ""
            assistant_msg = ask_several_questions_in_order(user_msg, assistant_msg, message_placeholder)
        # セッションにチャットログを追加
        chat_log.append({"name": USER_NAME, "msg": user_msg})
        chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})


def main():
    init_page()

    # セッション情報の初期化
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "current_session" not in st.session_state:
        st.session_state.current_session = generate_session_id()
        st.session_state.chat_sessions[st.session_state.current_session] = []

    # Sidebarの実装
    session_list = list(st.session_state.chat_sessions.keys())
    selected_session = st.sidebar.selectbox("Select Chat Session", session_list, index=len(session_list) - 1)
    st.session_state.current_session = selected_session

    if st.sidebar.button("New Chat"):
        new_session = generate_session_id()
        st.session_state.chat_sessions[new_session] = []
        st.session_state.current_session = new_session

    ask()


if __name__ == '__main__':
    main()
