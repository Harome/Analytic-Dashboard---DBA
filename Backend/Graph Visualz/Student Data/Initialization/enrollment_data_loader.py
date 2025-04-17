import pandas as pd


def load_school_data(file_path):
    df_school = pd.read_excel(file_path)

    region_order = ['Region I', 'Region II', 'Region III', 'Region IV-A', 'MIMAROPA', 'Region V',
                    'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI',
                    'Region XII', 'CARAGA', 'BARMM', 'CAR', 'NCR', 'PSO']

    grade_columns_male = ['Kindergarten_Male', 'G1_Male', 'G2_Male', 'G3_Male', 'G4_Male', 'G5_Male', 'G6_Male',
                         'Elem_NG_Male', 'G7_Male', 'G8_Male', 'G9_Male', 'G10_Male', 'JHS_NG_Male',
                          'G11_ABM_Male', 'G11_HUMSS_Male', 'G11_STEM_Male', 'G11_GAS_Male',
                          'G11_PBM_Male', 'G11_TVL_Male', 'G11_SPORTS_Male', 'G11_ARTS_Male',
                          'G12_ABM_Male', 'G12_HUMSS_Male', 'G12_STEM_Male', 'G12_GAS_Male',
                          'G12_PBM_Male', 'G12_TVL_Male', 'G12_SPORTS_Male', 'G12_ARTS_Male']

    grade_columns_female = [col.replace("Male", "Female") for col in grade_columns_male]

    elementary_male = grade_columns_male[1:7] + ["Elem_NG_Male"]
    elementary_female = [col.replace("Male", "Female") for col in elementary_male]

    junior_high_male = grade_columns_male[8:13]
    junior_high_female = [col.replace("Male", "Female") for col in junior_high_male]

    senior_high_male = grade_columns_male[13:]
    senior_high_female = [col.replace("Male", "Female") for col in senior_high_male]

    shs_strands = {
        "ABM": ["G11_ABM_Male", "G11_ABM_Female", "G12_ABM_Male", "G12_ABM_Female"],
        "HUMSS": ["G11_HUMSS_Male", "G11_HUMSS_Female", "G12_HUMSS_Male", "G12_HUMSS_Female"],
        "STEM": ["G11_STEM_Male", "G11_STEM_Female", "G12_STEM_Male", "G12_STEM_Female"],
        "GAS": ["G11_GAS_Male", "G11_GAS_Female", "G12_GAS_Male", "G12_GAS_Female"],
        "PBM": ["G11_PBM_Male", "G11_PBM_Female", "G12_PBM_Male", "G12_PBM_Female"],
        "TVL": ["G11_TVL_Male", "G11_TVL_Female", "G12_TVL_Male", "G12_TVL_Female"],
        "SPORTS": ["G11_SPORTS_Male", "G11_SPORTS_Female", "G12_SPORTS_Male", "G12_SPORTS_Female"],
        "ARTS": ["G11_ARTS_Male", "G11_ARTS_Female", "G12_ARTS_Male", "G12_ARTS_Female"]
    }

    sectors = ["Public", "Private", "SUCsLUCs", "PSO"]

    sector_distribution = df_school.groupby("Sector").sum(numeric_only=True)
    sector_distribution["Elementary_Total"] = sector_distribution[elementary_male].sum(axis=1) + sector_distribution[elementary_female].sum(axis=1)
    sector_distribution["Junior_HS_Total"] = sector_distribution[junior_high_male].sum(axis=1) + sector_distribution[junior_high_female].sum(axis=1)
    sector_distribution["Senior_HS_Total"] = sector_distribution[senior_high_male].sum(axis=1) + sector_distribution[senior_high_female].sum(axis=1)
    sector_distribution["Total"] = sector_distribution[["Elementary_Total", "Junior_HS_Total", "Senior_HS_Total"]].sum(axis=1)

    total_by_level = {
        "Elementary": df_school[elementary_male + elementary_female].sum().sum(),
        "Junior High": df_school[junior_high_male + junior_high_female].sum().sum(),
        "Senior High": df_school[senior_high_male + senior_high_female].sum().sum()
    }

    total_by_sector = {
        "Private": sector_distribution.loc["Private", "Total"],
        "Public": sector_distribution.loc["Public", "Total"],
        "SUCs/LUCs & PSO": sector_distribution.loc[["SUCsLUCs", "PSO"], "Total"].sum()
    }

    categories = {
        "regions": df_school['Region'].dropna().unique(),
        "subclassifications": df_school['School_Subclassification'].dropna().unique(),
        "school_types": df_school['School_Type'].dropna().unique(),
        "modified_coc": df_school['Modified_COC'].dropna().unique()
    }

    return {
        "df_school": df_school,
        "region_order": region_order,
        "grade_columns_male": grade_columns_male,
        "grade_columns_female": grade_columns_female,
        "elementary_male": elementary_male,
        "elementary_female": elementary_female,
        "junior_high_male": junior_high_male,
        "junior_high_female": junior_high_female,
        "senior_high_male": senior_high_male,
        "senior_high_female": senior_high_female,
        "shs_strands": shs_strands,
        "sector_distribution": sector_distribution,
        "total_by_level": total_by_level,
        "total_by_sector": total_by_sector,
        "categories": categories
    }
