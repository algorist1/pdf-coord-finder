
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.title("📍 PDF 좌표 추출 도구")
st.markdown("""
이 도구로 마스킹할 영역의 정확한 좌표를 찾으세요!

**사용 방법:**
1. PDF 파일 업로드
2. 1페이지 이미지에서 마우스로 클릭하여 좌표 확인
3. 좌표를 복사하여 코드에 입력
""")

uploaded_file = st.file_uploader("PDF 파일 업로드", type=['pdf'])

if uploaded_file:
    # PDF 열기
    pdf_bytes = uploaded_file.read()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = pdf_doc[0]  # 1페이지
    
    # 페이지 크기 정보
    rect = page.rect
    st.info(f"📏 페이지 크기: 가로 {rect.width:.1f}pt x 세로 {rect.height:.1f}pt")
    
    # 페이지를 이미지로 변환
    mat = fitz.Matrix(2.0, 2.0)  # 2배 확대
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # 이미지 표시
    st.markdown("### 1페이지 미리보기")
    st.markdown("**아래 이미지에서 마스킹할 영역을 확인하세요**")
    
    # 이미지 표시
    st.image(img, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🔍 좌표 입력 도우미")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 왼쪽 위 모서리")
        x0 = st.number_input("X 좌표 (왼쪽)", min_value=0.0, max_value=rect.width, value=0.0, step=1.0)
        y0 = st.number_input("Y 좌표 (위쪽)", min_value=0.0, max_value=rect.height, value=0.0, step=1.0)
    
    with col2:
        st.markdown("#### 오른쪽 아래 모서리")
        x1 = st.number_input("X 좌표 (오른쪽)", min_value=0.0, max_value=rect.width, value=100.0, step=1.0)
        y1 = st.number_input("Y 좌표 (아래)", min_value=0.0, max_value=rect.height, value=100.0, step=1.0)
    
    # 좌표 출력
    st.markdown("### 📋 복사할 좌표")
    coord_text = f"[{x0}, {y0}, {x1}, {y1}]"
    st.code(coord_text, language="python")
    
    st.markdown("---")
    st.markdown("### 💡 좌표 찾는 팁")
    st.markdown("""
    **PDF 좌표계:**
    - 왼쪽 **위**가 (0, 0)
    - 오른쪽으로 갈수록 X 증가
    - 아래로 갈수록 Y 증가
    - A4 용지: 약 595 x 842 포인트
    
    **측정 방법:**
    1. 이미지를 보며 대략적인 위치 파악
    2. 숫자를 조정하며 영역 확인
    3. 여러 개의 영역을 모두 기록
    """)
    
    # 미리보기 그리기
    if st.button("🎨 선택 영역 미리보기"):
        # 새 페이지 복사
        test_doc = fitz.open()
        test_page = test_doc.new_page(width=rect.width, height=rect.height)
        test_page.show_pdf_page(test_page.rect, pdf_doc, 0)
        
        # 빨간 사각형 그리기
        rect_to_draw = fitz.Rect(x0, y0, x1, y1)
        test_page.draw_rect(rect_to_draw, color=(1, 0, 0), width=2)
        
        # 이미지로 변환
        test_pix = test_page.get_pixmap(matrix=mat)
        test_img = Image.frombytes("RGB", [test_pix.width, test_pix.height], test_pix.samples)
        
        st.image(test_img, caption="빨간 박스: 선택된 영역", use_container_width=True)
        
        test_doc.close()
    
    pdf_doc.close()

st.markdown("---")
st.markdown("### 📝 모든 영역 기록하기")
st.markdown("""
아래 형식으로 모든 마스킹 영역을 기록해주세요:

```python
PAGE_1_BBOXES = [
    [x0, y0, x1, y1],  # 사진
    [x0, y0, x1, y1],  # 반/번호/담임성명
    [x0, y0, x1, y1],  # 성명/주민번호
    # ... 나머지 영역들
]
```
""")
