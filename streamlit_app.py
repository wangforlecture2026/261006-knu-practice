import pandas as pd
import streamlit as st

st.set_page_config(page_title="Streamlit 요소 체험실", page_icon="🧪", layout="wide")

st.title("🧪 Streamlit 요소 체험실")
st.write("화면을 만들 때 쓰는 요소들을 직접 눌러 보며 익혀 보세요.")
st.caption("아래 탭을 이동하고 값을 바꿔 보세요. 조작할 때마다 페이지가 다시 실행되며 결과가 업데이트됩니다.")

text_tab, input_tab, data_tab = st.tabs(["텍스트와 레이아웃", "입력 위젯", "표와 차트"])

with text_tab:
    st.header("텍스트와 화면 구성")
    st.markdown("`st.title`, `st.header`, `st.write`로 제목과 설명을 배치합니다.")
    st.subheader("제목은 정보를 층층이 정리해요")
    st.write("`st.write`는 글, 숫자, 표 등 다양한 값을 화면에 보여 주는 기본 출력 도구입니다.")
    st.caption("`st.caption`은 출처나 짧은 보충 설명처럼 작은 글씨가 어울릴 때 사용합니다.")
    st.divider()

    left, right = st.columns(2)
    with left:
        st.info("안내 메시지: 참고할 내용을 알려 줍니다.")
        st.success("성공 메시지: 작업이 잘 끝났음을 알려 줍니다.")
    with right:
        st.warning("주의 메시지: 확인이 필요한 상황을 보여 줍니다.")
        st.error("오류 메시지: 문제가 생겼음을 알려 줍니다.")

    with st.expander("접었다 펼치는 설명 보기"):
        st.write("`st.expander`는 필요할 때만 펼쳐 보는 설명이나 부가 정보를 담습니다.")
    st.code('st.write("안녕하세요, Streamlit!")', language="python")

with input_tab:
    st.header("직접 값을 입력해 보세요")
    st.write("입력 위젯은 사용자의 선택이나 값을 받아 앱의 다음 동작에 전달합니다.")

    name = st.text_input("이름", placeholder="예: 민지")
    if st.button("인사 받기", icon="👋"):
        if name.strip():
            st.success(f"반가워요, {name.strip()}님!")
        else:
            st.warning("먼저 이름을 입력해 주세요.")

    comment = st.text_area("한 줄 소감", placeholder="어떤 요소가 가장 궁금한가요?")
    st.caption(f"글자 수: {len(comment)}")

    col_one, col_two = st.columns(2)
    with col_one:
        favorite = st.selectbox("좋아하는 과일", ["사과", "바나나", "포도", "귤"])
        mood = st.radio("오늘의 기분", ["좋음", "보통", "피곤함"], horizontal=True)
        quantity = st.number_input("개수", min_value=1, max_value=20, value=3)
    with col_two:
        toppings = st.multiselect("토핑 고르기", ["치즈", "올리브", "버섯", "옥수수"])
        score = st.slider("만족도", min_value=0, max_value=100, value=70, step=5)
        show_summary = st.checkbox("선택 결과 표시")

    if show_summary:
        st.info(f"{favorite} {quantity}개 · 기분: {mood} · 만족도: {score}점 · 토핑: {', '.join(toppings) or '없음'}")

    st.subheader("폼: 여러 입력을 한 번에 제출하기")
    st.write("폼 안의 값은 제출 버튼을 누를 때 함께 전달됩니다.")
    with st.form("favorite_form"):
        favorite_color = st.text_input("좋아하는 색", key="favorite_color")
        reason = st.text_input("좋아하는 이유", key="favorite_reason")
        submitted = st.form_submit_button("폼 제출", icon="📨")
    if submitted:
        st.success(f"응답을 받았어요: {favorite_color or '색 미입력'} / {reason or '이유 미입력'}")

with data_tab:
    st.header("데이터 표와 차트")
    st.write("표의 셀을 직접 수정하면 아래 요약과 차트도 바뀝니다.")

    sample_data = pd.DataFrame(
        [
            {"월": month, "분류": category, "매출": base + month * growth, "주문": 12 + month * 2 + offset}
            for category, base, growth, offset in [("음료", 40, 5, 2), ("간식", 28, 4, 0), ("식사", 55, 7, 4)]
            for month in range(1, 13)
        ]
    )

    filter_col, period_col, chart_col = st.columns(3)
    with filter_col:
        selected_category = st.selectbox("분류 필터", ["전체", "음료", "간식", "식사"])
    with period_col:
        month_count = st.slider("표시할 최근 개월 수", min_value=3, max_value=12, value=12)
    with chart_col:
        chart_type = st.radio("차트 종류", ["선", "막대", "영역"], horizontal=True)

    filtered_data = sample_data[sample_data["월"] > 12 - month_count]
    if selected_category != "전체":
        filtered_data = filtered_data[filtered_data["분류"] == selected_category]

    st.markdown("**편집 가능한 표** · `st.data_editor`로 데이터를 확인하고 수정합니다.")
    edited_data = st.data_editor(filtered_data, hide_index=True, width="stretch", num_rows="dynamic")

    if not edited_data.empty:
        total_sales = edited_data["매출"].sum()
        average_orders = edited_data["주문"].mean()
        metric_col_one, metric_col_two = st.columns(2)
        metric_col_one.metric("표에 담긴 매출 합계", f"{total_sales:,.0f}")
        metric_col_two.metric("평균 주문 수", f"{average_orders:,.1f}")

        chart_data = edited_data.pivot_table(index="월", columns="분류", values="매출", aggfunc="sum").sort_index()
        st.markdown("**차트** · 숫자 데이터를 선, 막대, 영역으로 시각화합니다.")
        if chart_type == "선":
            st.line_chart(chart_data)
        elif chart_type == "막대":
            st.bar_chart(chart_data)
        else:
            st.area_chart(chart_data)
    else:
        st.info("표시할 데이터가 없습니다. 필터를 바꿔 보세요.")

    st.markdown("**읽기 전용 표** · `st.dataframe`은 데이터를 살펴볼 때 사용합니다.")
    st.dataframe(sample_data.head(5), hide_index=True, width="stretch")
