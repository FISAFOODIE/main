# 점메츄: 우리만의 메뉴 리뷰 플랫폼

##  <a href="https://fisafoodie.streamlit.app/" style="text-decoration: none; color: #0066cc; font-weight: bold;"> Site

  <div style="text-align: center;">
    <img width="300" alt="image" src="https://github.com/user-attachments/assets/048302a4-997f-47ce-9ab3-7730c60d1b9b" />
    <p style="font-size: 18px; font-family: Arial, sans-serif; color: #333; margin-top: 10px;">
        Yes, get this app back up! 을 눌러주세요! 
    </p>
</div>



## ⚒️ Tools
- **프로그래밍 언어 및 라이브러리**
  
 ![Python](https://img.shields.io/badge/python-3776AB.svg?&style=for-the-badge&logo=python&logoColor=white)
 ![Pandas](https://img.shields.io/badge/pandas-150458.svg?&style=for-the-badge&logo=pandas&logoColor=white)
 ![NumPy](https://img.shields.io/badge/numpy-013243.svg?&style=for-the-badge&logo=numpy&logoColor=white)
 ![ Plotly](https://img.shields.io/badge/plotly-3F4F75.svg?&style=for-the-badge&logo=plotly&logoColor=white) 
 ![Streamlit](https://img.shields.io/badge/streamlit-FF4B4B.svg?&style=for-the-badge&logo=streamlit&logoColor=white)

- **데이터베이스 및 서버**

 ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?&style=for-the-badge&logo=mysql&logoColor=white)

- **지도 및 위치 기반 서비스:**

 ![OpenStreetMap](https://img.shields.io/badge/openstreetmap-7EBC6F.svg?&style=for-the-badge&logo=openstreetmap&logoColor=white)
 ![Folium](https://img.shields.io/badge/folium-77B829.svg?&style=for-the-badge&logo=folium&logoColor=white) 
- **버전 관리 및 협업 도구**
  
 ![GitHub](https://img.shields.io/badge/github-181717.svg?&style=for-the-badge&logo=github&logoColor=white) 
 ![Slack](https://img.shields.io/badge/slack-4A154B.svg?&style=for-the-badge&logo=slack&logoColor=white)


 




## 📌 주제 선정 이유
- 네이버나 카카오 같은 대형 플랫폼의 리뷰는 신뢰도가 부족하다고 느낀적이 종종 있었습니다.  
  (이벤트 참여를 위한 영수증 리뷰, 가게에서 생성한 리뷰 등으로 인한 평점 조작을 의심하며)
- 기존의 데이터만 활용하는 것은 진부하다고 생각해 **우리만의 데이터를 생성**하여 활용하고자 했습니다.

---

## 🌟 예상 기대효과
1. **신뢰도 향상:**  
   개인이 속한 공동체만의 음식점 리뷰를 통해 더 신뢰할 수 있는 정보를 제공합니다.
2. **공동체 유대감 증진:**  
   음식 취향이 비슷한 사람들과의 식사와 소소한 음식 이야기를 통해 유대감을 형성합니다.

---

## 🛠 주요 기능

### 1. **점심 메뉴 등록**
- 사용자가 방문한 식당에 대해 다음 정보를 입력합니다:
  - 식당 이름  
  - 메뉴  
  - 가격대  
  - 맛 점수  
  - 식당 접근성 점수
  - 사진

---

### 2. **우리 파헤쳐 보기**
#### (1) 전체 데이터 요약
- 전체 리뷰 수와 방문 누적 가게 수를 계산하여 요약 정보를 제공합니다.
- **전체 평균 데이터 표시:**
  - 맛 점수 평균  
  - 음식 단가 평균  

#### (2) 맛집 순위 시각화
- **Top 10 맛집 랭킹:**  
  맛 점수를 기준으로 상위 10개 맛집을 막대그래프로 시각화.
- **1주일간의 Top 3 맛집:**  
  - 사용자가 선택한 날짜를 기준으로, 해당 주의 상위 3개 맛집을 막대그래프로 표시.

#### (3) 선택한 가게 분석
- **평균 비교:**  
  선택한 가게의 평균 맛 점수와 가격대를 전체 평균과 비교하여 표시.
- **방문 분석:**  
  해당 가게를 가장 많이 방문한 트랙 정보를 제공.
- **추세 시각화:**  
  - 선택한 가게의 일자별 **누적 평균 맛 점수 변화**를 선 그래프로 시각화.
  - **메뉴별 맛 점수:** 메뉴별 평균 맛 점수와 가격 정보를 막대그래프로 시각화.

---

### 3. 방문 식당 위치 보기

**기능 개요**  
- OpenStreetMap의 Nominatim API를 활용하여 식당들의 위도와 경도를 조회하고, Folium을 사용해 지도를 생성하여 시각적으로 표시

**구체적인 흐름**

1. **DB에서 식당 이름 가져오기**  

2. **OpenStreetMap의 Nominatim API를 사용하여 위치 정보 조회**  

3. **위치 정보 저장 통한 반복적인 API 요청 줄이기**  

4. **Folium사용하여 지도로 표시**  


---

### 4. 우리 갤러리

**기능 개요**  
데이터베이스의 각 리뷰 정보와 함께 업로드된 음식 사진을 표시

**구체적인 흐름**

1. **리뷰 정보 조회**

2. **페이지네이션 처리**

3. **텍스트와 이미지 배치**

4.  **오류 처리**  

---
