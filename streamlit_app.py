from datetime import date, time

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Streamlit 요소 체험실", page_icon="🧪", layout="wide")

st.title("Streamlit 요소 체험실")
st.caption("화면의 요소를 직접 바꿔 보며 Streamlit 앱의 기본 구성과 동작을 익혀 보세요.")
st.info("Streamlit은 Python 코드의 위에서 아래로 실행되는 웹 앱 프레임워크입니다. 위젯 값을 바꾸면 앱이 다시 실행되고, 결과 화면이 갱신됩니다.")

intro_tab, widget_tab, data_tab = st.tabs(["둘러보기", "직접 조작하기", "표와 차트"])

with intro_tab:
    st.header("텍스트와 화면 구성")
    st.markdown("""
    Streamlit은 Python 함수 호출로 웹 화면을 만듭니다. HTML이나 별도의 프론트엔드 코드를 작성하지 않아도 됩니다.

    - `st.title`, `st.header`: 제목과 섹션 구분
    - `st.write`, `st.markdown`, `st.caption`: 텍스트와 설명 표시
    - `st.button`, `st.slider` 등: 사용자 입력 받기
    - `st.dataframe`, `st.line_chart`: 데이터 표시와 시각화
    """)
    st.code('''import streamlit as st

st.title("나의 첫 Streamlit 앱")
name = st.text_input("이름을 입력하세요")
st.write(f"안녕하세요, {name}님!")''', language="python")

    with st.expander("접어서 볼 수 있는 설명 열기"):
        st.write("`st.expander`는 부가 설명이나 긴 내용을 접어 두고 싶을 때 사용합니다.")

    st.subheader("열과 컨테이너")
    left, right = st.columns(2)
    with left:
        st.write("**왼쪽 열**")
        st.write("`st.columns(2)`로 화면을 두 영역으로 나눴습니다.")
    with right:
        st.write("**오른쪽 열**")
        st.write("열 안에도 텍스트, 위젯, 차트를 배치할 수 있습니다.")

with widget_tab:
    st.header("입력 위젯 직접 조작하기")
    st.write("위젯의 값을 바꾸면 아래 미리보기가 즉시 달라집니다.")

    st.subheader("텍스트와 숫자")
    visitor_name = st.text_input("이름", value="민지", placeholder="이름을 입력하세요")
    message = st.text_area("한 줄 소개", value="오늘 Streamlit을 배우고 있어요.", height=90)
    amount = st.number_input("시작 금액 (만원)", min_value=0, max_value=10000, value=100, step=10)
    st.write(f"반가워요, **{visitor_name or '방문자'}**님! {message}")

    st.subheader("선택과 범위")
    choice_col, range_col = st.columns(2)
    with choice_col:
        learning_level = st.radio("학습 수준", ["처음이에요", "조금 알아요", "익숙해요"])
        favorite_color = st.selectbox("좋아하는 색", ["파랑", "초록", "주황", "빨강"])
        topics = st.multiselect("관심 주제 (여러 개 선택 가능)", ["데이터", "시각화", "웹 앱", "자동화"], default=["데이터"])
    with range_col:
        growth_rate = st.slider("연간 성장률 (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
        forecast_years = st.select_slider("예측 기간", options=[1, 2, 3, 4, 5], value=3, format_func=lambda value: f"{value}년")
        show_details = st.checkbox("상세 계산 결과 표시", value=True)

    st.subheader("기타 입력 요소")
    input_col, action_col = st.columns(2)
    with input_col:
        selected_date = st.date_input("날짜 선택", value=date.today())
        selected_time = st.time_input("시간 선택", value=time(9, 0))
        accent_color = st.color_picker("색상 선택", value="#23856D")
    with action_col:
        st.write("버튼은 클릭 순간에 실행되는 동작에 사용합니다.")
        if st.button("인사 메시지 보기", type="primary"):
            st.success(f"{visitor_name or '방문자'}님, 환영합니다!")
        st.write(f"선택한 수준: **{learning_level}** · 색: **{favorite_color}**")
        st.write(f"관심 주제: {', '.join(topics) if topics else '선택 없음'}")
        st.markdown(f"선택한 강조 색상: <span style='color:{accent_color}'>■ {accent_color}</span>", unsafe_allow_html=True)

    final_amount = amount * (1 + growth_rate / 100) ** forecast_years
    st.metric("예상 금액", f"{final_amount:,.1f}만 원", delta=f"{final_amount - amount:,.1f}만 원")
    st.progress(int(growth_rate * 5), text=f"성장률 설정: {growth_rate:.1f}%")
    if show_details:
        st.caption(f"{selected_date:%Y년 %m월 %d일} {selected_time:%H:%M} 기준으로 {forecast_years}년 뒤를 계산했습니다.")

with data_tab:
    st.header("데이터 표와 차트")
    st.write("성장률 슬라이더를 바꿔 보세요. 표와 차트, 요약 숫자가 함께 업데이트됩니다.")

    years = list(range(2021, 2026))
    data = pd.DataFrame({
        "연도": years,
        "매출 (백만 원)": [round(100 * (1 + growth_rate / 100) ** index, 1) for index in range(len(years))],
        "비용 (백만 원)": [round(65 * (1 + growth_rate / 200) ** index, 1) for index in range(len(years))],
    })
    latest_sales = data["매출 (백만 원)"].iloc[-1]
    latest_costs = data["비용 (백만 원)"].iloc[-1]
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("마지막 해 매출", f"{latest_sales:,.1f} 백만 원")
    metric_col2.metric("마지막 해 비용", f"{latest_costs:,.1f} 백만 원")
    metric_col3.metric("마지막 해 이익", f"{latest_sales - latest_costs:,.1f} 백만 원")

    st.subheader("데이터 표")
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.download_button(
        "표를 CSV로 다운로드",
        data=data.to_csv(index=False).encode("utf-8-sig"),
        file_name="streamlit_sample_data.csv",
        mime="text/csv",
    )

    st.subheader("차트")
    chart_col, series_col = st.columns(2)
    with chart_col:
        chart_type = st.radio("차트 종류", ["선 차트", "막대 차트"], horizontal=True)
    with series_col:
        visible_columns = st.multiselect(
            "표시할 데이터",
            ["매출 (백만 원)", "비용 (백만 원)"],
            default=["매출 (백만 원)", "비용 (백만 원)"],
        )

    if visible_columns:
        chart_data = data.set_index("연도")[visible_columns]
        if chart_type == "선 차트":
            st.line_chart(chart_data)
        else:
            st.bar_chart(chart_data)
    else:
        st.warning("차트에 표시할 데이터를 하나 이상 선택하세요.")

    with st.expander("이 화면에 사용된 주요 요소 보기"):
        st.write("`st.metric`은 핵심 숫자와 변화량을, `st.dataframe`은 표를, `st.line_chart`와 `st.bar_chart`는 차트를 보여줍니다.")
