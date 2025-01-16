- CSV 파일에서 DB 테이블 생성 -> Column 조회 실패
1. INSERT 과정에서 계속해서 "track" 컬럼을 찾지 못하였음..
   
![image](https://github.com/user-attachments/assets/45d99f78-4726-4ef2-8a7a-3f2d7a6ca998)

2. 1시간 가량 구글링을 하다가 테이블 재생성 직전에 테이블 구조 확인하였음..

![image](https://github.com/user-attachments/assets/a93eba97-f6e0-4f86-a259-4640fb32ad3b)

3. "track"에서 앞자리에 공백이 추가된 " track"으로 확인..


---


- Streamlit에서 별점 선택시 인덱스 처리 -> 별점 5개 선택시 4 입력, 별점 1개 선택시 0 입력

![image](https://github.com/user-attachments/assets/93eb3c86-098b-4c13-9721-e0cbae53adb7)


---


#### FE Trouble shooting

1. 문제 요약 (Problem Summary)
- streamlit 위젯들에 사용자 정의 CSS가 적용되지 않음
<br>

2. 발생 조건 (Conditions or Symptoms)
- streamlit 위젯 중에서도 마크다운에는 CSS 적용 가능했으나
함수가 사용되는 위젯들에는 적용이 되지 않음
<br>

3. 원인 분석 (Root Cause)
- treamlit은 위젯의 변수명을 랜덤으로 지정해서 생성하기 때문에 CSS가 그 변수를 찾아서 적용을 할 수가 없음
<br>

4. 해결 방법 (Resolution Steps)
마크다운에는 CSS로 스타일링,
함수가 적용되는 위젯을 염두에 두고 streamlit의 API reference를 참고하여 UI를 스타일링
<br>

5. 추가 정보 및 참고자료
[Stremalit API reference](https://docs.streamlit.io/develop/api-reference)


---


문제1
- streamlit에서 사용자의 입력값에 대한 출력을 박스안에 표현하려고 함. 
- CSS를 사용해보았지만 반영이 되지 않음.
  
- 해결방법: with st.container안에 출력해야 할 값을 넣어 검색한 결과에 대한 값을 container 내에 불러옴
- 느낀점: streamlit은 css처럼 사용하면 안되는 것이 있기 때문에 그것을 염두에 두고 UI를 수정해야 함
