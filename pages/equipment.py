from pathlib import Path

import streamlit as st

import calc


st.title("장비별 상세")
st.caption("교육용 가상 데이터입니다.")

week = st.selectbox("주차", ["W44", "W45"], index=1)
data_dir = Path(__file__).resolve().parents[1] / "data"
data = calc.load_readiness(data_dir / f"readiness_{week}.csv")
equipment = calc.rate_by_equipment(data)
labels = equipment.set_index("장비코드")["장비명"].to_dict()
code = st.selectbox(
    "장비", equipment["장비코드"].tolist(),
    format_func=lambda value: f"{value} · {labels[value]}",
)
selected = equipment.loc[equipment["장비코드"].eq(code)].iloc[0]
rate_column, actual_column, planned_column = st.columns(3)
rate_column.metric("가동률", f"{selected['가동률']:.1f}%")
actual_column.metric("가동시간 합계", f"{selected['가동시간']:g}시간")
planned_column.metric("계획시간 합계", f"{selected['계획시간']:g}시간")

daily = (
    data.loc[data["장비코드"].eq(code)]
    .groupby("일자", as_index=False)[["계획시간(h)", "가동시간(h)"]]
    .sum()
    .sort_values("일자")
)
st.subheader("일별 계획·가동시간")
st.caption("음수 정정 행도 해당 일자의 합계에 포함합니다.")
st.line_chart(
    daily, x="일자", y=["계획시간(h)", "가동시간(h)"],
    x_label="일자", y_label="시간 (h)",
)
st.dataframe(daily, hide_index=True)
