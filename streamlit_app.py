import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# 1. 기본 설정
# -------------------------------
st.set_page_config(
    page_title="탁구 선수 경력 통계 분석",
    page_icon="🏓",
    layout="wide"
)

# -------------------------------
# 2. 제목과 설명
# -------------------------------
st.title("🏓 탁구 선수의 직업 경력 통계 분석")
st.write("""
    프로 탁구 선수들의 경기 수, 승률, 우승 기록 등을 시각화하여 한눈에 분석할 수 있는 대시보드입니다.
    사이드바에서 필터를 설정하여 원하는 데이터를 확인하세요.
""")

# -------------------------------
# 3. 데이터 생성 (더 완성된 형태)
# -------------------------------
@st.cache_data  # 数据缓存，提升性能
def load_data():
    players = {
        "선수명": ["판젠동", "마롱", "장본", "이상수", "장우진", "티모 볼", "볼리스라브 샤라тов", "다니엘 헤르만"],
        "국가": ["중국", "중국", "중국", "한국", "한국", "독일", "러시아", "독일"],
        "나이": [27, 36, 25, 33, 28, 43, 31, 29],
        "세계랭킹 최고": [1, 1, 3, 6, 5, 1, 4, 8],
        "우승 횟수": [23, 30, 12, 5, 8, 27, 15, 9],
        "커리어 경기 수": [420, 680, 350, 500, 410, 900, 450, 380],
        "승률(%)": [89, 86, 78, 74, 76, 80, 79, 75]
    }
    return pd.DataFrame(players)

df = load_data()

# -------------------------------
# 4. 사이드바 필터 설정
# -------------------------------
with st.sidebar:
    st.header("⚙️ 필터 설정")
    
    # 국가 선택
    country_filter = st.multiselect(
        "국가 선택:",
        options=df["국가"].unique(),
        default=df["국가"].unique(),
        help="분석할 선수의 국가를 선택하세요"
    )
    
    # 선수 검색 (대소문자 무시)
    search_name = st.text_input(
        "선수 검색 (예: 마롱)",
        help="선수명을 부분적으로 입력해도 검색 가능합니다"
    )
    
    # 정렬 옵션과 순서
    col1, col2 = st.columns(2)
    with col1:
        sort_option = st.selectbox(
            "정렬 기준:",
            ["승률(%)", "우승 횟수", "커리어 경기 수", "나이"],
            help="데이터 정렬 기준을 선택하세요"
        )
    with col2:
        sort_order = st.radio(
            "정렬 순서:",
            ["내림차순", "오름차순"],
            horizontal=True
        )
    
    # 데이터 보이기 여부
    show_table = st.checkbox("선수 데이터 표시", value=True)
    
    # 그래프 선택
    graph_type = st.radio(
        "그래프 종류 선택:",
        ["승률 비교", "경기 수 비교", "우승 횟수 비교", "국가 분포"]
    )

# -------------------------------
# 5. 데이터 필터링 처리
# -------------------------------
#  국가 필터 적용
filtered_df = df[df["국가"].isin(country_filter)].copy()

#  이름 검색 필터 (대소문자 무시)
if search_name:
    filtered_df = filtered_df[
        filtered_df["선수명"].str.contains(search_name, case=False, na=False)
    ]

#  정렬 처리
ascending = (sort_order == "오름차순")
filtered_df = filtered_df.sort_values(by=sort_option, ascending=ascending)

# -------------------------------
# 6. 데이터 확인 및 통계 정보
# -------------------------------
st.subheader("📊 데이터 개요")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 선수 수", len(filtered_df))
with col2:
    if not filtered_df.empty:
        st.metric("평균 승률", f"{filtered_df['승률(%)'].mean():.1f}%")
with col3:
    if not filtered_df.empty:
        st.metric("총 우승 횟수", filtered_df['우승 횟수'].sum())

#  데이터 테이블 표시 (데이터가 비어있을 때 처리)
if show_table:
    st.subheader("📋 선수 기본 데이터")
    if filtered_df.empty:
        st.info("선택한 조건에 해당하는 선수 데이터가 없습니다. 필터를 조정해보세요.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# 7. 그래프 출력 (데이터가 비어있을 때 처리)
# -------------------------------
if filtered_df.empty:
    st.warning("필터 조건에 맞는 데이터가 없어 그래프를 표시할 수 없습니다.")
else:
    if graph_type == "승률 비교":
        st.subheader("📈 선수별 승률 비교")
        fig = px.bar(
            filtered_df,
            x="선수명",
            y="승률(%)",
            color="국가",
            text="승률(%)",
            color_discrete_sequence=px.colors.qualitative.D3,
            title="선수별 승률 분포"
        )
        fig.update_layout(yaxis_range=[0, 100])  # 승률은 0-100%로 제한
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == "경기 수 비교":
        st.subheader("🏆 선수별 커리어 경기 수")
        fig = px.line(
            filtered_df,
            x="선수명",
            y="커리어 경기 수",
            markers=True,
            color="국가",
            title="선수별 경력 경기 수",
            text="커리어 경기 수"
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == "우승 횟수 비교":
        st.subheader("🥇 선수 우승 횟수 비교")
        fig = px.bar(
            filtered_df,
            x="선수명",
            y="우승 횟수",
            color="국가",
            text="우승 횟수",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="선수별 총 우승 횟수"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == "국가 분포":
        st.subheader("🌍 국가별 선수 분포")
        country_counts = filtered_df["국가"].value_counts().reset_index()
        country_counts.columns = ["국가", "선수 수"]
        
        fig = px.pie(
            country_counts,
            names="국가",
            values="선수 수",
            title="국가별 선수 수 분포",
            hole=0.3,  #  doughnut chart 형태
            hover_data=["선수 수"],
            labels={"선수 수": "총 선수 수"}
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

# 页脚信息
st.caption("💡 데이터는 예시이며, 실제 프로 선수 통계와는 다를 수 있습니다.")
