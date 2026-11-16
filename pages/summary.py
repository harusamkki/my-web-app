from pathlib import Path

import streamlit as st

import calc


st.title("요약")
st.caption("교육용 가상 데이터입니다. 실제 부대·장비·사람 정보가 아닙니다.")

data_dir = Path(__file__).resolve().parents[1] / "data"
previous = calc.load_readiness(data_dir / "readiness_W44.csv")
current = calc.load_readiness(data_dir / "readiness_W45.csv")
previous_rate = calc.total_rate(previous)
current_rate = calc.total_rate(current)
change = round(current_rate - previous_rate, 1)
target_gap = round(current_rate - 90.0, 1)

current_column, previous_column, target_column = st.columns(3)
current_column.metric(
    "이번 주 전체 가동률 (W45)",
    f"{current_rate:.1f}%",
    delta=f"{change:+.1f}%p",
    help="지난주 대비 가동률 증감입니다.",
)
previous_column.metric("지난주 전체 가동률 (W44)", f"{previous_rate:.1f}%")
target_column.metric("목표 가동률", "90.0%", delta=f"{target_gap:+.1f}%p")
st.caption("목표 카드의 증감은 이번 주 가동률과 목표 90%의 차이입니다.")

st.subheader("장비별 이번 주 가동률")
equipment = calc.rate_by_equipment(current)
equipment["장비"] = equipment["장비코드"] + " · " + equipment["장비명"]
st.bar_chart(equipment, x="장비", y="가동률", x_label="장비", y_label="가동률 (%)")
