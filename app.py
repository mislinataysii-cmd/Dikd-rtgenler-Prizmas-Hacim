import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="MAT.7.4.4.ç - 3D Prizma ve Hacim Laboratuvarı",
    layout="wide",
)


# --- YARDIMCI FONKSİYON: TÜM 6 YÜZÜ TAM BOYALI 3B KÜP / PRİZMA ÇİZİMİ ---
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
    edge_color="#222222",
    edge_width=3,
    name="",
):
  # 8 Köşe Noktası
  vx = [x0, x0 + dx, x0 + dx, x0, x0, x0 + dx, x0 + dx, x0]
  vy = [y0, y0, y0 + dy, y0 + dy, y0, y0, y0 + dy, y0 + dy]
  vz = [z0, z0, z0, z0, z0 + dz, z0 + dz, z0 + dz, z0 + dz]

  # 6 Yüzeyi Eksiksiz Kapatan 12 Üçgen İndeksi
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
          lighting=dict(ambient=0.75, diffuse=0.6, specular=0.2),
          name=name,
          showscale=False,
          hoverinfo="name",
      )
  )

  # 12 Ayrıt Çerçevesi (GeoGebra ve Somut Materyal Görünümü İçin)
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


# --- YARDIMCI FONKSİYON: DÜZLEMDE 2B DİKDÖRTGEN (AÇINIM YÜZLERİ İÇİN) ---
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
  # Birim kare ızgaraları
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


# --- BAŞLIK VE DERS PLANI SENARYOSU ---
st.title(
    "📐 Dikdörtgenler Prizmasının Hacim Bağıntısı Laboratuvarı (MAT.7.4.4.ç)"
)

with st.expander(
    "📜 Robinson Crusoe'nun 1. Günlük Sayfası ve Ders Senaryosu (Adım 1 -"
    " Dikkat Çekme)",
    expanded=False,
):
  st.markdown("""
    > **13 Kasım 1705...** *"Fırtına öncesi erzaklarımı saklamak için üç farklı boyutta (**2×2×4**, **2×4×4** ve **4×4×4**) şeffaf sandık yaptım. Önceki günlerden sandıkların içine birim küpleri tamamen doldurup sayarak hacimlerini bulmayı biliyorum. Ancak bugün sandıkların hepsini ağzına kadar dolduracak kadar birim küpüm yok; elimde sadece **16-17 tane birim küp** var! Büyük sandıkların tamamını doldurup tek tek sayamayacağıma göre, bu sandıkların hacmini elimdeki sınırlı sayıda birim küple nasıl hesaplayabilirim?"*

    **Sınıf Yönetimi (Renkli Durum Kartları):** 🟨 **Sarı Kart:** Çalışma sürüyor | 🟥 **Kırmızı Kart:** İpucu/Destek gerekiyor | 🟩 **Yeşil Kart:** Görev tamamlandı, iç sayfadaki ek göreve geçildi.
    """)

# --- ÜST SEKMELER (DERSİN 4 AŞAMASI) ---
tab1, tab2, tab3 = st.tabs([
    "🧊 1. 3D Şeffaf Sandıklar, Stratejiler ve Açınım (Adım 2 & 3)",
    "📊 2. Gözlem Çizelgesi, Sütun Grafiği ve Yanılgı Kontrolü (Adım 3 & 4)",
    "🧱 3. 2. Günlük Sayfası: 16 Küple Hacmin Korunumu (Adım 4)",
])

# ==============================================================================
# SEKME 1: ANA 3D GEOGEBRA LABORATUVARI
# ==============================================================================
with tab1:
  st.sidebar.header("🎛️ 3D Laboratuvar Kontrolleri")

  # 1. Kutu Seçimi (İlk sırada Dikdörtgenler Prizması)
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
    a, b, h = 2, 4, 4
    varsayilan_renk = "#e53935"  # Fotoğraftaki kırmızı küpler
  elif "4 × 4 × 2" in kutu_secimi:
    a, b, h = 4, 4, 2
    varsayilan_renk = "#e53935"
  elif "2 × 2 × 4" in kutu_secimi:
    a, b, h = 2, 2, 4
    varsayilan_renk = "#1e88e5"  # Fotoğraftaki mavi küpler
  elif "4 × 4 × 4" in kutu_secimi:
    a, b, h = 4, 4, 4
    varsayilan_renk = "#8e24aa"  # Fotoğraftaki mor küpler
  else:
    a = st.sidebar.slider("En (a)", 1, 6, 3)
    b = st.sidebar.slider("Boy (b)", 1, 6, 4)
    h = st.sidebar.slider("Yükseklik (h)", 1, 6, 5)
    varsayilan_renk = "#ffb300"

  # 2. Sayma Stratejisi Seçimi (Ders Planı Adım 2 ve Adım 3)
  strateji = st.sidebar.radio(
      "2. Birim Küp Sayma Stratejisi",
      [
          "Strateji 3: L-İskelet (Taban Ayrıtları + Yükseklik Kulesi)",
          "Strateji 2: Taban Alanını Tam Doldur + Yükseklik Kulesi Çık",
          "Strateji 1 & 4: Katmanlama ve Farklı Yüzü Taban Seçme",
          "Alternatif: Birim Küpleri Tek Tek Diz (Adım Sürgüsü)",
      ],
  )

  # 3. Taban Seçimi ve Katman Sürgüsü
  yon_secimi = st.sidebar.selectbox(
      "3. Taban Kabul Edilen Yüz (Yön)",
      [
          "Alt Yüz Taban (a × b) -> Yukarı Katmanlanma",
          "Ön Yüz Taban (a × h) -> Arkaya Katmanlanma",
          "Yan Yüz Taban (b × h) -> Sağa Katmanlanma",
      ],
  )

  if "Alt Yüz" in yon_secimi:
    yon_val, ta, yuksek = 1, a * b, h
    taban_etiket = f"Alt Taban ({a} × {b} = {a*b} br²)"
  elif "Ön Yüz" in yon_secimi:
    yon_val, ta, yuksek = 2, a * h, b
    taban_etiket = f"Ön Yüz ({a} × {h} = {a*h} br²)"
  else:
    yon_val, ta, yuksek = 3, b * h, a
    taban_etiket = f"Yan Yüz ({b} × {h} = {b*h} br²)"

  kat = st.sidebar.slider("4. Dolu Katman Sayısı (kat)", 0, yuksek, 0)

  # 4. Renk Seçimi (Kullanıcı Özelleştirmesi)
  st.sidebar.markdown("---")
  st.sidebar.subheader("🎨 Renk ve Görünüm Özelleştirme")
  iskelet_renk = st.sidebar.color_picker(
      "Birim Küp / L-İskelet Rengi", varsayilan_renk
  )
  katman_renk = st.sidebar.color_picker("Katman Küpleri Rengi", "#ffb300")
  kutu_renk = st.sidebar.color_picker(
      "Şeffaf Büyük Prizma Rengi", "#ec407a"
  )  # GeoGebra Pembesi

  # 5. Ek Pedagojik Araçlar (Açınım ve Kaynaştırma Desteği)
  goster_acinim = st.sidebar.checkbox(
      "📦 Yüzey Açınımını (Net) Düzlemde Göster", value=False
  )
  kaynastirma_destegi = st.sidebar.checkbox(
      "🔢 Kaynaştırma Desteği (Numaralı Taban & Kat Şeridi)",
      value=("2 × 2 × 4" in kutu_secimi),
  )

  # --- KOORDİNAT HESAPLAMA (SEÇİLEN STRATEJİYE GÖRE KÜPLER) ---
  iskelet_kupler = set()
  if "L-İskelet" in strateji:
    # Fotoğraflardaki gibi: Köşe (0,0,0) merkezli X ayrıtı, Y ayrıtı ve Z kulesi
    for ix in range(a):
      iskelet_kupler.add((ix, 0, 0))
    for iy in range(b):
      iskelet_kupler.add((0, iy, 0))
    for iz in range(h):
      iskelet_kupler.add((0, 0, iz))
  elif "Taban Alanını Tam Doldur" in strateji:
    # Alt tabanın tamamı + köşeden yukarı kule (3. Grup stratejisi)
    for ix in range(a):
      for iy in range(b):
        iskelet_kupler.add((ix, iy, 0))
    for iz in range(h):
      iskelet_kupler.add((0, 0, iz))
  elif "Tek Tek Diz" in strateji:
    # Önce L-iskelet küpleri, sonra kalan küpler sırayla
    sirali_liste = []
    for ix in range(a):
      sirali_liste.append((ix, 0, 0))
    for iy in range(1, b):
      sirali_liste.append((0, iy, 0))
    for iz in range(1, h):
      sirali_liste.append((0, 0, iz))
    for iz in range(h):
      for iy in range(b):
        for ix in range(a):
          if (ix, iy, iz) not in sirali_liste:
            sirali_liste.append((ix, iy, iz))
    adim_sayisi = st.sidebar.slider(
        "Tek Tek Birim Küp Ekle",
        0,
        a * b * h,
        min(a + b + h - 2, a * b * h),
    )
    iskelet_kupler = set(sirali_liste[:adim_sayisi])

  # Katman Küpleri
  katman_kupler = set()
  if kat > 0:
    for k_i in range(kat):
      if yon_val == 1:  # Alt tabandan yukarı
        for ix in range(a):
          for iy in range(b):
            katman_kupler.add((ix, iy, k_i))
      elif yon_val == 2:  # Ön yüzden arkaya
        for ix in range(a):
          for iz in range(h):
            katman_kupler.add((ix, k_i, iz))
      else:  # Yan yüzden sağa
        for iy in range(b):
          for iz in range(h):
            katman_kupler.add((k_i, iy, iz))

  # --- 3D PLOTLY SAHNESİ OLUŞTURMA ---
  fig3d = go.Figure()

  # 1) İçteki Birim Küpleri Çiz (Tüm 6 yüzü boyalı ve siyah/koyu çerçeveli)
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
        name=f"Birim Küp ({ix+1},{iy+1},{iz+1})",
    )

  # Katman küplerini (iskeletle çakışmayanları veya katman rengiyle) çiz
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
        name=f"Katman Küpü ({ix+1},{iy+1},{iz+1})",
    )

  # 2) Dıştaki Şeffaf Pembe Büyük Prizmayı Çiz (GeoGebra Görünümü)
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

  # 3) Kaynaştırma Öğrencisi Desteği: Numaralı Taban Kareleri ve Kat Şeritleri
  if kaynastirma_destegi:
    num_x, num_y, num_z, num_text = [], [], [], []
    sayac = 1
    for iy in range(b):
      for ix in range(a):
        num_x.append(ix + 0.5)
        num_y.append(iy + 0.5)
        num_z.append(0.05)
        num_text.append(f"{sayac}. Kare")
        sayac += 1
    fig3d.add_trace(
        go.Scatter3d(
            x=num_x,
            y=num_y,
            z=num_z,
            mode="text",
            text=num_text,
            textfont=dict(size=13, color="#0d47a1", family="Arial Black"),
            name="Numaralı Taban",
        )
    )
    # Dikey ayrıtta kat seviyesi etiketleri
    kat_renkleri = ["#e53935", "#fb8c00", "#43a047", "#1e88e5", "#8e24aa", "#00acc1"]
    for iz in range(h):
      fig3d.add_trace(
          go.Scatter3d(
              x=[a + 0.15],
              y=[0],
              z=[iz + 0.5],
              mode="markers+text",
              marker=dict(size=7, color=kat_renkleri[iz % len(kat_renkleri)]),
              text=[f" {iz+1}. Kat"],
              textposition="middle right",
              textfont=dict(
                  size=12, color=kat_renkleri[iz % len(kat_renkleri)]
              ),
              showlegend=False,
          )
      )

  # 4) Yüzey Açınımı (Net) Gösterimi (Düzlemde Açılmış Kapaklar)
  if goster_acinim:
    # Alt taban (0,0) - (a,b)
    add_flat_face(fig3d, 0, 0, a, b, "#ff80ab", opacity=0.5, name="Alt Taban (TA)")
    # Ön ve Arka kapaklar
    add_flat_face(fig3d, 0, -h, a, h, "#f48fb1", opacity=0.35, name="Ön Yüz Açınımı")
    add_flat_face(fig3d, 0, b, a, h, "#f48fb1", opacity=0.35, name="Arka Yüz Açınımı")
    # Sol ve Sağ kapaklar
    add_flat_face(fig3d, -h, 0, h, b, "#ce93d8", opacity=0.35, name="Sol Yüz Açınımı")
    add_flat_face(fig3d, a, 0, h, b, "#ce93d8", opacity=0.35, name="Sağ Yüz Açınımı")
    # Üst kapak
    add_flat_face(
        fig3d, a + h, 0, a, b, "#ff80ab", opacity=0.35, name="Üst Taban Açınımı"
    )

  max_boyut = max(a, b, h) + (h + 2 if goster_acinim else 1)
  min_boyut = -(h + 1) if goster_acinim else -0.5

  fig3d.update_layout(
      scene=dict(
          xaxis=dict(
              title=f"En (a = {a} br)",
              range=[min_boyut, max_boyut],
              dtick=1,
              backgroundcolor="#f8f9fa",
          ),
          yaxis=dict(
              title=f"Boy (b = {b} br)",
              range=[min_boyut, max_boyut],
              dtick=1,
              backgroundcolor="#f8f9fa",
          ),
          zaxis=dict(
              title=f"Yükseklik (h = {h} br)",
              range=[0, max(a, b, h) + 1],
              dtick=1,
              backgroundcolor="#eef2f6",
          ),
          aspectmode="data",
          camera=dict(eye=dict(x=1.6, y=-1.6, z=1.3)),
      ),
      margin=dict(l=0, r=0, b=0, t=10),
      height=600,
      showlegend=False,
  )

  # --- EKRAN YERLEŞİMİ: SOLDA 3D LABORATUVAR, SAĞDA FORMÜL & 2B TABAN ---
  col_3d, col_info = st.columns([2, 1])

  with col_3d:
    st.subheader(f"🧊 {kutu_secimi}")
    st.plotly_chart(fig3d, use_container_width=True)

  with col_info:
    toplam_yerlesen = len(iskelet_kupler.union(katman_kupler))
    st.subheader("📐 Matematiksel Keşif Paneli")
    st.markdown(f"""
        <div style="background-color:#fce4ec; border-left:6px solid #c2185b; padding:14px; border-radius:8px; font-size:15px;">
        <b>• Prizma Ayrıtları:</b> a = {a} br, b = {b} br, h = {h} br<br>
        <b>• Seçilen Taban:</b> {taban_etiket}<br>
        <b>• 1. Katmandaki Küp Sayısı (TA):</b> <b>{ta} br²</b><br>
        <b>• Kat Sayısı (Yükseklik - h):</b> <b>{yuksek} br</b><br>
        <b>• Şu An Kutuda Gösterilen Küp:</b> {toplam_yerlesen} adet (Sınırlı Küp!)<br>
        <hr style="margin:8px 0;">
        <span style="font-size:18px; color:#880e4f;"><b>Hacim (V) = TA × h = {ta} × {yuksek} = {a*b*h} br³</b></span>
        </div>
        """, unsafe_allow_html=True)

    # 2B Taban Alanı Izgarası (GeoGebra Ekran Görüntüsündeki Sol Alt Kutu)
    st.markdown("##### 🟩 Seçilen Taban Yüzeyinin 2B Görünümü ($TA$)")
    boyut_x = a if yon_val in [1, 2] else b
    boyut_y = b if yon_val == 1 else h
    fig2d = go.Figure()
    for ix in range(boyut_x):
      for iy in range(boyut_y):
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
            text=f"{iy*boyut_x + ix + 1}",
            showarrow=False,
            font=dict(size=12, color="#880e4f"),
        )
    fig2d.update_layout(
        xaxis=dict(
            range=[-0.2, boyut_x + 0.2],
            dtick=1,
            title=f"{boyut_x} birim",
            constrain="domain",
        ),
        yaxis=dict(
            range=[-0.2, boyut_y + 0.2],
            dtick=1,
            title
