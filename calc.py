"""교육용 장비 가동률 계산."""

import pandas as pd


def load_readiness(path) -> pd.DataFrame:
    """음수 정정 행을 포함해 CSV를 그대로 읽는다."""
    return pd.read_csv(path, encoding="utf-8-sig")


def total_rate(df) -> float:
    """전체 시간 합계로 가동률을 계산하며, 계획시간이 0이면 0을 반환한다."""
    planned = df["계획시간(h)"].sum()
    if planned == 0:
        return 0.0
    return round(float(df["가동시간(h)"].sum() / planned * 100), 1)


def rate_by_equipment(df) -> pd.DataFrame:
    """장비별 시간을 합산하고 가동률을 소수 첫째 자리까지 계산한다."""
    result = (
        df.groupby(["장비코드", "장비명"], as_index=False)[
            ["계획시간(h)", "가동시간(h)"]
        ]
        .sum()
        .rename(columns={"계획시간(h)": "계획시간", "가동시간(h)": "가동시간"})
    )
    planned = result["계획시간"].where(result["계획시간"].ne(0))
    result["가동률"] = (result["가동시간"] / planned * 100).fillna(0.0).round(1)
    return result[["장비코드", "장비명", "계획시간", "가동시간", "가동률"]]


def compare_weeks(prev, cur) -> pd.DataFrame:
    """두 주에 공통으로 있는 장비의 가동률 증감을 내림차순으로 반환한다."""
    previous = rate_by_equipment(prev)[["장비코드", "장비명", "가동률"]]
    current = rate_by_equipment(cur)[["장비코드", "장비명", "가동률"]]
    result = previous.merge(
        current, on=["장비코드", "장비명"], suffixes=("_이전", "_이번")
    )
    result["증감"] = (result["가동률_이번"] - result["가동률_이전"]).round(1)
    return result.sort_values("증감", ascending=False, kind="stable").reset_index(drop=True)
