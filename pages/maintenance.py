from pathlib import Path

import streamlit as st

import calc
import db


st.title("정비 요청")
st.caption("교육용 가상 데이터입니다.")
st.write(f"현재 저장소: {db.backend_name()}")

data_dir = Path(__file__).resolve().parents[1] / "data"
equipment = calc.load_readiness(data_dir / "readiness_W45.csv")
equipment = equipment[["장비코드", "장비명"]].drop_duplicates().sort_values("장비코드")
labels = equipment.set_index("장비코드")["장비명"].to_dict()

st.subheader("정비 요청 등록")
st.caption("요청 내용과 역할명에는 실제 부대·장비·사람 정보를 입력하지 마세요.")
with st.form("maintenance_request", clear_on_submit=True):
    code = st.selectbox(
        "장비", equipment["장비코드"].tolist(),
        format_func=lambda value: f"{value} · {labels[value]}",
    )
    title = st.text_area("요청 내용", max_chars=200)
    priority = st.selectbox("우선순위", db.PRIORITIES)
    requester_role = st.text_input("요청자 역할명", max_chars=50)
    submitted = st.form_submit_button("등록")

if submitted:
    if not title.strip():
        st.warning("요청 내용을 입력해 주세요.")
    else:
        try:
            request_id = db.add_request(code, title, priority, requester_role)
        except Exception:
            st.error("정비 요청을 등록하지 못했습니다. 저장소 연결을 확인해 주세요.")
        else:
            st.success(f"정비 요청 {request_id}번을 등록했습니다.")

st.subheader("정비 요청 목록")
status_filter = st.selectbox("목록 상태", ["전체", *db.STATUSES])
try:
    requests = db.list_requests(status=None if status_filter == "전체" else status_filter)
except Exception:
    st.error("정비 요청 목록을 불러오지 못했습니다. 저장소 연결을 확인해 주세요.")
    st.stop()

if requests.empty:
    st.info("선택한 상태의 정비 요청이 없습니다.")
else:
    st.dataframe(
        requests.rename(columns={
            "id": "번호", "created_at": "등록 시각", "equipment_code": "장비코드",
            "title": "요청 내용", "priority": "우선순위",
            "requester_role": "요청자 역할명", "status": "상태",
        }),
        hide_index=True,
    )

st.subheader("상태 변경")
if not requests.empty:
    st.caption("현재 목록에 표시된 요청 중에서 번호를 선택하세요.")
    with st.form("maintenance_status"):
        request_id = st.selectbox("요청 번호", requests["id"].tolist())
        new_status = st.selectbox("바꿀 상태", db.STATUSES)
        change_submitted = st.form_submit_button("상태 변경")
    if change_submitted:
        try:
            db.update_status(int(request_id), new_status)
        except Exception:
            st.error("상태를 변경하지 못했습니다. 저장소 연결을 확인해 주세요.")
        else:
            st.session_state["maintenance_notice"] = f"요청 {request_id}번의 상태를 {new_status}(으)로 변경했습니다."
            st.rerun()
else:
    st.info("상태를 변경할 요청이 없습니다.")

if "maintenance_notice" in st.session_state:
    st.success(st.session_state.pop("maintenance_notice"))
