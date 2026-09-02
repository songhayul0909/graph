import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 가운데, 해당 기간에 개봉한 216편을 정리한 자료입니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일(여덟 자리 숫자) -> 날짜 타입
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    # 장르는 세로막대(|) 기호로 여러 개가 적혀 있으므로, 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0]

    return df


df = load_data()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# 그래프 1. 장르별 영화 편수 - 도넛 그래프
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .rename_axis("genre")
    .reset_index(name="count")
)

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textposition="inside",
    textinfo="label+percent",
    hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=20, b=20, l=0, r=0),
)

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "장르마다 흥행 상위권에 진입한 영화 편수가 얼마나 차이 나는지, "
    "어떤 장르가 박스오피스 10위권을 자주 차지했는지 알 수 있습니다."
)

st.divider()

# ---------------------------------------------------------
# 이후 그래프를 위한 구역 (추가 예정)
# ---------------------------------------------------------
# st.header("2. ...")
# ...
# st.markdown("**이 그래프로 알 수 있는 것:** ...")
# st.divider()
