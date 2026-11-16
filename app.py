import streamlit as st

import db


st.set_page_config(page_title="장비 가동률", layout="wide")

if "db_initialized" not in st.session_state:
    db.init_db()
    st.session_state["db_initialized"] = True

page = st.navigation(
    [
        st.Page("pages/summary.py", title="요약", default=True),
        st.Page("pages/equipment.py", title="장비별 상세"),
        st.Page("pages/comparison.py", title="주간 비교"),
        st.Page("pages/maintenance.py", title="정비 요청"),
    ]
)
page.run()
