from pathlib import Path

import pandas as pd
import streamlit as st

import calc


st.title("주간 비교")
st.caption("교육용 가상 데이터입니다.")

data_dir = Path(__file__).resolve().parents[1] / "data"
previous = calc.load_readiness(data_dir / "readiness_W44.csv")
current = calc.load_readiness(data_dir / "readiness_W45.csv")
comparison = calc.compare_weeks(previous, current)
st.caption("W44 → W45 비교입니다. 가동률 단위는 %, 증감 단위는 %p입니다.")

rising_column, falling_column = st.columns(2)
with rising_column:
    st.subheader("상승 상위 3")
    rising = comparison.loc[comparison["증감"].gt(0)].head(3)
    if rising.empty:
        st.info("가동률이 상승한 장비가 없습니다.")
    else:
        st.dataframe(rising, hide_index=True)
with falling_column:
    st.subheader("하락 상위 3")
    falling = comparison.loc[comparison["증감"].lt(0)].sort_values(
        "증감", ascending=True, kind="stable"
    ).head(3)
    if falling.empty:
        st.info("가동률이 하락한 장비가 없습니다.")
    else:
        st.dataframe(falling, hide_index=True)

st.subheader("전체 주간 비교")
st.dataframe(comparison, hide_index=True)

st.subheader("비고가 있는 원본 행")
st.caption("음수 정정 행을 포함하며, W44와 W45의 비고를 함께 표시합니다.")
notes = pd.concat(
    [previous.assign(주차="W44"), current.assign(주차="W45")],
    ignore_index=True,
)
notes = notes.loc[notes["비고"].fillna("").astype(str).str.strip().ne("")]
notes = notes[["주차", *previous.columns]].sort_values(
    ["주차", "일자", "장비코드"], kind="stable"
)
if notes.empty:
    st.info("비고가 있는 행이 없습니다.")
else:
    st.dataframe(notes, hide_index=True)
