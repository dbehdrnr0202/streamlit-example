import pandas as pd
import plotly.express as px
import os

def print_corr_plot(df : pd.DataFrame, column1:str, column2 : str) :
    ord_dict = {'소득수준' : ['소득없음', '월평균 100만원 미만', '월평균 100만원 ~ 200만원 미만', '월평균 200만원 ~ 300만원 미만', '월평균 300만원 ~ 400만원 미만', '월평균 400만원 ~ 500만원 미만', '월평균 500만원 ~ 600만원 미만', '월평균 600만원 ~ 700만원 미만', '월평균 700만원 ~ 800만원 미만', '월평균 800만원 ~ 900만원 미만', '월평균 900만원 ~ 1,000만원 미만', '월평균 1,000만원 이상'],
                '계획에 따른 여행 vs 상황에 따른 여행' : ['상황에 따른 여행 매우선호', '상황에 따른 여행 중간선호', '상황에 따른 여행 약간선호', '중립', '계획에 따른 여행 약간선호', '계획에 따른 여행 중간선호', '계획에 따른 여행 매우선호'],
                '여행 시작 월' : ['8월', '9월', '10월', '11월'],
                '자연 vs 도시' : ['자연 매우선호', '자연 중간선호', '자연 약간선호', '중립', '도시 약간선호', '도시 중간선호', '도시 매우선호'],
                '숙박 vs 당일' : ['숙박 매우선호', '숙박 중간선호', '숙박 약간선호', '중립', '당일 약간선호' , '당일 중간선호', '당일 매우선호'],
                '새로운 지역 vs 익숙한 지역' : ['새로운 지역 매우선호', '새로운 지역 중간선호', '새로운 지역 약간선호', '중립', '익숙한 지역 약간선호' , '익숙한 지역 중간선호', '익숙한 지역 매우선호'],
                '편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소' : ['편하지만 비싼 숙소 매우선호', '편하지만 비싼 숙소 중간선호', '편하지만 비싼 숙소 약간선호', '중립', '불편하지만 저렴한 숙소 약간선호' , '불편하지만 저렴한 숙소 중간선호', '불편하지만 저렴한 숙소 매우선호'],
                '휴양/휴식 vs 체험활동' : ['휴양/휴식 매우선호', '휴양/휴식 중간선호', '휴양/휴식 약간선호', '중립', '체험활동 약간선호', '체험활동 중간선호', '체험활동 매우선호'],
                '잘 알려지지 않은 방문지 vs 잘 알려진 방문지' : ['잘 알려지지 않은 방문지 매우선호', '잘 알려지지 않은 방문지 중간선호', '잘 알려지지 않은 방문지 약간선호', '중립', '알려진 방문지 약간선호', '알려진 방문지 중간선호', '알려진 방문지 매우선호'],
                '사진촬영 중요하지 않음 vs 사진촬영 중요함' : ['사진촬영 중요하지 않음 매우선호', '사진촬영 중요하지 않음 중간선호', '사진촬영 중요하지 않음 약간선호', '중립', '사진촬영 중요함 약간선호', '사진촬영 중요함 중간선호', '사진촬영 중요함 매우선호'],
}
    #if column2 in ord_dict.keys() :
    #    ord2 = pd.api.types.CategoricalDtype(categories=ord_dict[column2], ordered = True)
    #    df[column2] = df[column2].astype(ord2)
    if column1 in ord_dict.keys() and column2 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column1: ord_dict[column1], column2: ord_dict[column2]})
    elif column1 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column1: ord_dict[column1]})
    elif column2 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column2: ord_dict[column2]})
    else :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True)
    #fig.show()
    return fig

