import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------
# 1. 기본 설정 (페이지 구성)
# -------------------------------
st.set_page_config(
    page_title="영화 관객 통계 분석",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용 (가독성 향상)
st.markdown("""
    <style>
        .metric-card {
            background-color: #f8f9fa;
            padding: 18px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .main-title {
            color: #2d3748;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .section-title {
            color: #4a5568;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 2. 제목과 설명
# -------------------------------
st.markdown("<h1 class='main-title'>🎬 영화 관객 통계 분석 대시보드</h1>", unsafe_allow_html=True)
st.write("""
    최신 영화들의 관객수、매출액、평점等을 종합적으로 분석할 수 있는 플랫폼입니다.
    - 사이드바에서 장르、국가、개봉년도等 필터를 설정하여 원하는 영화 데이터를 찾아보세요.
    - 다양한 그래프를 통해 영화 성과를 직관적으로 비교할 수 있습니다.
    - 실시간으로 필터에 맞는 통계 정보를 제공합니다.
""")

# -------------------------------
# 3. 영화 데이터 생성 (실제 데이터와 유사한 형태)
# -------------------------------
@st.cache_data(ttl=3600)  # 1시간 캐시 유지 (성능 최적화)
def load_movie_data():
    """영화 데이터 로딩 함수 (실제 서비스에서는 DB/API 연동 가능)"""
    movies = {
        "영화명": [
            "오ppenheimer", "바비", "스파이더맨: 노 웨이 홈", "아바타: 물의 길",
            "이터널스", "블랙 팬서: 와칸다 포에버", "토르: 러브 앤 썬더",
            "극한직업", "알라딘", "겨울왕국 2", "기생충", "올드보이",
            "매드맥스: 분노의 도로", "인셉션", "어벤져스: 엔드게임",
            "겨울왕국", "冰雪奇缘", "주토피아", "슬럼독 밀리어네어", "쇼생크 탈출"
        ],
        "국가": [
            "미국", "미국", "미국", "미국", "미국", "미국", "미국",
            "한국", "미국", "미국", "한국", "한국", "호주", "미국", "미국",
            "미국", "중국", "미국", "인도", "미국"
        ],
        "장르": [
            "역사/드라마", "코미디/판타지", "액션/슈퍼히어로", "SF/어드벤처",
            "슈퍼히어로/판타지", "액션/드라마", "코미디/슈퍼히어로",
            "코미디/범죄", "어드벤처/가족", "애니메이션/가족", "드라마/스릴러",
            "스릴러/역동", "액션/SF", "SF/스릴러", "액션/슈퍼히어로",
            "애니메이션/가족", "애니메이션/가족", "애니메이션/어드벤처",
            "드라마/모험", "드라마/범죄"
        ],
        "개봉년도": [
            2023, 2023, 2021, 2022, 2021, 2022, 2022,
            2019, 2019, 2019, 2019, 2003, 2015, 2010, 2019,
            2013, 2013, 2016, 2008, 1994
        ],
        "관객수(만명)": [
            1280, 1420, 2280, 1830, 890, 1150, 980,
            1620, 1380, 1250, 1030, 380, 720, 1050, 2350,
            1580, 950, 1420, 680, 450
        ],
        "매출액(억원)": [
            1850, 2080, 3250, 2650, 1280, 1680, 1420,
            2380, 1980, 1820, 1520, 560, 1050, 1530, 3420,
            2280, 1380, 2050, 980, 650
        ],
        "평점(IMDB)": [
            8.5, 7.1, 8.4, 7.9, 6.3, 6.9, 6.8,
            7.6, 7.0, 7.0, 8.5, 8.4, 8.1, 8.8, 8.4,
            7.5, 7.8, 8.1, 8.0, 9.3
        ],
        "상영 기간(일)": [
            120, 150, 180, 210, 90, 120, 100,
            160, 140, 150, 130, 80, 110, 140, 190,
            160, 120, 150, 100, 90
        ]
    }
    return pd.DataFrame(movies)

# 데이터 로드
df_movies = load_movie_data()

# -------------------------------
# 4. 사이드바 필터 설정 (영화 관련 필터)
# -------------------------------
with st.sidebar:
    st.header("⚙️ 필터 설정")
    st.markdown("---")  # 구분선
    
    # 1. 국가 필터
    country_filter = st.multiselect(
        "국가 선택:",
        options=df_movies["국가"].unique(),
        default=df_movies["국가"].unique(),
        help="분석할 영화의 제작 국가를 선택하세요"
    )
    
    # 2. 장르 필터
    genre_filter = st.multiselect(
        "장르 선택:",
        options=df_movies["장르"].unique(),
        default=df_movies["장르"].unique(),
        help="관심있는 영화 장르를 선택하세요"
    )
    
    # 3. 개봉년도 필터 (슬라이더)
    min_year = df_movies["개봉년도"].min()
    max_year = df_movies["개봉년도"].max()
    year_range = st.slider(
        "개봉년도 범위:",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(int(min_year), int(max_year)),
        help="원하는 기간의 영화를 필터링하세요"
    )
    
    # 4. 영화 검색 (부분 검색 가능)
    search_movie = st.text_input(
        "영화명 검색 (예: 기생충)",
        help="영화명을 부분적으로 입력해도 검색 가능합니다"
    )
    
    # 5. 정렬 옵션
    st.markdown("---")
    st.subheader("📶 정렬 설정")
    col1, col2 = st.columns(2)
    with col1:
        sort_option = st.selectbox(
            "정렬 기준:",
            ["관객수(만명)", "매출액(억원)", "평점(IMDB)", "개봉년도"],
            index=0
        )
    with col2:
        sort_order = st.radio(
            "순서:",
            ["내림차순", "오름차순"],
            horizontal=True,
            index=0
        )
    
    # 6. 그래프 종류 선택
    st.markdown("---")
    st.subheader("📊 그래프 선택")
    graph_type = st.radio(
        "보고 싶은 그래프:",
        [
            "관객수 비교", "매출액 비교", "평점 비교", 
            "장르 분포", "국가별 영화 수"
        ],
        index=0
    )
    
    # 7. 데이터 테이블 표시 여부
    show_table = st.checkbox("영화 데이터 표시", value=True)

# -------------------------------
# 5. 데이터 필터링 처리
# -------------------------------
# 기본 필터 적용 (국가、장르、개봉년도)
filtered_df = df_movies[
    (df_movies["국가"].isin(country_filter)) &
    (df_movies["장르"].isin(genre_filter)) &
    (df_movies["개봉년도"].between(year_range[0], year_range[1]))
].copy()

# 영화명 검색 필터 (대소문자 무시)
if search_movie:
    filtered_df = filtered_df[
        filtered_df["영화명"].str.contains(search_movie, case=False, na=False)
    ]

# 정렬 처리
ascending = (sort_order == "오름차순")
filtered_df = filtered_df.sort_values(by=sort_option, ascending=ascending).reset_index(drop=True)

# -------------------------------
# 6. 통계 정보 및 데이터 개요
# -------------------------------
st.markdown("<h2 class='section-title'>📈 데이터 개요</h2>", unsafe_allow_html=True)

# 통계 메트릭 카드 (3열로 표시)
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("총 영화 수")
    st.metric(label="", value=len(filtered_df), delta=f"총 {len(df_movies)}편 중")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("평균 관객수")
    if not filtered_df.empty:
        avg_audience = filtered_df["관객수(만명)"].mean()
        st.metric(label="", value=f"{avg_audience:.1f}만명")
    else:
        st.metric(label="", value="0만명")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("평균 평점")
    if not filtered_df.empty:
        avg_rating = filtered_df["평점(IMDB)"].mean()
        st.metric(label="", value=f"{avg_rating:.1f}점")
    else:
        st.metric(label="", value="0.0점")
    st.markdown("</div>", unsafe_allow_html=True)

# 추가 통계 메트릭 (2열로 표시)
col4, col5 = st.columns(2, gap="medium")

with col4:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("총 매출액")
    if not filtered_df.empty:
        total_revenue = filtered_df["매출액(억원)"].sum()
        st.metric(label="", value=f"{total_revenue:,.0f}억원")
    else:
        st.metric(label="", value="0억원")
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.subheader("평균 상영 기간")
    if not filtered_df.empty:
        avg_run_time = filtered_df["상영 기간(일)"].mean()
        st.metric(label="", value=f"{avg_run_time:.0f}일")
    else:
        st.metric(label="", value="0일")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 7. 영화 데이터 테이블 표시
# -------------------------------
if show_table:
    st.markdown("<h2 class='section-title'>📋 영화 상세 데이터</h2>", unsafe_allow_html=True)
    if filtered_df.empty:
        st.info("🔍 선택한 필터 조건에 해당하는 영화 데이터가 없습니다. 필터를 조정해보세요.")
    else:
        # 데이터프레임 스타일 적용
        st.dataframe(
            filtered_df.style.format({
                "관객수(만명)": "{:.1f}",
                "매출액(억원)": "{:,.0f}",
                "평점(IMDB)": "{:.1f}",
                "상영 기간(일)": "{:.0f}"
            }),
            use_container_width=True,
            height=300
        )

# -------------------------------
# 8. 그래프 출력 (데이터 유무에 따른 처리)
# -------------------------------
st.markdown("<h2 class='section-title'>📊 시각화 분석</h2>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ 필터 조건에 맞는 데이터가 없어 그래프를 표시할 수 없습니다.")
else:
    # 그래프 색상 테마 설정
    color_theme = px.colors.qualitative.Set3
    
    if graph_type == "관객수 비교":
        # 막대 그래프 - 영화별 관객수 비교
        fig = px.bar(
            filtered_df.head(10),  # 상위 10개만 표시 (가독성 향상)
            x="영화명",
            y="관객수(만명)",
            color="국가",
            text="관객수(만명)",
            title="영화별 관객수 TOP 10",
            color_discrete_sequence=color_theme,
            labels={"관객수(만명)": "관객수 (만명)"}
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "매출액 비교":
        # 라인 그래프 - 영화별 매출액 비교
        fig = px.line(
            filtered_df.head(10),
            x="영화명",
            y="매출액(억원)",
            markers=True,
            color="장르",
            title="영화별 매출액 TOP 10",
            text="매출액(억원)",
            color_discrete_sequence=color_theme,
            labels={"매출액(억원)": "매출액 (억원)"}
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="top center")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "평점 비교":
        # 산점도 그래프 - 평점 vs 관객수 관계
        fig = px.scatter(
            filtered_df,
            x="평점(IMDB)",
            y="관객수(만명)",
            size="매출액(억원)",
            color="장르",
            hover_name="영화명",
            title="영화 평점 vs 관객수 관계",
            color_discrete_sequence=color_theme,
            labels={
                "평점(IMDB)": "IMDB 평점",
                "관객수(만명)": "관객수 (만명)",
                "매출액(억원)": "매출액 (억원)"
            },
            size_max=60
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "장르 분포":
        # 원형 그래프 - 장르별 영화 수 분포
        genre_counts = filtered_df["장르"].value_counts().reset_index()
        genre_counts.columns = ["장르", "영화 수"]
        
        fig = px.pie(
            genre_counts,
            names="장르",
            values="영화 수",
            title="장르별 영화 수 분포",
            color_discrete_sequence=color_theme,
            hole=0.3,  # 도넛 차트 형태
            hover_data=["영화 수"]
        )
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "국가별 영화 수":
        # 막대 그래프 - 국가별 영화 수 및 평균 관객수
        country_stats = filtered_df.groupby("국가").agg({
            "영화명": "count",
            "관객수(만명)": "mean"
        }).reset_index()
        country_stats.columns = ["국가", "영화 수", "평균 관객수"]
        
        fig = px.bar(
            country_stats,
            x="국가",
            y="영화 수",
            color="국가",
            title="국가별 영화 수 및 평균 관객수",
            color_discrete_sequence=color_theme,
            secondary_y="평균 관객수",
            labels={
                "영화 수": "영화 편수",
                "평균 관객수": "평균 관객수 (만명)"
            }
        )
        fig.add_trace(
            px.line(
                country_stats,
                x="국가",
                y="평균 관객수",
                color_discrete_sequence=["red"]
            ).data[0],
            secondary_y=True
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 9. 푸터 정보
# -------------------------------
st.markdown("---")
st.caption("📌 데이터는 예시이며, 실제 영화 통계와는 다를 수 있습니다. | 업데이트 날짜: 2024.10.20")
