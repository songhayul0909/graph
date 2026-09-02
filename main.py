import streamlit as st
import pandas as pd
import numpy as np
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
# 그래프 2. 장르 안에 영화 - 트리맵 (칸 크기: 총 관객)
# ---------------------------------------------------------
st.header("2. 장르 속 영화별 총 관객 (트리맵)")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(margin=dict(t=20, b=20, l=0, r=0))

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "같은 장르 안에서도 어떤 영화가 총 관객을 많이 끌어모았는지, "
    "장르별 흥행을 이끈 대표작이 무엇인지 한눈에 알 수 있습니다."
)

st.divider()

# ---------------------------------------------------------
# 그래프 3. 총 관객 히스토그램
# ---------------------------------------------------------
st.header("3. 총 관객 분포 (히스토그램)")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
)
fig_hist.update_traces(
    hovertemplate="총 관객 구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수",
    margin=dict(t=20, b=20, l=0, r=0),
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 많이 몰려 있는 구간과 최다 관객 영화 계산
hist_counts, hist_edges = np.histogram(df["total_audi"], bins=30)
top_bin_idx = hist_counts.argmax()
bin_start, bin_end = hist_edges[top_bin_idx], hist_edges[top_bin_idx + 1]

top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"**이 그래프로 알 수 있는 것:** "
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있고, "
    f"가장 관객이 많은 영화는 **'{top_movie['movieNm']}'**"
    f"(총 관객 {top_movie['total_audi']:,}명)입니다."
)

st.divider()

# ---------------------------------------------------------
# 그래프 4. 개봉일 스크린수 vs 총 관객 - 산점도 (장르별 색)
# ---------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계 (산점도)")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="영화명: %{hovertext}<br>개봉일 스크린수: %{x:,}<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르",
    margin=dict(t=20, b=20, l=0, r=0),
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "개봉일에 스크린을 많이 확보한 영화일수록 총 관객이 많은 경향이 있는지, "
    "장르에 따라 그 경향이 어떻게 다른지 알 수 있습니다."
)

st.divider()

# ---------------------------------------------------------
# 그래프 5. 영화 10편 이상 장르의 총 관객 상자 그림
# ---------------------------------------------------------
st.header("5. 장르별 총 관객 분포 (상자 그림)")

genre_movie_counts = df["genre"].value_counts()
major_genres = genre_movie_counts[genre_movie_counts >= 10].index
df_major_genres = df[df["genre"].isin(major_genres)]

fig_box = px.box(
    df_major_genres,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_data={"movieNm": True},
)
fig_box.update_traces(
    hovertemplate="영화명: %{customdata[0]}<br>총 관객: %{y:,}명<extra></extra>",
)
fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객",
    margin=dict(t=20, b=20, l=0, r=0),
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "영화 10편 이상인 주요 장르들의 총 관객 중앙값과 흩어진 정도를 비교할 수 있고, "
    "상자 밖으로 튀는 이상치(대박 흥행작)가 어떤 영화인지 알 수 있습니다."
)

st.divider()

# ---------------------------------------------------------
# 그래프 6. 스크린수 x 총 관객 x 첫 주 관객 - 버블 그래프
# ---------------------------------------------------------
st.header("6. 개봉일 스크린수·총 관객·첫 주 관객 (버블 그래프)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
)
fig_bubble.update_traces(
    hovertemplate="영화명: %{hovertext}<br>개봉일 스크린수: %{x:,}<br>총 관객: %{y:,}명<extra></extra>",
)
fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르",
    margin=dict(t=20, b=20, l=0, r=0),
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "같은 스크린수·총 관객 조합이라도 첫 주 관객(거품 크기)이 큰 영화는 "
    "초반 흥행 몰이가 얼마나 강했는지를 함께 비교할 수 있습니다."
)

st.divider()

# ---------------------------------------------------------
# 그래프 7. 제작 국가 -> 장르 - 선버스트 그래프
# ---------------------------------------------------------
st.header("7. 제작 국가별 장르 구성 (선버스트)")

fig_sunburst = px.sunburst(
    df,
    path=["nation", "genre"],
)
fig_sunburst.update_traces(
    hovertemplate="%{label}<br>영화 편수: %{value}편<extra></extra>",
)
fig_sunburst.update_layout(margin=dict(t=20, b=20, l=0, r=0))

st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "어떤 국가가 박스오피스 10위권 영화를 많이 만들었는지, "
    "그 국가 안에서는 어떤 장르가 주로 흥행했는지 함께 알 수 있습니다."
)

st.divider()
