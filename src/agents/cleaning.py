from config.settings import settings

def clean_data(df):
    # EN: Access config directly with type safety
    # FR: Accès direct à la config avec typage sûr
    if settings.cleaning.drop_duplicates:
        df = df.drop_duplicates()
    return df