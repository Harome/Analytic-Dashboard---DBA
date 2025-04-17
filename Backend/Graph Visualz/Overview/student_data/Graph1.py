from Initialization.enrollment_data_loader import load_school_data
import pandas as pd
import plotly.graph_objects as go

data = load_school_data("/Users/annmargaretteconcepcion/dba 2/4/Analytic-Dashboard---DBA/Data/Raw_data/ANALYZED_SY_2023-2024_School_Level_Data_on_Official_Enrollment_13.xlsx")

df_school = data["df_school"]
grade_columns_male = data["grade_columns_male"]
grade_columns_female = data["grade_columns_female"]
total_male = df_school[grade_columns_male].sum().sum()
total_female = df_school[grade_columns_female].sum().sum()

df_gender = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Total Enrollees': [total_male, total_female]
})

gender_dashboard_colors = {'Male': '#33C3FF','Female': '#FFB533'}

pie_chart = go.Figure(
    data=[go.Pie(
        labels=df_gender['Gender'],
        values=df_gender['Total Enrollees'],
        marker=dict(colors=[gender_dashboard_colors[g] for g in df_gender['Gender']]),
        textinfo='percent+label'
    )]
)

pie_chart.update_layout(
    title="📈 Gender Distribution of Enrollees",
    title_x=0.5,
    plot_bgcolor='rgba(255,255,255,0.7)',
    paper_bgcolor='rgba(255,255,255,0.7)',
    font_color='#1b8e3e',
    title_font=dict(size=20, family='Arial Black'),
    legend_title=dict(text='Gender', font=dict(size=12)),
    legend=dict(font=dict(size=11))
)

pie_chart.show()
