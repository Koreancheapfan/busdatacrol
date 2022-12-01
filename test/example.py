import pandas as pd #데이터 프레임형태로 csv에 저장하기 위해 사용
import csv #csv형태로 저장하기 위해 사용

student_Num = ['1','2','3','4','5','6','7']     #변수 값 지정
subject_Id = ["자바","파이썬","DB","네트워크","리눅스","자바","네트워크"]     #변수 값 지정
Grades = ['A','B''C''A','B','B','B']            #변수 값 지정
School_year = ['1','2','3','3','2','2','1']     #변수 값 지정
df = pd.DataFrame(student_Num, columns=['student_Num'])    #데이터 프레임 지정(표에 첫번째 열)
df['subject_Id'] = subject_Id       #데이터 프레임 지정
df['School_year'] = School_year     #데이터 프레임 지정
df.to_csv("학교.csv", index=False)   #학교csv파일에 숫자열을 제외하고 저장
