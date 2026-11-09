import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="MAT.7.4.4.ç - 3D Prizma ve Hacim Laboratuvarı", layout="wide"
)


# --- TÜM 6 YÜZÜ TAM BOYALI 3B KÜP / PRİZMA ÇİZİM FONKSİYONU ---
def add_solid_box(
    fig,
    x0,
    y0,
    z0,
    dx,
    dy,
    dz,
    color,
    opacity=1.0,
    edge_color="#1a1a1a",
    edge_width=3,
    name="",
):
  vx = [x0, x0 + dx, x0 + dx, x0, x0, x0 + dx, x0 + dx, x0]
  vy = [y0, y0, y0 + dy, y0 + dy, y0, y0, y0 + dy, y0 + dy]
  vz = [z0, z0, z0, z0, z0 + dz, z0 + dz, z0 + dz, z0 + dz]
  i_idx = [0, 0, 4, 4, 0, 0, 3, 3, 0, 0, 1, 1]
  j_idx = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 2, 6]
  k_idx = [2, 3, 6, 7, 5, 4, 6, 7, 7, 4, 6, 5]

  fig.add_trace(
      go.Mesh3d(
          x=vx,
          y=vy,
          z=vz,
          i=i_idx,
          j=j_idx,
          k=k_idx,
          color=color,
          opacity=opacity,
          flatshading=True,
          lighting=dict(ambient=0.8, diffuse=0.6, specular=0.2),
          name=name,
          showscale=False,
          hoverinfo="name",
      )
  )

  ex = [
      x0,
      x0 + dx,
      x0 + dx,
      x0,
      x0,
      None,
      x0,
      x0 + dx,
      x0 + dx,
      x0,
      x0,
      None,
      x0,
      x0,
      None,
      x0 + dx,
      x0 + dx,
      None,
      x0 + dx,
      x0 + dx,
      None,
      x0,
      x0,
  ]
  ey = [
      y0,
      y0,
      y0 + dy,
      y0 + dy,
      y0,
      None,
      y0,
      y0,
      y0 + dy,
      y0 + dy,
      y0,
      None,
      y0,
      y0,
      None,
      y0,
      y0,
      None,
      y0 + dy,
      y0 + dy,
      None,
      y0 + dy,
      y0 + dy,
  ]
  ez = [
      z0,
      z0,
      z0,
      z0,
      z0,
      None,
      z0 + dz,
      z0 + dz,
      z0 + dz,
      z0 + dz,
      z0 + dz,
      None,
      z0,
      z0 + dz,
      None,
      z0,
      z0 + dz,
      None,
      z0,
      z0 + dz,
      None,
      z0,
      z0 + dz,
  ]
  fig.add_trace(
      go.Scatter3d(
          x=ex,
          y=ey,
          z=ez,
          mode="lines",
          line=dict(color=edge_color, width=edge_width),
          showlegend=False,
          hoverinfo="skip",
      )
  )


# --- DÜZLEMDE 2B AÇINIM YÜZÜ ÇİZİM FONKSİYONU ---
def add_flat_face(
    fig, x0, y0, dx, dy, color, opacity=0.45, edge_color="#ad1457", name="Açınım"
):
  vx = [x0, x0 + dx, x0 + dx, x0]
  vy = [y0, y0, y0 + dy, y0 + dy]
  vz = [0, 0, 0, 0]
  fig.add_trace(
      go.Mesh3d(
          x=vx,
          y=vy,
          z=vz,
          i=[0, 0],
          j=[1, 2],
          k=[2, 3],
          color=color,
          opacity=opacity,
          flatshading=True,
          name=name,
          hoverinfo="name",
      )
  )
  gx, gy, gz = [], [], []
  for ix in range(int(dx) + 1):
    gx.extend([x0 + ix, x0 + ix, None])
    gy.extend([y0, y0 + dy, None])
    gz.extend([0.01, 0.01, None])
  for iy in range(int(dy) + 1):
    gx.extend([x0, x0 + dx, None])
    gy.extend([y0 + iy, y0 + iy, None])
    gz.extend([0.01, 0.01, None])
  fig.add_trace(
      go.Scatter3d(
          x=gx,
          y=gy,
          z=gz,
          mode="lines",
          line=dict(color=edge_color, width=2),
          showlegend=False,
          hoverinfo="skip",
      )
  )


st.title(
    "📐 Dikdörtgenler Prizmasının Hacim Bağıntısı Laboratuvarı (MAT.7.4.4.ç)"
)

with st.expander(
    "📜 Robinson Crusoe'nun 1. Günlük Sayfası ve Ders Senaryosu (Adım 1)",
    expanded=False,
):
  st.markdown(
      "**13 Kasım 1705...** *'Fırtına öncesi erzaklarımı saklamak için üç"
      " farklı boyutta (**2×2×4**, **2×4×4** ve **4×4×4**) şeffaf sandık"
      " yaptım. Ancak bugün sandıkların hepsini ağzına kadar dolduracak kadar"
      " birim küpüm yok; elimde sadece **16-17 tane birim küp** var! Büyük"
      " sandıkların tamamını doldurup tek tek sayamayacağıma göre, bu"
      " sandıkların hacmini elimdeki sınırlı sayıda birim küple nasıl"
      " hesaplayabilirim?'*\n\n**Renkli Durum Kartları:** 🟨 **Sarı Kart:**"
      " Çalışma sürüyor | 🟥 **Kırmızı Kart:** İpucu/Destek gerekiyor | 🟩"
      " **Yeşil Kart:** Görev tamamlandı."
  )

tab1, tab2, tab3 = st.tabs([
    "🧊 1. 3D Şeffaf Sandıklar, Stratejiler ve Açınım (Adım 2 & 3)",
    "📊 2. Gözlem Çizelgesi, Sütun Grafiği ve Yanılgı Kontrolü (Adım 3 & 4)",
    "🧱 3. 2. Günlük Sayfası: 16 Küple Hacmin Korunumu (Adım 4)",
])

# ==============================================================================
# SEKME 1: 3D GEOGEBRA LABORATUVARI
# ==============================================================================
with tab1:
  st.sidebar.header("🎛️ 3D Laboratuvar Kontrolleri")

  kutu_secimi = st.sidebar.selectbox(
      "1. Şeffaf Prizma Modeli Seçimi",
      [
          "1. Model: 2 × 4 × 4 (Dikdörtgenler Prizması - Dik)",
          "2. Model: 4 × 4 × 2 (Dikdörtgenler Prizması - Yan Yatırılmış)",
          "3. Model: 2 × 2 × 4 (Kare Prizma - Kaynaştırma Destekli)",
          "4. Model: 4 × 4 × 4 (Küp Sandık)",
          "5. Model: Özel Boyut (Sürgülü Keşif Aracı)",
      ],
  )

  if "2 × 4 × 4" in kutu_secimi:
    a, b, h, varsayilan_renk = 2, 4, 4, "#e53935"
  elif "4 × 4 × 2" in kutu_secimi:
    a, b, h, varsayilan_renk = 4, 4, 2, "#e53935"
  elif "2 × 2 × 4" in kutu_secimi:
    a, b, h, varsayilan_renk = 2, 2, 4, "#1e88e5"
  elif "4 × 4 × 4" in kutu_secimi:
    a, b, h, varsayilan_renk = 4, 4, 4, "#8e24aa"
  else:
    a = st.sidebar.slider("En (a)", 1, 6, 3)
    b = st.sidebar.slider("Boy (b)", 1, 6, 4)
    h = st.sidebar.slider("Yükseklik (h)", 1, 6, 5)
    varsayilan_renk = "#ffb300"

  strateji = st.sidebar.radio(
      "2. Birim Küp Sayma Stratejisi",
      [
          "Strateji 3: L-İskelet (Taban Ayrıtları + Yükseklik Kulesi)",
          "Strateji 2: Taban Alanını Tam Doldur + Yükseklik Kulesi Çık",
          "Strateji 1 & 4: Katmanlama ve Farklı Yüzü Taban Seçme",
          "Alternatif: Birim Küpleri Tek Tek Diz (Adım Sürgüsü)",
      ],
  )

  yon_secimi = st.sidebar.selectbox(
      "3. Taban Kabul Edilen Yüz (Yön)",
      [
          "Alt Yüz Taban (a × b) -> Yukarı Katmanlanma",
          "Ön Yüz Taban (a × h) -> Arkaya Katmanlanma",
          "Yan Yüz Taban (b × h) -> Sağa Katmanlanma",
      ],
  )

  if "Alt Yüz" in yon_secimi:
    yon_val, ta, yuksek, taban_etiket = (
        1,
        a * b,
        h,
        f"Alt Taban ({a} × {b} = {a*b} br²)",
    )
  elif "Ön Yüz" in yon_secimi:
    yon_val, ta, yuksek, taban_etiket = (
        2,
        a * h,
        b,
        f"Ön Yüz ({a} × {h} = {a*h} br²)",
    )
  else:
    yon_val, ta, yuksek, taban_etiket = (
        3,
        b * h,
        a,
        f"Yan Yüz ({b} × {h} = {b*h} br²)",
    )

  kat = st.sidebar.slider("4. Dolu Katman Sayısı (kat)", 0, yuksek, 0)

  st.sidebar.markdown("---")
  iskelet_renk = st.sidebar.color_picker(
      "Birim Küp / L-İskelet Rengi", varsayilan_renk
  )
  katman_renk = st.sidebar.color_picker("Katman Küpleri Rengi", "#ffb300")
  kutu_renk = st.sidebar.color_picker("Şeffaf Büyük Prizma Rengi", "#ec407a")

  goster_acinim = st.sidebar.checkbox(
      "📦 Yüzey Açınımını (Net) Düzlemde Göster", value=False
  )
  kaynastirma_destegi = st.sidebar.checkbox(
      "🔢 Kaynaştırma Desteği (Numaralı Taban & Kat Şeridi)",
      value=("2 × 2 × 4" in kutu_secimi),
  )

  iskelet_kupler = set()
  if "L-İskelet" in strateji:
    for ix in range(a):
      iskelet_kupler.add((ix, 0, 0))
    for iy in range(b):
      iskelet_kupler.add((0, iy, 0))
    for iz in range(h):
      iskelet_kupler.add((0, 0, iz))
  elif "Taban Alanını Tam Doldur" in strateji:
    for ix in range(a):
      for iy in range(b):
        iskelet_kupler.add((ix, iy, 0))
    for iz in range(h):
      iskelet_kupler.add((0, 0, iz))
  elif "Tek Tek Diz" in strateji:
    sirali = (
        [(ix, 0, 0) for ix in range(a)]
        + [(0, iy, 0) for iy in range(1, b)]
        + [(0, 0, iz) for iz in range(1, h)]
    )
    for iz in range(h):
      for iy in range(b):
        for ix in range(a):
          if (ix, iy, iz) not in sirali:
            sirali.append((ix, iy, iz))
    adim = st.sidebar.slider(
        "Tek Tek Birim Küp Ekle", 0, a * b * h, min(a + b + h - 2, a * b * h)
    )
    iskelet_kupler = set(sirali[:adim])

  katman_kupler = set()
  if kat > 0:
    for k_i in range(kat):
      if yon_val == 1:
        for ix in range(a):
          for iy in range(b):
            katman_kupler.add((ix, iy, k_i))
      elif yon_val == 2:
        for ix in range(a):
          for iz in range(h):
            katman_kupler.add((ix, k_i, iz))
      else:
        for iy in range(b):
          for iz in range(h):
            katman_kupler.add((k_i, iy, iz))

  fig3d = go.Figure()

  for ix, iy, iz in iskelet_kupler:
    add_solid_box(
        fig3d,
        ix,
        iy,
        iz,
        1,
        1,
        1,
        color=iskelet_renk,
        opacity=1.0,
        edge_color="#1a1a1a",
        edge_width=3,
        name=f"Küp ({ix+1},{iy+1},{iz+1})",
    )

  for ix, iy, iz in katman_kupler - iskelet_kupler:
    add_solid_box(
        fig3d,
        ix,
        iy,
        iz,
        1,
        1,
        1,
        color=katman_renk,
        opacity=0.95,
        edge_color="#333333",
        edge_width=2,
        name=f"Katman ({ix+1},{iy+1},{iz+1})",
    )

  add_solid_box(
      fig3d,
      0,
      0,
      0,
      a,
      b,
      h,
      color=kutu_renk,
      opacity=0.18,
      edge_color="#880e4f",
      edge_width=5,
      name=f"Şeffaf Prizma ({a}×{b}×{h})",
  )

  if kaynastirma_destegi:
    nx, ny, nz, ntxt = [], [], [], []
    s = 1
    for iy in range(b):
      for ix in range(a):
        nx.append(ix + 0.5)
        ny.append(iy + 0.5)
        nz.append(0.05)
        ntxt.append(f"{s}. Kare")
        s += 1
    fig3d.add_trace(
        go.Scatter3d(
            x=nx,
            y=ny,
            z=nz,
            mode="text",
            text=ntxt,
            textfont=dict(size=13, color="#0d47a1"),
            name="Numaralı Taban",
        )
    )
    k_renk = ["#e53935", "#fb8c00", "#43a047", "#1e88e5", "#8e24aa", "#00acc1"]
    for iz in range(h):
      fig3d.add_trace(
          go.Scatter3d(
              x=[a + 0.15],
              y=[0],
              z=[iz + 0.5],
              mode="markers+text",
              marker=dict(size=7, color=k_renk[iz % 6]),
              text=[f" {iz+1}. Kat"],
              textposition="middle right",
              textfont=dict(size=12, color=k_renk[iz % 6]),
              showlegend=False,
          )
      )

  if goster_acinim:
    add_flat_face(
        fig3d, 0, 0, a, b, "#ff80ab", opacity=0.5, name="Alt Taban (TA)"
    )
    add_flat_face(
        fig3d, 0, -h, a, h, "#f48fb1", opacity=0.35, name="Ön Yüz Açınımı"
    )
    add_flat_face(
        fig3d, 0, b, a, h, "#f48fb1", opacity=0.35, name="Arka Yüz Açınımı"
    )
    add_flat_face(
        fig3d, -h, 0, h, b, "#ce93d8", opacity=0.35, name="Sol Yüz Açınımı"
    )
    add_flat_face(
        fig3d, a, 0, h, b, "#ce93d8", opacity=0.35, name="Sağ Yüz Açınımı"
    )
    add_flat_face(
        fig3d, a + h, 0, a, b, "#ff80ab", opacity=0.35, name="Üst Taban Açınımı"
    )

  max_b = max(a, b, h) + (h + 2 if goster_acinim else 1)
  min_b = -(h + 1) if goster_acinim else -0.5

  fig3d.update_layout(
      scene=dict(
          xaxis=dict(title=f"En (a={a})", range=[min_b, max_b], dtick=1),
          yaxis=dict(title=f"Boy (b={b})", range=[min_b, max_b], dtick=1),
          zaxis=dict(
              title=f"Yükseklik (h={h})", range=[0, max(a, b, h) + 1], dtick=1
          ),
          aspectmode="data",
          camera=dict(eye=dict(x=1.6, y=-1.6, z=1.3)),
      ),
      margin=dict(l=0, r=0, b=0, t=10),
      height=580,
      showlegend=False,
  )

  col_3d, col_info = st.columns([2, 1])
  with col_3d:
    st.subheader(f"🧊 {kutu_secimi}")
    st.plotly_chart(fig3d, use_container_width=True)

  with col_info:
    toplam_kup = len(iskelet_kupler.union(katman_kupler))
    st.subheader("📐 Matematiksel Keşif Paneli")
    st.info(
        f"**• Prizma Ayrıtları:** a = {a} br, b = {b} br, h = {h} br\n\n"
        f"**• Seçilen Taban:** {taban_etiket}\n\n"
        f"**• 1. Katmandaki Küp Sayısı (TA):** **{ta} br²**\n\n"
        f"**• Kat Sayısı (Yükseklik - h):** **{yuksek} br**\n\n"
        f"**• Kutuda Gösterilen Küp:** {toplam_kup} adet\n\n"
        f"### Hacim (V) = TA × h = {ta} × {yuksek} = **{a*b*h} br³**"
    )

    st.markdown("##### 🟩 Seçilen Taban Yüzeyinin 2B Görünümü (TA)")
    bx = a if yon_val in [1, 2] else b
    by = b if yon_val == 1 else h
    fig2d = go.Figure()
    for ix in range(bx):
      for iy in range(by):
        fig2d.add_shape(
            type="rect",
            x0=ix,
            y0=iy,
            x1=ix + 1,
            y1=iy + 1,
            line=dict(color="#880e4f", width=2),
            fillcolor="#f8bbd0",
        )
        fig2d.add_annotation(
            x=ix + 0.5,
            y=iy + 0.5,
            text=str(iy * bx + ix + 1),
            showarrow=False,
            font=dict(size=12, color="#880e4f"),
        )
    fig2d.update_layout(
        xaxis=dict(range=[-0.2, bx + 0.2], dtick=1, title=f"{bx} birim"),
        yaxis=dict(
            range=[-0.2, by + 0.2],
            dtick=1,
            title=f"{by} birim",
            scaleanchor="x",
            scaleratio=1,
        ),
        margin=dict(l=20, r=20, t=10, b=20),
        height=220,
    )
    st.plotly_chart(fig2d, use_container_width=True)

# ==============================================================================
# SEKME 2: GÖZLEM ÇİZELGESİ, SÜTUN GRAFİĞİ VE YANILGI KONTROLÜ
# ==============================================================================
with tab2:
  st.subheader("📋 Grupların Gözlem Çizelgesi Verileri (Adım 3)")
  st.table({
      "Şeffaf Kutu Modeli": [
          "1. Kutu: Dikdörtgenler Prizması (Dik)",
          "2. Kutu: Dikdörtgenler Prizması (Yan Yatırılmış)",
          "3. Kutu: Kare Prizma (2×2×4)",
          "4. Kutu: Küp (4×4×4)",
      ],
      "Taban Ayrıtları (a ve b)": [
          "2 br ve 4 br",
          "4 br ve 4 br",
          "2 br ve 2 br",
          "4 br ve 4 br",
      ],
      "1. Katmandaki Küp Sayısı (TA)": [
          "2 × 4 = 8 br²",
          "4 × 4 = 16 br²",
          "2 × 2 = 4 br²",
          "4 × 4 = 16 br²",
      ],
      "Kat Sayısı (Yükseklik - h)": ["4 br", "2 br", "4 br", "4 br"],
      "Toplam Birim Küp Sayısı (Hacim V = TA × h)": [
          "8 × 4 = 32 br³",
          "16 × 2 = 32 br³",
          "4 × 4 = 16 br³",
          "16 × 4 = 64 br³",
      ],
  })

  col_g1, col_g2 = st.columns([3, 2])
  with col_g1:
    st.subheader(
        "📊 Yükseklik Sabitken (h=4) Taban Alanı - Hacim İlişkisi Grafiği"
    )
    modeller = [
        "Kare Prizma (2×2×4)",
        "Dikdörtgenler P. (2×4×4)",
        "Küp (4×4×4)",
    ]
    fig_bar = go.Figure(
        data=[
            go.Bar(
                name="Taban Alanı (TA - br²)",
                x=modeller,
                y=[4, 8, 16],
                marker_color="#1e88e5",
                text=[4, 8, 16],
                textposition="auto",
            ),
            go.Bar(
                name="Yükseklik (h - br)",
                x=modeller,
                y=[4, 4, 4],
                marker_color="#fb8c00",
                text=[4, 4, 4],
                textposition="auto",
            ),
            go.Bar(
                name="Hacim (V = TA × h - br³)",
                x=modeller,
                y=[16, 32, 64],
                marker_color="#d81b60",
                text=[16, 32, 64],
                textposition="auto",
            ),
        ]
    )
    fig_bar.update_layout(barmode="group", height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

  with col_g2:
    st.subheader("⚠️ Kavram Yanılgısı Kontrolü")
    st.warning(
        "**Soru (Adım 3):** Bir kişi **2 × 4 × 4** prizmasının hacmini bulurken"
        " ayrıtları çarpmak yerine toplasaydı (**2 + 4 + 4 = 10**) veya sadece"
        " L-iskelette gördüğü küpleri saysaydı neden hata yapmış olurdu?"
    )
    st.success(
        "**Cevap:** Toplama yaparsa sadece kenardaki tek sıra birim küpleri"
        " toplamış olur; taban alanının içini (**2 × 4 = 8 br²**) ve üst üste"
        " binen **4 katmanı** hesaba katmamış olur (**8 × 4 = 32 br³**).\n\n•"
        " **Kare Prizma:** V = a² × h\n• **Küp:** V = a³"
    )

# ==============================================================================
# SEKME 3: 2. GÜNLÜK SAYFASI - 16 KÜPLE HACMİN KORUNUMU
# ==============================================================================
with tab3:
  st.markdown(
      "**📜 Robinson Crusoe'nun 2. Günlük Sayfası (14 Kasım 1705):** *'2×2×4"
      " boyutundaki kare prizma sandığın içini tamamen dolduran **16 tane birim"
      " küp** erzak kutusunu dışarı çıkardım. Önce tek katlı **4×4×1** kare"
      " prizma dizdim. Sonra yardımcım bu 16 küpü bozup **basamaklı bir"
      " merdiven** yaptı! Ona kutularımızın hacmi azaldı dedim, o ise itiraz"
      " etti. Hangimiz haklıyız?'*"
  )

  yapi_secimi = st.radio(
      "16 Adet Birim Küple Oluşturulan Yapıyı Seçin:",
      [
          "1. 2 × 2 × 4 Kare Prizma (TA = 4 br², h = 4 br -> V = 16 br³)",
          (
              "2. 2 × 4 × 2 Dikdörtgenler Prizması (TA = 8 br², h = 2 br -> V ="
              " 16 br³)"
          ),
          (
              "3. 4 × 4 × 1 Tek Katlı Kare Prizma (TA = 16 br², h = 1 br -> V ="
              " 16 br³)"
          ),
          (
              "4. Basamaklı Merdiven - Prizma Olmayan Yapı (16 Birim Küp -> V ="
              " 16 br³)"
          ),
          (
              "5. L-Duvar / Kule - Prizma Olmayan Yapı (16 Birim Küp -> V = 16"
              " br³)"
          ),
      ],
  )

  korunum_kupler = []
  if "2 × 2 × 4" in yapi_secimi:
    korunum_kupler = [
        (ix, iy, iz) for ix in range(2) for iy in range(2) for iz in range(4)
    ]
  elif "2 × 4 × 2" in yapi_secimi:
    korunum_kupler = [
        (ix, iy, iz) for ix in range(2) for iy in range(4) for iz in range(2)
    ]
  elif "4 × 4 × 1" in yapi_secimi:
    korunum_kupler = [(ix, iy, 0) for ix in range(4) for iy in range(4)]
  elif "Basamaklı Merdiven" in yapi_secimi:
    for ix, hb in enumerate([4, 3, 2, 1]):
      for iz in range(hb):
        korunum_kupler.append((ix, 0, iz))
    for ix, hb in enumerate([3, 2, 1]):
      for iz in range(hb):
        korunum_kupler.append((ix, 1, iz))
  else:
    korunum_kupler = [(ix, 0, iz) for ix in range(4) for iz in range(3)] + [
        (0, iy, 0) for iy in range(1, 5)
    ]

  fig_k = go.Figure()
  for idx, (ix, iy, iz) in enumerate(korunum_kupler):
    add_solid_box(
        fig_k,
        ix,
        iy,
        iz,
        1,
        1,
        1,
        color="#26a69a",
        opacity=1.0,
        edge_color="#004d40",
        edge_width=3,
        name=f"Küp {idx+1}",
    )

  fig_k.update_layout(
      scene=dict(
          xaxis=dict(title="En", range=[-0.5, 5], dtick=1),
          yaxis=dict(title="Boy", range=[-0.5, 5], dtick=1),
          zaxis=dict(title="Yükseklik", range=[0, 5], dtick=1),
          aspectmode="data",
      ),
      height=420,
      margin=dict(l=0, r=0, t=10, b=0),
      showlegend=False,
  )

  ck1, ck2 = st.columns([2, 1])
  with ck1:
    st.plotly_chart(fig_k, use_container_width=True)
  with ck2:
    st.info(
        f"**Toplam Birim Küp Sayısı:** **{len(korunum_kupler)} adet**\n\n"
        f"**Kapladığı Yer (Hacim):** **{len(korunum_kupler)} br³**\n\n"
        "**Sonuç (Yardımcısı Haklıdır!):** Şekil değişse veya prizma bozulup"
        " merdiven/kule yapılsa bile 16 birim küpten hiçbiri eksilmediği için"
        " **hacim korunur (16 br³)**."
    )
# --- KODUN SONU ---
