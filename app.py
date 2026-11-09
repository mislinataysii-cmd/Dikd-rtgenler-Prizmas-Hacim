import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="MAT.7.4.4.ç - 3D Prizma ve Hacim Laboratuvarı",
    layout="wide",
)

st.title("📐 3D Prizma ve Hacim Hesaplama Laboratuvarı (MAT.7.4.4.ç)")
st.write(
    "Bu uygulama; şeffaf kutuları, sınırlı birim küpleri (L-iskelet), farklı"
    " yüzleri taban seçme stratejilerini ve dinamik renklendirmeyi tamamen kendi"
    " kontrolünüzde deneyimlemeniz için tasarlandı."
)

# --- YAN PANEL (KONTROL MERKEZİ) ---
st.sidebar.header("🎛️ Laboratuvar Kontrolleri")

# 1. Kutu / Prizma Seçimi
kutu_tipi = st.sidebar.selectbox(
    "1. Şeffaf Kutu / Model Seçimi",
    [
        "1. Kutu: 2 x 2 x 4 (Kare Prizma)",
        "2. Kutu: 2 x 4 x 4 (Dik Konum)",
        "2. Kutu: 4 x 4 x 2 (Yan Yatırılmış)",
        "3. Kutu: 4 x 4 x 4 (Küp Kiler)",
        "Özel Boyut (Manuel Sürgüler)",
    ],
)

if "Kare Prizma" in kutu_tipi:
  a, b, h = 2, 2, 4
elif "Dik Konum" in kutu_tipi:
  a, b, h = 2, 4, 4
elif "Yan Yatırılmış" in kutu_tipi:
  a, b, h = 4, 4, 2
elif "Küp Kiler" in kutu_tipi:
  a, b, h = 4, 4, 4
else:
  a = st.sidebar.slider("Boy (a)", 1, 6, 2)
  b = st.sidebar.slider("En (b)", 1, 6, 4)
  h = st.sidebar.slider("Yükseklik (h)", 1, 6, 4)

# 2. Taban Kabul Edilen Yüz (Yön)
yon = st.sidebar.selectbox(
    "2. Taban Kabul Edilen Yüz",
    [
        "Alt Yüz Taban (Yukarı Katmanlanma)",
        "Ön Yüz Taban (Arkaya Katmanlanma)",
        "Yan Yüz Taban (Sağa Katmanlanma)",
    ],
)

if "Alt Yüz" in yon:
  yon_val, ta, yuksek = 1, a * b, h
elif "Ön Yüz" in yon:
  yon_val, ta, yuksek = 2, a * h, b
else:
  yon_val, ta, yuksek = 3, b * h, a

# 3. Katman Sürgüsü
max_kat = yuksek
kat = st.sidebar.slider(
    "3. Dolu Katman Sayısı (kat)", 0, max_kat, min(1, max_kat)
)

# 4. Görünüm Seçenekleri
goster_iskelet = st.sidebar.checkbox(
    "Sınırlı Küp (L-İskelet) Göster", value=True
)

# 5. Renk Seçimi
secilen_renk = st.sidebar.color_picker(
    "4. Katman / Küp Rengi Seçimi", "#43a047"
)

# --- 3D GRAFİK OLUŞTURMA (PLOTLY) ---
fig = go.Figure()

# A. Şeffaf Ana Kutu
fig.add_trace(
    go.Mesh3d(
        x=[0, a, a, 0, 0, a, a, 0],
        y=[0, 0, b, b, 0, 0, b, b],
        z=[0, 0, 0, 0, h, h, h, h],
        i=[7, 0, 0, 0, 4, 4, 2, 1, 6, 5, 2, 3],
        j=[3, 4, 1, 2, 5, 6, 3, 5, 5, 1, 6, 7],
        k=[0, 1, 2, 3, 6, 7, 1, 2, 4, 0, 5, 6],
        color="lightblue",
        opacity=0.15,
        name="Şeffaf Prizma Kutu",
        flatshading=True,
    )
)

# B. Sınırlı Küp (L-İskelet) Çizimi
if goster_iskelet:
  for i in range(1, a + 1):
    fig.add_trace(
        go.Mesh3d(
            x=[i - 1, i, i, i - 1, i - 1, i, i, i - 1],
            y=[0, 0, 1, 1, 0, 0, 1, 1],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
            color="royalblue",
            opacity=0.8,
            name="L-İskelet",
        )
    )
  for j in range(2, b + 1):
    fig.add_trace(
        go.Mesh3d(
            x=[0, 1, 1, 0, 0, 1, 1, 0],
            y=[j - 1, j - 1, j, j, j - 1, j - 1, j, j],
            z=[0, 0, 0, 0, 1, 1, 1, 1],
            color="gold",
            opacity=0.8,
            name="L-İskelet",
        )
    )
  for k in range(2, h + 1):
    fig.add_trace(
        go.Mesh3d(
            x=[0, 1, 1, 0, 0, 1, 1, 0],
            y=[0, 0, 1, 1, 0, 0, 1, 1],
            z=[k - 1, k - 1, k - 1, k - 1, k, k, k, k],
            color="crimson",
            opacity=0.8,
            name="L-İskelet",
        )
    )

# C. Seçilen Yöne ve Katmana Göre Birim Küplerin Katmanlanması
if kat > 0:
  for k_idx in range(kat):
    if yon_val == 1:
      for i in range(1, a + 1):
        for j in range(1, b + 1):
          fig.add_trace(
              go.Mesh3d(
                  x=[
                      i - 1,
                      i,
                      i,
                      i - 1,
                      i - 1,
                      i,
                      i,
                      i - 1,
                  ],
                  y=[
                      j - 1,
                      j - 1,
                      j,
                      j,
                      j - 1,
                      j - 1,
                      j,
                      j,
                  ],
                  z=[
                      k_idx,
                      k_idx,
                      k_idx,
                      k_idx,
                      k_idx + 1,
                      k_idx + 1,
                      k_idx + 1,
                      k_idx + 1,
                  ],
                  color=secilen_renk,
                  opacity=0.75,
                  name=f"Katman {k_idx+1}",
              )
          )
    elif yon_val == 2:
      for i in range(1, a + 1):
        for k_i in range(1, h + 1):
          fig.add_trace(
              go.Mesh3d(
                  x=[
                      i - 1,
                      i,
                      i,
                      i - 1,
                      i - 1,
                      i,
                      i,
                      i - 1,
                  ],
                  y=[
                      k_idx,
                      k_idx,
                      k_idx + 1,
                      k_idx + 1,
                      k_idx,
                      k_idx,
                      k_idx + 1,
                      k_idx + 1,
                  ],
                  z=[
                      k_i - 1,
                      k_i - 1,
                      k_i - 1,
                      k_i - 1,
                      k_i,
                      k_i,
                      k_i,
                      k_i,
                  ],
                  color=secilen_renk,
                  opacity=0.75,
                  name=f"Katman {k_idx+1}",
              )
          )
    else:
      for j in range(1, b + 1):
        for k_i in range(1, h + 1):
          fig.add_trace(
              go.Mesh3d(
                  x=[
                      k_idx,
                      k_idx + 1,
                      k_idx + 1,
                      k_idx,
                      k_idx,
                      k_idx + 1,
                      k_idx + 1,
                      k_idx,
                  ],
                  y=[
                      j - 1,
                      j - 1,
                      j,
                      j,
                      j - 1,
                      j - 1,
                      j,
                      j,
                  ],
                  z=[
                      k_i - 1,
                      k_i - 1,
                      k_i - 1,
                      k_i - 1,
                      k_i,
                      k_i,
                      k_i,
                      k_i,
                  ],
                  color=secilen_renk,
                  opacity=0.75,
                  name=f"Katman {k_idx+1}",
              )
          )

fig.update_layout(
    scene=dict(
        xaxis_title="Boy (a)",
        yaxis_title="En (b)",
        zaxis_title="Yükseklik (h)",
        xaxis=dict(range=[0, max(a, b, h)]),
        yaxis=dict(range=[0, max(a, b, h)]),
        zaxis=dict(range=[0, max(a, b, h)]),
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600,
)

# --- ANA EKRAN BİLGİ VE ANALİZ PANELİ ---
col1, col2 = st.columns([2, 1])

with col1:
  st.subheader("🧊 3D Prizma Görselleştirme Laboratuvarı")
  st.plotly_chart(fig, use_container_width=True, key="prizma_3d_grafik")

with col2:
  st.subheader("📊 Hacim Analizi (V = TA × h)")
  st.info(
      f"**Seçilen Kutu Boyutları:** {a} × {b} × {h}\n\n"
      f"**Seçilen Taban Alanı (TA):** {ta} br²\n\n"
      f"**İlgili Yükseklik (h):** {yuksek} br\n\n"
      f"**Toplam Hacim (V):** {ta} × {yuksek} = **{a * b * h} br³**"
  )

  st.success(
      "💡 **Pedagojik Not:** Sol panelden kutu seçebilir, katmanları"
      " artırabilir, farklı yüzleri taban seçebilir ve renk paletiyle küpleri"
      " dilediğiniz renge boyayarak hacmin korunumunu gözlemleyebilirsiniz."
  )
